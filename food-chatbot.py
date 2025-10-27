import streamlit as st
import time
from typing import List, Dict

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(page_title="Kamala 🤖", layout="wide", page_icon="🤖")

# -------------------------------------------------
# THEME & LAYOUT CSS (mobile-first, high-contrast)
# -------------------------------------------------
st.markdown("""
<style>
/* Container widths */
.block-container { padding-top: 0.75rem; padding-bottom: 2rem; max-width: 1100px; }

/* Global dark look */
body, .main { background:#0b0f1a !important; color:#e5e7eb !important; }
hr { border-color:#1f2937; }

/* Top bar */
.topbar {
  display:flex; align-items:center; justify-content:space-between;
  gap:12px; padding:10px 12px; border:1px solid #263042; border-radius:12px;
  background:#0f172a;
}
.brand { display:flex; align-items:center; gap:10px; min-width:0; }
.brand h1 { font-size:1.05rem; font-weight:700; margin:0; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.userwrap { display:flex; align-items:center; gap:10px; }
.userpill {
  background:#111827; border:1px solid #263042; padding:6px 10px; border-radius:999px;
  font-size:.85rem; max-width:45vw; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;
}
.logout-btn button { background:#1f2937; color:#e5e7eb; border:1px solid #374151; }
.logout-btn button:hover { background:#374151; }

/* Section headings */
.section-title { margin:10px 0 6px 0; font-size:1.05rem; font-weight:700; display:flex; align-items:center; gap:8px; }

/* Two-column area */
.wrap { display:grid; grid-template-columns: 1fr 360px; gap:18px; }
@media (max-width: 768px) {
  .wrap { grid-template-columns: 1fr; }
}

/* Card */
.card { background:#0f172a; border:1px solid #263042; border-radius:14px; padding:12px; }

/* Chat area */
.chat-scroll {
  max-height: 52vh; min-height: 38vh; overflow-y: auto; padding-right:6px;
}
.chat-bubble-user{
  background:#1f2937; color:#e5e7eb; padding:10px 14px; border-radius:12px; display:inline-block; max-width:92%;
}
.chat-bubble-bot{
  background:#111827; color:#e5e7eb; padding:10px 14px; border-radius:12px; display:inline-block; max-width:92%;
}
.k-notice {
  background:#0b3b2b; color:#d1fae5; border:1px solid #115e59; border-radius:10px; padding:8px 10px; font-size:.9rem;
}

/* Chat input readability */
[data-testid="stChatInput"] textarea, [data-testid="stChatInput"] div[contenteditable="true"] {
  color:#e5e7eb !important;
}

/* Order cards */
.order-card { background:#0f172a; border:1px solid #263042; border-radius:12px; padding:10px 12px; }
.order-card + .order-card { margin-top:10px; }
.order-title { font-weight:700; margin-bottom:2px; }
.order-meta { font-size:.9rem; opacity:.95; }

/* Spacing helpers */
.mt-8 { margin-top:8px; }
.mb-8 { margin-bottom:8px; }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# STATE
# -------------------------------------------------
if "user" not in st.session_state:
    st.session_state.user = None
if "history" not in st.session_state:
    st.session_state.history: List[Dict[str, str]] = []
if "notice" not in st.session_state:
    st.session_state.notice = ""   # ephemeral banner text set by bot

# -------------------------------------------------
# MOCK DATA / REPLACE WITH REAL DB
# -------------------------------------------------
def get_user_orders(email: str):
    return [
        {"id":"#1045","item":"Margherita Pizza","status":"Out for Delivery 🛵","eta":"12 mins"},
        {"id":"#1038","item":"Garlic Breadsticks","status":"Delivered ✅","eta":"Delivered"},
    ]

# Kamala replies WITHOUT dumping orders into chat
def kamala_reply(user_msg: str) -> str:
    m = user_msg.lower()
    if any(k in m for k in ["track","where","status","order","eta"]):
        # refresh orders panel; show a compact notice instead of long lines
        st.session_state.notice = "I’ve refreshed your latest order status below 👇"
        return "Sure. Showing your current order status below."
    if "menu" in m:
        return "📋 Menu highlights: Margherita, Peri-Peri Chicken, Veggie Delight, Cheese Garlic Bread, Brownie Sundae."
    if "offer" in m or "discount" in m:
        return "💸 Offer: Buy 1 Get 1 Free on Medium Pizzas until 10 PM."
    if any(k in m for k in ["hi","hello","hey"]):
        name = st.session_state.user.split("@")[0].title()
        return f"Hello {name}! I’m **Kamala 🤖**. How can I help you today?"
    return "I can help with *menu*, *offers*, or *order tracking*. What would you like to check?"

# -------------------------------------------------
# VIEWS
# -------------------------------------------------
def show_login():
    st.markdown("<div class='topbar'><div class='brand'>🍜 <h1>Kamala 🤖</h1></div><div class='userwrap'></div></div>", unsafe_allow_html=True)
    with st.form("login_form"):
        email = st.text_input("Sign in with email", placeholder="you@example.com")
        submitted = st.form_submit_button("Continue")
    if submitted:
        if email and "@" in email:
            st.session_state.user = email.strip()
            st.session_state.history = []
            st.session_state.notice = ""
            st.rerun()
        else:
            st.warning("Please enter a valid email.")

def logout():
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.session_state.user = None
    st.rerun()

def show_app():
    # Top bar
    st.markdown(
        f"<div class='topbar'>"
        f"  <div class='brand'>🍜 <h1>Kamala 🤖</h1></div>"
        f"  <div class='userwrap'>"
        f"     <div class='userpill'>{st.session_state.user}</div>"
        f"     <div class='logout-btn'>"
        f"       {''}"
        f"     </div>"
        f"  </div>"
        f"</div>", unsafe_allow_html=True
    )
    # Place the real logout button (inside container after HTML to get Streamlit control)
    col1, col2, col3 = st.columns([0.6, 0.25, 0.15])
    with col3:
        if st.button("Logout", use_container_width=True):
            logout()

    st.markdown("<div class='section-title'>💬 Chat with Kamala</div>", unsafe_allow_html=True)

    # Main wrap: chat left, orders right
    st.markdown("<div class='wrap'>", unsafe_allow_html=True)

    # LEFT: Chat
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        # Notice banner if any
        if st.session_state.notice:
            st.markdown(f"<div class='k-notice'>✅ {st.session_state.notice}</div>", unsafe_allow_html=True)
            st.session_state.notice = ""  # clear after showing once

        # Scrollable chat history
        st.markdown("<div class='chat-scroll'>", unsafe_allow_html=True)
        for m in st.session_state.history:
            with st.chat_message("user" if m["role"]=="user" else "assistant"):
                bubble = "chat-bubble-user" if m["role"]=="user" else "chat-bubble-bot"
                st.markdown(f"<div class='{bubble}'>{m['content']}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Input (sticky bottom by Streamlit)
        prompt = st.chat_input("Ask about your order, offers, or menu…")
        if prompt:
            st.session_state.history.append({"role":"user","content":prompt})
            reply = kamala_reply(prompt)
            st.session_state.history.append({"role":"assistant","content":reply})
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # RIGHT: Orders panel
    with st.container():
        st.markdown("<div class='section-title'>📦 Your Orders</div>", unsafe_allow_html=True)
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        for o in get_user_orders(st.session_state.user):
            st.markdown(
                f"<div class='order-card'>"
                f"<div class='order-title'>Order {o['id']}</div>"
                f"{o['item']}<br>"
                f"<div class='order-meta'>Status: {o['status']} &nbsp; | &nbsp; ETA: {o['eta']}</div>"
                f"</div>", unsafe_allow_html=True
            )
        st.caption("🔒 Orders are filtered to your account.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # end wrap

# -------------------------------------------------
# ROUTER
# -------------------------------------------------
if st.session_state.user:
    show_app()
else:
    show_login()
