import pickle

file_path = "Sample_3.pdf"
# load model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# load vectorizer
with open('tfidf.pkl', 'rb') as f:
    tfidf = pickle.load(f)


from phase_2 import parse_resume

def predict_role_from_resume(file_path):
    data = parse_resume(file_path)

    # combine important text
    combined_text = (
        data["education"] + " " +
        data["experience"] + " " +
        data["projects"]
    )

    # clean again (VERY IMPORTANT for ML consistency)
    import re
    combined_text = combined_text.lower()
    combined_text = re.sub(r'[^a-z\s]', ' ', combined_text)
    combined_text = re.sub(r'\s+', ' ', combined_text).strip()

    # transform
    vector = tfidf.transform([combined_text])

    # predict
    prediction = model.predict(vector)

    return prediction[0]


if __name__ == "__main__":
    file_path = "Sample_3.pdf"

    role = predict_role_from_resume(file_path)

    print("\nPREDICTED ROLE:\n", role)


from phase_2 import parse_resume
from phase_1 import (
    recommend_top_roles,
    get_skill_gap,
    suggest_certifications
)

import re

# load model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# load tfidf
with open('tfidf.pkl', 'rb') as f:
    tfidf = pickle.load(f)


def full_resume_analysis(file_path):
    # ===== Phase 2 =====
    data = parse_resume(file_path)

    skills = data["skills"]

    # ===== Phase 3 (ML Prediction) =====
    combined_text = (
        data["education"] + " " +
        data["experience"] + " " +
        data["projects"]
    )

    combined_text = combined_text.lower()
    combined_text = re.sub(r'[^a-z\s]', ' ', combined_text)
    combined_text = re.sub(r'\s+', ' ', combined_text).strip()

    vector = tfidf.transform([combined_text])
    predicted_role = model.predict(vector)[0]

    # ===== Phase 1 (Recommendation) =====
    top_roles = recommend_top_roles(skills)

    final_output = []

    for role, score in top_roles:
        missing = get_skill_gap(skills, role)
        certs = suggest_certifications(missing)

        final_output.append({
            "role": role,
            "score": score,
            "missing_skills": missing,
            "recommendations": certs
        })

    return {
        "predicted_role": predicted_role,
        "skills": skills,
        "recommendations": final_output
    }


if __name__ == "__main__":
    # file_path = "sample_resume.pdf"

    result = full_resume_analysis(file_path)

    print("\nFINAL RESULT:\n")

    print("Predicted Role:", result["predicted_role"])
    print("\nExtracted Skills:", result["skills"])

    for item in result["recommendations"]:
        print("\n----------------------")
        print("Role:", item["role"])
        print("Score:", item["score"])
        print("Missing Skills:", item["missing_skills"])
        print("Courses:", item["recommendations"])