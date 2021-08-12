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

## hoverLabel

### Sinais

- `mouseMove`: Sinal é emitido quando o cursor do mouse está em movimento sobre a label.
- `mouseLeave`: Sinal é emitido quando o cursor do mouse deixa a label.

### Métodos

- `hoverLabel(QWidget pai, str s)`: Constroi uma label customizada que herda de QLabel, dado o pai e o texto.
- `void mouseMoveEvent()`: Método sobrecarregado responsável por emitir o sinal `mouseMove`.
- `void leaveEvent()`: Método sobrecarregado responsábel por emitir o sinal `mouseLeave`.
- `void on()`: Método utilizado como slot para modificar a cor de fundo da label.
- `void off()`: Método utilizado como slot para modificar a cor de fundo para a cor original.

## janelaInicial

### Atributos

- `bool arquivo`: Atributo atua como uma flag para sinalizar se existe um arquivo carregado.
- `QMessageBox msg`: QMessageBox utilizada para exibir mensagens de erro.
- `QWidget centralWidget`: QWidget utilizado como widget principal da janela.
- `QVBoxLayout layout`: Layout vertical do widget principal.

### Métodos

- `janelaInicial()`: Controi uma janela que herda de QMainWindow.
- `void line()`: Método que adiciona um QLineEdit no widget principal.
- `void btns()`: Método que adiciona os botões Karnaugh e Quine no widget principal.
- `void open()`: Método responsável por carregar e processar a tabela verdade fornecida pelo usuário.
- `bool valido(_csv.reader f)`: Método auxiliar para verificar se o arquivo fornecido é válido.
- `void openKarnaugh()`: Método que atua como slot conectado ao botão Karnaugh. Quando acionado irá abrir uma nova janela com o Mapa de Karnaugh da entrada.
- `void openQuine()`: Método que atua como slot conectado ao botão Quine. Quando acionado irá abrir uma nova janela com o passo a passo do algoritmo Quine McCluskey.
- `void recebeSinal()`: Método que atua como slot conectado às novas janelas criadas. Quando acionado irá exibir a `janelaInicial`.

## janela2var

### Atributos

- `QWidget centralWidget`: QWidget utilizado como widget principal da janela.
- `QGridLayout layout`: Layout do widget principal.
- `dict hL`: Dicionário que armazena as hoverLabels adicionadas na janela.
- `Quine q`: Atributo que armazena o objeto Quine.

### Métodos 

- `janela2var(Quine quine, QWidget pai)`: Constroi uma janela que herda de QMainWindow, o objeto Quine será utilizado para construir o Mapa de Karnaugh.
- `QLabel newLabel(QWidget pai, str text)`: Método auxiliar que retorna uma nova label dado o pai e o texto.
- `void MapaW()`: Constroi um novo widget do Mapa de Karnaugh e o adiciona em `centralWidget`.
- `void respostaW()`: Constroi um novo widget para a resposta e o adiciona em `centralWidget`.
- `void backButton()`: Adiciona o botão de voltar na janela.
- `list fillMapa(list termos)`: Método auxiliar para preencher um Mapa de Karnaugh referente aos termos recebidos.
- `bool isTopLeft(list m, int i, int j)`: Método que dado um agrupamento e a posição de um termo retornará verdadeiro se for topLeft, falso caso contrário.
- `bool isTopRight(list m, int i, int j)`: Método que dado um agrupamento e a posição de um termo retornará verdadeiro se for topRight, falso caso contrário.
- `bool isBottomRight(list m, int i, int j)`: Método que dado um agrupamento e a posição de um termo retornará verdadeiro se for bottomRight, falso caso contrário.
- `bool isBottomLeft(list m, int i, int j)`: Método que dado um agrupamento e a posição de um termo retornará verdadeiro se for bottomLeft, falso caso contrário. Um exemplo pode ser visto na imagem a seguir.




