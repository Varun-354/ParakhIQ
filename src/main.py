import pdfplumber

# Path of the resume PDF
resume_path = "Resumes/Sample_Resume_Data.pdf"

# Open and read the PDF
with pdfplumber.open(resume_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            print(text)

