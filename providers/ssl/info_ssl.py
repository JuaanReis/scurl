import ssl
import socket
from parsers.parse_issue_ssl import parse_issuer

def get_ssl_cert(structure: dict) -> dict:
    """
        Realiza a verificação do certificado SSL de um servidor, estabelecendo uma conexão segura e extraindo informações relevantes sobre o certificado, como o emissor, as datas de validade e os nomes alternativos do assunto (SAN). A função utiliza a biblioteca ssl para criar um contexto de segurança e socket para estabelecer a conexão com o servidor na porta 443. Caso a conexão ou a obtenção do certificado falhem, a função retorna um dicionário com valores padrão indicando a ausência de informações do certificado.
        
        Atributos:
            - structure (dict): Dicionário contendo as informações estruturais da URL, incluindo o campo "hostname" que representa o domínio do servidor a ser verificado.
        
        Retorna:
            dict: Dicionário contendo as informações extraídas do certificado SSL, incluindo:
                - "issuer": Dicionário com as informações do emissor do certificado (extraídas do campo "issuer").
                - "notBefore": Data de início da validade do certificado.
                - "notAfter": Data de término da validade do certificado.
                - "san": Lista de nomes alternativos do assunto (SAN) presentes no certificado.

        Exemplo de uso:
        ```
        structure = {
            "hostname": "www.example.com"
        }   
        cert_info = get_ssl_cert(structure)
        print(cert_info)
        # Saída:
        # {
        #     "issuer": {
        #         "CN": "Let's Encrypt Authority X3",
        #         "O": "Let's Encrypt",
        #         "C": "US"
        #     },
        #     "notBefore": "Jan 1 00:00:00 2020 GMT",
        #     "notAfter": "Dec 31 23:59:59 202
        #     "san": ["www.example.com", "example.com"]
        # }
        ```
    """

    host = structure.get('hostname', "")
    if not host:
        return {}
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_OPTIONAL

    try:
        with socket.create_connection((host, 443), timeout=3) as sock:
            with ctx.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()

    except ConnectionRefusedError:
        return {
            "connection_error": True
        }

    except socket.timeout:
        return {
            "timeout": True
        }

    except ssl.SSLCertVerificationError:
        return {
            "invalid_cert": True
        }
    
    except socket.gaierror:
        return {
            "dns_error": True
        }

    except Exception:
        return {
            "unknown": True
        }

    subject = parse_issuer(cert.get('subject', []))

    return {
        "issuer": parse_issuer(cert.get('issuer', [])),
        "subject": subject,
        "notBefore": cert.get('notBefore', ""),
        "notAfter": cert.get('notAfter', ""),
        "san": [entry[1] for entry in cert.get('subjectAltName', []) if entry[0] == 'DNS'],
        "self_signed": cert.get('issuer', []) == cert.get('subject', []),
        "organization": subject.get('O', "")
    }
