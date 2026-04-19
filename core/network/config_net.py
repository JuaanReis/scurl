"""
    Configura clientes HTTP utilizados pela aplicação.

    O módulo define e inicializa múltiplas instâncias de `httpx.Client`,
    que são reutilizadas durante a execução do programa para melhorar
    o desempenho das requisições HTTP.

    A reutilização dos clientes permite o aproveitamento de conexões
    persistentes (keep-alive), reduzindo o custo de criação de novas
    conexões e tornando as requisições mais eficientes em cenários
    com alto volume de chamadas.

    As configurações aplicadas incluem suporte a HTTP/2, limites de
    conexões simultâneas, controle de timeout e compressão de respostas
    por meio do cabeçalho `Accept-Encoding`.

    Attributes:
        - clients_number (int): Número de clientes HTTP que serão criados
        e utilizados para distribuir as requisições.

        - client_kwargs (dict): Conjunto de parâmetros utilizados na
        configuração das instâncias de `httpx.Client`.

        - clients (list[httpx.Client]): Lista contendo os clientes HTTP
        inicializados com as configurações definidas neste módulo.
"""

from httpx import Client, Timeout, Limits, HTTPStatusError, ConnectError, RequestError

clients_number = 1      # Número de clientes simutaneos.
client_kwargs = {
    "http2": False,
    "verify": False,
    "follow_redirects": True,
    "timeout": Timeout(
        timeout=6.0,   
        connect=1.5,    
        read=3.0        
    ),
    "limits": Limits(
        max_keepalive_connections=10,
        max_connections=20
    ),
    "headers": {
        "Accept-Encoding": "gzip, br",
        "User-Agent": "URL-Security-Analyzer/0.0.1 (Academic Research)"
    }
}

clients = [
    Client(**client_kwargs)
    for _ in range(clients_number)
]