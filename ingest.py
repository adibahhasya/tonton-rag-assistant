import requests
import chromadb

from pathlib import Path
from sentence_transformers import SentenceTransformer


DOC_ID = "1RrkdMo2oENLJaR6tRAFirHUp1_-8AhgJH08Z-YT01TQ"

GOOGLE_DOC_URL = (
    f"https://docs.google.com/document/d/"
    f"{DOC_ID}/export?format=txt"
)

EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"

COLLECTION_NAME = "tonton_faq"

BASE_DIR = Path(__file__).resolve().parent
CHROMA_PATH = BASE_DIR / "chroma_db"


# Shared embedding model
embedding_model = SentenceTransformer(
    EMBEDDING_MODEL
)


def load_document():
    print("Loading Google Doc...")

    response = requests.get(
        GOOGLE_DOC_URL,
        timeout=15
    )

    response.raise_for_status()

    print("Google Doc loaded successfully!")

    return response.text


def create_chunks(faq_text):
    raw_chunks = faq_text.split("Question:")

    chunks = []

    for chunk in raw_chunks:
        chunk = chunk.strip()

        if chunk and "Answer:" in chunk:
            chunks.append(
                "Question: " + chunk
            )

    print(
        "Total FAQ chunks:",
        len(chunks)
    )

    return chunks


def create_embeddings(chunks):
    print("Creating embeddings...")

    embeddings = embedding_model.encode(
        chunks,
        normalize_embeddings=True
    )

    print(
        "Embedding shape:",
        embeddings.shape
    )

    return embeddings


def build_vector_store():
    faq_text = load_document()

    chunks = create_chunks(
        faq_text
    )

    embeddings = create_embeddings(
        chunks
    )

    client = chromadb.PersistentClient(
        path=str(CHROMA_PATH)
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        configuration={
            "hnsw": {
                "space": "cosine"
            }
        }
    )

    ids = [
        f"faq_{i}"
        for i in range(len(chunks))
    ]

    metadatas = [
        {
            "source": "Tonton FAQ",
            "chunk_id": i
        }
        for i in range(len(chunks))
    ]

    collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )

    print(
        "Total records in vector store:",
        collection.count()
    )

    print(
        "ChromaDB ingestion completed successfully!"
    )

    return collection


def ensure_vector_store():
    """
    Return existing Chroma collection.
    Build it automatically if it does not exist.
    """

    client = chromadb.PersistentClient(
        path=str(CHROMA_PATH)
    )

    try:
        collection = client.get_collection(
            name=COLLECTION_NAME
        )

        if collection.count() > 0:
            print(
                "Existing ChromaDB collection found."
            )
            return collection

    except Exception:
        pass

    print(
        "ChromaDB collection not found. "
        "Building knowledge base..."
    )

    return build_vector_store()


if __name__ == "__main__":
    build_vector_store()