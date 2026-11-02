import math
import matplotlib.pyplot as plt
import numpy as np

def calcular_metricas_ajuste(y_dados, y_predito, qtd, grau):
    desvio = sum((y_obs - y_pred)**2 for y_obs, y_pred in zip(y_dados, y_predito))
    
    y_media = sum(y_dados) / qtd
    soma_dif_total = sum((y - y_media)**2 for y in y_dados)
    
    if soma_dif_total == 0:
        r2 = 1.0 if desvio < 1e-9 else 0.0
    else:
        r2 = 1.0 - (desvio / soma_dif_total)
        
    graus_de_liberdade = qtd - (grau + 1)
    
    if graus_de_liberdade > 0:
        chi2_reduzido = desvio / graus_de_liberdade
    else:
        chi2_reduzido = float('inf') 
        
    return chi2_reduzido, r2

def diagrama_dispersao(x_dados, y_dados):

    plt.figure(figsize=(8, 5))
    plt.scatter(x_dados, y_dados, color='blue', marker='o')
    plt.title('Diagrama de Dispersão dos Dados')
    plt.xlabel('Variável X (Independente)')
    plt.ylabel('Variável Y (Dependente)')
    plt.grid(True)
    plt.show()

def eliminacao_gauss(A, b):
    n = len(A)
    for i in range(n):
    
        if A[i][i] == 0:
            for k in range(i + 1, n):
                if A[k][i] != 0:
                    A[i], A[k] = A[k], A[i]
                    b[i], b[k] = b[k], b[i]
                    break
        
        for j in range(i + 1, n):
            if A[i][i] == 0:
                raise ValueError("Sistema singular detectado.")
            fator = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= fator * A[i][k]
            b[j] -= fator * b[i]

    x = [0] * n
    for i in range(n - 1, -1, -1):
        soma = 0
        for j in range(i + 1, n):
            soma += A[i][j] * x[j]
        x[i] = (b[i] - soma) / A[i][i]
    
    return x

def interpolacao_linear(x_pontos, y_pontos, x_estimado):
    
    if len(x_pontos) != 2:
        
        return None, None, None 
    
    x0 = x_pontos[0]
    y0 = y_pontos[0]
    x1 = x_pontos[1]
    y1 = y_pontos[1]
    
    denominador = x1 - x0
    
    if denominador == 0:

        return None, None, None 

    m = (y1 - y0) / denominador 
    b = y0 - m * x0
    
    y_estimado = m * x_estimado + b 

    return y_estimado, m, b

def regressao_linear_simples(x_dados, y_dados):
    n = len(x_dados)
    
    soma_x = sum(x_dados)
    soma_y = sum(y_dados)
    soma_xy = sum(x * y for x, y in zip(x_dados, y_dados))
    soma_x2 = sum(x * x for x in x_dados)

    denominador_a1 = (n * soma_x2) - (soma_x * soma_x)
    
    if denominador_a1 == 0:
        return float('nan'), float('nan')
        
    numerador_a1 = (n * soma_xy) - (soma_x * soma_y)
    a1 = numerador_a1 / denominador_a1

    media_x = soma_x / n
    media_y = soma_y / n
    a0 = media_y - (a1 * media_x)

    return a0, a1

def regressao_polinomial_quadratica(x_dados, y_dados):
    n = len(x_dados)
    
    S0 = n
    S1, S2, S3, S4 = sum(x for x in x_dados), sum(x**2 for x in x_dados), sum(x**3 for x in x_dados), sum(x**4 for x in x_dados)
    Sy, Sxy, Sx2y = sum(y for y in y_dados), sum(x * y for x, y in zip(x_dados, y_dados)), sum(x**2 * y for x, y in zip(x_dados, y_dados))
        
    A = [
        [S0, S1, S2],
        [S1, S2, S3],
        [S2, S3, S4]
    ]
    b = [Sy, Sxy, Sx2y]
    
    A_clone = [row[:] for row in A]
    b_clone = b[:]

    coefs = eliminacao_gauss(A_clone, b_clone)
    
    return coefs[0], coefs[1], coefs[2]

