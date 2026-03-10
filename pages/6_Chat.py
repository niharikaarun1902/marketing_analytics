import os
import openai
import streamlit as st
from utils.layout import setup_page
from utils.data_loader import load_merged_data
from utils.chatbot import sanitize_input, query_llm

setup_page("Chat")

# --- API key: env, Streamlit secrets, or in-app input ---
def _get_api_key() -> str | None:
    key = os.environ.get("OPENAI_API_KEY")
    if key:
        return key
    try:
        key = st.secrets.get("OPENAI_API_KEY")
        if key:
            os.environ["OPENAI_API_KEY"] = key
            return key
    except Exception:
        pass
    return st.session_state.get("openai_api_key")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

api_key = _get_api_key()
if not api_key:
    st.info("🔑 **Set your OpenAI API key** to use Ask AI. Paste it below (stored for this session only) or add it to `.streamlit/secrets.toml`.")
    key_input = st.text_input(
        "OpenAI API Key",
        type="password",
        placeholder="sk-...",
        key="api_key_input",
        help="Get your key at platform.openai.com/api-keys",
    )
    if key_input and key_input.strip().startswith("sk-"):
        st.session_state["openai_api_key"] = key_input.strip()
        os.environ["OPENAI_API_KEY"] = key_input.strip()
        st.success("API key saved for this session. You can ask questions now.")
        st.rerun()
    elif key_input:
        st.warning("Key should start with 'sk-'. Check platform.openai.com/api-keys")
    st.markdown("---")
elif "openai_api_key" in st.session_state:
    if st.button("🔑 Change API key", key="change_key"):
        del st.session_state["openai_api_key"]
        if os.environ.get("OPENAI_API_KEY") == api_key:
            del os.environ["OPENAI_API_KEY"]
        st.rerun()

st.markdown("### Chat with Your Data")
st.caption(
    "Ask questions about your marketing campaigns, engagement, leads, "
    "funnel performance, or anything in the dataset."
)
st.markdown("")

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
                reply, _ = query_llm(conversation, df, api_key=api_key)
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
