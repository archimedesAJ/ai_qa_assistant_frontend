import time
import streamlit as st
import pandas as pd
import base64
from io import BytesIO
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# --- Logo in Sidebar ---
st.sidebar.image("images/purplewave-logo.jpg", use_container_width=True)

# --- App Title ---
st.sidebar.title("QA Assistant Platform")

# --- Project Selection ---
project = st.sidebar.selectbox("Select Your Team", ["PW Appraisal", "PW Field Tool", "PW CRM", "PW Accounting Service"])

# --- Tabs ---
tab = st.sidebar.radio("Navigation", ["Test Cases", "Test Plan"])

# --- Data Storage ---
if "test_cases" not in st.session_state:
    st.session_state.test_cases = []

if "file_uploader_key" not in st.session_state:
    st.session_state.file_uploader_key = 0

if "test_plan" not in st.session_state:
    st.session_state.test_plan = ""


# --- Test Cases Tab ---
if tab == "Test Cases":
    st.title("Test Case Generator")

    user_story = st.text_area("User Story *", key="user_story")
    acceptance_criteria = st.text_area("Acceptance Criteria *", key="acceptance_criteria")

    error_placeholder = st.empty()  # placeholder for error

    if st.button("Generate Test Cases"):
        if not user_story.strip() or not acceptance_criteria.strip():
            error_placeholder.error("⚠️ Please fill in both *User Story* and *Acceptance Criteria* before generating test cases.")
            time.sleep(3)  # wait 3 seconds
            error_placeholder.empty()  # clear the alert
            st.rerun()  # refresh after alert disappears
        else:
            # Placeholder Gherkin generator
            # test_case = {
            #     "title": "Verify login functionality",
            #     "description": f"Story: {user_story}\nCriteria: {acceptance_criteria}",
            #     "gherkin": """Feature: Login
            #     Scenario: Valid user login
            #         Given user is on login page
            #         When user enters valid credentials
            #         Then dashboard is displayed"""
            # }
            # st.session_state.test_cases.append(test_case)

            # --- Generate multiple test cases ---
            test_cases = [
                {
                    "title": "Verify login with valid credentials",
                    "description": f"Story: {user_story}\nCriteria: {acceptance_criteria}",
                    "gherkin": """Feature: Login
                Scenario: Valid user login
                    Given user is on login page
                    When user enters valid credentials
                    Then dashboard is displayed"""
                },
                {
                    "title": "Verify login with invalid password",
                    "description": f"Story: {user_story}\nCriteria: {acceptance_criteria}",
                    "gherkin": """Feature: Login
                Scenario: Invalid password
                    Given user is on login page
                    When user enters valid username and invalid password
                    Then error message is displayed"""
                },
                {
                    "title": "Verify login with empty fields",
                    "description": f"Story: {user_story}\nCriteria: {acceptance_criteria}",
                    "gherkin": """Feature: Login
                Scenario: Empty fields
                    Given user is on login page
                    When user clicks login without entering credentials
                    Then error message is displayed"""
                }
            ]

            st.session_state.test_cases.extend(test_cases)


    if st.session_state.test_cases:
        st.subheader("Generated Test Cases")
        for i, tc in enumerate(st.session_state.test_cases):
            with st.expander(tc["title"]):
                st.write(tc["description"])
                st.code(tc["gherkin"], language="gherkin")
                if st.button(f"Delete {i}"):
                    st.session_state.test_cases.pop(i)
                    st.rerun()

        # --- Row with Export, Send to Jira, Reset ---
        col1, col2, col3 = st.columns([6, 1, 1])

        # Export button
        with col1:
            if st.button("⬇️ Export All"):
                df = pd.DataFrame(st.session_state.test_cases)
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "Download CSV",
                    data=csv,
                    file_name="test_cases.csv",
                    mime="text/csv"
                )

        jira_placeholder = st.empty()  # placeholder for Jira alert

        # Send to Jira button
        with col2:
            if st.button("📨", help="Send to Jira"):
                jira_placeholder.success("✅ Sent to Jira")
                time.sleep(3)
                jira_placeholder.empty()
                st.rerun()

        # Reset Test Case Generator button
        with col3:
            if st.button("🔄", help="Reset Test Case Generator"):
                st.session_state.clear()  # clear everything
                st.rerun() 


# --- Test Plan Tab ---
if tab == "Test Plan":
    st.title("Test Plan Generator")

    uploaded_files = st.file_uploader(
        "Upload Documents [BRD / SRS / FSD]",
        type=["docx", "pdf"],   # restrict file types
        accept_multiple_files=True,
        key=f"file_uploader_{st.session_state.file_uploader_key}"
    )

    if uploaded_files:
        st.subheader("Uploaded Files")
        content = ""
        for file in uploaded_files:
            content += file.read().decode("utf-8", errors="ignore") + "\n"
        st.text_area("Combined Content", content, height=200)

        if st.button("Generate Test Plan"):
            st.session_state.test_plan = f"Test Plan for {project}\n\n{content[:500]}..."

    if st.session_state.test_plan:
        st.subheader("Generated Test Plan")
        st.text_area("Test Plan", st.session_state.test_plan, height=300)

        # --- Right-aligned Reset Button (icon only) ---
        col1, col2 = st.columns([8, 1])
        with col2:
            if st.button("🔄", help="Reset Test Plan"):
                st.session_state.test_plan = ""
                st.session_state.file_uploader_key += 1
                st.rerun()

        # Export DOCX
        if st.button("Export as DOCX"):
            doc = Document()
            doc.add_heading(f"Test Plan - {project}", 0)
            doc.add_paragraph(st.session_state.test_plan)
            buffer = BytesIO()
            doc.save(buffer)
            buffer.seek(0)
            st.download_button("Download DOCX", buffer, file_name="test_plan.docx")

        # Export PDF
        if st.button("Export as PDF"):
            buffer = BytesIO()
            c = canvas.Canvas(buffer, pagesize=letter)
            text_object = c.beginText(40, 750)
            for line in st.session_state.test_plan.split("\n"):
                text_object.textLine(line)
            c.drawText(text_object)
            c.showPage()
            c.save()
            buffer.seek(0)
            st.download_button("Download PDF", buffer, file_name="test_plan.pdf")

# --- Footer ---
st.markdown(
    """
    <hr style="margin-top: 50px; margin-bottom: 10px;">
    <div style="text-align: center; color: grey; font-size: 14px;">
        © 2025 QA Assistant Platform. Built with ❤️ by Team 4
    </div>
    """,
    unsafe_allow_html=True
)
