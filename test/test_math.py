from core.math import jaccard_similarity, sequence_matcher, shannon_entropy
from time import time

def _run_tests():
    """
        Executa uma bateria de testes simples para validar funções matemáticas
        utilizadas no sistema de análise de strings.

        A função testa três algoritmos principais:

        1. Jaccard Similarity
           Mede a similaridade entre dois textos comparando o conjunto de
           palavras compartilhadas entre eles.

        2. Sequence Matcher
           Mede a similaridade de sequência entre duas strings, útil para
           detectar pequenas variações como erros de digitação ou mudanças
           mínimas em palavras.

        3. Shannon Entropy
           Calcula o nível de aleatoriedade de uma string, sendo útil para
           detectar padrões suspeitos como tokens, hashes ou strings
           geradas aleatoriamente.

        Para cada algoritmo, um conjunto de casos de teste é executado e os
        resultados são exibidos no terminal.

        Além disso, o tempo total de execução do teste é medido para fins
        de benchmarking simples.

        Returns:
            None

        Example:
            >>> run_tests()

            ___ TESTE JACCARD ___                                                         
            A: carros são legais                                                                        
            B: carros são chatos                                                                                
            Jaccard: 0.333

            ___ TESTE SEQUENCE MATCHER ___                                                                        
            A: login                                                    
            B: logon                                            
            Sequence similarity: 0.800

            ___ TESTE SHANNON ENTROPY ___                                                                          
            Text: aaaaaa                                
            Entropy: 0.000                                          

            Teste concluido em 0.02s
    """
    
    start = time()
    print("\n___ TESTE JACCARD ___")

    tests_jaccard = [
        ("carros são legais", "carros são chatos"),
        ("python é legal", "python é legal"),
        ("gato cachorro", "banana laranja"),
        ("segurança da informação", "segurança ofensiva"),
    ]

    for a, b in tests_jaccard:
        score = jaccard_similarity.similarity_jaccard(a, b)
        print(f"\nA: {a}")
        print(f"B: {b}")
        print(f"Jaccard: {score:.3f}")

    print("\n___ TESTE SEQUENCE MATCHER ___")

    tests_sequence = [
        ("ola", "carro"),
        ("login", "logon"),
        ("admin", "administrator"),
        ("segurança", "seguranca"),
    ]

    for a, b in tests_sequence:
        score = sequence_matcher.string_similarity(a, b)
        print(f"\nA: {a}")
        print(f"B: {b}")
        print(f"Sequence similarity: {score:.3f}")

    print("\n___ TESTE SHANNON ENTROPY ___")

    tests_entropy = [
        "aaaaaa",
        "abcabcabc",
        "carro",
        "x9F$2kP1z",
        "123456789",
        "swbhjedkswnj"
    ]

    for text in tests_entropy:
        score = shannon_entropy.shannon_entropy(text)
        print(f"\nText: {text}")
        print(f"Entropy: {score:.3f}")

    print(f"\nTeste concluido em {time() - start:.2f}s")

if __name__ == "__main__":
    _run_tests()