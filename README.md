# Dexalo Task - RAG Chat UI

This repository contains the front-end React component for a Retrieval-Augmented Generation (RAG) chat application. Users can upload documents, ask questions based on those documents, and utilize an AI agent with a built-in calculator tool for basic reasoning and calculations.

## Features

- **Document Upload**: Supports `.txt` and `.pdf` uploads via the `/upload` endpoint.
- **Chat Interface**: Single-page chat UI built with React, Tailwind CSS, and shadcn/ui components.
- **RAG-Based Q&A**: Sends user questions to the `/chat` endpoint, which runs a RAG pipeline to retrieve relevant document chunks and generate answers.
- **AI Agent & Calculator Tool**: Detects math queries and invokes a calculator tool for operations like square roots, additions, etc.

## Tech Stack

- **React** with functional components and hooks
- **Tailwind CSS** for utility-first styling
- **shadcn/ui** for ready-made UI components (Button, Input, Card, ScrollArea)
- **lucide-react** for icons



## File Structure Backend

```
├── public/                 # Static assets
├── package.json            # Project metadata and dependencies
├── src/
│   ├── components/         # Reusable UI components
│   │   ├── Chat.jsx
│   │   ├── ChatInput.jsx
│   │   ├── ChatMessage.jsx
│   │   ├── DocumentUpload.jsx
│   │   └── Sidebar.jsx
│   ├── context/            # React context for state management
│   │   └── ChatContext.jsx
│   ├── services/           # API service layer
│   │   └── api.js
│   ├── App.jsx             # Main application component
│   ├── index.js            # ReactDOM render and entry point
│   └── index.css           # Global CSS
├── backend/                # FastAPI backend service
│   ├── agent.py
│   ├── AnswerGenerator.py  # Class for generating answers from retrieved documents
│   ├── app.py              # FastAPI application entrypoint
│   ├── ChromaDBManager.py  # Class for chromadb mangement 
│   ├── EmbeddingProvider.py # Class for embedding model manegement
│   ├── LLMProvider.py       # Class for llm model manegement
│   ├── PromptManager.py     # Class for prompt manegement
│   ├── rag_service.py      # RAG & agent orchestration
│   ├── RAGPipelineManager.py # Class for full rag pipline 
│   ├── TextProcessor.py    # Class for text chunking and text processor
│   ├── vector_db/          # Local vector store data
│   └── data_file/          # Raw document storage
└── README.md               # Project documentation
```

## Setup & Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Mohamed28112003/Dexalo_task.git
   cd Dexalo_task
   ```

2. **Install dependencies**
   ```bash
   npm install 
   # and
   pip install -r requirements.txt
   ```

3. **Run the app**
   ```bash
   cd backend
   python app.py
   # and
   cd frontend 
   npm start
   ```

## Usage

1. Click **Upload Documents** and select one or more `.txt`/`.pdf` files.
2. Type your question in the chat input. For math operations (e.g., “√(144) + 5”), the calculator tool will be invoked automatically.
3. Press **Enter** or click the send icon (calculator glyph) to submit.
4. View AI responses in the scrollable chat area.

## [Project Demo](https://drive.google.com/file/d/17JtOZWr7wl1jZlobrx72g9w_CIlSevyw/view?usp=drivesdk)
