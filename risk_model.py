def get_risk_level(symptoms: str):
    symptoms = symptoms.lower()

    if any(word in symptoms for word in ["chest pain", "collapse", "unconscious"]):
        return "HIGH"

    if any(word in symptoms for word in ["fever", "vomiting", "persistent pain"]):
        return "MEDIUM"

    return "LOW"