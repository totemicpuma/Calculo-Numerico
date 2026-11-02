import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import sys

class CalculadoraRaizes:
    def __init__(self):
        self.f_expr = None
        self.f_num = None
        self.df_num = None
        self.str_funcao = ""
        self.a = None
        self.b = None
        self.tol = None
        self.max_iter = 500

    def definir_parametros(self):
        print("\n" + "="*50)
        print("   CONFIGURAÇÃO DA FUNÇÃO E INTERVALO")
        print("="*50)
        print("Digite a função em função de x (ex: x**4 - 2*x**3 + 2*x - 1)")
        self.str_funcao = input("f(x) = ")
        
        try:
            x = sp.symbols('x')
            expr_tratada = self.str_funcao.replace('^', '**')
            self.f_expr = sp.sympify(expr_tratada)
            
            df_expr = sp.diff(self.f_expr, x)
            
            self.f_num = sp.lambdify(x, self.f_expr, modules=['numpy'])
            self.df_num = sp.lambdify(x, df_expr, modules=['numpy'])
            
            print(f"   -> Interpretado: f(x) = {self.f_expr}")
            print(f"   -> Derivada:    f'(x) = {df_expr}")
            print("-" * 50)
            
            self.a = float(input("Início do intervalo [a]: "))
            self.b = float(input("Fim do intervalo    [b]: "))
            self.tol = float(input("Tolerância (ex: 1e-4): "))
            
            print("\n>> DADOS CONFIGURADOS COM SUCESSO!")
            
        except Exception as e:
            print(f"\n[ERRO FATAL] Não foi possível ler a função.\nDetalhe: {e}")
            self.f_num = None

    def checar_dados(self):
        if self.f_num is None or self.a is None:
            print("\n[!] ALERTA: Configure a função primeiro (Opção 1).")
            return False
        return True

    def plotar_grafico(self):
        if not self.checar_dados(): return
        
        print("\n>> [GRÁFICO] Abrindo janela do gráfico...")
        print(">> [AVISO] Feche a janela do gráfico para ver os cálculos.")
        
        margem = abs(self.b - self.a) * 0.5
        if margem == 0: margem = 1.0
        
        min_val = min(self.a, self.b) - margem
        max_val = max(self.a, self.b) + margem
        
        x_vals = np.linspace(min_val, max_val, 200)
        y_vals = self.f_num(x_vals)
        
        plt.figure(figsize=(10, 6))
        plt.plot(x_vals, y_vals, label=f'f(x) = {self.str_funcao}', color='blue', linewidth=2)
        plt.axhline(0, color='black', linewidth=1)
        plt.axvline(self.a, color='red', linestyle='--', label=f'Intervalo a={self.a}')
        plt.axvline(self.b, color='green', linestyle='--', label=f'Intervalo b={self.b}')
        
        plt.title(f"Análise Gráfica: {self.str_funcao}")
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.show()

    def bissecao(self, verbose=True):
        if not self.checar_dados(): return None, 0
        
        a, b = self.a, self.b
        
        try:
            fa = self.f_num(a)
            fb = self.f_num(b)
        except Exception as e:
            print(f"\n[ERRO MATEMÁTICO] Falha em f(a) ou f(b): {e}")
            return None, 0
        
        if fa * fb >= 0:
            if verbose:
                print(f"\n[ERRO] Sinais iguais em f({a}) e f({b}). Escolha outro intervalo!")
            return None, 0

        if verbose:
            print(f"\n>>> MÉTODO DA BISSEÇÃO (Versão Final - Padrão Frederico Campos)")
            print(f"{'It':<4} {'x_m (Médio)':<12} {'f(x_m)':<12} {'Intervalo |b-a|':<15}")
            print("-" * 55)

        it = 0
        erro = abs(b - a) 
        x_m = a

        while erro > self.tol and it < self.max_iter:
            it += 1
            x_m = (a + b) / 2.0
            fx_m = self.f_num(x_m)
            
            if verbose:
                print(f"{it:<4} {x_m:<12.8f} {fx_m:<12.2e} {erro:<15.8f}")

          
            if fx_m == 0:
                if verbose: print(f"{' ':>4} >> Raiz exata encontrada em x = {x_m}")
                a = b = x_m 
                break 
                
          
            if fa * fx_m < 0:
                b = x_m
                fb = fx_m
            else:
                a = x_m
                fa = fx_m
            
          
            erro = abs(b - a)
            
        return x_m, it

    def newton(self, verbose=True):
        if not self.checar_dados(): return None, 0
        
        x0 = self.b
        
        if verbose:
            print(f"\n>>> MÉTODO DE NEWTON (Chute inicial: {x0})")
            print(f"{'It':<4} {'x_ant':<12} {'x_novo':<12} {'f(x_novo)':<12} {'Erro':<10}")
            print("-" * 65)
        
        it = 0
        erro = float('inf')
        x_atual = x0
        
        while erro > self.tol and it < self.max_iter:
            it += 1
            x_ant = x_atual
            
            deriv = self.df_num(x_ant)
            if deriv == 0:
                if verbose: print("[ERRO] Derivada zero em Newton.")
                return None, it
            
            x_atual = x_ant - self.f_num(x_ant) / deriv
            erro = abs(x_atual - x_ant)
            fx = self.f_num(x_atual)
            
            if verbose:
                print(f"{it:<4} {x_ant:<12.6f} {x_atual:<12.6f} {fx:<12.2e} {erro:<10.2e}")
                
        return x_atual, it

    def secante(self, verbose=True):
        if not self.checar_dados(): return None, 0
        
        x0 = self.a
        x1 = self.b
        
        if verbose:
            print(f"\n>>> MÉTODO DA SECANTE (Início: {x0} e {x1})")
            print(f"{'It':<4} {'x_ant':<12} {'x_prox':<12} {'f(x_prox)':<12} {'Erro':<10}")
            print("-" * 65)

        it = 0
        erro = float('inf')
        
        while erro > self.tol and it < self.max_iter:
            it += 1
            fx0 = self.f_num(x0)
            fx1 = self.f_num(x1)
            
            if fx1 - fx0 == 0:
                if verbose: print("[ERRO] Divisão por zero na Secante.")
                return None, it

            x_prox = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
            erro = abs(x_prox - x1)
            fx_prox = self.f_num(x_prox)
            
            if verbose:
                print(f"{it:<4} {x0:<12.6f} {x_prox:<12.6f} {fx_prox:<12.2e} {erro:<10.2e}")
            
            x0 = x1
            x1 = x_prox
            
        return x_prox, it

    def resolver_e_comparar(self):
        if not self.checar_dados(): return

        self.plotar_grafico()
        
        print("\n[Executando Bisseção...]")
        raiz_b, it_b = self.bissecao(verbose=True)
        
        print("\n[Executando Newton...]")
        raiz_n, it_n = self.newton(verbose=True)
        
        print("\n[Executando Secante...]")
        raiz_s, it_s = self.secante(verbose=True)
        
        print(f"{'RESUMO COMPARATIVO':^60}")
        print(f"{'MÉTODO':<15} | {'ITERAÇÕES':<10} | {'RAIZ FINAL':<12} | {'CONVERGIU?'}")
        
        def linha(nome, r, i):
            if r is None: return f"{nome:<15} | {'-':<10} | {'FALHA':<12} | {'NÃO'}"
            ok = "SIM" if i < self.max_iter else "NÃO"
            return f"{nome:<15} | {i:<10} | {r:<12.8f} | {ok}"

        print(linha("Bisseção", raiz_b, it_b))
        print(linha("Newton", raiz_n, it_n))
        print(linha("Secante", raiz_s, it_s))
        print("-" * 60)
        
        candidatos = []
        if raiz_b: candidatos.append((it_b, 'Bisseção'))
        if raiz_n: candidatos.append((it_n, 'Newton'))
        if raiz_s: candidatos.append((it_s, 'Secante'))
        
        if candidatos:
            vencedor = min(candidatos)
            print(f"\n>> CAMPEÃO: {vencedor[1]} com {vencedor[0]} iterações.")
        else:
            print("\n>> Nenhum método convergiu.")
            
        input("\nPressione ENTER para voltar ao menu...")

def main():
    sistema = CalculadoraRaizes()
    
    while True:
        print("1 - [CONFIGURAR] Definir Função e Intervalo")
        print("2 - [BISSEÇÃO]  ")
        print("3 - [NEWTON]    ")
        print("4 - [SECANTE]   ")
        print("5 - [COMPARAR]  ")
        print("0 - Sair")
        
        op = input("Escolha uma opção: ")
        
        if op == '0':
            print("Progama encerrado")
            break
        elif op == '1':
            sistema.definir_parametros()
        elif op == '2':
            sistema.plotar_grafico()
            sistema.bissecao(verbose=True)
            input("\nPressione ENTER para continuar...")
        elif op == '3':
            sistema.plotar_grafico()
            sistema.newton(verbose=True)
            input("\nPressione ENTER para continuar...")
        elif op == '4':
            sistema.plotar_grafico()
            sistema.secante(verbose=True)
            input("\nPressione ENTER para continuar...")
        elif op == '5':
            sistema.resolver_e_comparar()
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()