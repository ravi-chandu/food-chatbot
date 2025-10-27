import streamlit as st
import time, random

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(page_title="PizzaNow 🍕 Chat Assistant", layout="wide", page_icon="🍕")

# High-contrast dark theme CSS
st.markdown("""
<style>
/* Page */
.main, body { background:#0b0f1a !important; color:#e5e7eb !important; }
hr { border-color:#1f2937; }

/* Chat bubbles */
.chat-bubble-user{
  background:#1f2937; color:#e5e7eb; padding:10px 14px; border-radius:12px; display:inline-block; max-width:90%;
}
.chat-bubble-bot{
  background:#111827; color:#e5e7eb; padding:10px 14px; border-radius:12px; display:inline-block; max-width:90%;
}

/* Order cards */
.order-box{
  background:#0f172a; color:#e5e7eb; border:1px solid #263042; border-radius:12px; padding:12px 14px; box-shadow:none;
}

/* Chat input */
[data-testid="stChatInput"] textarea { color:#e5e7eb !important; }
[data-testid="stChatInput"] div[contenteditable="true"] { color:#e5e7eb !important; }

/* Buttons */
.stButton>button { background:#1f2937; color:#e5e7eb; border:1px solid #374151; }
.stButton>button:hover { background:#374151; }
</style>
""", unsafe_allow_html=True)

# -------------------------
# STATE
# -------------------------
if "user" not in st.session_state:
    st.session_state.user = "ravichandu392@example.com"   # mock login; replace with real auth
if "history" not in st.session_state:
    st.session_state.history = []  # list[dict]: {"role": "user"|"assistant", "content": str}

# -------------------------
# Mock user-specific data
# -------------------------
def get_user_orders(email):
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
    if "track" in m or "order" in m or "status" in m:
        lines = [f"{o['id']} → {o['item']} • {o['status']} • ETA: {o['eta'] or 'Delivered'}"
                 for o in get_user_orders(st.session_state.user)]
        return "📦 Your orders:\n" + "\n".join(lines)
    if "hi" in m or "hello" in m:
        name = st.session_state.user.split('@')[0].title()
        return f"Hello {name} 👋 How can I help you today?"
    return "I can help with *menu*, *offers*, or *order tracking*. What would you like to check?"

# -------------------------
# UI HEADER
# -------------------------
col_logo, col_title, col_btn = st.columns([0.06, 0.74, 0.20])
with col_logo: st.markdown("### 🍕")
with col_title: st.markdown("## PizzaNow Chat Assistant")
with col_btn:
    if st.button("Logout"):
        st.session_state.clear()
        st.experimental_rerun()
st.markdown("---")

# -------------------------
# LAYOUT
# -------------------------
col_chat, col_orders = st.columns([0.68, 0.32], gap="large")

with col_chat:
    st.subheader("💬 Chat with PizzaNow Assistant")

    # 1) Render history FIRST (prevents duplicates)
    for m in st.session_state.history:
        with st.chat_message("user" if m["role"]=="user" else "assistant"):
            bubble = "chat-bubble-user" if m["role"]=="user" else "chat-bubble-bot"
            st.markdown(f"<div class='{bubble}'>{m['content']}</div>", unsafe_allow_html=True)

    # 2) Input -> append -> compute -> append -> rerun
    prompt = st.chat_input("Ask about your order, offers, or menu…")
    if prompt:
        st.session_state.history.append({"role":"user","content":prompt})
        reply = bot_reply(prompt)            # plug your real LLM/agent here
        st.session_state.history.append({"role":"assistant","content":reply})
        st.rerun()                           # re-render once; no double prints

with col_orders:
    st.subheader("📦 Your Orders")
    for o in get_user_orders(st.session_state.user):
        st.markdown(
            f"<div class='order-box'><b>Order {o['id']}</b><br>{o['item']}<br>"
            f"<small>Status: {o['status']} &nbsp;|&nbsp; ETA: {o['eta'] or 'Delivered'}</small></div>",
            unsafe_allow_html=True
        )
    st.caption("🔒 Showing orders for your account only")

st.markdown("<br><center><small>Built with ❤️ using Streamlit</small></center>", unsafe_allow_html=True)
