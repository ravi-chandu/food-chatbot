import streamlit as st
import time, random, os

# --------------------------------------------
# Page Config
# --------------------------------------------
st.set_page_config(
    page_title="Food Delivery Chatbot ❤️",
    layout="wide",
    page_icon="🍕",
)

# --------------------------------------------
# Sidebar: Restaurant Info & Quick Stats
# --------------------------------------------
with st.sidebar:
    st.image(
        "https://cdn-icons-png.flaticon.com/512/3595/3595455.png",
        width=120,
    )
    st.title("🍴 PizzaNow")
    st.markdown("**City:** Hyderabad\n**Branches:** 5\n**Active Riders:** 23")
    st.divider()
    st.subheader("⚡ Quick Actions")
    if st.button("Track My Order"):
        st.session_state.history.append(
            ("user", "Track my latest order status.")
        )
    if st.button("Show Menu"):
        st.session_state.history.append(
            ("user", "What’s on the menu today?")
        )
    if st.button("Offers 💸"):
        st.session_state.history.append(("user", "Any special offers today?"))

# --------------------------------------------
# Chat State
# --------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# --------------------------------------------
# Helper: Simulated LLM/Agent Response
# --------------------------------------------
def chat_response(user_input: str):
    """Placeholder for LLM/SQL agent logic"""
    user_input = user_input.lower()
    if "menu" in user_input:
        return "🍕 Today's Menu:\n- Margherita\n- Veggie Supreme\n- BBQ Chicken\n- Cheese Burst Garlic Bread\n- Chocolate Lava Cake 🍫"
    elif "offer" in user_input:
        return "🎉 Ongoing Offers:\nBuy 1 Get 1 Free on Medium Pizzas (till 9 PM)"
    elif "track" in user_input or "order" in user_input:
        eta = random.randint(5, 20)
        status = random.choice(["Preparing 🍳", "Out for Delivery 🛵", "Almost There 🚦"])
        return f"Your order is currently **{status}**.\nEstimated arrival: {eta} minutes."
    elif "thanks" in user_input or "thank you" in user_input:
        return "You're most welcome! 😊 Enjoy your meal!"
    else:
        return "🤖 I'm still learning! You can ask about *menu*, *order status*, or *offers*."

# --------------------------------------------
# Header Section
# --------------------------------------------
st.markdown(
    "<h2 style='text-align:center;'>🍜 Food Delivery Chatbot ❤️</h2>",
    unsafe_allow_html=True,
)

# --------------------------------------------
# Two-Column Layout: Chat (70%) | Order Summary (30%)
# --------------------------------------------
col_chat, col_summary = st.columns([0.7, 0.3])

with col_chat:
    prompt = st.chat_input("Ask about menu, order, delivery, offers…")

    if prompt:
        st.session_state.history.append(("user", prompt))
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            placeholder.markdown("⏳ Thinking...")
            time.sleep(0.8)
            reply = chat_response(prompt)
            placeholder.markdown(reply)

        st.session_state.history.append(("assistant", reply))

    # Show chat history
    for role, msg in st.session_state.history:
        if role == "user":
            with st.chat_message("user"):
                st.markdown(msg)
        else:
            with st.chat_message("assistant"):
                st.markdown(msg)

with col_summary:
    st.subheader("🧾 Order Summary (Live)")
    dummy_orders = [
        {"id": "#1245", "item": "Margherita Pizza", "status": "Preparing 🍳"},
        {"id": "#1239", "item": "Cheese Garlic Bread", "status": "Delivered ✅"},
        {"id": "#1234", "item": "Veg Supreme Pizza", "status": "Out for Delivery 🛵"},
    ]
    for o in dummy_orders:
        with st.container(border=True):
            st.markdown(f"**Order {o['id']}** — {o['item']}")
            st.markdown(f"Status: {o['status']}")
            st.progress(random.randint(40, 100))

    st.divider()
    st.caption("🔔 Real-time tracking simulation enabled")

# --------------------------------------------
# Footer
# --------------------------------------------
st.markdown(
    "<br><center><small>Built with ❤️ using Streamlit | Powered by Microsoft Fabric RTI</small></center>",
    unsafe_allow_html=True,
)
