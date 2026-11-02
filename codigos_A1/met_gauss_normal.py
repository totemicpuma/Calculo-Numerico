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

def resolver_gauss(matriz_aumentada):
    n = len(matriz_aumentada)
    for i in range(n):
        if matriz_aumentada[i][i] == 0:
            return "O pivô é zero. O método de Gauss falhou sem pivotação."
        for k in range(i + 1, n):
            fator = matriz_aumentada[k][i] / matriz_aumentada[i][i]
            for j in range(i, n + 1):
                matriz_aumentada[k][j] -= fator * matriz_aumentada[i][j]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        soma = 0
        for j in range(i + 1, n):
            soma += matriz_aumentada[i][j] * x[j]
        x[i] = (matriz_aumentada[i][n] - soma) / matriz_aumentada[i][i]
    return x

def calcular_residuo_vetor(A, x, b):
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

if __name__ == "__main__":
    try:
        ordem = int(input("Informe a ordem do sistema (o número de equações): "))
        if ordem <= 0:
            print("A ordem do sistema deve ser um número inteiro positivo.")
        else:
            matriz_aumentada_completa = gerar_matriz_aumentada(ordem)
            
            # Matriz A original e vetor b original
            A_original = [row[:ordem] for row in matriz_aumentada_completa]
            b_original = [row[ordem] for row in matriz_aumentada_completa]

            # Criando uma cópia da matriz aumentada para o método de Gauss,
            # pois ele a modifica no local.
            matriz_para_gauss = [row[:] for row in matriz_aumentada_completa]
            
            print("\nMatriz aumentada do sistema:")
            for linha in matriz_aumentada_completa:
                print(linha)
            
            solucao = resolver_gauss(matriz_para_gauss)
            
            print("\n---")
            if isinstance(solucao, list):
                print("Solução do sistema:")
                for i, valor in enumerate(solucao):
                    print(f"x{i+1} = {valor:.4f}")
                
                # Chamada da função para calcular o resíduo
                residuo_vetor = calcular_residuo_vetor(A_original, solucao, b_original)
                print("\nResíduo (b - Ax):")
                print([f"{valor:.4f}" for valor in residuo_vetor])
                
            else:
                print(f"Erro: {solucao}")
    except ValueError:
        print("Entrada inválida. Por favor, digite números válidos.")