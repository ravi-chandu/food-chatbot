import streamlit as st

st.set_page_config(page_title="Food Chatbot ❤️", layout="wide")

if "history" not in st.session_state:
    st.session_state.history = []

st.title("🍜 Food Chatbot ❤️")

prompt = st.chat_input("Ask about menu, order status, delivery time…")
if prompt:
    st.session_state.history.append(("user", prompt))
    # TODO: replace with your real logic
    reply = f"Order bot 🤖: I heard '{prompt}'."
    st.session_state.history.append(("assistant", reply))

for role, msg in st.session_state.history:
    with st.chat_message(role):
        st.markdown(msg)
