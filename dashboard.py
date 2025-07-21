import streamlit as st
import json
import os

st.set_page_config(page_title="Job Alert Bujji 💌", page_icon="📬")
st.title("📬 Subscribe to Job Alerts")

email = st.text_input("📧 Your Email")
keywords = st.text_input("📝 Interested Keywords (comma separated)")

if st.button("🔔 Subscribe Me!"):
    if email and keywords:
        subscriber = {
            "email": email,
            "keywords": [kw.strip().lower() for kw in keywords.split(",")]
        }

        # Load or create subscribers file
        if os.path.exists("subscribers.json"):
            with open("subscribers.json", "r") as f:
                subscribers = json.load(f)
        else:
            subscribers = []

        if any(s["email"] == email for s in subscribers):
            st.warning("⚠️ You're already subscribed!")
        else:
            subscribers.append(subscriber)
            with open("subscribers.json", "w") as f:
                json.dump(subscribers, f, indent=2)
            st.success("✅ Subscribed successfully!")
    else:
        st.error("❌ Please enter both fields.")
