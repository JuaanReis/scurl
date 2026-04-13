"""
    Módulo responsável pelas operações de rede da aplicação.
    
    Este módulo centraliza a configuração dos clients HTTP e fornece
    funções utilitárias para execução de requisições a servidores externos.
    As implementações utilizam a biblioteca httpx e são projetadas para
    reutilizar conexões, controlar erros de rede e padronizar o acesso
    HTTP dentro da aplicação.
    
    Funcionalidades
    ---------------
    Configuração de clients HTTP
        Define e inicializa múltiplas instâncias de clients configuradas
        com suporte a HTTP/2, limites de conexões simultâneas, controle
        de timeout e cabeçalhos padrão. Essas instâncias são reutilizadas
        pelas funções de requisição para reduzir o custo de abertura de
        novas conexões.
    
    Execução de requisições GET
        Implementa uma função responsável por realizar requisições HTTP
        do tipo GET utilizando os clients configurados. A função inclui:
    
        - distribuição das requisições entre múltiplos clients
        - tratamento de exceções relacionadas a rede
        - mecanismo de tentativas (retries)
        - controle de atraso entre tentativas consecutivas
        - tratamento específico para respostas HTTP 429 (rate limiting),
          respeitando o cabeçalho Retry-After antes de uma nova tentativa
    
    As funções do módulo retornam objetos de resposta HTTP quando a
    requisição é bem-sucedida ou `None` caso todas as tentativas de
    requisição falhem.
"""