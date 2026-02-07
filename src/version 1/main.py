# ==========================================
# BASELINE AI RESUME SHORTLISTING MODEL (v1)
# ==========================================

# -------- STEP 1: Imports --------
import os
import pdfplumber
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# -------- STEP 2: Paths --------
RESUME_FOLDER = "Resumes/"
JD_PATH = "Job_Descripter/JD1.txt"


# -------- STEP 3: Text Preprocessing --------
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


# -------- STEP 4: Load & Clean Resumes --------
def load_resumes(resume_folder):
    resumes = []
    resume_names = []

    for file in os.listdir(resume_folder):
        if file.endswith(".pdf"):
            file_path = os.path.join(resume_folder, file)

            with pdfplumber.open(file_path) as pdf:
                full_text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        full_text += page_text + " "

            cleaned_text = preprocess_text(full_text)
            resumes.append(cleaned_text)
            resume_names.append(file)

    return resumes, resume_names


# -------- STEP 5: Load & Clean Job Description --------
with open(JD_PATH, "r", encoding="utf-8") as f:
    jd_text = preprocess_text(f.read())


# -------- STEP 6: TF-IDF Vectorization --------
resumes_text, resume_files = load_resumes(RESUME_FOLDER)

documents = resumes_text + [jd_text]

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(documents)


# -------- STEP 7: Similarity Scoring --------
resume_vectors = tfidf_matrix[:-1]
jd_vector = tfidf_matrix[-1]

similarity_scores = cosine_similarity(resume_vectors, jd_vector)


# -------- STEP 8: Selection Decision --------
THRESHOLD = 0.60

print("\n=== Resume Shortlisting Results ===\n")

for i, score in enumerate(similarity_scores):
    status = "SELECTED" if score[0] >= THRESHOLD else "DISQUALIFIED"
    print(f"{resume_files[i]} | Score: {score[0]:.2f} | Status: {status}")
