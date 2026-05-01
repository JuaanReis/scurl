"""
Módulo de Heurísticas para Análise de URLs Maliciosas

Este módulo implementa um conjunto abrangente de heurísticas para detectar URLs potencialmente maliciosas
através de análise estatística, estrutural e comportamental. O sistema utiliza múltiplas abordagens
para identificar indicadores de comprometimento, phishing, malware e outras ameaças web.

Funcionalidades Principais:
========================

1. Análise de Caracteres Especiais:
   - Detecção de caracteres suspeitos (@, =, hífens excessivos)
   - Análise de codificações mistas (percent-encoding, punycode, Unicode)
   - Detecção de indicadores XSS em URLs

2. Análise de Domínios:
   - Detecção de endereços IP em URLs
   - Análise de entropia para domínios/subdomínios aleatórios
   - Contagem e avaliação de subdomínios suspeitos

3. Análise de Componentes da URL:
   - Avaliação de caminhos (paths) com alta entropia
   - Detecção de parâmetros de query suspeitos
   - Análise de comprimento e profundidade de caminhos
   - Verificação de fragmentos com entropia elevada

4. Detecção de Técnicas de Ofuscação:
   - Identificação de URLs encurtadas
   - Detecção de domínios typosquatting
   - Análise de segmentos codificados em Base64

Estrutura do Módulo:
===================

- url_analyzer/: Análise principal de componentes da URL
  - checks/: Funções de verificação específicas
    - character_check.py: Análise de caracteres especiais
    - domain_check.py: Análise de domínios e subdomínios
    - parts_check.py: Análise de caminhos, queries e fragmentos
  - rules/: Regras de avaliação para diferentes componentes
  - suspects_keywords.py: Lista de palavras-chave suspeitas
  - base64_detect/: Detecção e análise de conteúdo Base64

- server_info/: Análise de informações do servidor
  - server_info.py: Verificação de headers e certificados

Integração com o Sistema:
========================

O módulo heuristics é integrado ao scanner principal através do ResultBase, que padroniza
os resultados de todas as verificações. Cada heurística retorna um objeto com:
- value: Valor bruto da métrica analisada
- normalized: Valor normalizado (0-1) para comparação
- details: Informações adicionais sobre a análise

Os resultados são agregados e ponderados para calcular um score de risco geral da URL.

Exemplo de Uso:
==============

    from core.heuristics.url_analyzer.checks import character_check, domain_check

    url_structure = {
        "url": "http://suspicious-domain.com/path?param=http://evil.com",
        "registered_domain": "suspicious-domain.com",
        "path": "/path",
        "query": "param=http://evil.com"
    }

    # Análise de caracteres
    char_result = character_check.at_risk(url_structure)

    # Análise de domínio
    domain_result = domain_check.ip_in_url(url_structure)

    # Agregação de resultados para score final
    total_risk = (char_result.normalized + domain_result.normalized) / 2

Considerações de Segurança:
==========================

- As heurísticas são baseadas em análise estatística e padrões observados
- Falsos positivos podem ocorrer em URLs legítimas complexas
- Recomenda-se combinação com outras técnicas de detecção (ML, listas negras, etc.)
- Os thresholds são ajustáveis baseado no contexto de uso

Desenvolvimento:
==============

Para adicionar novas heurísticas:
1. Criar função seguindo o padrão ResultBase
2. Adicionar docstring detalhada com exemplo
3. Integrar nos módulos de regras apropriados
4. Atualizar testes unitários
"""

from core.heuristics.server_analyzer.rules import server_rules
from core.heuristics.url_analyzer.rules import character_rules
from core.heuristics.url_analyzer.rules import domain_rules
from core.heuristics.url_analyzer.rules import parts_rules
from core.heuristics.response_analyzer.rules import response_rules