# This file evaluates resume skills against a single job role
# and returns score, fit status, matched and missing skills
# calculatoin part

def evaluate_role(resume_skills, role_name, role_skills):
    matched = []
    missing = []

    for skill in role_skills:
        if skill in resume_skills:
            matched.append(skill)
        else:
            missing.append(skill)

    # Avoid division error
    total_skills = len(role_skills)
    score = len(matched) / total_skills if total_skills > 0 else 0

    if score >= 0.75:
        fit = "Good"
    elif score >= 0.45:
        fit = "Moderate"
    else:
        fit = "Poor"

    return {
        "role": role_name,
        "score": round(score * 100, 2),   # percentage
        "fit": fit,
        "matched_skills": matched,
        "missing_skills": missing
    }
