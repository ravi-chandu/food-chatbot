import streamlit as st
import random, time

# -------------------------
# CONFIG & THEME
# -------------------------
st.set_page_config(page_title="Food Chatbot ", layout="wide", page_icon="🍜")
st.markdown("""
<style>
.main, body { background:#0b0f1a !important; color:#e5e7eb !important; }
hr { border-color:#1f2937; }
.chat-bubble-user{ background:#1f2937; color:#e5e7eb; padding:10px 14px; border-radius:12px; display:inline-block; max-width:90%; }
.chat-bubble-bot{  background:#111827; color:#e5e7eb; padding:10px 14px; border-radius:12px; display:inline-block; max-width:90%; }
.order-box{ background:#0f172a; color:#e5e7eb; border:1px solid #263042; border-radius:12px; padding:12px 14px; }
[data-testid="stChatInput"] textarea, [data-testid="stChatInput"] div[contenteditable="true"] { color:#e5e7eb !important; }
.stButton>button { background:#1f2937; color:#e5e7eb; border:1px solid #374151; }
.stButton>button:hover { background:#374151; }
</style>
""", unsafe_allow_html=True)

# -------------------------
# STATE
# -------------------------
if "user" not in st.session_state:
    st.session_state.user = None          # email when logged in
if "history" not in st.session_state:
    st.session_state.history = []         # [{"role":"user|assistant", "content": "..."}]

# -------------------------
# MOCK DATA + BOT
# -------------------------
def get_user_orders(email: str):
    # Replace with real DB lookup filtered by email/user_id
    return [
        {"id": "#1045", "item": "Margherita Pizza", "status": "Out for Delivery 🛵", "eta": "12 mins"},
        {"id": "#1038", "item": "Garlic Breadsticks", "status": "Delivered ✅", "eta": None},
    ]

def bot_reply(text: str) -> str:
    m = text.lower()
    if "menu" in m:
        return "📋 Menu: Margherita, Peri Peri Chicken, Veggie Delight, Cheese Garlic Bread, Brownie Sundae."
    if "offer" in m or "discount" in m:
        return "💸 Offer: Buy 1 Get 1 Free on Medium Pizzas till 10 PM."
    if any(k in m for k in ["track","order","status","where","eta"]):
        lines = [f"{o['id']} → {o['item']} • {o['status']} • ETA: {o['eta'] or 'Delivered'}"
                 for o in get_user_orders(st.session_state.user)]
        return "📦 Your orders:\n" + "\n".join(lines)
    if any(k in m for k in ["hi","hello","hey"]):
        name = st.session_state.user.split('@')[0].title()
        return f"Hello {name} 👋 How can I help you today?"
    return "I can help with *menu*, *offers*, or *order tracking*. What would you like to check?"

# -------------------------
# VIEWS
# -------------------------
def show_login():
    st.markdown("### 🍜 Food Chatbot — Sign in")
    with st.form("login_form", clear_on_submit=False):
        email = st.text_input("Email", placeholder="you@example.com")
        submitted = st.form_submit_button("Login")
    if submitted:
        if email and "@" in email:
            st.session_state.user = email.strip()
            st.session_state.history = []     # fresh chat per login
            st.rerun()
        else:
            st.warning("Please enter a valid email.")

def logout():
    # Clear everything and rerun
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.session_state.user = None
    st.rerun()

def navbar():
    col_logo, col_title, col_btn = st.columns([0.06, 0.74, 0.20])
    with col_logo: st.markdown("### 🍜")
    with col_title: st.markdown("## PizzaNow Chat Assistant")
    with col_btn:
        st.markdown(f"**{st.session_state.user}**")
        if st.button("Logout", key="logout_btn", use_container_width=True):
            logout()
    st.markdown("---")

def show_app():
    navbar()
    col_chat, col_orders = st.columns([0.68, 0.32], gap="large")

    with col_chat:
        st.subheader("💬 Chat with Food Chatbot")

        # 1) render existing history (prevents duplicates)
        for m in st.session_state.history:
            with st.chat_message("user" if m["role"]=="user" else "assistant"):
                bubble = "chat-bubble-user" if m["role"]=="user" else "chat-bubble-bot"
                st.markdown(f"<div class='{bubble}'>{m['content']}</div>", unsafe_allow_html=True)

        # 2) input → append → bot → append → rerun
        prompt = st.chat_input("Ask about your order, offers, or menu…")
        if prompt:
            st.session_state.history.append({"role":"user","content":prompt})
            reply = bot_reply(prompt)                    # swap with real LLM/Agent call
            st.session_state.history.append({"role":"assistant","content":reply})
            st.rerun()

    with col_orders:
        st.subheader("📦 Your Orders")
        for o in get_user_orders(st.session_state.user):
            st.markdown(
                f"<div class='order-box'><b>Order {o['id']}</b><br>{o['item']}<br>"
                f"<small>Status: {o['status']} &nbsp;|&nbsp; ETA: {o['eta'] or 'Delivered'}</small></div>",
                unsafe_allow_html=True
            )
        st.caption("🔒 Orders are filtered to your account")

# -------------------------
# ROUTER
# -------------------------
if st.session_state.user:
    show_app()
else:
    show_login()
