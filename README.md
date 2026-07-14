# 🧠 AI Research Copilot - RAG Application

> A production-inspired Retrieval-Augmented Generation (RAG) platform that enables semantic search and AI-powered question answering across research papers using FastAPI, FAISS, Sentence Transformers, and Google's Gemini.

---

## ✨ Features

- 📄 Upload and manage PDF research papers
- 🔍 Semantic search using Sentence Transformers
- 🧩 Intelligent text chunking with overlapping windows
- 🗂️ Persistent FAISS vector database
- 💬 AI-powered question answering using Gemini
- 📑 Page-aware retrieval with document/page citations
- 📋 List uploaded documents
- 🗑️ Delete documents and automatically rebuild the vector index
- 📝 Metadata persistence using JSON
- ⚡ RESTful FastAPI backend
- 🛡️ File validation (type, signature, size)

---

## 🏗️ Architecture

```text
                Upload PDF
                     │
                     ▼
              PDF Validation
                     │
                     ▼
              PDF Parser (PyPDF)
                     │
         Page-wise Text Extraction
                     │
                     ▼
            Text Chunking Service
                     │
                     ▼
       SentenceTransformer Embeddings
                     │
                     ▼
               FAISS Vector Store
                     │
          Persistent Storage
      (index.faiss + metadata.json)
                     │
                     ▼
              Semantic Retrieval
                     │
                     ▼
             Prompt Construction
                     │
                     ▼
               Gemini 2.5 Flash
                     │
                     ▼
               Final AI Response
```

---

# 📂 Project Structure

```text
backend/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── dependencies/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── storage/
│
├── tests/
├── requirements.txt
└── README.md
```

---

# 🚀 Current Pipeline

```
Upload PDF
      │
      ▼
Extract Pages
      │
      ▼
Chunk Text
      │
      ▼
Generate Embeddings
      │
      ▼
Store in FAISS
      │
      ▼
Semantic Retrieval
      │
      ▼
Build Prompt
      │
      ▼
Gemini
      │
      ▼
Answer + Page Citation
```

---

# 🛠️ Tech Stack

### Backend

- Python
- FastAPI
- Uvicorn

### AI / NLP

- Sentence Transformers
- Google Gemini 2.5 Flash
- FAISS

### Document Processing

- PyPDF

### Data Storage

- FAISS
- JSON Metadata

---

# 📌 Example API

## Upload

```http
POST /documents/upload
```

---

## List Documents

```http
GET /documents
```

---

## Delete Document

```http
DELETE /documents/{document_id}
```

---

## Chat

```http
POST /chat
```

Example:

```json
{
    "question": "What methodology does the paper use?"
}
```

Example Response

```json
{
    "answer": "The paper proposes a Graph Neural Network... (paper.pdf, Page 7)"
}
```

---

# ✨ Implemented Features

- ✅ Secure PDF upload
- ✅ PDF validation
- ✅ Page extraction
- ✅ Page-aware chunking
- ✅ Metadata extraction
- ✅ SentenceTransformer embeddings
- ✅ Persistent FAISS index
- ✅ Persistent metadata
- ✅ Semantic similarity search
- ✅ Gemini integration
- ✅ Prompt engineering
- ✅ Page-aware citations
- ✅ Document management
- ✅ Vector store rebuilding after deletion

---

# 🚧 Roadmap

- [ ] Document-level filtering
- [ ] Source citation API
- [ ] Multi-turn conversations
- [ ] Hybrid Search (BM25 + Dense Retrieval)
- [ ] PostgreSQL metadata storage
- [ ] AWS S3 document storage
- [ ] Docker deployment
- [ ] Authentication
- [ ] React frontend

---

# 💡 Why this project?

This project was built to explore how modern Retrieval-Augmented Generation (RAG) systems work beyond simple LLM API calls. It focuses on modular architecture, semantic search, persistent vector storage, page-aware retrieval, and scalable backend design.

Rather than acting as a basic chatbot, the application demonstrates how production-inspired AI assistants retrieve relevant context, ground responses in uploaded documents, and provide page-level references.

---

# 📈 Future Improvements

- Cross-document reasoning
- Document selection before querying
- Streaming responses
- OCR support for scanned PDFs
- Citation confidence scores
- Re-ranking models
- Evaluation pipeline
- Kubernetes deployment

---

# 👨‍💻 Author

**Kanishka Kashyap**

- GitHub: https://github.com/kanishka18-bee
- LinkedIn: https://linkedin.com/in/kkanishka

---
