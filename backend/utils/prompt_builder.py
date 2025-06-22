# backend/utils/prompt_builder.py
def build_prompt(user_input, context_chunks, history=None):
    context = "\n\n".join(context_chunks)
    system_message = (
        "Eres un asistente experto. Sigue estas reglas estrictamente:\n"
        "1. Usa exclusivamente el CONTEXTO proporcionado y el historial de conversación.\n"
        "2. No inventes. Si no hay información, responde: 'No tengo información sobre eso'.\n"
        "3. Responde en Markdown válido con títulos, listas y código si aplica.\n"
        "4. Nunca menciones documentos ni archivos.\n"
        "6. Mantén un tono profesional, claro, empático y responde siempre en el idioma original del usuario.\n"
        "7. Da respuestas coherentes con el historial, manteniendo continuidad en nombres, temas y contexto previo.\n"
        "8. Si el usuario hace una referencia vaga (como 'eso', 'más de eso', 'continúa'), intenta asociarla con la última respuesta válida del asistente.\n"
        "9. No des consejos, explicaciones técnicas ni definiciones que no estén explícitamente respaldadas por el contexto o historial.\n"
        "10. Toda respuesta debe estar en formato **Markdown válido** y estructurado:\n"
        "    - Usa títulos (`#`, `##`, `###`) si aplican.\n"
        "    - Usa listas (`-`, `*`, `1.`) para pasos o elementos.\n"
        "    - Usa negritas (`**texto**`) o itálicas (`*texto*`) según el énfasis.\n"
        "    - Usa bloques de código (```) para fragmentos técnicos o textuales.\n"
        "    - Evita emojis, adornos innecesarios o respuestas con tono informal.\n"
        "11. Si la pregunta no tiene relación directa con el CONTEXTO del documento, responde: 'Esa pregunta no está relacionada con la información disponible'.\n"
        "12. Si el usuario hace una pregunta que deriva de una respuesta anterior del bot, pero no está respaldada por el CONTEXTO del documento original, responde: 'Esa pregunta no está relacionada con la información disponible'. No continúes la conversación por esa línea.\n"

    )

    messages = [{"role": "system", "content": system_message}]
    if history:
        messages.extend(history)
    messages.append({
        "role": "user",
        "content": f"--- CONTEXTO ---\n{context}\n--- FIN DEL CONTEXTO ---\n\nPregunta: {user_input}"
    })
    return messages
