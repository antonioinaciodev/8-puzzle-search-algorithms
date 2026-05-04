import heapq
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


def _report_progress(progress_cb, visited, max_frontier_size, max_depth):
    if progress_cb is not None:
        progress_cb(visited, max_frontier_size, max_depth)


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


def calculate_manhattan(state: list[int], goal_state: list[int]) -> int:
    distance = 0
    lado = 3 if len(state) == 9 else 4
    
    for number in range(1, len(state)):
        current_index = state.index(number)
        current_row = current_index // lado
        current_col = current_index % lado
        
        goal_index = goal_state.index(number)
        goal_row = goal_index // lado
        goal_col = goal_index % lado
        
        passos_da_peca = abs(goal_row - current_row) + abs(goal_col - current_col)
        
        distance += passos_da_peca
        
    return distance


def breadth_first_search(initial_state: list[int], goal_state: list[int], progress_cb=None, cancel_event=None) -> tuple[Node | None, int, int, int]:
    start_node = Node(initial_state, depth=0)
    frontier = deque([start_node])
    explored = set()
    frontier_states = {tuple(initial_state)}
    
    # métricas
    nodes_visited = 0
    max_frontier_size = 1
    max_depth = 0
    
    while frontier:
        if cancel_event is not None and cancel_event.is_set():
            return None, nodes_visited, max_frontier_size, max_depth
        
        if len(frontier) > max_frontier_size:
            max_frontier_size = len(frontier)
        
        current_node = frontier.popleft()
        frontier_states.discard(tuple(current_node.state))
        nodes_visited += 1

        if nodes_visited % 500 == 0:
            _report_progress(progress_cb, nodes_visited, max_frontier_size, max_depth)
        
        if current_node.state == goal_state:
            return current_node, nodes_visited, max_frontier_size, max_depth
        
        explored.add(tuple(current_node.state))
        
        children_states = generate_children(current_node.state)
        
        for child_state in children_states:
            if tuple(child_state) not in explored and tuple(child_state) not in frontier_states:
                new_node = Node(child_state, parent=current_node, depth=current_node.depth + 1)
            
                if new_node.depth > max_depth:
                    max_depth = new_node.depth
                
                frontier.append(new_node)
                frontier_states.add(tuple(child_state))
            
    return None, nodes_visited, max_frontier_size, max_depth


def depth_first_search(initial_state: list[int], goal_state: list[int], progress_cb=None, cancel_event=None) -> tuple[Node | None, int, int, int]:
    start_node = Node(initial_state, depth=0)
    frontier = [start_node]
    explored = set()
    frontier_states = {tuple(initial_state)}
    
    nodes_visited = 0
    max_frontier_size = 1
    max_depth = 0
    
    while frontier:
        if cancel_event is not None and cancel_event.is_set():
            return None, nodes_visited, max_frontier_size, max_depth
        
        if len(frontier) > max_frontier_size:
            max_frontier_size = len(frontier)
        
        current_node = frontier.pop()
        frontier_states.discard(tuple(current_node.state))
        nodes_visited += 1

        if nodes_visited % 500 == 0:
            _report_progress(progress_cb, nodes_visited, max_frontier_size, max_depth)
        
        if current_node.state == goal_state:
            return current_node, nodes_visited, max_frontier_size, max_depth
                
        explored.add(tuple(current_node.state))
        
        children_states = generate_children(current_node.state)
        
        for child_state in children_states:
            if tuple(child_state) not in explored and tuple(child_state) not in frontier_states:
                new_node = Node(child_state, parent=current_node, depth=current_node.depth + 1)
            
                if new_node.depth > max_depth:
                        max_depth = new_node.depth
                
                frontier.append(new_node)
                frontier_states.add(tuple(child_state))
            
    return None, nodes_visited, max_frontier_size, max_depth


def greedy_search(initial_state: list[int], goal_state: list[int], progress_cb=None, cancel_event=None) -> tuple[Node | None, int, int, int]:
    start_node = Node(initial_state, depth=0)
    
    start_node.h = calculate_manhattan(start_node.state, goal_state)
    
    frontier = []
    heapq.heappush(frontier, (start_node.h, id(start_node), start_node))
    
    explored = set()
    frontier_states = {tuple(initial_state)}
    
    nodes_visited = 0
    max_frontier_size = 1
    max_depth = 0
    
    while frontier:
        if cancel_event is not None and cancel_event.is_set():
            return None, nodes_visited, max_frontier_size, max_depth
        
        if len(frontier) > max_frontier_size:
            max_frontier_size = len(frontier)
        
        _, _, current_node = heapq.heappop(frontier)
        frontier_states.discard(tuple(current_node.state))
        
        nodes_visited += 1

        if nodes_visited % 200 == 0:
            _report_progress(progress_cb, nodes_visited, max_frontier_size, max_depth)
        
        if current_node.state == goal_state:
            return current_node, nodes_visited, max_frontier_size, max_depth
        
        explored.add(tuple(current_node.state))
        
        children_states = generate_children(current_node.state)
        
        for child_state in children_states:
            if tuple(child_state) not in explored and tuple(child_state) not in frontier_states:
                new_node = Node(child_state, parent=current_node, depth=current_node.depth + 1)
            
                if new_node.depth > max_depth:
                        max_depth = new_node.depth
                
                new_node.h = calculate_manhattan(child_state, goal_state)
                heapq.heappush(frontier, (new_node.h, id(new_node), new_node))
                frontier_states.add(tuple(child_state))
            
    return None, nodes_visited, max_frontier_size, max_depth


def a_star_search(initial_state: list[int], goal_state: list[int], progress_cb=None, cancel_event=None) -> tuple[Node | None, int, int, int]:
    start_node = Node(initial_state, depth=0)
    
    start_node.f = start_node.depth + calculate_manhattan(start_node.state, goal_state)
    
    frontier = []
    heapq.heappush(frontier, (start_node.f, id(start_node), start_node))
    
    explored = set()
    frontier_states = {tuple(initial_state)}
    
    nodes_visited = 0
    max_frontier_size = 1
    max_depth = 0
    
    while frontier:
        if cancel_event is not None and cancel_event.is_set():
            return None, nodes_visited, max_frontier_size, max_depth
        
        if len(frontier) > max_frontier_size:
            max_frontier_size = len(frontier)
        
        _, _, current_node = heapq.heappop(frontier)
        frontier_states.discard(tuple(current_node.state))
        
        nodes_visited += 1

        if nodes_visited % 200 == 0:
            _report_progress(progress_cb, nodes_visited, max_frontier_size, max_depth)
        
        if current_node.state == goal_state:
            return current_node, nodes_visited, max_frontier_size, max_depth
        
        explored.add(tuple(current_node.state))
        
        children_states = generate_children(current_node.state)
        
        for child_state in children_states:
            if tuple(child_state) not in explored and tuple(child_state) not in frontier_states:
                new_node = Node(child_state, parent=current_node, depth=current_node.depth + 1)
            
                if new_node.depth > max_depth:
                        max_depth = new_node.depth
                
                new_node.f = new_node.depth + calculate_manhattan(child_state, goal_state)
                heapq.heappush(frontier, (new_node.f, id(new_node), new_node))
                frontier_states.add(tuple(child_state))
            
    return None, nodes_visited, max_frontier_size, max_depth