import numpy as np
import math
import sympy 

def lagrange_interpolation(x_points, y_points, x_interp):
    n = len(x_points)
    result = 0.0

    for i in range(n):
        L_i = 1.0 
        for j in range(n):
            if i != j:
                L_i *= (x_interp - x_points[j]) / (x_points[i] - x_points[j])

        result += y_points[i] * L_i

    return result

def newton_divided_differences_interpolation(x_points, y_points, x_interp):
    n = len(x_points)
    diff_table = np.zeros((n, n))
    diff_table[:, 0] = y_points

    for j in range(1, n):
        for i in range(n - j):
            numerator = diff_table[i+1, j-1] - diff_table[i, j-1]
            denominator = x_points[i+j] - x_points[i]
            diff_table[i, j] = numerator / denominator

    coefficients = diff_table[0, :]
    result = coefficients[0]

    for j in range(1, n):
        term = coefficients[j]
        for i in range(j):
            term *= (x_interp - x_points[i])
        result += term

    return result, coefficients

def gregory_newton_interpolation(x_points, y_points, x_interp):
    n = len(x_points)

    h = x_points[1] - x_points[0]
    for i in range(2, n):
        if abs((x_points[i] - x_points[i-1]) - h) > 1e-9:
            return f"ERRO: Gregory-Newton requer pontos x igualmente espaçados (h constante).", None

    diff_table = np.zeros((n, n))
    diff_table[:, 0] = y_points

    for j in range(1, n):
        for i in range(n - j):
            diff_table[i, j] = diff_table[i+1, j-1] - diff_table[i, j-1]

    coefficients = diff_table[0, :]

    s = (x_interp - x_points[0]) / h
    result = coefficients[0]

    for j in range(1, n):
        s_factor = 1.0
        for i in range(j):
            s_factor *= (s - i)

        s_factor /= math.factorial(j)

        result += s_factor * coefficients[j]

    return result, coefficients

def neville_interpolation(x_points, y_points, x_interp):
    n = len(x_points)
    Q = np.zeros((n, n))
    Q[:, 0] = y_points

    for j in range(1, n):
        for i in range(n - j):
            term1 = (x_interp - x_points[i]) * Q[i+1, j-1]
            term2 = (x_interp - x_points[i+j]) * Q[i, j-1]
            denominator = x_points[i+j] - x_points[i]

            Q[i, j] = (term1 - term2) / denominator

    return Q[0, n-1], Q

def calcular_produtorio_erro(vetor_x, x_interpolar):

    omega_x = 1.0
    try:
        for xi in vetor_x:
            omega_x *= (x_interpolar - xi)
        return omega_x
    except Exception:
        return None

def estimar_erro_truncamento_maximo(vetor_x, x_interpolar, max_derivada_n_mais_1):
    
    num_pontos = len(vetor_x)
    if num_pontos == 0: return None
    n = num_pontos - 1

    omega_x = calcular_produtorio_erro(vetor_x, x_interpolar)
    if omega_x is None: return None

    try:
        fatorial_n_mais_1 = math.factorial(n + 1)
        if fatorial_n_mais_1 == 0: return None
    except (ValueError, OverflowError): return None

    try:
        erro_max_estimado = (abs(max_derivada_n_mais_1) / fatorial_n_mais_1) * abs(omega_x)
        return erro_max_estimado
    except Exception: 
        return None

def calcular_erro_com_funcao(funcao_str, vetor_x, x_interpolar):
   
    num_pontos = len(vetor_x)
    if num_pontos == 0: return None, None
    n = num_pontos - 1
    ordem_derivada = n + 1

    try:
        x_sym = sympy.Symbol('x')
        f_sym = sympy.sympify(funcao_str)
        derivada_n_mais_1 = sympy.diff(f_sym, x_sym, ordem_derivada)

        deriv_func = sympy.lambdify(x_sym, derivada_n_mais_1, modules=['numpy', 'math'])

        intervalo_min = min(min(vetor_x), x_interpolar)
        intervalo_max = max(max(vetor_x), x_interpolar)
        num_samples = 1000
        pontos_amostra = np.linspace(intervalo_min, intervalo_max, num_samples)
        
        try:
            valores_derivada = [abs(deriv_func(pt)) for pt in pontos_amostra if isinstance(deriv_func(pt), (int, float, np.number))]
            max_deriv_estimado = max(valores_derivada) if valores_derivada else 0.0
        except (TypeError, ValueError, NameError):
            max_deriv_estimado = None

        if max_deriv_estimado is None or max_deriv_estimado == 0.0: 
            return None, None

        erro_max_estimado = estimar_erro_truncamento_maximo(vetor_x, x_interpolar, max_deriv_estimado)
        
        if erro_max_estimado is None: return None, None
        
        omega_x = calcular_produtorio_erro(vetor_x, x_interpolar) 
        return erro_max_estimado, omega_x

    except (sympy.SympifyError, SyntaxError): 
        return None, None
    except Exception: 
        return None, None


