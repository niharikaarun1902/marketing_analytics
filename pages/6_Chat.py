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
if "chat_usage" not in st.session_state:
    st.session_state["chat_usage"] = {
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
        "request_count": 0,
    }

# --- Usage metrics (session) ---
u = st.session_state["chat_usage"]
if u["request_count"] > 0:
    with st.expander("📊 API usage this session", expanded=False):
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Prompt tokens", f"{u['prompt_tokens']:,}")
        c2.metric("Completion tokens", f"{u['completion_tokens']:,}")
        c3.metric("Total tokens", f"{u['total_tokens']:,}")
        c4.metric("Requests", u["request_count"])
        # GPT-4.1-mini approx: $0.15/1M input, $0.60/1M output (as of 2024)
        est_cost = (u["prompt_tokens"] * 0.15 + u["completion_tokens"] * 0.60) / 1_000_000
        st.caption(f"Estimated cost this session: ~${est_cost:.4f} (GPT-4.1-mini pricing). Check [platform.openai.com](https://platform.openai.com/usage) for account limits.")

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
                reply, usage_dict = query_llm(conversation, df)
            st.session_state["chat_usage"]["prompt_tokens"] += usage_dict["prompt_tokens"]
            st.session_state["chat_usage"]["completion_tokens"] += usage_dict["completion_tokens"]
            st.session_state["chat_usage"]["total_tokens"] += usage_dict["total_tokens"]
            st.session_state["chat_usage"]["request_count"] += 1
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
