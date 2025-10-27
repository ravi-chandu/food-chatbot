import streamlit as st
import time, random, datetime

# --------------------------------------------
# CONFIG
# --------------------------------------------
st.set_page_config(page_title="PizzaNow 🍕 Chat Assistant", layout="wide", page_icon="🍕")
st.markdown("""
    <style>
        /* Global clean look */
        body { background-color: #fafafa; }
        .main { padding: 0rem 2rem; }
        .chat-bubble-user {
            background-color: #DCF8C6;
            padding: 10px 15px;
            border-radius: 12px;
            margin: 5px 0;
            display: inline-block;
            max-width: 80%;
        }
        .chat-bubble-bot {
            background-color: #f1f0f0;
            padding: 10px 15px;
            border-radius: 12px;
            margin: 5px 0;
            display: inline-block;
            max-width: 80%;
        }
        .order-box {
            background: white;
            padding: 12px 15px;
            border-radius: 10px;
            box-shadow: 0px 1px 5px rgba(0,0,0,0.1);
            margin-bottom: 10px;
        }
        hr { margin: 0.5rem 0rem; }
    </style>
""", unsafe_allow_html=True)

# --------------------------------------------
# SIMULATED LOGIN (mock user session)
# --------------------------------------------
if "user" not in st.session_state:
    st.session_state.user = None
if "history" not in st.session_state:
    st.session_state.history = []

def login_ui():
    st.image("https://cdn-icons-png.flaticon.com/512/3595/3595455.png", width=100)
    st.title("🍕 Welcome to PizzaNow")
    username = st.text_input("Enter your registered email")
    if st.button("Login"):
        if username.strip():
            st.session_state.user = username.strip()
            st.success(f"Welcome back, {username.split('@')[0].title()}!")
            st.rerun()
        else:
            st.warning("Please enter your email to continue.")

def logout_ui():
    st.session_state.user = None
    st.session_state.history = []
    st.rerun()

# --------------------------------------------
# APP NAVBAR
# --------------------------------------------
def navbar():
    with st.container():
        col1, col2, col3 = st.columns([0.05, 0.8, 0.15])
        with col1:
            st.image("https://cdn-icons-png.flaticon.com/512/3595/3595455.png", width=40)
        with col2:
            st.markdown("<h4 style='margin-top:8px;'>PizzaNow Chat Assistant</h4>", unsafe_allow_html=True)
        with col3:
            if st.button("Logout", use_container_width=True):
                logout_ui()
    st.markdown("---")

# --------------------------------------------
# SIMULATED DATA for current user
# --------------------------------------------
def get_user_orders(email):
    return [
        {"id": "#1045", "item": "Margherita Pizza", "status": "Out for Delivery 🛵", "eta": "12 mins"},
        {"id": "#1038", "item": "Garlic Breadsticks", "status": "Delivered ✅", "eta": None},
    ]

def bot_reply(user_input):
    msg = user_input.lower()
    if "menu" in msg:
        return "📋 Today's Menu:\n- Margherita\n- Peri Peri Chicken\n- Veggie Delight\n- Cheese Burst Garlic Bread\n- Brownie Sundae 🍨"
    elif "offer" in msg or "discount" in msg:
        return "💸 Current Offer: Buy 1 Get 1 on all Medium Pizzas till 10 PM!"
    elif "track" in msg or "order" in msg:
        orders = get_user_orders(st.session_state.user)
        lines = [f"{o['id']} → {o['item']} ({o['status']}) ETA: {o['eta'] or 'Delivered'}" for o in orders]
        return "📦 Your orders:\n" + "\n".join(lines)
    elif "hello" in msg or "hi" in msg:
        return f"Hello {st.session_state.user.split('@')[0].title()} 👋! How can I help you today?"
    elif "thank" in msg:
        return "Always happy to help! 😊"
    else:
        return "🤖 I can assist with your *menu*, *offers*, or *order tracking*. What would you like to check?"

# --------------------------------------------
# MAIN APP VIEW (after login)
# --------------------------------------------
def chat_ui():
    navbar()

    user_email = st.session_state.user
    user_orders = get_user_orders(user_email)

    col_chat, col_orders = st.columns([0.7, 0.3], gap="large")

    with col_chat:
        st.subheader("💬 Chat with PizzaNow Assistant")
        prompt = st.chat_input("Ask about your order, offers, or menu…")
        if prompt:
            st.session_state.history.append(("user", prompt))
            with st.chat_message("user"):
                st.markdown(f"<div class='chat-bubble-user'>{prompt}</div>", unsafe_allow_html=True)
            with st.chat_message("assistant"):
                placeholder = st.empty()
                placeholder.markdown("<div class='chat-bubble-bot'>Typing...</div>", unsafe_allow_html=True)
                time.sleep(0.7)
                reply = bot_reply(prompt)
                placeholder.markdown(f"<div class='chat-bubble-bot'>{reply}</div>", unsafe_allow_html=True)
            st.session_state.history.append(("assistant", reply))

        # Render previous messages
        for role, msg in st.session_state.history:
            if role == "user":
                with st.chat_message("user"):
                    st.markdown(f"<div class='chat-bubble-user'>{msg}</div>", unsafe_allow_html=True)
            else:
                with st.chat_message("assistant"):
                    st.markdown(f"<div class='chat-bubble-bot'>{msg}</div>", unsafe_allow_html=True)

    with col_orders:
        st.subheader("📦 Your Orders")
        for o in user_orders:
            with st.container():
                st.markdown(f"""
                    <div class='order-box'>
                        <b>Order {o['id']}</b><br>
                        {o['item']}<br>
                        <small>Status: {o['status']}<br>ETA: {o['eta'] or 'Delivered'}</small>
                    </div>
                """, unsafe_allow_html=True)
        st.caption("🔄 Auto-refresh every few minutes (simulated)")

    st.markdown("<br><center><small>Built with ❤️ using Streamlit</small></center>", unsafe_allow_html=True)

# --------------------------------------------
# RENDER
# --------------------------------------------
if st.session_state.user:
    chat_ui()
else:
    login_ui()
