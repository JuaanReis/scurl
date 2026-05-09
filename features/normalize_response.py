import re
from html import unescape

def normalize(html: str) -> str:
    """
        Normaliza conteúdo HTML convertendo-o em texto limpo para análise.
    
        A função remove elementos que podem introduzir ruído na análise de
        conteúdo, como tags HTML, scripts, estilos, comentários e valores
        dinâmicos frequentemente presentes em páginas web (tokens, hashes,
        sessões, timestamps e URLs).
    
        O objetivo é gerar uma representação textual mais estável e
        comparável do conteúdo da página, útil para métricas de similaridade,
        análise de texto ou detecção de padrões.
    
        Args:
            html (str): Conteúdo HTML bruto que será normalizado.
    
        Returns:
            str: Texto normalizado contendo apenas caracteres alfanuméricos
            e espaços, pronto para análise ou comparação.
    """

    if not html:
        return ""
    
    html = unescape(html).lower()
    html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
    html = re.sub(r'<script.*?>.*?</script>', '', html, flags=re.DOTALL)
    html = re.sub(r'<style.*?>.*?</style>', '', html, flags=re.DOTALL)
    html = re.sub(r'<[^>]+>', ' ', html)
    html = re.sub(r'\b\d{6,}\b', '', html)
    
    html = re.sub(
        r'\b[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\b',
        '',
        html,
        flags=re.IGNORECASE
    )
    
    html = re.sub(r'\b[a-f0-9]{32,64}\b', '', html, flags=re.IGNORECASE)
    html = re.sub(r'\b\d{4}-\d{2}-\d{2}t\d{2}:\d{2}:\d{2}.*?\b', '', html)
    
    html = re.sub(
        r'\b(csrf|token|auth|session|nonce|sid|phpsessid)[^a-z0-9]*[a-z0-9\-_]+\b',
        '',
        html,
        flags=re.IGNORECASE
    )
    
    html = re.sub(r'https?://\S+', '', html)
    html = re.sub(r"[^a-z0-9\s_]", "", html)
    html = re.sub(r'\s+', ' ', html)

    return html.strip()