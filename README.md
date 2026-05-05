# 🧩 8-Puzzle Search Algorithms

## 📌 Sobre o Projeto
Este repositório contém a modelagem e a resolução do clássico problema do **8-Puzzle** (Jogo do Quinze em um tabuleiro 3x3) utilizando fundamentos de **Inteligência Artificial** e busca em espaço de estados.

O objetivo principal deste projeto é implementar, analisar e comparar a performance e o comportamento de diferentes algoritmos de busca (cega e informada) para encontrar a sequência ideal de movimentos que leva o tabuleiro do seu estado inicial (desordenado) ao estado objetivo (ordenado).

## 🧠 Algoritmos Implementados
O motor de resolução foi arquitetado para suportar múltiplas estratégias de busca. As seguintes abordagens foram implementadas:

**Busca Cega (Uninformed Search):**
*   **Busca em Largura (BFS - Breadth-First Search):** Explora nível por nível. Garante a solução ótima (mínimo de movimentos), mas consome muita memória.
*   **Busca em Profundidade (DFS - Depth-First Search):** Explora até o limite de um ramo antes de retroceder. Usa menos memória, mas não garante a solução ótima e pode entrar em loops infinitos sem controle de estados visitados.

**Busca Informada/Heurística (Informed Search):**
*   **Busca Gulosa (Greedy Best-First Search):** Escolhe o próximo movimento baseando-se apenas na heurística (o quão perto parece estar do objetivo). Rápida, mas não garante a solução ótima.
*   **A* (A-Star):** A joia da coroa. Combina o custo do caminho já percorrido ($g(n)$) com a heurística do custo restante ($h(n)$). Garante a solução ótima com grande eficiência temporal.

**Funções Heurísticas Utilizadas:**
1.  **Peças Fora do Lugar (Misplaced Tiles):** Conta quantas peças não estão em suas posições finais.
2.  **Distância de Manhattan (Manhattan Distance):** Soma da distância absoluta (horizontal + vertical) de cada peça até sua posição correta. *(Heurística mais forte adotada).*

## 🗂️ Estrutura do Repositório
A arquitetura do código separa claramente o modelo de domínio da lógica de busca:

*   **`src/model/`**: Contém a representação do tabuleiro (`State`, `Board`), a definição do estado objetivo e as regras de transição (movimentos válidos: Cima, Baixo, Esquerda, Direita).
*   **`src/algorithms/`**: Implementação das estratégias de busca isoladas (BFS, DFS, A*, etc).
*   **`src/heuristics/`**: Classes responsáveis por calcular os custos heurísticos.
*   **`src/Main`**: Motor de execução e central de testes.

## 🛠️ Tecnologias e Padrões
*   **Linguagem:** Java / Python *(Ajuste conforme a linguagem que você usou)*
*   **Estruturas de Dados Chave:** Filas (Queues), Filas de Prioridade (Priority Queues/Heaps) para o A*, e Conjuntos (Sets/HashSets) para rastreio de estados já visitados e prevenção de ciclos.
