import streamlit as st
import time

# --- 1. Setup ---
st.set_page_config(page_title="Food Delivery Bot", page_icon="🍕")
st.title("🍕 Fake Food Delivery Bot")
st.write("Ask me about an order ID! (Try 'FX101', 'FX102', or 'FX103')")
st.write("This app is deployed via an automated MLOps pipeline!")

# --- 2. Chat Interface ---
user_question = st.text_input("Your order ID:")

if user_question:
    # --- 3. Fake Bot Logic ---
    # Convert to uppercase and remove spaces to make it easier to check
    order_id = user_question.upper().strip()
    
    with st.spinner("Accessing order database..."):
        time.sleep(1.5) # Pretend to be thinking

        if order_id == "FX101":
            st.success("**Status for FX101:** Your Pepperoni Pizza is out for delivery!")
        elif order_id == "FX102":
            st.info("**Status for FX102:** Your Chicken Biryani was delivered at 1:30 PM.")
        elif order_id == "FX103":
            st.warning("**Status for FX103:** Your Veg Noodles are still being prepared.")
        else:
            st.error(f"**Error:** Sorry, I couldn't find any order with the ID '{order_id}'.")

