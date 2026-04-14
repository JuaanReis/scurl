def insights(heuristics: list[dict], score: float) -> list[str]:
    triggered = {h["name"] for h in heuristics}
    values = {h["name"]: h["value"] for h in heuristics}  # <-- adiciona isso
    msgs = []

    if (values.get("ssl_verify", 0) >= 0.7 and values.get("dns_verify", 0) >= 0.7):
        msgs.append("SSL inválido e DNS suspeito simultaneamente — múltiplos sinais de infraestrutura maliciosa.")

    if (values.get("domain_age", 0) >= 0.7 and values.get("ssl_verify", 0) >= 0.7):
        msgs.append("Domínio recente com SSL suspeito — padrão comum em infraestrutura de phishing descartável.")

    if (values.get("domain_age", 0) >= 0.7 and values.get("dns_verify", 0) >= 0.7):
        msgs.append("Domínio novo com DNS suspeito — possível infraestrutura criada exclusivamente para ataque.")

    if (values.get("domain_age", 0) >= 0.7 and values.get("ssl_verify", 0) >= 0.7 and values.get("dns_verify", 0) >= 0.7):
        msgs.append("Domínio novo, SSL inválido e DNS suspeito — combinação de alto risco, infraestrutura de ataque provável.")

    if (values.get("random_domain_risk", 0) >= 0.5 and values.get("hyphen_risk", 0) >= 0.5):
        msgs.append("Domínio com alta entropia e hífens — perfil compatível com geração automática (DGA).")

    if (values.get("random_domain_risk", 0) >= 0.5 and values.get("num_ratio_risk", 0) >= 0.5):
        msgs.append("Domínio com entropia alta e proporção elevada de números — forte indicativo de domínio gerado automaticamente.")

    if (values.get("random_domain_risk", 0) >= 0.5 and values.get("hyphen_risk", 0) >= 0.5 and values.get("num_ratio_risk", 0) >= 0.5):
        msgs.append("Entropia alta, hífens e números no domínio — perfil DGA com alta confiança.")

    if (values.get("random_domain_risk", 0) >= 0.5 and values.get("domain_age", 0) >= 0.7):
        msgs.append("Domínio com padrão aleatório recém-registrado — descartável, típico de campanhas de curta duração.")

    if (values.get("random_subdomain_risk", 0) >= 0.5 and values.get("random_domain_risk", 0) >= 0.5):
        msgs.append("Subdomínio e domínio base ambos com padrão aleatório — URL inteiramente gerada por automação.")

    if (values.get("random_path_risk", 0) >= 0.5 and values.get("random_domain_risk", 0) >= 0.5):
        msgs.append("Path e domínio com padrão aleatório — URL possivelmente gerada por automação para entrega de payload.")

    if (values.get("random_path_risk", 0) >= 0.5 and values.get("base64_segment", 0) >= 0.5):
        msgs.append("Path aleatório com segmento base64 — possível entrega de payload ofuscado.")

    if (values.get("random_path_risk", 0) >= 0.5 and values.get("path_depth_risk", 0) >= 0.5):
        msgs.append("Path profundo com segmentos aleatórios — estrutura de URL projetada para evasão de detecção.")

    if (values.get("query_contains_url", 0) >= 0.5 and values.get("mix_encoding", 0) >= 0.5):
        msgs.append("URL embutida na query com encoding misto — possível open redirect com obfuscação intencional.")

    if (values.get("query_contains_url", 0) >= 0.5 and values.get("query_no_value", 0) >= 0.5):
        msgs.append("URL na query combinada com parâmetros vazios — estrutura de open redirect com evasão.")

    if (values.get("xss_pattern", 0) >= 0.5 and values.get("query_contains_url", 0) >= 0.5):
        msgs.append("Padrão XSS detectado com URL na query — possível ataque de redirecionamento com payload injetado.")

    if (values.get("xss_pattern", 0) >= 0.5 and values.get("mix_encoding", 0) >= 0.5):
        msgs.append("Padrão XSS com encoding misto — tentativa de evasão de filtros via obfuscação.")

    if (values.get("xss_pattern", 0) >= 0.5 and values.get("fragment_risk", 0) >= 0.5):
        msgs.append("Padrão XSS no fragmento da URL — possível injeção via hash, comum em ataques DOM-based.")

    if (values.get("base64_segment", 0) >= 0.5 and values.get("mix_encoding", 0) >= 0.5):
        msgs.append("Base64 e encoding misto na mesma URL — obfuscação em múltiplas camadas, evasão intencional.")

    if (values.get("at_risk", 0) >= 0.5 and values.get("query_contains_url", 0) >= 0.5):
        msgs.append("Símbolo '@' com URL na query — técnica clássica de mascaramento de destino real.")

    if (values.get("at_risk", 0) >= 0.5 and values.get("mix_encoding", 0) >= 0.5):
        msgs.append("Símbolo '@' com encoding misto — possível tentativa de confundir parsers de URL.")

    if (values.get("subdomain_count", 0) >= 0.5 and values.get("random_subdomain_risk", 0) >= 0.5):
        msgs.append("Múltiplos subdomínios com padrão aleatório — estrutura típica de phishing hospedado em plataforma cloud.")

    if (values.get("subdomain_count", 0) >= 0.5 and values.get("domain_age", 0) >= 0.7):
        msgs.append("Múltiplos subdomínios em domínio recém-registrado — infraestrutura descartável em cloud.")

    if (values.get("random_subdomain_risk", 0) >= 0.5 and values.get("domain_age", 0) >= 0.7):
        msgs.append("Subdomínio aleatório em domínio novo — phishing em plataforma com identidade descartável.")

    if (values.get("form_action_check", 0) >= 0.5 and values.get("password_input_check", 0) >= 0.5):
        msgs.append("Formulário com ação externa e campo de senha detectados — risco elevado de coleta de credenciais.")

    if (values.get("form_action_check", 0) >= 0.5 and values.get("hidden_fields_check", 0) >= 0.5):
        msgs.append("Formulário com ação externa e campos ocultos — possível exfiltração de dados.")

    if (values.get("external_script", 0) >= 0.5 and values.get("form_action_check", 0) >= 0.5):
        msgs.append("Scripts externos combinados com formulário de destino externo — padrão de credential harvesting.")

    if (values.get("password_input_check", 0) >= 0.5 and values.get("ssl_verify", 0) >= 0.7):
        msgs.append("Campo de senha em página com SSL inválido — credenciais submetidas sem proteção.")

    if (values.get("password_input_check", 0) >= 0.5 and values.get("domain_age", 0) >= 0.7 and values.get("form_action_check", 0) >= 0.5):
        msgs.append("Domínio novo com formulário de senha e ação externa — credential harvesting em infraestrutura descartável.")

    if (values.get("hidden_fields_check", 0) >= 0.5 and values.get("ssl_verify", 0) >= 0.7):
        msgs.append("Campos ocultos em página com SSL inválido — exfiltração de dados sem proteção.")

    if (values.get("favicon_check", 0) >= 0.5 and values.get("password_input_check", 0) >= 0.5):
        msgs.append("Favicon externo com campo de senha — possível clone de site legítimo para captura de credenciais.")

    if (values.get("favicon_check", 0) >= 0.5 and values.get("image_src_check", 0) >= 0.5 and values.get("form_action_check", 0) >= 0.5):
        msgs.append("Favicon, imagens e formulário todos externos — clone completo de site legítimo provável.")

    if (values.get("image_src_check", 0) >= 0.5 and values.get("form_action_check", 0) >= 0.5):
        msgs.append("Imagens externas com formulário de destino externo — clonagem de interface de site legítimo.")

    if (values.get("external_script", 0) >= 0.5 and values.get("favicon_check", 0) >= 0.5 and values.get("domain_age", 0) >= 0.7):
        msgs.append("Scripts e favicon externos em domínio novo — clone de site legítimo em infraestrutura recente.")

    if (values.get("redirect_check", 0) >= 0.5 and values.get("random_domain_risk", 0) >= 0.5):
        msgs.append("Redirecionamento externo em domínio aleatório — evasão de detecção via cadeia de redirects.")

    if (values.get("redirect_check", 0) >= 0.5 and values.get("domain_age", 0) >= 0.7):
        msgs.append("Redirecionamento externo em domínio novo — possível uso como intermediário descartável.")

    if (values.get("redirect_check", 0) >= 0.5 and values.get("query_contains_url", 0) >= 0.5):
        msgs.append("Redirecionamento combinado com URL na query — cadeia de open redirect com destino ofuscado.")

    if score >= 70:
        msgs.append(f"Pontuação crítica ({score:.1f}) — URL apresenta múltiplos sinais convergentes de ameaça.")
    
    elif score >= 45:
        msgs.append(f"Pontuação elevada ({score:.1f}) — URL apresenta sinais relevantes que justificam investigação.")
    
    elif score >= 20:
        msgs.append(f"Pontuação moderada ({score:.1f}) — alguns sinais detectados, mas sem padrão conclusivo de ataque.")

    return msgs