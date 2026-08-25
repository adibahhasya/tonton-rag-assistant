# 💬 TontonAssist — Multilingual RAG Chatbot

TontonAssist is a multilingual customer support chatbot built using **Retrieval-Augmented Generation (RAG)**.

The chatbot answers Tonton-related customer enquiries using information retrieved from a Tonton FAQ knowledge base. It supports **Bahasa Melayu, English, and mixed Malay-English queries**.

## ✨ Features

- Tonton FAQ knowledge base loaded from Google Docs
- FAQ-based semantic chunking
- Multilingual text embeddings
- Semantic search using ChromaDB
- RAG-based grounded answer generation
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

This preserves the relationship between each question and its corresponding answer.

### 3. Embeddings

The project uses:

```text
paraphrase-multilingual-MiniLM-L12-v2
```

This multilingual Sentence Transformer model enables semantic retrieval across Malay, English, and mixed-language queries.

For example, these queries can retrieve the same relevant FAQ:

```text
Saya telah melanggan tetapi kenapa masih mempunyai iklan?

Saya dah subscribe, tapi kenapa still ada ads?

Why am I still getting ads after subscribing?
```

### 4. Vector Search

FAQ embeddings are stored in **ChromaDB**.

When a user submits a question, the query is embedded using the same multilingual embedding model and compared against the FAQ vectors using cosine similarity.

The **Top-K most relevant FAQ chunks** are then retrieved.

### 5. Response Generation

The retrieved FAQ context and user question are passed to Gemini.

Gemini is instructed to generate its response using only the retrieved Tonton FAQ context, helping reduce unsupported or hallucinated answers.

---

## 🤖 Gemini Model Selection

The assessment preferably requested the use of the **Gemini 2.5 Flash API**.

The initial implementation was therefore configured to use:

```text
gemini-2.5-flash
```

However, during development, the Gemini API returned the following response for the API access used in this project:

```text
404 NOT_FOUND

This model models/gemini-2.5-flash is no longer available to new users.
Please update your code to use models/gemini-3.6-flash for the latest
features and improvements.
```

Therefore, the final implementation uses:

```text
gemini-3.6-flash
```

This migration only changes the **generation model**. The underlying RAG architecture remains unchanged:

```text
User Query
     ↓
Multilingual Query Embedding
     ↓
ChromaDB Semantic Retrieval
     ↓
Relevant Tonton FAQ Context
     ↓
Gemini 3.6 Flash
     ↓
Grounded Response
```

The retrieval strategy, embedding model, vector store, knowledge source, and grounding approach remain the same.

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

These guardrails keep the assistant focused on its intended customer-support domain.

---

## 📂 Project Structure

```text
tonton-rag-assistant/
│
├── ingest.py
│   └── Document loading, chunking, embeddings and ChromaDB setup
│
├── rag_final_test.py
│   └── Semantic retrieval and Gemini response generation
│
├── rag_tonton.py
│   └── Streamlit conversational chat interface
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
| Embedding Framework | Sentence Transformers |
| Embedding Model | paraphrase-multilingual-MiniLM-L12-v2 |
| Vector Database | ChromaDB |
| LLM | Gemini 3.6 Flash |
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

### 3. Configure the Gemini API key

Create a `.env` file in the project directory:

```text
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

> **Important:** Never commit `.env` or API keys to GitHub.

### 4. Build the vector store

```bash
python ingest.py
```

The ingestion pipeline will:

```text
Google Docs
    ↓
Load FAQ
    ↓
FAQ Chunking
    ↓
Generate Embeddings
    ↓
Store in ChromaDB
```

### 5. Test the RAG pipeline

```bash
python rag_final_test.py
```

### 6. Run the Streamlit application

```bash
streamlit run rag_tonton.py
```

The application will be available locally at:

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

### Out-of-Scope Test

```text
How much is Netflix?
```

The assistant should decline the competitor-related query and remain within the Tonton support scope.

---

## 🔑 Key Design Decisions

### FAQ-Level Chunking

Each Question + Answer pair is treated as one semantic chunk because each FAQ represents a complete unit of information.

This avoids splitting an FAQ question from its corresponding answer.

### Multilingual Embeddings

A multilingual embedding model was selected to improve retrieval across:

- Formal Bahasa Melayu
- Conversational Bahasa Melayu
- English
- Mixed Malay-English

This is particularly useful for real-world customer queries that may contain informal or mixed-language phrasing.

### ChromaDB

ChromaDB provides a lightweight vector database suitable for the current FAQ knowledge base and local development.

It enables semantic similarity search without requiring external vector database infrastructure.

### Retrieval-Augmented Generation

Instead of sending the user's question directly to the LLM, the system first retrieves relevant information from the Tonton knowledge base.

```text
Traditional LLM:

User Question
      ↓
     LLM
      ↓
   Response


TontonAssist RAG:

User Question
      ↓
Semantic Retrieval
      ↓
Relevant Tonton FAQ
      ↓
Gemini + Retrieved Context
      ↓
Grounded Response
```

This helps keep responses relevant to the supplied Tonton knowledge base.

---

## 🔮 Future Improvements

Potential improvements include:

- Similarity thresholding
- Hybrid keyword + semantic search
- Retrieved-document reranking
- Retrieval evaluation dataset
- Conversation-aware retrieval
- Larger Tonton knowledge base
- Automated FAQ synchronization
- Monitoring and analytics
- Improved fallback and escalation handling
- Automated RAG evaluation

---

## 👤 Author

Developed as a multilingual RAG chatbot assessment project.

