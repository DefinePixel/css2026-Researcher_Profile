# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 13:38:34 2026

@author: DefinePixel
"""

import streamlit as st
import pandas as pd
import numpy as np
import random
import email
import mailbox
import time

# 1. Page Configuration
st.set_page_config(page_title="Student Researcher Profile", page_icon="🎓", layout="wide")

# 2. Sidebar Navigation
with st.sidebar:
    st.title("Navigation")
    # Using a radio button as a simple router
    selection = st.radio("Go to", ["Researcher Profile", "Research Projects", "Sources", "Contact"])
    
    st.markdown("---")
    st.info("Currently pursuing a MCOM in Information Systems at North West University (NWU).")

# 3. Content Sections
if selection == "Researcher Profile":
    st.title("Welcome to My Research Portfolio")
    st.sidebar.header("My Profile")

    # Profile Overview
    name = "DefinePixel"
    field = "Information Systems"
    institution = "North West University"

    # Display basic profile information
    st.write(f"**Name:** {name}")
    st.write(f"**Field of Research:** {field}")
    st.write(f"**Institution:** {institution}")
    

    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https://images2.pics4learning.com/catalog/c/cat0635227.jpg", caption="[DefinePixel]")
    with col2:
        st.subheader("About Me")
        st.write("I am a passionate student researcher focused on Information Systems and Data Management.")
        st.write("**Key Skills:** Java, Python, Streamlit, Data Visualization, Databases.")
        st.write("**Interests:** Data Analysis, Web Development, Databases.")
        st.write("Feel free to explore my projects and get in touch!")
        st.markdown("[Download CV](#)")

elif selection == "Research Projects":
    st.title("🔬 Research & Projects")
    
    with st.expander("Project 1: Interactive Data Analysis"):
        st.write("Analysis of [Topic] using [Tools].")
        if st.button("Run Mini Demo"):
            st.success("Project simulation running...")
            st.line_chart([10, 20, 15, 30, 25])
    
    with st.expander("Project 2: Web Application Development"):
        st.write("Created a web app using Streamlit for [CHPC 2026 Summer School].")
        st.write("Check out the code on [GitHub](https://github.com/DefinePixel/css2026-Researcher_Profile)")

    with st.expander("Project 3: Mini Memory Game", expanded=True):
        # font using a unique key 'game_area'
        with st.container(key="game_area"):
            # styles strictly to this container !!!!DOESN"T WORK
            st.markdown("""
            <link href="https://fonts.googleapis.com/css2?family=Pixelify+Sans:wght@400..700&display=swap" rel="stylesheet">
            <style>
            /* Targets only the container with key 'game_area' */
            [data-testid="stVerticalBlockBorderWrapper"]:has(.st-key-game_area) * {
                font-family: 'Pixelify Sans', sans-serif !important;
                font-size: 20.5px;
            }
            /* Scoped button styling */
            .st-key-game_area .stButton>button {
                border: 2px solid #000;
                border-radius: 0px;
                transition: 0.2s;
                width: 100%;
            }
            .st-key-game_area .stButton>button:hover {
                background-color: #fc4e7d;
                color: #000;
            }
            </style>
            """, unsafe_allow_html=True)

            st.title("🕹️ Mini Memory Game")
            st.write("Test your memory skills! Can you remember the sequence generated?")
            st.write("When ready, click 'Start New Game' to see the pattern for 3 seconds, then input your guess.")

            # Initialize State
            if 'stage' not in st.session_state:
                st.session_state.stage = "idle"

            def start_game():
                st.session_state.pattern = [random.choice(["🔴", "🔵", "🟢", "🟡"]) for _ in range(4)]
                st.session_state.stage = "showing"

            # Game Logic
            if st.session_state.stage == "idle":
                st.button("Start New Game", on_click=start_game)

            elif st.session_state.stage == "showing":
                st.subheader("Memorize this sequence:")
                cols = st.columns(4)
                for i, icon in enumerate(st.session_state.pattern):
                    cols[i].title(icon)
                
                progress_bar = st.progress(0)
                for percent_complete in range(100):
                    time.sleep(0.03)
                    progress_bar.progress(percent_complete + 1)
                    
                st.session_state.stage = "guessing"
                st.rerun()

            elif st.session_state.stage == "guessing":
                st.subheader("What was the pattern?")
                user_guess = st.text_input("Enter first letters (e.g., 'rbgy'):", key="guess_input").lower().strip()
                
                if st.button("Submit your Guess"):
                    mapping = {'r': "🔴", 'b': "🔵", 'g': "🟢", 'y': "🟡"}
                    clean_guess = [mapping.get(char) for char in user_guess if char in mapping]
                    
                    if clean_guess == st.session_state.pattern:
                        st.balloons()
                        st.success(f"Correct! {' '.join(clean_guess)}")
                        st.audio("34.wav", autoplay=True)
                    else:
                        st.audio("185.wav", autoplay=True)
                        st.error(f"Incorrect. It was {' '.join(st.session_state.pattern)}")
                    
                    st.session_state.stage = "idle"
                    st.button("Reset")


    with st.expander("Project 4: File Transfer Application"):
        st.write("A file transfer application using FRP (Fast Reverse Proxy).")
        st.markdown("**How it works:** This app uses **FRP** to tunnel local traffic through a public server, allowing you to securely share files from a private network without complex port forwarding.")
        # 1. Background Information
        st.markdown("**Steps to Use the App:**")
        st.markdown("1. Upload a file using the uploader below.\n2. Click 'Generate Secure Link' to create a public URL via FRP.\n3. Share the link for others to download the file securely.")
    
    #File Upload Logic
    uploaded_file = st.file_uploader("Choose a file to transfer", type=['pdf', 'zip', 'csv', 'txt'])
    
    if uploaded_file is not None:
        # Streamlit handles the file as a BytesIO object in memory
        file_bytes = uploaded_file.getvalue()
        st.success(f"File '{uploaded_file.name}' ready for transfer!")

        #Action Buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Generate Secure Link"):
                # Logic: In a real app, this would trigger the FRP tunnel 
                # and return the public URL mapped to your local instance.
                st.code(f"http://your-public-frp-server.com{uploaded_file.name}")
        
        with col2:
            # Download button for immediate local verification
            st.download_button(
                label="Verify & Download",
                data=file_bytes,
                file_name=uploaded_file.name,
                mime="application/octet-stream"
            )

    # 4. FRP Configuration Snippet
    with st.status("View FRP Configuration"):
        st.code("""
