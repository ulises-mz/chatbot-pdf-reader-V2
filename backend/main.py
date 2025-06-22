import os
import json
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from backend.utils.pdf_loader import load_pdf_text_chunks
from backend.utils.embeddings import build_faiss_index
from backend.utils.retriever import retrieve_relevant_chunks
from backend.utils.prompt_builder import build_prompt
from backend.utils.cost_utils import count_tokens_and_cost
from openai import AsyncOpenAI

# Carga .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

# App FastAPI
app = FastAPI()

# CORS para conectar con frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# PDF cargado al inicio
pdf_path = os.path.join("backend", "docs", "PB_TravelAbility_DI-v3.pdf")
pdf_chunks = load_pdf_text_chunks(pdf_path)
faiss_index, vectors, raw_chunks = build_faiss_index(pdf_chunks)

# Sesiones en memoria
sessions = {}  # { id: [ {role, content} ] }

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    user_input = body.get("message", "")
    conversation_id = body.get("conversation_id", "default")

    # Saludo automático
    if user_input.strip().lower() in ["hola", "buenas", "hey", "hi"]:
        return StreamingResponse(
            iter([
                f"data: {json.dumps({'type': 'content', 'content': '¡Hola! Puedes preguntarme sobre el contenido del documento y con gusto te ayudaré.'})}\n\n",
                'data: {"type": "done"}\n\n'
            ]),
            media_type="text/event-stream"
        )

    # Historial
    if conversation_id not in sessions:
        sessions[conversation_id] = []
    sessions[conversation_id].append({"role": "user", "content": user_input})

    # Detectar si es pregunta meta
    meta_keywords = ["sobre qué tienes", "qué sabes", "temas", "información tienes", "de qué trata", "resumen", "alcance"]
    is_meta = any(kw in user_input.lower() for kw in meta_keywords)

    # Contexto
    context_chunks = []
    if not is_meta:
        context_chunks = retrieve_relevant_chunks(faiss_index, raw_chunks, vectors, user_input)
    context = "\n".join(context_chunks).strip()
    context = context if len(context) > 50 else None

    if not context and not is_meta:
        return StreamingResponse(
            iter([
                f"data: {json.dumps({'type': 'content', 'content': 'No tengo información sobre eso.'})}\n\n",
                'data: {"type": "done"}\n\n'
            ]),
            media_type="text/event-stream"
        )

    # Construir prompt
    messages = build_prompt(user_input, context_chunks, sessions[conversation_id])

    # Streaming OpenAI response
    async def stream_response():
        accumulated = ""
        try:
            response = await client.chat.completions.create(
                model="gpt-4-turbo",
                messages=messages,
                stream=True
            )
            async for chunk in response:
                if delta := chunk.choices[0].delta.content:
                    accumulated += delta
                    yield f"data: {json.dumps({'type': 'content', 'content': delta})}\n\n"

            if accumulated.strip():
                sessions[conversation_id].append({"role": "assistant", "content": accumulated})
                usage = count_tokens_and_cost(messages)
                yield f"data: {json.dumps({'type': 'usage', 'tokens': usage})}\n\n"

            yield 'data: {"type": "done"}\n\n'

        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"

    return StreamingResponse(stream_response(), media_type="text/event-stream")

@app.get("/debug/chat/{conversation_id}")
def debug_chat(conversation_id: str):
    history = sessions.get(conversation_id)
    if not history:
        return {"status": "not_found", "history": []}
    return {
        "conversation_id": conversation_id,
        "message_count": len(history),
        "history": history
    }

@app.get("/debug/conversations")
def list_all_conversations():
    return {
        "conversations": [
            {"conversation_id": cid, "message_count": len(h), "history": h}
            for cid, h in sessions.items()
        ]
    }

@app.delete("/debug/conversations/{conversation_id}")
def delete_conversation(conversation_id: str):
    if conversation_id in sessions:
        del sessions[conversation_id]
        return {"status": "deleted"}
    raise HTTPException(status_code=404, detail="Conversación no encontrada")
