def sigmoid(x: int):
    """
        A função sigmoid é uma função matemática que mapeia qualquer valor real para um intervalo entre 0 e 1. Ela é amplamente utilizada em machine learning, especialmente em modelos de classificação binária, para transformar a saída de um modelo linear em uma probabilidade. A fórmula da função sigmoid é dada por:
    
        Formula:
            sigmoid(x) = 1 / (1 + exp(-x))
            Onde exp(-x) é a função exponencial aplicada a -x.
        
        Atributos:
            - x (int): O valor de entrada para a função sigmoid, que pode ser qualquer número real.
    
        Retorna:
            float: O valor resultante da função sigmoid, que estará no intervalo entre 0 e 1.
    
        Exemplo de uso:
        ```
            print(sigmoid(0))   # Saída: 0.5
            print(sigmoid(1))   # Saída: 0.7310585786300049
            print(sigmoid(-1))  # Saída: 0.2689414213690024
        ```
    """
    from math import exp
    return 1 / (1 + exp(-x))