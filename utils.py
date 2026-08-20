import random

def calculate_risk_score(industry):
    scores = {
        "FinTech": random.randint(70, 95),
        "Healthcare": random.randint(50, 85),
        "E-Commerce": random.randint(45, 80),
        "Education": random.randint(30, 70),
        "Manufacturing": random.randint(40, 75)
    }

    return scores.get(industry, random.randint(40, 80))


def risk_level(score):
    if score >= 70:
        return "High Risk"
    elif score >= 40:
        return "Medium Risk"
    else:
        return "Low Risk"