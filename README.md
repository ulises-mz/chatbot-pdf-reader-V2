
# Chatbot PDF Reader

Aplicación web que responde preguntas con base en el contenido de un archivo PDF. Construida con **FastAPI** y **React**, sin LangChain, usando procesamiento desde cero con **PyPDF2**, **FAISS** y **OpenAI**.

---

## 🚀 Características principales

- 📄 Procesamiento completo de PDF usando PyPDF2
- 🔍 Recuperación semántica mediante FAISS y embeddings OpenAI
- 🧠 Chat multi-sesión con memoria en backend
- 🔄 Streaming de respuestas vía SSE en tiempo real
- 📊 Visualización de tokens y costo estimado por conversación
- 📤 Exportación de conversaciones a Markdown
- 🎨 Interfaz moderna inspirada en ChatGPT

---

## 🗂️ Estructura del proyecto

```
chatbot-pdf-reader/
├── backend/
│   ├── docs/                    # PDF cargado en el backend
│   ├── utils/                   # Módulos de procesamiento, embeddings, FAISS, etc.
│   ├── main.py                  # API FastAPI con SSE
│   ├── .env.example             # Variables de entorno requeridas
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── api/                 # Lógica de comunicación con backend (chatApi.js)
│   │   ├── components/          # Componentes del chat (ChatBox, InputBar, Sidebar, etc.)
│   │   ├── pages/               # Vista principal del chat (ChatPage.jsx)
│   │   ├── styles/              # Archivos CSS por componente
│   │   ├── utils/               # Exportación de conversación (exportChat.js)
│   │   ├── App.jsx
│   │   └── index.js
│   ├── .env.example
│   ├── package.json
│   └── README.md
```

---

## ⚙️ Requisitos

- Node.js (>= 16)
- Python 3.10 o superior
- API Key válida de OpenAI (`OPENAI_API_KEY`)

---

## 🔧 Instalación y ejecución local

### 1. Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

Copia `.env.example` a `.env` y agrega tu clave de OpenAI.

---

### 2. Frontend (React)

```bash
cd frontend
npm install
npm start
```

Accede desde: [http://localhost:3000](http://localhost:3000)

---

## 🔐 Variables de entorno

### `.env` del backend

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### `.env` del frontend (opcional)

```env
REACT_APP_API_URL=http://localhost:8000
```

---

## 📦 Dependencias importantes

### Backend (`requirements.txt`)

```txt
fastapi
uvicorn
python-multipart
python-dotenv
openai
tiktoken
PyPDF2
faiss-cpu
numpy
```

### Frontend (`package.json`)

```json
"dependencies": {
  "axios": "^1.6.0",
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "react-markdown": "^9.0.0",
  "react-scripts": "5.0.1"
}
```

---

## 🧪 Endpoints útiles del backend

- `GET /health` — Verifica que el backend esté activo
- `POST /chat` — Envía mensaje y recibe respuesta por SSE
- `GET /debug/chat/{conversation_id}` — Historial de conversación
- `GET /debug/conversations` — Lista de sesiones
- `DELETE /debug/conversations/{id}` — Eliminar conversación

---

## 📝 Notas

- El archivo PDF debe estar ubicado en `backend/docs/` al arrancar el backend.
- El chatbot solo responde sobre contenido incluido en el PDF.
- Las respuestas están formateadas en **Markdown** para mejorar legibilidad.
- Todo el procesamiento de chunks, embeddings y recuperación es interno, sin LangChain.

---

## ✅ Estado del proyecto

✅ Backend funcionando con streaming OpenAI  
✅ Frontend responsivo tipo ChatGPT  
✅ Procesamiento desde cero usando PyPDF2 + FAISS  
✅ Listo para mejoras como carga dinámica de PDF, autenticación o exportaciones

---

## 🖼️ Vista previa

### 💻 Desktop
![Preview del chatbot](/Preview.png)

### 📱 Mobile
![Preview móvil](/MobilePreview.png)


---

## 📄 Licencia

MIT © 2025
