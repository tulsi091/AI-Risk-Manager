import re


# =====================================================
# Risk Score Calculation
# =====================================================

def calculate_risk_score(text: str) -> int:
    """
    Calculate a risk score from AI response.

    Priority:
    1. Read explicit Risk Score from Gemini response.
    2. Otherwise estimate using keywords.
    """

    if not text:
        return 0

    # Try to extract explicit score
    patterns = [
        r"Risk Score\s*[:\-]?\s*(\d{1,3})",
        r"Score\s*[:\-]?\s*(\d{1,3})/100",
        r"(\d{1,3})\s*/\s*100"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            score = int(match.group(1))
            return max(0, min(score, 100))

    # Keyword based estimation
    score = 0

    high_words = [
        "critical",
        "severe",
        "high risk",
        "cyber attack",
        "breach",
        "fraud",
        "lawsuit",
        "bankruptcy",
        "regulatory violation",
        "data leak",
    ]

    medium_words = [
        "medium risk",
        "compliance",
        "competition",
        "inflation",
        "market volatility",
        "operational",
        "security",
        "supply chain",
    ]

    low_words = [
        "stable",
        "strong",
        "secure",
        "low risk",
        "growth",
        "opportunity",
    ]

    lower = text.lower()

    for word in high_words:
        if word in lower:
            score += 15

    for word in medium_words:
        if word in lower:
            score += 8

    for word in low_words:
        if word in lower:
            score -= 3

    score = max(5, min(score, 100))

    return score


# =====================================================
# Risk Level
# =====================================================

def risk_level(score: int) -> str:

    if score >= 80:
        return "🔴 Critical"

    elif score >= 60:
        return "🟠 High"

    elif score >= 40:
        return "🟡 Medium"

    elif score >= 20:
        return "🟢 Low"

    else:
        return "✅ Very Low"
    # =====================================================
# Recommendations
# =====================================================

def extract_recommendations(text: str) -> list:
    """
    Extract recommendation bullet points from AI response.
    """

    if not text:
        return []

    patterns = [
        r"#\s*Recommendations\s*(.*?)(?=#\s*Final\s*Conclusion|$)",
        r"##\s*Recommendations\s*(.*?)(?=##\s*Final\s*Conclusion|$)",
        r"Recommendations\s*:?\s*(.*?)(?=Final\s*Conclusion|$)",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE | re.DOTALL
        )

        if match:

            block = match.group(1).strip()

            recommendations = []

            for line in block.splitlines():

                line = line.strip()

                if line.startswith(("-", "*", "•")):
                    recommendations.append(
                        line.lstrip("-*• ").strip()
                    )

                elif re.match(r"^\d+\.", line):
                    recommendations.append(
                        re.sub(r"^\d+\.\s*", "", line)
                    )

            if recommendations:
                return recommendations

    return []
# =====================================================
# Conclusion
# =====================================================

def extract_conclusion(text: str) -> str:
    """
    Extract Final Conclusion section.
    """

    if not text:
        return "Conclusion not available."

    patterns = [

        r"#\s*Final\s*Conclusion\s*(.*)$",

        r"##\s*Final\s*Conclusion\s*(.*)$",

        r"Final\s*Conclusion\s*:?\s*(.*)$",

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE | re.DOTALL
        )

        if match:

            conclusion = match.group(1).strip()

            if conclusion:
                return conclusion

    return "Conclusion not available."
# =====================================================
# Clean Markdown
# =====================================================

def clean_markdown(text: str) -> str:
    """
    Remove markdown symbols from AI output.
    """

    if not text:
        return ""

    text = re.sub(r"[*#>`]", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()
# =====================================================
# Business Description
# =====================================================

def extract_business_description(text: str) -> str:

    if not text:
        return "Business description not available."

    match = re.search(
        r"Business Description(.*?)(Executive Summary|$)",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )

    if match:
        return match.group(1).strip()

    return "Business description not available."


# =====================================================
# Executive Summary
# =====================================================

def extract_summary(text: str) -> str:

    if not text:
        return "Summary not available."

    match = re.search(
        r"Executive Summary(.*?)(Top 5 Risks|Risk Score|Severity|Recommendations|$)",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )

    if match:
        return match.group(1).strip()

    return "Summary not available."


# =====================================================
# Top Risks
# =====================================================

def extract_top_risks(text: str) -> list:

    if not text:
        return []

    match = re.search(
        r"Top 5 Risks(.*?)(Risk Score|Severity|Recommendations|Final Conclusion|$)",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )

    if not match:
        return []

    block = match.group(1).strip()

    risks = []

    for line in block.splitlines():

        line = line.strip()

        if line.startswith(("-", "*", "•")):
            risks.append(line.lstrip("-*• ").strip())

        elif re.match(r"^\d+\.", line):
            risks.append(re.sub(r"^\d+\.\s*", "", line))

    return risks