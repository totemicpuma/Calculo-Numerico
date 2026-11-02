import math
import sympy as sp
import numpy as np

def resolver_simpson_13():
    print("\n--- Método de Simpson 1/3 ---")
    print("1. Usar Função (f(x))")
    print("2. Usar Tabela de Pontos (Dados Discretos)")
    escolha = input("Escolha o tipo de entrada (1 ou 2): ")

    # --- OPÇÃO 1: FUNCÃO MATEMÁTICA (Lógica original) ---
    if escolha == '1':
        try:
            funcao_str = input("Digite a função f(x) (ex: cos(x), x**2 + 1): ")
            a = float(input("Limite inferior (a): "))
            b = float(input("Limite superior (b): "))
            h_input = float(input("Digite o passo (h) desejado: "))
        except ValueError:
            print("Erro: Certifique-se de digitar números válidos.")
            return

        x_sym = sp.symbols('x')
        try:
            expressao = sp.sympify(funcao_str)
            f_num = sp.lambdify(x_sym, expressao, "math")
            f_num(a) 
        except Exception as e:
            print(f"Erro na função digitada: {e}")
            return

        n = int(round((b - a) / h_input))
        
        if n % 2 != 0:
            print(f"Aviso: n={n} é ímpar. Ajustando para par...")
            n += 1
            h = (b - a) / n
            print(f"Novo n = {n}, Novo h = {h:.6f}")
        else:
            h = h_input
            print(f"n = {n}, h = {h}")

        try:
            soma = f_num(a) + f_num(b)
            for i in range(1, n):
                x_val = a + i * h
                if i % 2 == 0:
                    soma += 2 * f_num(x_val)
                else:
                    soma += 4 * f_num(x_val)
                    
            resultado = (h / 3) * soma
            print(f"\n>>> RESULTADO FINAL (Simpson 1/3): {resultado:.8f}")

            # Cálculo do Erro (Apenas para Funções)
            print("\n--- Erro de Truncamento ---")
            derivada_4 = sp.diff(expressao, x_sym, 4)
            d4_num = sp.lambdify(x_sym, derivada_4, "math")
            pontos_teste = np.linspace(a, b, 1000)
            valores_derivada = [abs(d4_num(p)) for p in pontos_teste]
            max_deriv = max(valores_derivada)
            erro_trunc = ((b - a) * (h**4) / 180) * max_deriv
            print(f">>> Erro estimado: {erro_trunc:.10e}")

        except Exception as e:
            print(f"Erro durante o cálculo: {e}")

   
    elif escolha == '2':
        try:
            entrada = input("Digite os valores de Y separados por vírgula: ")
            y = [float(val) for val in entrada.replace(" ", "").split(',')]
            
           
            if (len(y) - 1) % 2 != 0:
                print(f"ERRO: Para Simpson 1/3, o número de intervalos deve ser PAR.")
                print(f"Você forneceu {len(y)} pontos, o que gera {len(y)-1} intervalos (Ímpar).")
                return

            h = float(input("Digite o passo (h) entre os pontos: "))
            
            soma = y[0] + y[-1]
            n = len(y) - 1
            
            for i in range(1, n):
                if i % 2 == 0:
                    soma += 2 * y[i]
                else:
                    soma += 4 * y[i]
            
            resultado = (h / 3) * soma
            print(f"\n>>> RESULTADO FINAL (Simpson 1/3 Discreto): {resultado:.8f}")
            
        except ValueError:
            print("Erro: Digite apenas números separados por vírgula.")
    else:
        print("Opção inválida.")