def estimar_y(a0, a1, x_estimado):
    
    return a0 + a1 * x_estimado

def estimar_x(a0, a1, y_estimado):
    
    if abs(a1) < 1e-9: 
        raise ValueError("O coeficiente a1 é muito próximo de zero. Impossível inverter a reta para estimar X.")
    return (y_estimado - a0) / a1

def obter_dados_do_usuario():
    x_str = input("\n[X] Insira os valores de X separados por vírgula (ex: 1, 2, 3, 4): ")
    try:
        x_dados = [float(val.strip()) for val in x_str.split(',')]
    except ValueError:
        print("[ERRO] Valores de X inválidos.")
        return [], []
        
    y_str = input("[Y] Insira os valores de Y separados por vírgula (ex: 1.3, 3.5, 4.2, 5.0): ")
    try:
        y_dados = [float(val.strip()) for val in y_str.split(',')]
    except ValueError:
        print("[ERRO] Valores de Y inválidos.")
        return [], []
    
    if len(x_dados) != len(y_dados):
        print("\n[ERRO] O número de pontos em X e Y deve ser o mesmo. Reinicie o programa.")
        return [], []
    
    return x_dados, y_dados

def executar_diagrama_dispersao():
    print("\n--- Diagrama de Dispersão (Visualização) ---")
    x_dados, y_dados = obter_dados_do_usuario()
    
    if not x_dados:
        return

    diagrama_dispersao(x_dados, y_dados)

def executar_interpolacao_linear():
    print("\n--- Interpolação Linear (Ordem 1) ---")
    x_dados, y_dados = obter_dados_do_usuario()
    
    if not x_dados:
        return
    
    if len(x_dados) != 2:
        print("\n[ERRO] A Interpolação Linear requer *exatamente 2 pontos*. Você forneceu", len(x_dados))
        return

    try:
        x_estimado = float(input("[Ponto] Insira o ponto X para interpolação: "))
    except ValueError:
        print("[ERRO] Ponto de estimação X inválido.")
        return
    
    y_estimado, m, b = interpolacao_linear(x_dados, y_dados, x_estimado)
    
    if y_estimado is None:
        print("\n[ERRO] Não foi possível realizar a interpolação (divisão por zero ou erro de entrada).")
        return

    print("\n--- Resultado ---")
    print(f"  - Inclinação (m): {m:.4f}")
    print(f"  - Coeficiente Linear (b): {b:.4f}")
    print(f"  - Equação da Reta: Y = {b:.4f} + {m:.4f}*X")
    print(f"  - Valor Interpolado em X={x_estimado:.4f}: Y = {y_estimado:.4f}")

def plotar_regressao_linear(x_dados, y_dados, a0, a1):
    x_arr = np.array(x_dados)
    
    x_min, x_max = x_arr.min(), x_arr.max()
    offset = (x_max - x_min) * 0.1
    x_plot = np.linspace(x_min - offset, x_max + offset, 100)
    
    y_plot = a0 + a1 * x_plot

    plt.figure(figsize=(10, 6))
    
    plt.scatter(x_dados, y_dados, color='blue', marker='o', label='Dados Originais')
    
    plt.plot(x_plot, y_plot, color='red', linestyle='-', 
             label=f'Reta de Regressão: Y = {a0:.4f} + {a1:.4f}*X')
    
    plt.title('Regressão Linear Simples: Ajuste da Reta aos Dados (MQM)')
    plt.xlabel('Variável X (Independente)')
    plt.ylabel('Variável Y (Dependente)')
    plt.legend()
    plt.grid(True)
    plt.show()

