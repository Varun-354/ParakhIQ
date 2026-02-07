# This file runs the single-role evaluator for multiple roles
# and ranks roles based on fit score

def rank_roles(results):
    return sorted(results, key=lambda x: x["match_score"], reverse=True)


def best_fit(ranked_roles):
    top = ranked_roles[0]

    explanation = (
        f"The resume best aligns with the role '{top['role']}' "
        f"with a match score of {round(top['match_score'], 2)}. "
        f"This indicates strong overall alignment with the role requirements."
    )

    return top["role"], explanation


