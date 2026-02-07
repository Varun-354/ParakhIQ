# =====================================
# “This code acts as the controller that evaluates one resume against multiple job roles
#  and produces scores and skill evidence using modular components.”
# =====================================


import os

from multi_jd import ROLE_SKILLS
from Calculate import evaluate_role
from role import rank_roles, best_fit
from pdf_reader import extract_text_from_pdf

# ---------- PATH SETUP ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RESUME_PATH = os.path.join(
    BASE_DIR, "..", "..", "Resumes", "Sample_Resume_Data.pdf"
)

# ---------- PIPELINE ----------
def run_v2(resume_text):
    print("🚀 Running Version-2 Resume Pipeline...\n")

    results = []

    for role, jd_text in ROLE_SKILLS.items():
        score_dict = evaluate_role(
            resume_text,
            jd_text,
            ROLE_SKILLS[role]
        )

        # ---- SAFE SCORE EXTRACTION ----
        if isinstance(score_dict, dict):
            if "final_score" in score_dict:
                score = score_dict["final_score"]
            elif "score" in score_dict:
                score = score_dict["score"]
            else:
                # fallback: average numeric values
                numeric_vals = [v for v in score_dict.values() if isinstance(v, (int, float))]
                score = sum(numeric_vals) / len(numeric_vals) if numeric_vals else 0.0
        else:
            score = float(score_dict)

        results.append({
            "role": role,
            "match_score": score
        })

    return results


# ---------- RUNNER ----------
if __name__ == "__main__":
    resume_text = extract_text_from_pdf(RESUME_PATH)

    output = run_v2(resume_text)

    ranked = rank_roles(output)
    best, explanation = best_fit(ranked)

    print("\n🏆 Ranked Roles:")
    for r in ranked:
        print(f"{r['role']} → {round(r['match_score'], 2)}")

    print("\n🧠 Best Fit Explanation:")
    print(explanation)
