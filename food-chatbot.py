import streamlit as st
from typing import List, Dict

# -------------------- Page config --------------------
st.set_page_config(page_title="Kamala 🤖", layout="wide", page_icon="🤖")

# -------------------- Safe, minimal CSS --------------------
st.markdown("""
<style>
/* Tight container, readable on mobile */
.block-container {max-width: 980px; padding-top: 0.75rem; padding-bottom: 1.5rem;}
/* High-contrast dark */
body, .main {background:#0b0f1a !important; color:#e5e7eb !important;}
hr {border-color:#1f2937;}
/* Top bar */
.topbar {background:#0f172a; border:1px solid #263042; border-radius:12px; padding:10px;}
.email-pill {background:#111827; border:1px solid #263042; border-radius:999px; padding:6px 10px; font-size:.85rem; max-width:50vw; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;}
/* Cards */
.card {background:#0f172a; border:1px solid #263042; border-radius:12px; padding:12px;}
/* Headings */
.h3 {font-weight:700; font-size:1.05rem; margin:8px 0 6px;}
/* Chat bubbles */
.bubble-user  {background:#1f2937; color:#e5e7eb; padding:10px 14px; border-radius:12px; display:inline-block; max-width:95%;}
.bubble-bot   {background:#111827; color:#e5e7eb; padding:10px 14px; border-radius:12px; display:inline-block; max-width:95%;}
.notice       {background:#0b3b2b; color:#d1fae5; border:1px solid #115e59; border-radius:10px; padding:8px 10px; font-size:.9rem;}
/* Chat scroll */
.chat-box {max-height: 52vh; min-height: 36vh; overflow-y: auto; padding-right:6px;}
/* Inputs readable */
[data-testid="stChatInput"] textarea, [data-testid="stChatInput"] div[contenteditable="true"] {color:#e5e7eb !important;}
/* Buttons */
.stButton>button {background:#1f2937; color:#e5e7eb; border:1px solid #374151;}
.stButton>button:hover {background:#374151;}
</style>
""", unsafe_allow_html=True)

# -------------------- State --------------------
if "user" not in st.session_state: st.session_state.user = None
if "history" not in st.session_state: st.session_state.history: List[Dict[str,str]] = []
if "notice" not in st.session_state: st.session_state.notice = ""

# -------------------- Mock data (replace with DB) --------------------
def get_user_orders(email: str):
    return [
        {"id":"#1045","item":"Margherita Pizza","status":"Out for Delivery 🛵","eta":"12 mins"},
        {"id":"#1038","item":"Garlic Breadsticks","status":"Delivered ✅","eta":"Delivered"},
    ]

def kamala_reply(msg: str) -> str:
    m = msg.lower()
    if any(k in m for k in ["track","status","where","order","eta"]):
        st.session_state.notice = "I refreshed your latest order status below 👇"
        return "Sure — check your **Orders** section below."
    if "menu" in m:
        return "📋 Menu highlights: Margherita, Peri-Peri Chicken, Veggie Delight, Cheese Garlic Bread, Brownie Sundae."
    if "offer" in m or "discount" in m:
        return "💸 Offer: Buy-1-Get-1 on Medium Pizzas (till 10 PM)."
    if any(k in m for k in ["hi","hello","hey"]):
        name = st.session_state.user.split("@")[0].title()
        return f"Hello {name}! I’m **Kamala 🤖**. How can I help you today?"
    return "I can help with *menu*, *offers*, or *order tracking*. What would you like to check?"

# -------------------- Auth views --------------------
def show_login():
    st.markdown("<div class='topbar'><b>🍜 Kamala 🤖</b></div>", unsafe_allow_html=True)
    with st.form("login"):
        email = st.text_input("Sign in with email", placeholder="you@example.com")
        ok = st.form_submit_button("Continue")
    if ok:
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

# -------------------- App view --------------------
def show_app():
    # Top bar
    with st.container():
        st.markdown("<div class='topbar'>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([0.3, 0.5, 0.2], vertical_alignment="center")
        with c1:
            st.markdown("**🍜 Kamala 🤖**")
        with c2:
            st.markdown(f"<div class='email-pill'>{st.session_state.user}</div>", unsafe_allow_html=True)
        with c3:
            if st.button("Logout", use_container_width=True): logout()
        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    # --- Chat (always first) ---
    st.markdown("<div class='h3'>💬 Chat with Kamala</div>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        if st.session_state.notice:
            st.markdown(f"<div class='notice'>✅ {st.session_state.notice}</div>", unsafe_allow_html=True)
            st.session_state.notice = ""

        st.markdown("<div class='chat-box'>", unsafe_allow_html=True)
        for m in st.session_state.history:
            with st.chat_message("user" if m["role"]=="user" else "assistant"):
                bubble = "bubble-user" if m["role"]=="user" else "bubble-bot"
                st.markdown(f"<div class='{bubble}'>{m['content']}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        prompt = st.chat_input("Ask about your order, offers, or menu…")
        if prompt:
            st.session_state.history.append({"role":"user","content":prompt})
            reply = kamala_reply(prompt)
            st.session_state.history.append({"role":"assistant","content":reply})
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # --- Orders (separate, never in chat) ---
    st.markdown("<div class='h3'>📦 Your Orders</div>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        for o in get_user_orders(st.session_state.user):
            st.markdown(
                f"**Order {o['id']}**  \n"
                f"{o['item']}  \n"
                f"<span class='order-meta'>Status: {o['status']} &nbsp; | &nbsp; ETA: {o['eta']}</span>",
                unsafe_allow_html=True,
            )
            st.markdown("<hr/>", unsafe_allow_html=True)
        st.caption("🔒 Orders are filtered to your account.")
        st.markdown("</div>", unsafe_allow_html=True)

# -------------------- Router --------------------
if st.session_state.user:
    show_app()
else:
    show_login()
