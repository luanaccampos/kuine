# Kuine
Software educacional para ensino de minimização de expressões lógicas. A aplicação foi feita utilizando Python e PyQt5.

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

- `Quine(list termos, int n, bool minimal = True)`: Constroi um objeto Quine com os termos e número de variáveis recebidos. Por padrão a resposta será minimal, se setado como falso a resposta será uma aproximação.
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

- `list resposta`: Lista que armazena a resposta.

### Métodos

- `setCoverGreedy(list U, list S)`: Constroi um objeto que resolve o problema de cobertura de conjuntos de forma gulosa. Recebe o universo U
de termos e uma lista de sets que poderão ser utilizados na solução.
- `list getResposta()`: Retorna a resposta.

## setCoverPD

### Atributos

- `list S`: Lista dos sets.
- `dict pd`: Dicionário utiizado para armazenar as computações feitas pelo o algoritmo.
- `int n`: Inteiro que armazena a quantidade de sets.
- `list resposta`: Lista que armazena a resposta.

### Métodos

- `setCoverPD(list U, list S)`: Constroi um objeto que resolve o problema de cobertura de conjuntos utilizando programação dinâmica. Recebe o universo U
de termos e uma lista de sets que poderão ser utilizados na solução. 
- `int cover(int i, set s, int n)`: Método recursivo que encontra a solução com menor custo para o problema.
- `list getResposta()`: Retorna a resposta.
