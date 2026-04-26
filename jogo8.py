from collections import deque


class Node:
    def __init__(self, state, parent=None, depth=0):
        self.state = state
        self.parent = parent
        self.depth = depth

    def get_path(self):
        path = []
        current = self
        while current:
            path.append(current.state)
            current = current.parent
        return path[::-1]


def generate_children(board: list[int]) -> list[list[int]]:
    children = []
    empty_pos = board.index(0)
    
    lado = 3 if len(board) == 9 else 4
    
    linha = empty_pos // lado
    coluna = empty_pos % lado
    
    movimentos_validos = []
    
    if linha > 0:          movimentos_validos.append(empty_pos - lado) # Cima
    if linha < lado - 1:   movimentos_validos.append(empty_pos + lado) # Baixo
    if coluna > 0:         movimentos_validos.append(empty_pos - 1)    # Esquerda
    if coluna < lado - 1:  movimentos_validos.append(empty_pos + 1)    # Direita
        
    for target_pos in movimentos_validos:
        child = board.copy()
        child[empty_pos], child[target_pos] = child[target_pos], child[empty_pos]
        children.append(child)
            
    return children


def breadth_first_search(initial_state: list[int], goal_state: list[int]) -> tuple[Node | None, int, int, int]:
    start_node = Node(initial_state, depth=0)
    frontier = deque([start_node])
    explored = set()
    
    # métricas
    nodes_visited = 0
    max_frontier_size = 1
    max_depth = 0
    
    while frontier:
        
        # atualiza a métrica de memória máxima utilizada
        if len(frontier) > max_frontier_size:
            max_frontier_size = len(frontier)
        
        # atualiza a métrica de tempo de execução
        current_node = frontier.popleft()
        nodes_visited += 1
        
        if current_node.state == goal_state:
            return current_node, nodes_visited, max_frontier_size, max_depth
        
        explored.add(tuple(current_node.state))
        
        children_states = generate_children(current_node.state)
        
        for child_state in children_states:
            # se o estado filho não foi explorado ainda e não tem nenhum estado igual na fronteira, crie um novo nó na fronteira com o estado filho.
            if tuple(child_state) not in explored and not any(n.state == child_state for n in frontier):
                new_node = Node(child_state, parent=current_node, depth=current_node.depth + 1)
            
                # atualiza a métrica de profundidade máxima
                if new_node.depth > max_depth:
                    max_depth = new_node.depth
                
                frontier.append(new_node)
            
    return None, nodes_visited, max_frontier_size, max_depth


def depth_first_search(initial_state: list[int], goal_state: list[int]) -> tuple[Node | None, int, int, int]:
    start_node = Node(initial_state, depth=0)
    frontier = [start_node]
    explored = set()
    
    # métricas
    nodes_visited = 0
    max_frontier_size = 1
    max_depth = 0
    
    while frontier:
        
        # atualiza a métrica de memória máxima utilizada
        if len(frontier) > max_frontier_size:
            max_frontier_size = len(frontier)
        
        # atualiza a métrica de tempo de execução
        current_node = frontier.pop()
        nodes_visited += 1
        
        if current_node.state == goal_state:
            return current_node, nodes_visited, max_frontier_size, max_depth
        
        # limite de profundidade se não bagunça
        """
        if current_node.depth >= 32:
            continue
        """
        
        explored.add(tuple(current_node.state))
        
        children_states = generate_children(current_node.state)
        
        for child_state in children_states:
            # se o estado filho não foi explorado ainda e não tem nenhum estado igual na fronteira, crie um novo nó na fronteira com o estado filho.
            if tuple(child_state) not in explored and not any(n.state == child_state for n in frontier):
                new_node = Node(child_state, parent=current_node, depth=current_node.depth + 1)
            
                # atualiza a métrica de profundidade máxima
                if new_node.depth > max_depth:
                        max_depth = new_node.depth
                
                frontier.append(new_node)
            
    return None, nodes_visited, max_frontier_size, max_depth


