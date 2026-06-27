import pandas as pd


COMPLAINT_TERMS = [
    "angry",
    "annoyed",
    "awful",
    "bad service",
    "complaint",
    "disappointed",
    "frustrated",
    "horrible",
    "poor service",
    "ridiculous",
    "terrible",
    "unacceptable",
    "upset",
    "worst",
]

URGENCY_TERMS = [
    "asap",
    "immediately",
    "now",
    "urgent",
    "still waiting",
    "no response",
    "days",
    "hours",
    "again",
    "still not",
]

ESCALATION_TERMS = [
    "cancel",
    "cancellation",
    "chargeback",
    "compensation",
    "escalate",
    "lawyer",
    "manager",
    "refund",
    "report",
    "supervisor",
    "never again",
]


def count_terms(text: str, terms: list[str]) -> int:
    text = str(text).lower()
    return sum(term in text for term in terms)


def assign_risk_level(score: float) -> str:
    if score >= 0.65:
        return "High"
    if score >= 0.35:
        return "Medium"
    return "Low"


def build_risk_reason(row: pd.Series) -> str:
    reasons = []

    if row["complaint_score"] > 0:
        reasons.append("complaint language")

    if row["urgency_score"] > 0:
        reasons.append("urgency signals")

    if row["escalation_keyword_score"] > 0:
        reasons.append("escalation terms")

    if row["response_time_minutes"] >= 240:
        reasons.append("slow response time")

    if row["message_count"] >= 10:
        reasons.append("extended conversation")

    return ", ".join(reasons) if reasons else "No major risk signals"

def extract_terms(text: str, terms: list[str]) -> str:
    text = str(text).lower()
    matches = [term for term in terms if term in text]
    return ", ".join(matches)


def score_conversation_risk(df: pd.DataFrame) -> pd.DataFrame:
    output = df.copy()

    text = output["conversation_text"].fillna("").astype(str)

    output["complaint_term_count"] = text.apply(
        lambda value: count_terms(value, COMPLAINT_TERMS)
    )

    output["urgency_term_count"] = text.apply(
        lambda value: count_terms(value, URGENCY_TERMS)
    )

    output["escalation_term_count"] = text.apply(
        lambda value: count_terms(value, ESCALATION_TERMS)
    )
    output["complaint_terms"] = text.apply(
    lambda value: extract_terms(value, COMPLAINT_TERMS)
    )

    output["urgency_terms"] = text.apply(
        lambda value: extract_terms(value, URGENCY_TERMS)
    )

    output["escalation_terms"] = text.apply(
        lambda value: extract_terms(value, ESCALATION_TERMS)
    )

    output["complaint_score"] = (output["complaint_term_count"] / 3).clip(upper=1)
    output["urgency_score"] = (output["urgency_term_count"] / 3).clip(upper=1)
    output["escalation_keyword_score"] = (
        output["escalation_term_count"] / 3
    ).clip(upper=1)

    output["slow_response_score"] = (
        output["response_time_minutes"].fillna(0) / 240
    ).clip(upper=1)

    output["conversation_length_score"] = (
        output["message_count"].fillna(0) / 10
    ).clip(upper=1)

    output["escalation_score"] = (
        output["complaint_score"] * 0.30
        + output["urgency_score"] * 0.20
        + output["escalation_keyword_score"] * 0.25
        + output["slow_response_score"] * 0.15
        + output["conversation_length_score"] * 0.10
    ).round(3)

    output["risk_level"] = output["escalation_score"].apply(assign_risk_level)
    output["risk_reason"] = output.apply(build_risk_reason, axis=1)

    return output