# frpc.ini (Client side on your machine)
[common]
server_addr = x.x.x.x
server_port = 7000

[streamlit_file_share]
type = http
local_port = 8501
custom_domains = your-public-frp-server.com
        """, language="ini")

    with st.expander("Project 5: Data Cleaning Pipeline"):
        st.write("Automated data cleaning using Python scripts.")
        if st.button("Run Data Cleaning Demo"):
            st.success("Data cleaning process initiated...")
            sample_dirty_data = pd.DataFrame({
                'Name': [' Alice ', 'Bob', None, 'David', ' Eve '],
                'Age': [25, 30, 35, None, 28],
                'City': ['New York', 'London', 'Paris', 'Tokyo', None]
            })
            st.write("Sample Dirty Data:")
            st.dataframe(sample_dirty_data) 
            cleaned_data = sample_dirty_data.dropna().applymap(lambda x: x.strip() if isinstance(x, str) else x)
            st.write("Cleaned Data:")
            st.dataframe(cleaned_data)

# 4. Sources Section
elif selection == "Sources":
    st.title("📚 Publications & Sources")
    st.markdown("- **[Paper Title]**, *Conference Name*, 2024. [Link to PDF](#)")
    st.markdown("- **[Poster Title]**, *University Symposium*, 2023. [View Poster](#)")

# 5. Contact Section
elif selection == "Contact":
    st.title("📬 Contact Information")
    st.write("Feel free to reach out to me for collaborations or inquiries!")
    st.write("You can reach me at the following links:")
    st.markdown("[LinkedIn](www.linkedin.com/in/mpho-nhlapo-82683b232) | [GitHub](https://github.com/DefinePixel) | [Email](mailto:pixelseren@gmail.com)")
  
    # Simple Contact Form
    with st.form("contact_form"):
        name = st.text_input("Name")
        msg = st.text_area("Message")
        if st.form_submit_button("Send"):
            st.toast(f"Thanks {name}, message received!")

#Footer
st.markdown("---")
st.caption("Developed using Streamlit | © 2026 [DefinePixel]")
