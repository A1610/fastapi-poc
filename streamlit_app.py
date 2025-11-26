import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"   # Local FastAPI URL
# Later: change to your Railway URL when deployed

st.set_page_config(page_title="FastAPI + Streamlit Auth")

st.title("User Authentication (Streamlit + FastAPI)")

# Tabs: Login / Signup
tab1, tab2 = st.tabs(["Login", "Signup"])

# ----------------- SIGNUP -----------------
with tab2:
    st.subheader("Create Account")

    signup_email = st.text_input("Email", key="signup_email")
    signup_password = st.text_input("Password", type="password", key="signup_password")

    if st.button("Signup"):
        payload = {
            "email": signup_email,
            "password": signup_password
        }
        response = requests.post(f"{API_URL}/signup", json=payload)

        if response.status_code == 200:
            st.success("Signup successful! Now login.")
        else:
            st.error(f"Signup failed: {response.text}")

# ----------------- LOGIN -----------------
with tab1:
    st.subheader("Login to Continue")

    login_email = st.text_input("Email", key="login_email")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        payload = {
            "email": login_email,
            "password": login_password
        }
        response = requests.post(f"{API_URL}/login", json=payload)

        if response.status_code == 200:
            st.success("Login successful!")

            data = response.json()
            access_token = data.get("access_token") or data.get("data", {}).get("session", {}).get("access_token")

            if access_token:
                st.session_state["token"] = access_token
                st.session_state["logged_in"] = True
            else:
                st.error("Token not received!")

        else:
            st.error("Invalid credentials")

# ------------- AFTER LOGIN → SHOW ROADMAP -----------------
if st.session_state.get("logged_in"):
    st.header("AI Engineer Roadmap 🚀")

    st.markdown("""
### 1️⃣ Python Fundamentals  
- Variables, Loops  
- OOP, Modules  
- Virtualenv  
---

### 2️⃣ Data Science Basics  
- NumPy  
- Pandas  
- Matplotlib  
---

### 3️⃣ Machine Learning  
- Regression  
- Classification  
- Clustering  
---

### 4️⃣ Deep Learning  
- Neural Networks  
- CNN  
- RNN / LSTM  
- Transformers  
---

### 5️⃣ MLOps  
- Docker  
- FastAPI  
- CI/CD  
---

### 6️⃣ Projects  
- Chatbot  
- Recommendation System  
- Image Classifier  
""")
