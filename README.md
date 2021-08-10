# kuine
Software educacional para ensino de minimização de expressões lógicas.


# Documentação


## Quine

### Atributos

- `list quadros`: Lista que armazena quadros de cada iteração do algoritmo.
- `list implicantes`: Lista que armazena os implicantes primos.
- `dict quadro`: Dicionário auxiliar para armazenar um quadro.
- `set termos`: Set que armazena os termos.
- `int n`: Inteiro que armazena a quantidade de variáveis.
- `list var`: Lista que armazena o nome de cada variável.
- `dict grafo`: Dicionário que descreve um grafo das ligações entre os termos.
- `list resposta`: Lista que armazena a resposta.

### Métodos

- `Quine(list termos, int n, bool minimal)`: Constroi um objeto Quine com os termos e número de variáveis recebidos.
- `int bitsLigados(str s)`: Recebe uma string de um número representado na forma binária. Retorna a quantidade de bits ligados.
- `tuple match(str s1, str s1)`: Método que recebe dois termos. Caso seja possível a minimização dos dois termos, o método retornará verdadeiro e a nova combinação dos termos. Falso, caso contrário.
- `str toLiteral(str s)`: Recebe termo em forma binária e o transforma em forma literal.
- `list getResposta()`: Retorna a resposta.
- `list getQuadros()`: Retorna os quadros.
- `list getImplicantes()`: Retorna os implicantes primos.
- `set getTermos()`: Retorna os termos.
- `dict getGrafo()`: Retorna o grafo.

## setCoverGreedy

### Atributos







