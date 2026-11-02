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

def decomposicao_LU(A):
    
    n = len(A)
    L = [[0.0] * n for _ in range(n)]
    U = [[0.0] * n for _ in range(n)]

    for i in range(n):
        L[i][i] = 1.0  # L é uma matriz unitária na diagonal com o valor 1

    # Processo de Eliminação para encontrar L e U
    for j in range(n):
        # Elementos de U (linha j)
        for i in range(j, n):
            soma = sum(L[j][k] * U[k][i] for k in range(j))
            U[j][i] = A[j][i] - soma
        
        # Elementos de L (coluna j)
        for i in range(j + 1, n):
            soma = sum(L[i][k] * U[k][j] for k in range(j))
            if U[j][j] == 0:
                return None, None
            #calculador ocomo o multiplicadorm representando os fatores que iriam A[i][j]
            L[i][j] = (A[i][j] - soma) / U[j][j]
            
    return L, U

def resolver_sistema_triangular_inferior(L, b):

    n = len(L)
    y = [0.0] * n #cria um vetor y de zeros, com  mesmo de elementos de linhas da matriz L
    
    for i in range(n): #pecorre a matriz da primeira linha até a ultima
        soma = sum(L[i][j] * y[j] for j in range(i))
        y[i] = (b[i] - soma) / L[i][i]
    return y

def resolver_sistema_triangular_superior(U, y):

    n = len(U)
    x = [0.0] * n #mesmo exemplo da y
    
    for i in range(n - 1, -1, -1):
        soma = sum(U[i][j] * x[j] for j in range(i + 1, n))
        if U[i][i] == 0:
            return None # Evita divisão por zero
        x[i] = (y[i] - soma) / U[i][i]
    return x

def resolver_por_decomposicao_LU(A, b):
  
    L, U = decomposicao_LU(A)
    
    if L is None:
        return "Erro: A decomposição LU falhou (pivô zero)."

    # Passo 1: Resolver Ly = b
    y = resolver_sistema_triangular_inferior(L, b)
    
    # Passo 2: Resolver Ux = y
    x = resolver_sistema_triangular_superior(U, y)
    
    if x is None:
      return "Erro: A substituição retroativa falhou (pivô zero)."
      
    return x

def calcular_residuo_vetor(A, x, b):

    n = len(A)

    produto_Ax = [0.0] * n
    
    for i in range(n):
        soma_produto = 0
        for j in range(n):
            soma_produto += A[i][j] * x[j]
        produto_Ax[i] = soma_produto

    # Calcula o vetor resíduo r = b - Ax
    residuo = [0.0] * n
    for i in range(n):
        residuo[i] = b[i] - produto_Ax[i]
        
    return residuo

if __name__ == "__main__":
    try:
        ordem = int(input("Informe a ordem do sistema (o número de equações): "))

        if ordem <= 0:
            print("A ordem do sistema deve ser um número inteiro positivo.")
        else:
            # A função gerar_matriz_aumentada cria a matriz A com o vetor b na última coluna
            matriz_aumentada_completa = gerar_matriz_aumentada(ordem)
            
            # Separa a matriz A do vetor b
            A_matriz = [row[:ordem] for row in matriz_aumentada_completa]
            b_vetor = [row[ordem] for row in matriz_aumentada_completa]
            
            print("\nMatriz A:")
            for linha in A_matriz:
                print(linha)
            
            print("\nVetor b:")
            print(b_vetor)
            
            solucao = resolver_por_decomposicao_LU(A_matriz, b_vetor)
            residuo_vetor = calcular_residuo_vetor(A_matriz, solucao, b_vetor)
            print("\n---")
            if isinstance(solucao, str):
                print(solucao)
            else:
                L_result, U_result = decomposicao_LU(A_matriz)
                print("\nMatriz L:")
                for linha in L_result:
                    print([f"{valor:.4f}" for valor in linha])
                print("\nMatriz U:")
                for linha in U_result:
                    print([f"{valor:.4f}" for valor in linha])
                
                print("\nSolução do sistema x:")
                print([f"x{i+1} = {valor:.4f}" for i, valor in enumerate(solucao)])

                print("\nResíduo (b - Ax):")
                print([f"{valor:.4f}" for valor in residuo_vetor])

    except ValueError:
        print("Entrada inválida. Por favor, digite números válidos.")