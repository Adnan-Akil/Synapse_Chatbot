# <img src="https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/network.svg" width="32" height="32" style="vertical-align: bottom; margin-right: 8px;"> Synapse 🧠

> **Local-First RAG Chatbot with a "Butter Smooth" UI**

**Synapse** is a modern, privacy-focused AI chat application that allows you to "chat" with your documents (PDF, DOCX, TXT). Built with a state-of-the-art stack, it runs entirely locally on your machine, ensuring your data never leaves your control.

![Synapse UI Preview](https://via.placeholder.com/800x400?text=Synapse+UI+Preview+Coming+Soon)

---

## ✨ Features

- **🚀 Local Intelligence**: Powered by local embeddings (HuggingFace) and Groq API (optional for LLM).
- **🔒 Privacy First**: Your documents are processed and stored locally using ChromaDB and SQLite.
- **🎨 Stunning UI**: A "wow-factor" interface built with React, Tailwind v4, and Framer Motion.
- **📄 Multi-Format Support**: 
  - Drag-and-drop support for PDF, DOCX, TXT, CSV, and Excel.
  - Intelligent chunking and retrieval.
- **⚡ High Performance**: FASTAPI backend for rapid response times.

---

## 🏗️ Architecture

Synapse is built as a split-stack application:

### **Backend (Python)**
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **RAG Engine**: [LangChain](https://www.langchain.com/)
- **Vector Store**: [ChromaDB](https://www.trychroma.com/) (Local/In-Memory)
- **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2`
- **Security**: Basic input validation and CORS protection.

### **Frontend (JavaScript)**
- **Framework**: [React](https://react.dev/) + [Vite](https://vitejs.dev/)
- **Styling**: [Tailwind CSS v4](https://tailwindcss.com/)
- **Animations**: [Framer Motion](https://www.framer.com/motion/)
- **Icons**: [Lucide React](https://lucide.dev/)

---

## 🛠️ Getting Started

### Prerequisites

- **Python 3.10+**
- **Node.js 18+** & **npm**
- **Groq API Key** (for the LLM reasoning layer)

### Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Adnan-Akil/Synapse_Chatbot.git
    cd Synapse_Chatbot
    ```

2.  **Backend Setup**
    ```bash
    # Create a virtual environment
    python3 -m venv new_venv
    source new_venv/bin/activate  # On Windows: new_venv\Scripts\activate

    # Install Python dependencies
    pip install -r requirements.txt
    ```

3.  **Frontend Setup**
    ```bash
    cd ui
    npm install
    ```

4.  **Configuration**
    - Create a `.env` file in the root directory (copied from example).
    - Add your API keys:
      ```env
      GROQ_API_KEY=your_key_here
      ```

---

## 🚀 Running the Application

You will need two terminal windows running simultaneously.

### Terminal 1: Backend
```bash
# Ensure venv is active
source new_venv/bin/activate

# Start the API server
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```

### Terminal 2: Frontend
```bash
cd ui

# Start the dev server
npm run dev -- --host
```

Open your browser to **[http://localhost:5173](http://localhost:5173)** to launch Synapse.

---

## 📂 Project Structure

```
Synapse_Chatbot/
├── src/                # Python Backend
│   ├── api/            # API Endpoints (FastAPI)
│   ├── config/         # Environment Config
│   ├── database.py     # SQLite Manager (Chat History)
│   ├── retrieval.py    # RAG Logic & Vector DB
│   └── data_loader.py  # File Parsers
├── ui/                 # React Frontend
│   ├── src/
│   │   ├── components/ # ChatWindow, Sidebar
│   │   └── App.jsx     # Main Layout
│   └── tailwind.config.js
├── data/               # Local Data Storage (Chroma/SQLite)
├── requirements.txt    # Python Dependencies
└── README.md           # Documentation
```

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a Pull Request.

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.
