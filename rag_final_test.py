import os
import requests

from pathlib import Path
from dotenv import load_dotenv

from ingest import (
    ensure_vector_store,
    embedding_model
)


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def get_api_key():
    api_key = os.getenv("GEMINI_API_KEY")

    if api_key:
        return api_key

    try:
        import streamlit as st

        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]

    except Exception:
        pass

    raise ValueError("GEMINI_API_KEY not found.")


# =========================================================
# VECTOR STORE
# =========================================================

collection = ensure_vector_store()


# =========================================================
# RETRIEVAL FUNCTION
# =========================================================

def retrieve_faq(user_query, top_k=3):

    query_embedding = embedding_model.encode(
        [user_query],
        normalize_embeddings=True
    )

    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=top_k
    )

    return results


# =========================================================
# GEMINI CONFIG
# =========================================================

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/"
    "models/gemini-3.6-flash:generateContent"
)


# =========================================================
# GENERATION FUNCTION
# =========================================================

def generate_answer(user_query, results):

    api_key = get_api_key()

    context = "\n\n".join(
        results["documents"][0]
    )

    prompt = f"""
You are TontonAssist, a customer support assistant for Tonton.

Only answer questions related to Tonton.

If the user asks about competitors such as Netflix, Disney+, Viu,
iQIYI, WeTV, Astro, sooka, Prime Video, HBO, or other non-Tonton
services, politely say that you can only assist with Tonton-related
questions.

Do not compare Tonton with competitors.

For Tonton-related questions, answer using ONLY the retrieved FAQ
context below.

Do not invent information.

Respond in the same language as the user.

If the user uses mixed Malay and English, respond naturally in mixed
Malay and English.

If the answer is not found in the context, say:
"I could not find this information in the Tonton FAQ."

CONTEXT:
{context}

USER QUESTION:
{user_query}

ANSWER:
"""

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    }

    response = requests.post(
        GEMINI_URL,
        headers=headers,
        json=payload,
        timeout=30
    )

    print("Gemini status:", response.status_code)

    if response.status_code != 200:
        print(response.text)
        return "Unable to generate an answer at the moment."

    data = response.json()

    return (
        data["candidates"][0]
        ["content"]
        ["parts"][0]
        ["text"]
    )


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    user_query = "nak tukar password"

    results = retrieve_faq(
        user_query,
        top_k=3
    )

    print("\nRetrieved FAQ:")
    print(results["documents"][0][0])

    answer = generate_answer(
        user_query,
        results
    )

    print("\nFinal answer:")
    print(answer)