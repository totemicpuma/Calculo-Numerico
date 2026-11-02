def gerar_matriz_aumentada(n):
    
    print(f"\nDigite os valores para a matriz dos coeficientes (A) e o vetor de termos independentes (b).")
    matriz_aumentada = []
    for i in range(n):
        linha = []
        for j in range(n + 1):
            if j < n:
                valor = float(input(f"Digite o valor para a posição A[{i}][{j}]: "))
            else:
                valor = float(input(f"Digite o valor para o termo independente b[{i}]: "))
            linha.append(valor)
        matriz_aumentada.append(linha)
    return matriz_aumentada

def decomposicao_LU_parcial(A):

    n = len(A)
    pivot = list(range(n))
    det = 1.0

    for j in range(n):
        pivo_idx = j
        max_val = abs(A[j][j])
        for i in range(j + 1, n):
            if abs(A[i][j]) > max_val:
                max_val = abs(A[i][j])
                pivo_idx = i

        if pivo_idx != j:
            A[j], A[pivo_idx] = A[pivo_idx], A[j]
            pivot[j], pivot[pivo_idx] = pivot[pivo_idx], pivot[j]
            det *= -1

        if A[j][j] == 0:
            return A, pivot, 0.0

        det *= A[j][j]
        fator = 1.0 / A[j][j]
        
        for i in range(j + 1, n):
            multiplicador = A[i][j] * fator
            A[i][j] = multiplicador
            
            for k in range(j + 1, n):
                A[i][k] -= multiplicador * A[j][k]
    
    return A, pivot, det

def resolver_sistema_triangular_inferior_pivotal(L, b, pivot):

    n = len(L)
    y = [0.0] * n
    
    b_p = [b[p] for p in pivot]

    y[0] = b_p[0]

    for i in range(1, n):
        soma = sum(L[i][j] * y[j] for j in range(i))
        y[i] = b_p[i] - soma
        
    return y

def resolver_sistema_triangular_superior_pivotal(U, y):
    n = len(U)
    x = [0.0] * n
    
    for i in range(n - 1, -1, -1):
        soma = sum(U[i][j] * x[j] for j in range(i + 1, n))
        if U[i][i] == 0:
            raise ValueError("Divisão por zero. Matriz singular.")
        x[i] = (y[i] - soma) / U[i][i]
    return x

def calcular_residuo_vetor(A, x, b):
    """
    Calcula o vetor resíduo r = b - Ax.
    """
    n = len(A)
    produto_Ax = [0.0] * n
    
    for i in range(n):
        soma_produto = 0
        for j in range(n):
            soma_produto += A[i][j] * x[j]
        produto_Ax[i] = soma_produto

    residuo = [0.0] * n
    for i in range(n):
        residuo[i] = b[i] - produto_Ax[i]
        
    return residuo

def resolver_por_decomposicao_LU_parcial_completo(A, b):
    # CRIA UMA CÓPIA DO A PARA A DECOMPOSIÇÃO
    A_copia = [row[:] for row in A]
    
    A_modificada, pivot, det = decomposicao_LU_parcial(A_copia)
    
    if det == 0:
        return None, None, None, f"Erro: A matriz é singular. Determinante = {det:.4f}"

    n = len(A)
    L_fator = [[0.0] * n for _ in range(n)]
    U_fator = [[0.0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            if i == j:
                L_fator[i][j] = 1.0
                U_fator[i][j] = A_modificada[i][j]
            elif i > j:
                L_fator[i][j] = A_modificada[i][j]
            else:
                U_fator[i][j] = A_modificada[i][j]

    y = resolver_sistema_triangular_inferior_pivotal(L_fator, b, pivot)
    
    try:
        x = resolver_sistema_triangular_superior_pivotal(U_fator, y)
    except ValueError as e:
        return L_fator, U_fator, pivot, f"Erro na substituição retroativa: {e}"
    
    # Retorna os fatores L, U, o vetor de pivôs, o determinante E a solução x
    return L_fator, U_fator, pivot, det, x

if __name__ == "__main__":
    try:
        ordem = int(input("Informe a ordem do sistema (o número de equações): "))

        if ordem <= 0:
            print("A ordem do sistema deve ser um número inteiro positivo.")
        else:
            matriz_aumentada_completa = gerar_matriz_aumentada(ordem)
            
            # 1. Separa a matriz A original e o vetor b original (sem alterá-los)
            A_original = [row[:ordem] for row in matriz_aumentada_completa]
            b_original = [row[ordem] for row in matriz_aumentada_completa]
            
            print("\nMatriz A original:")
            for linha in A_original:
                print(linha)
            
            print("\nVetor b original:")
            print(b_original)
            
            # Chama a função de resolução, que retorna a solução 'solucao' (vetor x)
            L_result, U_result, pivot, det, solucao = resolver_por_decomposicao_LU_parcial_completo(A_original, b_original)

            print("\n---")
            if isinstance(solucao, str):
                # Se solucao for string, significa que houve um erro retornado
                print(solucao)
            else:
                print("Decomposição LU com pivotação parcial concluída.")
                
                print("\nMatriz L:")
                for linha in L_result:
                    print([f"{val:.4f}" for val in linha])
                
                print("\nMatriz U:")
                for linha in U_result:
                    print([f"{val:.4f}" for val in linha])
                
                print("\nSolução do sistema x:")
                print([f"x{i+1} = {val:.4f}" for i, val in enumerate(solucao)])

                # 2. Calcula e exibe o resíduo usando A_original, b_original e a solucao
                residuo_vetor = calcular_residuo_vetor(A_original, solucao, b_original)
                print("\nResíduo (b - Ax):")
                print([f"{val:.4f}" for val in residuo_vetor])
                
    except ValueError:
        print("Entrada inválida. Por favor, digite números válidos.")