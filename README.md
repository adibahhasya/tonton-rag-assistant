# 💬 TontonAssist — Multilingual RAG Chatbot

TontonAssist is a multilingual customer support chatbot built using **Retrieval-Augmented Generation (RAG)**.

The chatbot answers Tonton-related customer enquiries using information retrieved from a Tonton FAQ knowledge base. It supports **Bahasa Melayu, English, and mixed Malay-English queries**.

## ✨ Features

- Tonton FAQ knowledge base loaded from Google Docs
- FAQ-based semantic chunking
- Multilingual text embeddings
- Semantic search using ChromaDB
- RAG-based answer generation
- Gemini Flash integration
- Malay, English, and mixed-language support
- Tonton-only scope guardrails
- Competitor and unrelated-query restriction
- Streamlit conversational chat interface
- Automatic vector-store initialization

---

## 🏗️ Architecture

```text
Google Docs FAQ
       ↓
   ingest.py
       ↓
FAQ Question + Answer Chunking
       ↓
Multilingual Sentence Embeddings
       ↓
    ChromaDB
       ↓
    User Query
       ↓
Query Embedding
       ↓
Semantic Retrieval (Top-K)
       ↓
Retrieved FAQ Context
       ↓
Gemini Flash
       ↓
Grounded Response
       ↓
Streamlit Chat UI
```

---

## 🧠 RAG Pipeline

### 1. Document Loading

The Tonton FAQ knowledge base is retrieved from a Google Doc and exported as plain text.

### 2. Chunking

The document is structured as FAQ Question + Answer pairs.

Therefore:

```text
1 FAQ = 1 semantic chunk
```

This keeps each question together with its corresponding answer.

### 3. Embeddings

The project uses:

```text
paraphrase-multilingual-MiniLM-L12-v2
```

This multilingual Sentence Transformer model allows semantic retrieval across Malay, English, and mixed-language queries.

For example, these questions can retrieve the same relevant FAQ:

```text
Saya telah melanggan tetapi kenapa masih mempunyai iklan?

Saya dah subscribe, tapi kenapa still ada ads?

Why am I still getting ads after subscribing?
```

### 4. Vector Search

FAQ embeddings are stored in **ChromaDB**.

When a user submits a question, the query is embedded using the same embedding model and compared against the FAQ vectors using cosine similarity.

The most relevant FAQ chunks are then retrieved.

### 5. Response Generation

The retrieved FAQ context and user question are passed to Gemini.

The model is instructed to answer only using the supplied Tonton FAQ context to reduce unsupported or hallucinated answers.

---

## 🛡️ Scope Guardrails

TontonAssist is designed specifically for **Tonton customer support**.

The chatbot is instructed to:

- Answer only Tonton-related questions
- Use only information available in the retrieved FAQ
- Avoid inventing unsupported information
- Refuse unrelated questions
- Avoid answering questions about competing services
- Avoid comparing Tonton with competitors
- Respond in the same language as the user

Example:

```text
User:
How much is Netflix?

TontonAssist:
I can only assist with Tonton-related enquiries.
```

---

## 📂 Project Structure

```text
tonton-rag-assistant/
│
├── ingest.py
│   └── Document loading, chunking, embeddings and ChromaDB
│
├── rag_final_test.py
│   └── Semantic retrieval and Gemini response generation
│
├── rag_tonton.py
│   └── Streamlit chat interface
│
├── requirements.txt
│   └── Python dependencies
│
├── .gitignore
│   └── Excludes secrets, cache and local vector database
│
└── README.md
```

---

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Frontend | Streamlit |
| Embedding Model | Sentence Transformers |
| Embedding | paraphrase-multilingual-MiniLM-L12-v2 |
| Vector Database | ChromaDB |
| LLM | Gemini Flash |
| Knowledge Source | Google Docs |
| API Communication | Requests |

---

## 🚀 Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/adibahhasya/tonton-rag-assistant.git
cd tonton-rag-assistant
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Gemini API key

Create a `.env` file:

```text
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

### 4. Build the vector store

```bash
python ingest.py
```

### 5. Test the RAG pipeline

```bash
python rag_final_test.py
```

### 6. Run the Streamlit application

```bash
streamlit run rag_tonton.py
```

Open:

```text
http://localhost:8501
```

---

## 💬 Example Queries

### Bahasa Melayu

```text
Bagaimana saya nak menukar kata laluan?
```

### Mixed Malay-English

```text
Saya dah subscribe, tapi kenapa still ada ads?
```

### English

```text
Why am I still getting ads after subscribing?
```

---

## 🔑 Key Design Decisions

**FAQ-level chunking**

Each Question + Answer pair is treated as one chunk because each FAQ represents a complete semantic unit.

**Multilingual embeddings**

A multilingual embedding model improves retrieval for Malay, English, and informal mixed-language customer queries.

**ChromaDB**

ChromaDB provides a lightweight vector database suitable for the current FAQ knowledge base and local development.

**RAG**

Retrieval-Augmented Generation grounds the LLM response using relevant FAQ information instead of relying only on the model's general knowledge.

---

## 🔮 Future Improvements

Potential improvements include:

- Similarity thresholding
- Hybrid keyword + semantic search
- Reranking
- Retrieval evaluation dataset
- Conversation-aware retrieval
- Larger Tonton knowledge base
- Automated FAQ synchronization
- Monitoring and analytics
- Improved fallback and escalation handling

---

## 👤 Author

Developed as a multilingual RAG chatbot assessment project.


