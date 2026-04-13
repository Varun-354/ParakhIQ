import fitz  # PyMuPDF

def extract_text_from_pdf(file_path):
    text = ""

    doc = fitz.open(file_path)

    for page in doc:
        text += page.get_text()

    return text



import re

def clean_text(text):
    # remove multiple newlines
    text = re.sub(r'\n+', '\n', text)

    # remove multiple spaces
    text = re.sub(r'\s+', ' ', text)

    # remove special characters (keep basic ones)
    text = re.sub(r'[^\w\s.,@+-]', '', text)

    return text.strip()


def extract_sections(text):
    sections = {
        "skills": "",
        "education": "",
        "experience": "",
        "projects": ""
    }

    # keywords to detect sections
    keywords = {
        "skills": ["skills", "technical skills"],
        "education": ["education", "academic"],
        "experience": ["experience", "work experience"],
        "projects": ["projects", "personal projects"]
    }

    current_section = None

    for line in text.split('\n'):
        line_lower = line.lower()

        for section, keys in keywords.items():
            if any(key in line_lower for key in keys):
                current_section = section
                break

        if current_section:
            sections[current_section] += line + " "

    return sections


def extract_skills(text, skills_list):
    text = text.lower()
    found_skills = []

    for skill in skills_list:
        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))


ALL_SKILLS = [
    "python", "java", "sql", "machine learning",
    "django", "flask", "react", "html", "css",
    "javascript", "docker", "aws", "kubernetes"
]


def parse_resume(file_path):
    raw_text = extract_text_from_pdf(file_path)
    cleaned_text = clean_text(raw_text)

    sections = extract_sections(raw_text)

    skills = extract_skills(cleaned_text, ALL_SKILLS)

    return {
        "skills": skills,
        "education": sections["education"],
        "experience": sections["experience"],
        "projects": sections["projects"]
    }

if __name__ == "__main__":
    file_path = "Sample1.pdf"   # put your resume here

    text = extract_text_from_pdf(file_path)

    print("\n===== EXTRACTED TEXT =====\n")
    print(text[:500])  # print first 1000 chars
    raw_text = extract_text_from_pdf(file_path)
    cleaned_text = clean_text(raw_text)

    print("\nCLEANED TEXT:\n")
    print(cleaned_text[:500])

    sections = extract_sections(raw_text)  # use raw_text here

    print("\nSECTIONS:\n")
    for key, value in sections.items():
        print(f"{key.upper()}:\n{value[:200]}\n")



if __name__ == "__main__":
    file_path = "Sample1.pdf"

    result = parse_resume(file_path)

    print("\nFINAL OUTPUT:\n")
    for key, value in result.items():
        print(f"{key.upper()}:\n{value}\n")