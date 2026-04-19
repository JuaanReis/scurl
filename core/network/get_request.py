from .config_net import HTTPStatusError, ConnectError, RequestError, clients
from time import sleep
from core.models.http_result import HTTPResult

def get_response(url: str, retries: int = 3, delay: float = 0.6) -> HTTPResult | None:
    """
        Realiza uma requisição HTTP GET e retorna um objeto HTTPResult.
    
        A função tenta acessar a URL informada utilizando múltiplos clientes
        HTTP, com o objetivo de distribuir as requisições e reduzir possíveis
        gargalos de conexão.
    
        Caso ocorra um erro de rede ou uma falha temporária, a função realiza
        novas tentativas de acordo com o valor definido em `retries`. Se todas
        as tentativas falharem, a função retorna `None`.
    
        O código também trata respostas HTTP 429 (rate limit), respeitando o
        cabeçalho `Retry-After` antes de realizar uma nova tentativa.
    
        Args:
            url (str): URL a ser requisitada.
            retries (int): Número máximo de tentativas de requisição.
            delay (float): Tempo base de espera entre as tentativas.
    
        Returns:
            HTTPResult: Objeto contendo detalhes da resposta HTTP, ou `None`
            em caso de falha após todas as tentativas.
    """

    rr = 0

    for attempt in range(retries):

        c = clients[rr % len(clients)]
        rr += 1

        try:
            response = c.get(url)

            return HTTPResult(
                url = str(response.url),
                status = response.status_code,
                headers = response.headers,
                body = response.text,
                elapsed = response.elapsed.total_seconds(),
                size = len(response.content),
                redirects = len(response.history)
            )

        except HTTPStatusError as e:
            response = e.response
            status = response.status_code
        
            if status == 429:
                retry_after = int(response.headers.get("Retry-After", 1))
                sleep(retry_after)
                continue
            
            return HTTPResult(
                url=str(response.url),
                status=status,
                headers=response.headers,
                body=response.text,
                elapsed=response.elapsed.total_seconds(),
                size=len(response.content),
                redirects=len(response.history),
            )

        except (ConnectError, RequestError):
            sleep(delay * (2 ** attempt))
            continue

        except Exception:
            sleep(delay * (2 ** attempt))
            continue

    return None