from dataclasses import dataclass

@dataclass
class ResultBase:
    """
        Classe base para representar o resultado de uma análise ou escaneamento. Contém informações sobre o valor do resultado, sua normalização, peso e detalhes adicionais.
        Atributos:
        - value (float): O valor do resultado da análise.
        - normalized (float | None): O valor normalizado do resultado, geralmente entre 0 e 1. Padrão é 0.0.
        - weight (float): O peso atribuído a este resultado, usado para calcular a pontuação final. Padrão é 1.0.
        - details (dict | None): Um dicionário opcional para armazenar detalhes adicionais sobre o resultado, como informações de contexto ou explicações. Padrão é None.
    
        Exemplo de uso:
        ```
            >>> result = ResultBase(value=75)
            >>> result.normalized = minmax(result.value, 0, 100)
            >>> result.weight = 0.5
            >>> result.details = {"source": "scan1", "description": "Valor de exemplo"}
            >>> print(result)
            ResultBase(value=75, normalized=0.75, weight=0.5, details={'source': 'scan1', 'description': 'Valor de exemplo'})
        ```
    """
    
    value: float
    normalized: float = 0.0 or None
    weight: float = 1.0
    details: dict | None = None