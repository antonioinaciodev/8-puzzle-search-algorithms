import tkinter as tk
from tkinter import messagebox
import time

# Importa o motor que você construiu no outro arquivo
from jogo8 import breadth_first_search, depth_first_search, greedy_search, a_star_search

# Definição do tabuleiro final vencedor (Modifique se o professor usar outro formato)
GOAL_STATE = [1, 2, 3, 4, 5, 6, 7, 8, 0]

def rodar_testes_e_imprimir(initial_state):
    print("\n" + "="*50)
    print(f" INICIANDO TESTES PARA O TABULEIRO: {initial_state}")
    print("="*50)
    
    # Lista com as 4 funções para rodarmos em um loop
    algoritmos = [
        ("Busca em Largura (BFS)", breadth_first_search),
        ("Busca em Profundidade (DFS)", depth_first_search),
        ("Busca Gulosa (Greedy)", greedy_search),
        ("Busca A* (A-Star)", a_star_search)
    ]
    
    for nome, funcao_busca in algoritmos:
        print(f"\nRodando {nome}...")
        
        # Inicia o cronômetro
        inicio_tempo = time.time()
        
        # Chama a sua função de busca!
        resultado = funcao_busca(initial_state, GOAL_STATE)
        
        # Para o cronômetro
        fim_tempo = time.time()
        tempo_total = fim_tempo - inicio_tempo
        
        if resultado is not None and resultado[0] is not None:
            no_solucao, nos_visitados, max_fronteira, max_profundidade = resultado
            # O número de movimentos é o tamanho do caminho gerado menos o estado inicial
            movimentos = len(no_solucao.get_path()) - 1
            
            print(f"  -> Status: SOLUÇÃO ENCONTRADA")
            print(f"  -> Movimentos necessários: {movimentos}")
            print(f"  -> Tempo de execução: {tempo_total:.4f} segundos")
            print(f"  -> Nós visitados (Tempo): {nos_visitados}")
            print(f"  -> Tamanho máximo da fronteira (Memória): {max_fronteira}")
            print(f"  -> Profundidade máxima atingida: {max_profundidade}")
        else:
            print(f"  -> Status: FALHA. Nenhuma solução encontrada.")

# --- INTERFACE GRÁFICA (TKINTER) ---

def iniciar_buscas():
    """Lê os valores da interface, valida e chama o testador."""
    try:
        # Pega os valores das 9 caixinhas
        valores = [int(entradas[i].get()) for i in range(9)]
        
        # Validação básica
        if set(valores) != set(range(9)):
            messagebox.showerror("Erro", "O tabuleiro deve conter todos os números de 0 a 8, sem repetições.")
            return
            
        messagebox.showinfo("Rodando", "Olhe o terminal (console) para ver os resultados das buscas!")
        rodar_testes_e_imprimir(valores)
        
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira apenas números inteiros válidos.")

# Configuração da Janela
root = tk.Tk()
root.title("Jogo do 8 - Testador de IA")
root.geometry("300x350")
root.configure(padx=20, pady=20)

tk.Label(root, text="Insira o tabuleiro inicial\n(Use 0 para o espaço vazio):", font=("Arial", 10, "bold")).pack(pady=(0, 15))

# Criação do Grid 3x3
frame_grid = tk.Frame(root)
frame_grid.pack()

entradas = []
for i in range(9):
    linha = i // 3
    coluna = i % 3
    entry = tk.Entry(frame_grid, width=3, font=("Arial", 24), justify="center")
    entry.grid(row=linha, column=coluna, padx=5, pady=5)
    entradas.append(entry)

tk.Button(root, text="Resolver Tabuleiro", command=iniciar_buscas, font=("Arial", 12), bg="#4CAF50", fg="white", pady=5).pack(pady=20, fill="x")

# Mantém a janela aberta
root.mainloop()