def executar_regressao_linear_simples():
    print("\n--- Regressão Linear Simples (MQM) ---")
    x_dados, y_dados = obter_dados_do_usuario()
    
    if not x_dados:
        return

    a0, a1 = regressao_linear_simples(x_dados, y_dados)
    
    y_predito = [a0 + a1 * x for x in x_dados]
    
    chi2, r2 = calcular_metricas_ajuste(y_dados, y_predito, len(x_dados), 1)

    plotar_regressao_linear(x_dados, y_dados, a0, a1) 

    print("\n--- Resultados do Ajuste (Y = a0 + a1*X) ---")
    print(f"  - Coeficiente Linear (a0): {a0:.4f}")
    print(f"  - Coeficiente Angular (a1): {a1:.4f}")
    print(f"  - Equação da Reta: Y = {a0:.4f} + {a1:.4f}*X")
    print(f"  - R² (Coef. de Determinação): {r2:.4f}")
    print(f"  - Chi² Reduzido (Qualidade do Ajuste): {chi2:.4f}")
    
    continuar = input("\nDeseja estimar valores com a reta? (s/n): ").lower()
    if continuar == 's':
        try:
            x_est_y = float(input("  [Estimar Y] Insira o ponto X para estimar Y: "))
            y_regressao = estimar_y(a0, a1, x_est_y)
            print(f"  - Valor Estimado Y em X={x_est_y:.4f}: Y = {y_regressao:.4f}")

            y_est_x = float(input("  [Estimar X] Insira o ponto Y para estimar X: "))
            x_regressao = estimar_x(a0, a1, y_est_x)
            print(f"  - Valor Estimado X em Y={y_est_x:.4f}: X = {x_regressao:.4f} (Inversa)")

        except ValueError as e:
            print(f"\n[ERRO NA ESTIMAÇÃO] {e}")


def executar_regressao_polinomial_quadratica():
    print("\n--- Regressão Polinomial (Parábola/MQM) ---")
    x_dados, y_dados = obter_dados_do_usuario()
    
    if not x_dados:
        return
    
    if len(x_dados) < 3:
        print("\n[ERRO] A Regressão Quadrática requer no mínimo 3 pontos. Você forneceu", len(x_dados))
        return

    try:
        a0, a1, a2 = regressao_polinomial_quadratica(x_dados, y_dados)
    except ValueError as e:
        print(f"\n[ERRO] Não foi possível resolver o sistema de equações: {e}")
        return
    
    y_predito = [a0 + a1 * x + a2 * (x ** 2) for x in x_dados]

    chi2, r2 = calcular_metricas_ajuste(y_dados, y_predito, len(x_dados), 2)

    print("\n--- Resultados do Ajuste (Y = a0 + a1*X + a2*X^2) ---")
    print(f"  - Coeficiente (a0): {a0:.4f}")
    print(f"  - Coeficiente (a1): {a1:.4f}")
    print(f"  - Coeficiente (a2): {a2:.4f}")
    print(f"  - Equação da Parábola: Y = {a0:.4f} + {a1:.4f}*X + {a2:.4f}*X^2")
    print(f"  - R² (Coef. de Determinação): {r2:.4f}")
    print(f"  - Chi² Reduzido (Qualidade do Ajuste): {chi2:.4f}")
    
    continuar = input("\nDeseja estimar um valor X com a parábola? (s/n): ").lower()
    if continuar == 's':
        try:
            x_estimado = float(input("  [Ponto] Insira o ponto X para estimar: "))
            y_regressao = a0 + a1 * x_estimado + a2 * (x_estimado ** 2)
            print(f"  - Valor Estimado em X={x_estimado:.4f}: Y = {y_regressao:.4f}")
        except ValueError:
            print("[ERRO] Ponto de estimação X inválido.")

def menu_principal():
    while True:
        
        print("\n--- Menu de Análise Numérica ---")
        print(" Escolha uma opção:")
        print("0. Diagrama de Dispersão (Visualização)")
        print("1. Interpolação Linear (Ordem 1)")
        print("2. Regressão Linear Simples (Reta/MQM)")
        print("3. Regressão Polinomial (Parábola/MQM)")
        print("4. Sair")
        
        escolha = input("Escolha uma opção (0, 1, 2, 3 ou 4): ").strip()
        
        if escolha == '0':
            executar_diagrama_dispersao()
        elif escolha == '1':
            executar_interpolacao_linear()
        elif escolha == '2':
            executar_regressao_linear_simples()
        elif escolha == '3':
            executar_regressao_polinomial_quadratica()
        elif escolha == '4':
            print("\nPrograma encerrado")
            break
        else:
            print("\nOpção inválida.")

if __name__ == "__main__":
    menu_principal()