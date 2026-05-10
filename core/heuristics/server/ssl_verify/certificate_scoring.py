from math import exp, log
TRUSTED_CAS = ["google trust services", "digicert", "sectigo", "comodo", "globalsign", "entrust", "wr2", "gr3", "gr4"]
LE_INDICATORS = ["let's encrypt", "letsencrypt"]

def f_age(age_days: int):
    """
    Avalia risco baseado na idade do certificado.
    Certificados muito recentes são mais comuns em phishing.
    Quanto mais novo, maior o risco.
    normalized_score ∈ [0,1]
    """

    if age_days is None or age_days < 0:
        return 1.0
    if age_days < 7:
        return 0.8   
    if age_days < 30:
        return 0.3   
    return 1 - exp(-age_days / 60)

def f_valid(validity_days: int) -> float:
    
    if validity_days is None or validity_days <= 0:
        return 1.0
    
    if validity_days < 30:
        return 1.0  
    
    if validity_days <= 120:
        return 0.0  
    
    if validity_days <= 398:
        return 0.1   

    return 0.4  

def f_san(san_count: int) -> float:

    if san_count == 0:
        return 0.5
    
    if san_count == 1:
        return 0.3 
    
    if san_count >= 2:
        return 0.0

    return 0.6  

def f_wild(san_list: list):
    """
    Detecta presença de wildcard (*) nos SANs.
    Wildcards ampliam o escopo do certificado — penalização leve.
    normalized_score ∈ {0, 1}
    """
    if not san_list:
        return 0.0
    return 0.2 if any("*" in x for x in san_list) else 0.0

def f_issuer(issuer: str) -> float:

    if not issuer:
        return 0.5
    
    issuer_lower = issuer.lower()
    
    if any(ca in issuer_lower for ca in TRUSTED_CAS):
        return 0.0   
    
    if any(ind in issuer_lower for ind in LE_INDICATORS):
        return 0.3   
    
    return 0.6       

def f_mismatch(hostname_mismatch: bool):
    """
    Verifica correspondência entre hostname e certificado.
    Mismatch indica erro de configuração, MITM ou phishing.
    normalized_score ∈ {0, 1}
    """

    if hostname_mismatch is None:
        return 1.0
    return 1.0 if hostname_mismatch else 0.0

def f_self_signed(is_self_signed: bool) -> float:
    """
    Detecta certificados autoassinados (issuer == subject).
    Certificados autoassinados não são validados por nenhuma CA confiável.
    normalized_score ∈ {0, 1}
    """
    if is_self_signed is None:
        return 1.0
    return 1.0 if is_self_signed else 0.0

def f_expired(days_until_expiry: int) -> float:
    """
    Penaliza certificados expirados ou próximos do vencimento.
    Sites legítimos geralmente renovam antes de expirar.
    normalized_score ∈ [0,1]
    """
    if days_until_expiry is None:
        return 1.0
    if days_until_expiry <= 0:
        return 1.0  # já expirado
    return exp(-days_until_expiry / 15) 

def f_org(organization: str) -> float:
    """
    Verifica presença de campo Organization no certificado.
    Certificados sem organização são mais comuns em phishing.
    """
    if not organization or organization.strip() == "":
        return 0.3  
    return 0.0