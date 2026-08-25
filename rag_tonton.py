import streamlit as st

from rag_final_test import (
    retrieve_faq,
    generate_answer
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="TontonAssist",
    page_icon="💬",
    layout="centered"
)


# =========================================================
# HEADER
# =========================================================

st.title(
    "💬 TontonAssist"
)

st.caption(
    "AI-powered Tonton customer support assistant"
)

st.write(
    "Ask about Tonton subscriptions, accounts, "
    "payments, advertisements, password reset, "
    "technical issues and other Tonton FAQs."
)


# =========================================================
# CHAT SESSION
# =========================================================

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hi! 👋 How can I help you with Tonton today?"
            )
        }
    ]


# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# =========================================================
# USER INPUT
# =========================================================

user_query = st.chat_input(
    "Ask TontonAssist..."
)


# =========================================================
# PROCESS USER QUERY
# =========================================================

if user_query:

    # Store user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_query
        }
    )

    # Display user message
    with st.chat_message("user"):

        st.markdown(
            user_query
        )


    # =====================================================
    # ASSISTANT RESPONSE
    # =====================================================

    with st.chat_message(
        "assistant"
    ):

        with st.spinner(
            "Searching Tonton FAQ..."
        ):

            # Retrieve relevant FAQ chunks
            results = retrieve_faq(
                user_query,
                top_k=3
            )

            # Generate grounded response
            answer = generate_answer(
                user_query,
                results
            )


        # Display final answer
        st.markdown(
            answer
        )


        # ================================================
        # OPTIONAL RAG TRANSPARENCY
        # ================================================

        with st.expander(
            "View retrieved sources"
        ):

            for i, (document, distance) in enumerate(
                zip(
                    results["documents"][0],
                    results["distances"][0]
                ),
                start=1
            ):

                st.markdown(
                    f"**Source {i}**"
                )

                st.caption(
                    f"Distance: {distance:.4f}"
                )

                st.text(
                    document
                )

                st.divider()


    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header(
        "About"
    )

    st.write(
        "TontonAssist uses Retrieval-Augmented "
        "Generation (RAG) to answer questions "
        "from the Tonton FAQ knowledge base."
    )

    st.write(
        "**Languages:** Malay, English, "
        "and mixed Malay-English."
    )

    if st.button(
        "Clear chat"
    ):

        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Hi! 👋 How can I help you "
                    "with Tonton today?"
                )
            }
        ]

        st.rerun()