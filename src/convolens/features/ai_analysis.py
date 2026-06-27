import pandas as pd


NEGATIVE_TERMS = [
    "angry",
    "annoyed",
    "bad",
    "disappointed",
    "frustrated",
    "horrible",
    "issue",
    "problem",
    "ridiculous",
    "terrible",
    "unacceptable",
    "upset",
    "worst",
]

POSITIVE_TERMS = [
    "thanks",
    "thank you",
    "appreciate",
    "great",
    "helpful",
    "resolved",
    "perfect",
]


def estimate_customer_sentiment(text: str) -> str:
    text = str(text).lower()

    negative_count = sum(term in text for term in NEGATIVE_TERMS)
    positive_count = sum(term in text for term in POSITIVE_TERMS)

    if negative_count > positive_count:
        return "Negative"
    if positive_count > negative_count:
        return "Positive"
    return "Neutral"


def identify_root_cause(row: pd.Series) -> str:
    intent = row.get("intent", "General Support")
    risk_reason = row.get("risk_reason", "")

    if intent == "Refund / Compensation":
        return "The customer appears to be seeking financial resolution or compensation."
    if intent == "Billing / Charges":
        return "The conversation is likely driven by payment, billing, or unexpected charge concerns."
    if intent == "Delivery / Shipping":
        return "The customer appears to be affected by delivery, tracking, or fulfilment uncertainty."
    if intent == "Account / Login":
        return "The issue appears related to account access or authentication friction."
    if intent == "Technical Issue":
        return "The conversation appears to involve a product, platform, or service functionality issue."
    if "slow response time" in str(risk_reason):
        return "The customer experience may be affected by delayed support response."
    return "The conversation appears to be a general support enquiry without a clear dominant root cause."


def suggest_next_action(row: pd.Series) -> str:
    risk_level = row.get("risk_level", "Low")
    intent = row.get("intent", "General Support")

    if risk_level == "High":
        return "Prioritise for senior support review and provide a clear resolution path."
    if intent in ["Refund / Compensation", "Billing / Charges"]:
        return "Review the account history and confirm the financial resolution options available."
    if intent == "Delivery / Shipping":
        return "Check fulfilment status and provide a specific delivery or tracking update."
    if intent == "Technical Issue":
        return "Request technical details, confirm reproduction steps, and escalate if unresolved."
    return "Continue standard support handling and monitor for further escalation signals."


def generate_summary(row: pd.Series) -> str:
    company = row.get("company", "the support team")
    intent = row.get("intent", "General Support")
    risk_level = row.get("risk_level", "Low")
    message_count = int(row.get("message_count", 0))

    return (
        f"This conversation involves {company} and is classified as {intent}. "
        f"It contains {message_count} messages and is currently assessed as {risk_level.lower()} risk."
    )


def confidence_score(row: pd.Series) -> float:
    score = 0.45

    if pd.notna(row.get("intent")) and row.get("intent") != "General Support":
        score += 0.20

    if row.get("risk_reason") and row.get("risk_reason") != "No major risk signals":
        score += 0.20

    if row.get("message_count", 0) >= 3:
        score += 0.15

    return round(min(score, 1.0), 2)


def analyse_conversation(row: pd.Series) -> dict:
    text = row.get("conversation_text", "")

    return {
        "summary": generate_summary(row),
        "sentiment": estimate_customer_sentiment(text),
        "root_cause": identify_root_cause(row),
        "suggested_action": suggest_next_action(row),
        "confidence": confidence_score(row),
    }