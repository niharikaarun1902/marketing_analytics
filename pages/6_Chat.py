import openai
import streamlit as st
from utils.layout import setup_page
from utils.data_loader import load_merged_data
from utils.chatbot import sanitize_input, query_llm

setup_page("Chat")

st.markdown("### Chat with Your Data")
st.caption(
    "Ask questions about your marketing campaigns, engagement, leads, "
    "funnel performance, or anything in the dataset."
)

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

for msg in st.session_state["chat_history"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask about your campaigns…")

if user_input:
    st.session_state["chat_history"].append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    refusal = sanitize_input(user_input)
    if refusal:
        st.session_state["chat_history"].append(
            {"role": "assistant", "content": refusal}
        )
        with st.chat_message("assistant"):
            st.markdown(refusal)
        st.stop()

    with st.chat_message("assistant"):
        try:
            df = load_merged_data()
            conversation = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state["chat_history"]
            ]
            with st.spinner("Thinking…"):
                reply = query_llm(conversation, df)
        except ValueError as exc:
            reply = str(exc)
        except openai.AuthenticationError:
            reply = (
                "Invalid OpenAI API key. Check that OPENAI_API_KEY "
                "is set correctly in your environment."
            )
        except openai.RateLimitError:
            reply = "OpenAI rate limit reached. Please wait a moment and try again."
        except openai.APIConnectionError:
            reply = "Could not connect to OpenAI. Check your internet connection."
        except Exception as exc:
            reply = f"An error occurred: {exc}"

        st.markdown(reply)

    st.session_state["chat_history"].append(
        {"role": "assistant", "content": reply}
    )