def calculate_manhattan(state: list[int], goal_state: list[int]) -> int:
    distance = 0
    
    for number in range(1, len(state)):
        # acha a coordenada atual da peça (linha e coluna)
        current_index = state.index(number)
        current_row = current_index // 3
        current_col = current_index % 3
        
        # acha a coordenada de onde a peça deveria estar
        goal_index = goal_state.index(number)
        goal_row = goal_index // 3
        goal_col = goal_index % 3
        
        # calculo da distancia sem diagonais: |X2 - X1| + |Y2 - Y1|
        passos_da_peca = abs(goal_row - current_row) + abs(goal_col - current_col)
        
        distance += passos_da_peca
        
    return distance


def greedy_search(initial_state: list[int], goal_state: list[int]) -> tuple[Node | None, int, int, int]:
    start_node = Node(initial_state, depth=0)
    frontier = [start_node]
    explored = set()
    
    # métricas
    nodes_visited = 0
    max_frontier_size = 1
    max_depth = 0
    
    while frontier:
        
        # atualiza a métrica de memória máxima utilizada
        if len(frontier) > max_frontier_size:
            max_frontier_size = len(frontier)
        
        # ordena a fronteira de acordo com os valores heurísticos H e popa o menorzin.
        frontier.sort(key=lambda node: calculate_manhattan(node.state, goal_state))
        current_node = frontier.pop(0)
        
        # atualiza a métrica de tempo de execução
        nodes_visited += 1
        
        if current_node.state == goal_state:
            return current_node, nodes_visited, max_frontier_size, max_depth
        
        explored.add(tuple(current_node.state))
        
        children_states = generate_children(current_node.state)
        
        for child_state in children_states:
            # se o estado filho não foi explorado ainda e não tem nenhum estado igual na fronteira, crie um novo nó na fronteira com o estado filho.
            if tuple(child_state) not in explored and not any(n.state == child_state for n in frontier):
                new_node = Node(child_state, parent=current_node, depth=current_node.depth + 1)
            
                # atualiza a métrica de profundidade máxima
                if new_node.depth > max_depth:
                        max_depth = new_node.depth
                
                frontier.append(new_node)
            
    return None, nodes_visited, max_frontier_size, max_depth


def a_star_search(initial_state: list[int], goal_state: list[int]) -> tuple[Node | None, int, int, int]:
    start_node = Node(initial_state, depth=0)
    frontier = [start_node]
    explored = set()
    
    # métricas
    nodes_visited = 0
    max_frontier_size = 1
    max_depth = 0
    
    while frontier:
        
        # atualiza a métrica de memória máxima utilizada
        if len(frontier) > max_frontier_size:
            max_frontier_size = len(frontier)
        
        # ordena a fronteira de acordo a profundidade do nó + valor heurístico H do e popa o menorzin.
        frontier.sort(key=lambda node: node.depth + calculate_manhattan(node.state, goal_state))
        current_node = frontier.pop(0)
        
        # atualiza a métrica de tempo de execução
        nodes_visited += 1
        
        if current_node.state == goal_state:
            return current_node, nodes_visited, max_frontier_size, max_depth
        
        explored.add(tuple(current_node.state))
        
        children_states = generate_children(current_node.state)
        
        for child_state in children_states:
            # se o estado filho não foi explorado ainda e não tem nenhum estado igual na fronteira, crie um novo nó na fronteira com o estado filho.
            if tuple(child_state) not in explored and not any(n.state == child_state for n in frontier):
                new_node = Node(child_state, parent=current_node, depth=current_node.depth + 1)
            
                # atualiza a métrica de profundidade máxima
                if new_node.depth > max_depth:
                        max_depth = new_node.depth
                
                frontier.append(new_node)
            
    return None, nodes_visited, max_frontier_size, max_depth