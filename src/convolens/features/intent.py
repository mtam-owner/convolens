import pandas as pd


INTENT_KEYWORDS = {
    "Refund / Compensation": [
        "refund", "compensation", "money back", "reimburse", "chargeback"
    ],
    "Billing / Charges": [
        "charged", "charge", "billing", "bill", "payment", "invoice", "fee"
    ],
    "Cancellation": [
        "cancel", "cancellation", "unsubscribe", "terminate"
    ],
    "Delivery / Shipping": [
        "delivery", "delivered", "shipping", "shipment", "package", "tracking"
    ],
    "Account / Login": [
        "login", "log in", "password", "account", "locked out", "sign in"
    ],
    "Technical Issue": [
        "error", "bug", "not working", "broken", "issue", "problem", "crash"
    ],
    "Service Delay": [
        "waiting", "delayed", "delay", "late", "still waiting", "no response"
    ],
}


def detect_intent(text: str) -> str:
    text = str(text).lower()

    scores = {
        intent: sum(keyword in text for keyword in keywords)
        for intent, keywords in INTENT_KEYWORDS.items()
    }

    best_intent = max(scores, key=scores.get)

    if scores[best_intent] == 0:
        return "General Support"

    return best_intent


def enrich_with_intent(df: pd.DataFrame) -> pd.DataFrame:
    output = df.copy()
    output["intent"] = output["conversation_text"].fillna("").apply(detect_intent)
    return output