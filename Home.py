import streamlit as st
import base64
import os
import subprocess


image_path = "images\picture.jpg"  
if os.path.exists(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

with open(image_path, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode()

# Page configuration
st.set_page_config(page_title="BusinessBuddy - Get Started", layout="centered")

# Custom background CSS
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{encoded_string}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    .overlay-container {{
        # background-color: rgba(255, 255, 255, 0.85);
        padding: 50px;
        margin-top: 2px;
        border-radius: 15px;
        text-align: center;
        max-width: 800px;
        margin-left: 100%;
        margin-right: auto;
        # box-shadow: 0px 4px 20px rgba(0,0,0,0.2);
    }}
    .stButton>button {{
        background-color: #28a745;
        color: white;
        font-size: 18px;
        padding: 10px 30px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        transition: 0.3s;
         margin-left:32%;
    }}
    .stButton>button:hover {{
        background-color: #218838;
        transform: scale(1.05);
        
    }}
   
    </style>
""", unsafe_allow_html=True)


st.markdown('<div class="overlay-container">', unsafe_allow_html=True)

st.markdown("""<div class="content">,
    <h1>     Welcome to <span style="color:#28a745">BusinessBuddy</span> 💼</h1>
    <p><strong>BusinessBuddy</strong> is your smart business companion for real-time market discovery, trend analysis, and data-powered insights.</p>
    <p>Get started on your journey to smarter decisions and better opportunities today!</p>
""", unsafe_allow_html=True)

# Button
if st.button("🚀 Get Started"):
    subprocess.Popen(["streamlit", "run", "app.py"])
    st.success("Launching BusinessBuddy...")
    st.stop()

st.markdown('</div>', unsafe_allow_html=True)
