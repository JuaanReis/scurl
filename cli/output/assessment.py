from .formatter import section

ASSESSMENTS: dict[str, str] = {
    "very low": (
        "O alvo apresenta características típicas de infraestrutura\n"
        "corporativa altamente estabelecida.\n"
        "Nenhum indicador forte de phishing, hospedagem descartável,\n"
        "ou manipulação suspeita de DNS foi detectado."
    ),
    "low": (
        "O alvo apresenta baixo risco geral.\n"
        "Alguns indicadores merecem atenção mas não são conclusivos."
    ),
    "medium": (
        "O alvo apresenta indicadores moderados de risco.\n"
        "Recomenda-se cautela e verificação adicional."
    ),
    "high": (
        "O alvo apresenta múltiplos indicadores de risco.\n"
        "Evite interagir com o conteúdo sem verificação prévia."
    ),
    "very high": (
        "O alvo apresenta fortes indicadores de atividade maliciosa.\n"
        "Interação não recomendada."
    ),
}

def print_assessment(result: dict):
    section("Assessment")
    risk_level = result.get("risk_level", "").lower()
    print(ASSESSMENTS.get(risk_level, "Avaliação indisponível."))