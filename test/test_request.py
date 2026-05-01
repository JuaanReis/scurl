from core.network.get_request import get_response
from core.heuristics.response_analyzer.response_normalizator import normalize

def _run_test():
    """
        Script de teste para validação de requisição HTTP e normalização de conteúdo.

        Este script realiza uma requisição HTTP para uma URL definida, obtém o
        conteúdo da resposta e aplica uma função de normalização no texto retornado.

        O objetivo é verificar o funcionamento conjunto dos seguintes componentes:

        - get_response:
            Responsável por realizar a requisição HTTP e retornar o objeto de resposta.

        - normalize:
            Função responsável por processar e padronizar o conteúdo da resposta,
            removendo ruído ou transformando o texto para facilitar análises posteriores.

        Fluxo de execução:
            1. Define uma URL alvo.
            2. Realiza uma requisição HTTP utilizando get_response.
            3. Extrai o conteúdo textual da resposta.
            4. Exibe os primeiros 700 caracteres da resposta bruta.
            5. Aplica a função de normalização ao conteúdo.
            6. Exibe o resultado normalizado.

        Esse tipo de teste é útil para validar o pipeline de:
            requisição -> captura de resposta -> processamento de conteúdo.

        Dependências:
            core.network.get_request.get_response
            core.scanner.normalizator.normalize
    """

    try:
        url = input("[?] Digite uma URL: ")
    except (EOFError, KeyboardInterrupt):
        print("\n[!] Entrada de URL não fornecida. Encerrando o programa.")
        return
    
    response = get_response(url)
    print("[+] Tamanho do texto:   ", len(response.body) if response else "")
    print("[+] Status Code:   ", response.status if response else "")
    print("[+] Headers:   ", [f"{key}: {value}" for key, value in response.headers.items()] if response else "")
    print("[+] Len headers:   ", len(response.headers) if response else "", "\n")
    print("[+] Texto normalizado:   ", normalize(response.body) if response else "", "\n")
    print(f"[+] Requisição concluída em {response.elapsed:.4}s\n")


if __name__ == "__main__":
    _run_test()