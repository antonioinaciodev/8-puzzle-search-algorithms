# 🧩 8-Puzzle Search Algorithms

## 📌 Sobre o Projeto
Este repositório contém a modelagem e a resolução do clássico problema do **8-Puzzle** (Jogo do Quinze em um tabuleiro 3x3) utilizando fundamentos de **Inteligência Artificial** e busca em espaço de estados.

O objetivo principal deste projeto é **estudar os métodos de árvore de busca** e a modelagem de estados, utilizando o 8-Puzzle como cenário de experimentação, ao invés de focar apenas em solucionar o jogo. Através dele, é possível analisar e comparar a performance e o comportamento da fronteira de exploração de diferentes algoritmos (cegos e informados).

## 🧠 Algoritmos Implementados
O motor de resolução foi arquitetado para suportar múltiplas estratégias de busca. As seguintes abordagens foram implementadas:

**Busca Cega (Uninformed Search):**
*   **Busca em Largura (BFS - Breadth-First Search):** Explora nível por nível. Garante a solução ótima (mínimo de movimentos), mas consome muita memória.
*   **Busca em Profundidade (DFS - Depth-First Search):** Explora até o limite de um ramo antes de retroceder. Usa menos memória, mas não garante a solução ótima e pode entrar em loops infinitos sem controle de estados visitados.

**Busca Informada/Heurística (Informed Search):**
*   **Busca Gulosa (Greedy Best-First Search):** Escolhe o próximo movimento baseando-se apenas na heurística (o quão perto parece estar do objetivo). Rápida, mas não garante a solução ótima.
*   **A* (A-Star):** A joia da coroa. Combina o custo do caminho já percorrido ($g(n)$) com a heurística do custo restante ($h(n)$). Garante a solução ótima com grande eficiência temporal.

**Função Heurística Utilizada:**
*   **Distância de Manhattan (Manhattan Distance):** Soma da distância absoluta (horizontal + vertical) de cada peça até sua posição correta.

## 🗂️ Estrutura do Repositório
A arquitetura do código é direta e baseada em scripts Python na raiz do projeto:

*   **`search_algorithms.py`**: Concentra toda a lógica central do problema. Contém a classe `Node`, as regras de transição de estados (`generate_children`), o cálculo da heurística (Distância de Manhattan) e as implementações nativas dos algoritmos (BFS, DFS, Gulosa e A*).
*   **`interface.py`**: Arquivo principal de execução. Implementa a interface gráfica interativa utilizando `tkinter`, gerencia a execução dos algoritmos em segundo plano (*threads*) e exibe a tabela comparativa e o player passo a passo da solução.
*   **`docs/`**: Diretório que armazena os relatórios teóricos e análises de desempenho do projeto.

## 🚀 Como Executar
O projeto foi desenvolvido em **Python** e utiliza exclusivamente bibliotecas nativas da linguagem (como `tkinter` e `heapq`), não sendo necessária a instalação de dependências externas via `pip`.

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/SEU-USUARIO/8-puzzle-search-algorithms.git](https://github.com/SEU-USUARIO/8-puzzle-search-algorithms.git)
   cd 8-puzzle-search-algorithms
   ```

2. **Execute a aplicação gráfica:**
   ```bash
   python interface.py
   ```

## 🛠️ Tecnologias e Padrões
*   **Linguagem:** Python
*   **Interface Gráfica:** Tkinter (biblioteca nativa) para visualização interativa e animação passo a passo da solução.
*   **Estruturas de Dados Chave:** 
    *   **Deques (`collections.deque`):** Utilizados para operações otimizadas (O(1)) de enfileiramento e desenfileiramento na Busca em Largura (BFS).
    *   **Filas de Prioridade (`heapq`):** Essenciais para guiar a fronteira de exploração baseada no menor custo computado pelo algoritmo A* e pela Busca Gulosa.
    *   **Conjuntos (`set`):** Implementados como tabelas Hash para rastreio rigoroso de estados já visitados e na fronteira, garantindo tempo de busca O(1) para prevenir ciclos infinitos na árvore.
*   **Concorrência:** Uso do módulo `threading` para rodar o motor pesado de busca da IA em segundo plano, evitando o travamento da interface gráfica.
