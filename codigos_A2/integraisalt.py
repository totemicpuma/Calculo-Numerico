import math

def f_usuario(funcao_str, x):
    contexto_matematico = {
        "x": x,
        "sin": math.sin, "cos": math.cos, "tan": math.tan,
        "exp": math.exp, "log": math.log, "sqrt": math.sqrt,
        "pi": math.pi, "e": math.e
    }
    return eval(funcao_str, {"__builtins__": None}, contexto_matematico)

def resolver_simpson_13():
    print("\n--- Método de Simpson 1/3 ---")
    funcao = input("Digite a função f(x) (ex: cos(x), x**2 + 1): ")
    a = float(input("Limite inferior (a): "))
    b = float(input("Limite superior (b): "))
    n = int(input("Número de subintervalos (n) [deve ser PAR]: "))

    if n % 2 != 0:
        print("ERRO: Para Simpson 1/3, 'n' DEVE ser par!")
        return

    h = (b - a) / n
    soma = f_usuario(funcao, a) + f_usuario(funcao, b)

    print(f"\nProcessando com h = {h}...")
    
    for i in range(1, n):
        x = a + i * h
        if i % 2 == 0:
            soma += 2 * f_usuario(funcao, x)
        else:
            soma += 4 * f_usuario(funcao, x)

    resultado = (h / 3) * soma
    print(f"\n>>> RESULTADO FINAL (Simpson 1/3): {resultado:.6f}")

def resolver_simpson_38():
    print("\n--- Método de Simpson 3/8 ---")
    funcao = input("Digite a função f(x) (ex: x**2 + x): ")
    a = float(input("Limite inferior (a): "))
    b = float(input("Limite superior (b): "))
    n = int(input("Número de subintervalos (n) [múltiplo de 3]: "))

    if n % 3 != 0:
        print("ERRO: Para Simpson 3/8, 'n' DEVE ser múltiplo de 3!")
        return

    h = (b - a) / n
    soma = f_usuario(funcao, a) + f_usuario(funcao, b)
    
    print(f"\nProcessando com h = {h}...")

    for i in range(1, n):
        x = a + i * h
        if i % 3 == 0:
            soma += 2 * f_usuario(funcao, x)
        else:
            soma += 3 * f_usuario(funcao, x)

    resultado = (3 * h / 8) * soma
    print(f"\n>>> RESULTADO FINAL (Simpson 3/8): {resultado:.6f}")

def trapezio_simples():
    print("\n--- Método do Trapézio (Dados Discretos/Tabela) ---")
    entrada_y = input("Digite as alturas/profundidades separadas por vírgula: ")
    y_valores = [float(num) for num in entrada_y.replace(" ", "").split(",")]
    h = float(input("Digite o passo (h) entre os pontos: "))
    
    soma = y_valores[0] + y_valores[-1]
    for i in range(1, len(y_valores) - 1):
        soma += 2 * y_valores[i]
        
    area = (h / 2) * soma
    print(f"\n>>> RESULTADO FINAL (Área Aproximada): {area:.6f}")

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
    main()