def _processar_erro(vx, x_interpolar):
    print("\n--- Opção 6: Cálculo do Erro Máximo de Truncamento ---")
    
    funcao_str = input("Informe a função f(x) para cálculo do Erro Máximo (ex: 'exp(3*x)', x**3 + 2, cos(x)): ")
    
    erro_max, _ = calcular_erro_com_funcao(funcao_str, vx, x_interpolar)

    if erro_max is not None:
        print(f"Estimativa Erro Máx ≈ {erro_max:.8f}") 
    else:
        print("Erro: Não foi possível calcular a Estimativa do Erro Máximo. Verifique a função f(x) informada.")

def get_data():
    print("\nEntrada de Dados")

    while True:
        try:
            x_str = input("Digite os pontos de x separados por vírgula (ex: 1.0, 2.5, 3.0): ")
            y_str = input("Digite os pontos de y (f(x)) correspondentes separados por vírgula (ex: 0.5, 2.0, 4.5): ")

            x_points = np.array([float(val.strip()) for val in x_str.split(',')])
            y_points = np.array([float(val.strip()) for val in y_str.split(',')])

            if len(x_points) != len(y_points):
                print("ERRO: O número de pontos em x e em y deve ser o mesmo. Tente novamente.")
                continue

            if len(x_points) < 2:
                print("ERRO: É necessário pelo menos 2 pontos para a interpolação. Tente novamente.")
                continue

            x_interp = float(input("Digite o ponto 'x' que você deseja interpolar: "))

            return x_points, y_points, x_interp

        except ValueError:
            print("ERRO: Entrada inválida. Certifique-se de usar números e separar os valores por vírgula.")
        except Exception as e:
            print(f"Ocorreu um erro: {e}. Tente novamente.")

def main_menu():

    x_points = None
    y_points = None
    x_interp = None

    while True:
        print("\nMENU DE INTERPOLAÇÃO E ANÁLISE DE ERRO")
        print("1. Inserir/Atualizar Pontos de Dados")
        print("2. Interpolação de Lagrange")
        print("3. Interpolação de Newton")
        print("4. Interpolação de Gregory-Newton")
        print("5. Método Prático")
        print("6. Cálculo do Erro Máximo de Truncamento")
        print("0. Sair")

        choice = input("Escolha uma opção (0-6): ")

        if choice == '0':
            print("Código Encerrado")
            break

        if choice == '1':
            x_points, y_points, x_interp = get_data()
            if x_points is not None:
                 print(f"\nDados carregados: X={x_points}, Y={y_points}, x_interp={x_interp}")
            continue

        if x_points is None:
            print("\nAVISO: Por favor, insira os pontos de dados primeiro (Opção 1).")
            continue

        try:
            if choice == '2':
                result = lagrange_interpolation(x_points, y_points, x_interp)
                print("\n--- Resultado Interpolação de Lagrange ---")
                print(f"P({x_interp}) ≈ {result:.8f}")

            elif choice == '3':
                result, coefficients = newton_divided_differences_interpolation(x_points, y_points, x_interp)
                print("\n--- Resultado Interpolação de Newton (Diferenças Divididas) ---")
                print(f"Coeficientes do Polinômio (Diferenças Divididas, primeira linha): {coefficients}")
                print(f"P({x_interp}) ≈ {result:.8f}")

            elif choice == '4':
                result_or_error, coefficients = gregory_newton_interpolation(x_points, y_points, x_interp)
                print("\n--- Resultado Interpolação de Gregory-Newton ---")

                if isinstance(result_or_error, str):
                    print(result_or_error)
                else:
                    h = x_points[1] - x_points[0]
                    s = (x_interp - x_points[0]) / h
                    print(f"h (espaçamento) = {h:.4f}, s (parâmetro) = {s:.4f}")
                    print(f"Coeficientes do Polinômio (Diferenças Finitas, primeira linha): {coefficients}")
                    print(f"P({x_interp}) ≈ {result_or_error:.8f}")

            elif choice == '5':
                result, Q_table = neville_interpolation(x_points, y_points, x_interp)
                print("\nResultado Método Prático (Neville)")
                print("Tabela de Neville (Polinômios Iterativos Q):")

                for row in Q_table:
                    print([f"{val:.8f}" for val in row if val != 0])
                print(f"P({x_interp}) ≈ {result:.8f}")

            elif choice == '6':
                _processar_erro(x_points, x_interp)

            else:
                print("\nOpção inválida. Por favor, escolha um número de 0 a 6.")

        except Exception as e:
            print(f"\nERRO de execução no algoritmo: {e}")
            print("Verifique seus dados de entrada e a validade do método.")

main_menu()