import streamlit as st
import requests
from PIL import Image


st.image("images/purplewave-CndzKbNl.svg", width=150)

st.title("AI QA Assistant")
st.write("Generate test cases and test plans from your requirements.")


# --- Custom CSS for toggle ---
toggle_css = """
<style>
.theme-toggle {
    position: absolute;
    top: 15px;
    right: 25px;
    font-size: 26px;
    cursor: pointer;
}
</style>
"""
st.markdown(toggle_css, unsafe_allow_html=True)

# --- Initialize theme ---
if "theme" not in st.session_state:
    st.session_state.theme = "light"

# --- Toggle Button ---
toggle_icon = "🌞" if st.session_state.theme == "light" else "🌙"
if st.button(toggle_icon, key="theme_toggle", help="Toggle theme"):
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

# --- Apply Theme ---
if st.session_state.theme == "dark":
    st.markdown(
        """
        <style>
        body { background-color: #0E1117; color: white; }
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
        body { background-color: white; color: black; }
        </style>
        """,
        unsafe_allow_html=True
    )

st.write(f"Current theme: **{st.session_state.theme.capitalize()}**")
# --- Mode Selection ---
mode = st.radio("Select what you want to generate:", ["Test Cases", "Test Plan"], horizontal=True)

result = None  # placeholder for results

# --- Test Cases Flow ---
if mode == "Test Cases":
    st.subheader("Generate Test Cases")

    user_story = st.text_area("User Story", placeholder="As a user, I want to...")
    acceptance_criteria = st.text_area("Acceptance Criteria", placeholder="Given..., When..., Then...")

    if st.button("Generate Test Cases"):
        if user_story.strip() or acceptance_criteria.strip():
            # TODO: Replace with Django API call
            result = f"""
            ✅ **Generated Test Cases:**
            1. Verify valid login with correct username and password
            2. Verify error message for incorrect password
            3. Verify account is locked after 3 failed attempts
            """
        else:
            st.warning("Please provide a user story or acceptance criteria.")

# --- Test Plan Flow ---
elif mode == "Test Plan":
    st.subheader("Generate Test Plan")

    uploaded_files = st.file_uploader(
        "Upload Requirement Document(s) (BRD, SRS, etc.)",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True
    )

    if st.button("Generate Test Plan"):
        if uploaded_files:
            # TODO: Replace with Django API call
            filenames = [f.name for f in uploaded_files]
            result = f"""
            ✅ **Generated Test Plan (from {', '.join(filenames)}):**
            - Scope: Login functionality
            - Risks: Weak passwords, brute force attempts
            - Assumptions: User already registered
            """
        else:
            st.warning("Please upload at least one requirement document.")

# --- Display Result ---
if result:
    st.markdown("### 📌 Generated Output")
    st.markdown(result)