def resolver_simpson_38():
    print("\n--- Método de Simpson 3/8 ---")
    print("1. Usar Função (f(x))")
    print("2. Usar Tabela de Pontos (Dados Discretos)")
    escolha = input("Escolha o tipo de entrada (1 ou 2): ")

    if escolha == '1':
        try:
            funcao_str = input("Digite a função f(x) (ex: x**2 + x): ")
            a = float(input("Limite inferior (a): "))
            b = float(input("Limite superior (b): "))
            h_input = float(input("Digite o passo (h) desejado: "))
        except ValueError:
            print("Erro: Digite apenas números válidos.")
            return

        x_sym = sp.symbols('x')
        try:
            expressao = sp.sympify(funcao_str)
            f_num = sp.lambdify(x_sym, expressao, "math")
            f_num(a) 
        except Exception as e:
            print(f"Erro na sintaxe da função: {e}")
            return

        n = int(round((b - a) / h_input))
        
        if n % 3 != 0:
            print(f"Aviso: n={n} não é múltiplo de 3. Ajustando...")
            resto = n % 3
            n += (3 - resto)
            h = (b - a) / n
            print(f"Novo n = {n}, Novo h = {h:.6f}")
        else:
            h = h_input
            print(f"n = {n}, h = {h}")

        try:
            soma = f_num(a) + f_num(b)
            for i in range(1, n):
                x_val = a + i * h
                if i % 3 == 0:
                    soma += 2 * f_num(x_val)
                else:
                    soma += 3 * f_num(x_val)

            resultado = (3 * h / 8) * soma
            print(f"\n>>> RESULTADO FINAL (Simpson 3/8): {resultado:.8f}")
            
            print("\n--- Erro de Truncamento ---")
            derivada_4 = sp.diff(expressao, x_sym, 4)
            d4_num = sp.lambdify(x_sym, derivada_4, "math")
            pontos_teste = np.linspace(a, b, 1000)
            valores_derivada = [abs(d4_num(p)) for p in pontos_teste]
            max_deriv = max(valores_derivada)
            erro_trunc = ((b - a) * (h**4) / 80) * max_deriv
            print(f">>> Erro estimado: {erro_trunc:.10e}")

        except Exception as e:
            print(f"Erro no cálculo: {e}")

    elif escolha == '2':
        try:
            entrada = input("Digite os valores de Y separados por vírgula: ")
            y = [float(val) for val in entrada.replace(" ", "").split(',')]
            
            if (len(y) - 1) % 3 != 0:
                print(f"ERRO: Para Simpson 3/8, o número de intervalos deve ser múltiplo de 3.")
                return

            h = float(input("Digite o passo (h) entre os pontos: "))
            
            soma = y[0] + y[-1]
            n = len(y) - 1
            
            for i in range(1, n):
                if i % 3 == 0:
                    soma += 2 * y[i]
                else:
                    soma += 3 * y[i]
            
            resultado = (3 * h / 8) * soma
            print(f"\n>>> RESULTADO FINAL (Simpson 3/8 Discreto): {resultado:.8f}")

        except ValueError:
            print("Erro: Digite apenas números.")
    else:
        print("Opção inválida.")

def trapezio_simples():
    print("\n--- Método do Trapézio (Dados Discretos) ---")
    try:
        entrada = input("Digite as alturas/profundidades separadas por vírgula: ")
        y = [float(val) for val in entrada.replace(" ", "").split(',')]
        h = float(input("Digite o passo (h) entre os pontos: "))
        
        if len(y) < 2:
            print("Erro: Preciso de pelo menos 2 pontos.")
            return

        soma = y[0] + y[-1]
        for i in range(1, len(y)-1):
            soma += 2 * y[i]
            
        area = (h/2) * soma
        print(f"\n>>> RESULTADO FINAL (Área Aproximada): {area:.6f}")
        
    except ValueError:
        print("Erro: Certifique-se de usar vírgulas para separar e pontos para decimais.")
    except Exception as e:
        print(f"Erro inesperado: {e}")

def main():
    while True:
        print("\n" + "="*40)
        print("   CALCULADORA DE CÁLCULO NUMÉRICO")
        print("="*40)
        print("1. Calcular Integral por Simpson 1/3")
        print("2. Calcular Integral por Simpson 3/8")
        print("3. Calcular Área por Trapézio (Lista de Pontos)")
        print("0. Sair")
        
        opcao = input("\nEscolha sua ferramenta: ")
        
        if opcao == '1':
            resolver_simpson_13()
        elif opcao == '2':
            resolver_simpson_38()
        elif opcao == '3':
            trapezio_simples()
        elif opcao == '0':
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma interrompido pelo usuário.")