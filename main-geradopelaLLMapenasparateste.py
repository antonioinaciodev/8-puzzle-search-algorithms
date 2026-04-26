import tkinter as tk
from tkinter import messagebox
import time

# Importa o motor que você construiu no outro arquivo
from jogo8 import breadth_first_search, depth_first_search, greedy_search, a_star_search

class JogoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Testador de IA - Jogo do 8 e 15")
        self.root.geometry("400x500")
        self.root.configure(padx=20, pady=20)
        
        # Variável que guarda o tamanho atual (3 para 3x3, 4 para 4x4)
        self.tamanho_var = tk.IntVar(value=3) 
        
        # --- ELEMENTOS DA INTERFACE ---
        tk.Label(root, text="Selecione o tamanho do tabuleiro:", font=("Arial", 10, "bold")).pack(pady=(0, 5))
        
        frame_radios = tk.Frame(root)
        frame_radios.pack(pady=(0, 10))
        tk.Radiobutton(frame_radios, text="3x3 (Jogo do 8)", variable=self.tamanho_var, value=3, command=self.desenhar_grid).pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(frame_radios, text="4x4 (Jogo do 15)", variable=self.tamanho_var, value=4, command=self.desenhar_grid).pack(side=tk.LEFT, padx=10)
        
        tk.Label(root, text="Insira o tabuleiro inicial\n(Use 0 para o espaço vazio):", font=("Arial", 10)).pack(pady=(0, 15))
        
        self.frame_grid = tk.Frame(root)
        self.frame_grid.pack()
        
        self.entradas = []
        self.desenhar_grid() # Desenha o grid inicial 3x3
        
        tk.Button(root, text="Resolver Tabuleiro", command=self.iniciar_buscas, font=("Arial", 12), bg="#4CAF50", fg="white", pady=5).pack(pady=20, fill="x")

    def desenhar_grid(self):
        """Apaga o grid atual e desenha um novo baseado na escolha do usuário."""
        for widget in self.frame_grid.winfo_children():
            widget.destroy()
        
        self.entradas = []
        lado = self.tamanho_var.get()
        
        for i in range(lado * lado):
            linha = i // lado
            coluna = i % lado
            entry = tk.Entry(self.frame_grid, width=3, font=("Arial", 20), justify="center")
            entry.grid(row=linha, column=coluna, padx=5, pady=5)
            self.entradas.append(entry)

    def rodar_testes_e_imprimir(self, initial_state, goal_state):
        lado = self.tamanho_var.get()
        print("\n" + "="*55)
        print(f" INICIANDO TESTES PARA O TABULEIRO {lado}x{lado}: {initial_state}")
        print("="*55)
        
        algoritmos = [
            ("Busca em Largura (BFS)", breadth_first_search),
            ("Busca em Profundidade (DFS)", depth_first_search),
            ("Busca Gulosa (Greedy)", greedy_search),
            ("Busca A* (A-Star)", a_star_search)
        ]
        
        for nome, funcao_busca in algoritmos:
            print(f"\nRodando {nome}...")
            inicio_tempo = time.time()
            resultado = funcao_busca(initial_state, goal_state)
            fim_tempo = time.time()
            tempo_total = fim_tempo - inicio_tempo
            
            if resultado is not None and resultado[0] is not None:
                no_solucao, nos_visitados, max_fronteira, max_profundidade = resultado
                movimentos = len(no_solucao.get_path()) - 1
                
                print(f"  -> Status: SOLUÇÃO ENCONTRADA")
                print(f"  -> Movimentos necessários: {movimentos}")
                print(f"  -> Tempo de execução: {tempo_total:.4f} segundos")
                print(f"  -> Nós visitados (Tempo): {nos_visitados}")
                print(f"  -> Tamanho máximo da fronteira (Memória): {max_fronteira}")
                print(f"  -> Profundidade máxima atingida: {max_profundidade}")
            else:
                print(f"  -> Status: FALHA. Nenhuma solução encontrada.")

    def iniciar_buscas(self):
        lado = self.tamanho_var.get()
        total_pecas = lado * lado
        
        try:
            valores = [int(self.entradas[i].get()) for i in range(total_pecas)]
            
            # Validação dinâmica: checa se tem todos os números de 0 até (total_pecas - 1)
            if set(valores) != set(range(total_pecas)):
                messagebox.showerror("Erro", f"O tabuleiro deve conter todos os números de 0 a {total_pecas - 1}, sem repetições.")
                return
                
            # Gera o estado objetivo dinamicamente. Ex: [1, 2, ..., 15, 0]
            goal_state = list(range(1, total_pecas)) + [0]
            
            messagebox.showinfo("Rodando", "Olhe o terminal (console) para ver os resultados das buscas!")
            self.root.update() # Força a tela a atualizar antes de travar com a busca
            self.rodar_testes_e_imprimir(valores, goal_state)
            
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira apenas números inteiros válidos em todas as casas.")

if __name__ == "__main__":
    root = tk.Tk()
    app = JogoApp(root)
    root.mainloop()