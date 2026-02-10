import streamlit as st
import pdfplumber
from v2_main import run_v2  # your V2 function

# Title of the app
st.title("AI Resume Role Suggestion (Version 2)")
st.write("Upload any resume PDF and get suggested roles with reasoning.")

# File uploader widget
uploaded_file = st.file_uploader("Upload Resume PDF", type="pdf")

if uploaded_file is not None:
    # Extract text from uploaded PDF
    with pdfplumber.open(uploaded_file) as pdf:
        resume_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            if text:  # some PDFs may have blank pages
                resume_text += text

    # Pass extracted text to your V2 model
    suggested_roles = run_v2(resume_text)  # skill_ck untouched

    # sorting
    suggested_roles = sorted(
        suggested_roles,
        key=lambda x: x["match_score"],
        reverse=True
    )

    # Display the results
    st.subheader("Suggested Roles and Match Score:")

    if suggested_roles:
        for item in suggested_roles:
            if item["match_score"] > 0:
                st.write(
                    f"• **{item['role']}** — Match Score: {item['match_score']}%"
                )
    else:
        st.write("No roles matched. Check resume formatting or content.")

# Code to run his file : .\venv\Scripts\Activate.ps1  , streamlit run app.py

