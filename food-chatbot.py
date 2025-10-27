import streamlit as st
import time, random

# ============ CONFIG ============
st.set_page_config(page_title="Kamala 🤖", layout="wide", page_icon="🤖")

# ============ THEME / MOBILE CSS ============
st.markdown("""
<style>
/* base */
.block-container { padding-top: 1rem; padding-bottom: 2rem; }
body, .main { background:#0b0f1a; color:#e5e7eb; }

/* compact header */
.header {
  display:flex; align-items:center; justify-content:space-between;
  gap:12px; margin-bottom:10px;
}
.brand { display:flex; align-items:center; gap:10px; }
.brand h2 { margin:0; font-weight:700; font-size:1.25rem; }  /* short title */
.badge { font-size:.85rem; opacity:.9; }

/* sections */
.section { margin-top:12px; margin-bottom:8px; }
.card { background:#0f172a; border:1px solid #263042; border-radius:14px; padding:12px 14px; }
.card + .card { margin-top:10px; }

/* chat */
.chat-wrap { margin-top:6px; }
.chat-bubble-user{
  background:#1f2937; color:#e5e7eb; padding:10px 14px; border-radius:12px;
  display:inline-block; max-width:92%;
}
.chat-bubble-bot{
  background:#111827; color:#e5e7eb; padding:10px 14px; border-radius:12px;
  display:inline-block; max-width:92%;
}
[data-testid="stChatInput"] textarea, [data-testid="stChatInput"] div[contenteditable="true"] {
  color:#e5e7eb !important;
}

/* buttons */
.stButton>button { background:#1f2937; color:#e5e7eb; border:1px solid #374151; }
.stButton>button:hover { background:#374151; }

/* mobile tweaks */
@media (max-width: 768px) {
  .block-container { padding-left: .75rem; padding-right: .75rem; }
  .brand h2 { font-size:1.1rem; }
  .section h3 { font-size:1.05rem; }
  .card { padding:12px; }
  .chat-wrap { margin-top:2px; }
}
</style>
""", unsafe_allow_html=True)

# ============ STATE ============
if "user" not in st.session_state: st.session_state.user = None
if "history" not in st.session_state: st.session_state.history = []  # [{"role":..., "content":...}]

# ============ MOCK DATA ============
def get_user_orders(email:str):
    return [
        {"id":"#1045","item":"Margherita Pizza","status":"Out for Delivery 🛵","eta":"12 mins"},
        {"id":"#1038","item":"Garlic Breadsticks","status":"Delivered ✅","eta":None},
    ]

def kamala_reply(text:str)->str:
    m = text.lower()
    if "menu" in m:
        return "📋 Menu: Margherita, Peri-Peri Chicken, Veggie Delight, Cheese Garlic Bread, Brownie Sundae."
    if "offer" in m or "discount" in m:
        return "💸 Offer: Buy 1 Get 1 Free on all Medium Pizzas till 10 PM."
    if any(k in m for k in ["track","order","status","where","eta"]):
        lines = [f"{o['id']} • {o['item']} — {o['status']} • ETA: {o['eta'] or 'Delivered'}"
                 for o in get_user_orders(st.session_state.user)]
        return "📦 Your orders:\n" + "\n".join(lines)
    if any(k in m for k in ["hi","hello","hey"]):
        name = st.session_state.user.split("@")[0].title()
        return f"Hello {name}! I’m **Kamala 🤖**. How can I help you today?"
    return "I can help with *menu*, *offers*, or *order tracking*. What would you like to check?"

# ============ VIEWS ============
def show_login():
    st.markdown("<div class='header'><div class='brand'><span>🍜</span><h2>Kamala 🤖</h2></div></div>", unsafe_allow_html=True)
    with st.form("login"):
        email = st.text_input("Sign in with email", placeholder="you@example.com")
        ok = st.form_submit_button("Continue")
    if ok:
        if email and "@" in email:
            st.session_state.user = email.strip()
            st.session_state.history = []
            st.rerun()
        else:
            st.warning("Please enter a valid email.")

def logout():
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.session_state.user = None
    st.rerun()

def show_app():
    # header
    st.markdown(
        f"<div class='header'>"
        f"<div class='brand'><span>🍜</span><h2>Kamala 🤖</h2></div>"
        f"<div class='badge'>{st.session_state.user}</div>"
        f"</div>", unsafe_allow_html=True
    )
    col_btn, _ = st.columns([0.25, 0.75])
    with col_btn:
        if st.button("Logout", use_container_width=True): logout()

    st.divider()

    # layout: chat then orders; mobile-friendly spacing
    st.markdown("<div class='section'><h3>💬 Chat with Kamala</h3></div>", unsafe_allow_html=True)

    # render history first (prevents duplicates)
    for m in st.session_state.history:
        with st.chat_message("user" if m["role"]=="user" else "assistant"):
            bubble = "chat-bubble-user" if m["role"]=="user" else "chat-bubble-bot"
            st.markdown(f"<div class='{bubble}'>{m['content']}</div>", unsafe_allow_html=True)

    # input
    prompt = st.chat_input("Ask about your order, offers, or menu…")
    if prompt:
        st.session_state.history.append({"role":"user","content":prompt})
        reply = kamala_reply(prompt)  # plug your real LLM/agent here
        st.session_state.history.append({"role":"assistant","content":reply})
        st.rerun()

    st.markdown("<div class='section'><h3>📦 Your Orders</h3></div>", unsafe_allow_html=True)
    for o in get_user_orders(st.session_state.user):
        st.markdown(
            f"<div class='card'><b>Order {o['id']}</b><br>{o['item']}<br>"
            f"<small>Status: {o['status']} &nbsp;|&nbsp; ETA: {o['eta'] or 'Delivered'}</small></div>",
            unsafe_allow_html=True
        )
    st.caption("🔒 Orders are filtered to your account.")

# ============ ROUTER ============
if st.session_state.user:
    show_app()
else:
    show_login()
