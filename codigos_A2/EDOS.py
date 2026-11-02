import math
import sympy as sp

def ler_funcao_1a_ordem():
    print("\n--- EDO 1a Ordem (y') ---")
    f_str = input("Função f(x, y): ")
    try:
        x, y = sp.symbols('x y')
        expr = sp.sympify(f_str)
        return sp.lambdify((x, y), expr, "math"), f_str
    except:
        return None, None

def ler_funcao_2a_ordem():
    print("\n--- EDO 2a Ordem (y'') ---")
    print("Use 'z' para y'. Ex: y''+y=0 -> digite: -y")
    f_str = input("Função f(x, y, z): ")
    try:
        x, y, z = sp.symbols('x y z')
        expr = sp.sympify(f_str)
        return sp.lambdify((x, y, z), expr, "math"), f_str
    except:
        return None, None

def ler_params(ordem=1):
    try:
        x0 = float(input("x0: "))
        y0 = float(input("y0: "))
        z0 = 0.0
        if ordem == 2:
            z0 = float(input("y'(0) [z0]: "))
        h = float(input("Passo h: "))
        xf = float(input("x final: "))
        return x0, y0, z0, h, xf
    except:
        return None

def euler_simples():
    f, f_str = ler_funcao_1a_ordem()
    if not f: return
    vals = ler_params(1)
    if not vals: return
    x, y, _, h, xf = vals

    print(f"\nResolvendo: y' = {f_str}")
    print(f"{'x':<8} | {'y':<15}")
    print("-" * 25)

    while x <= xf + 1e-9:
        print(f"{x:<8.4f} | {y:<15.6f}")
        y += h * f(x, y)
        x += h

def euler_melhorado():
    f, f_str = ler_funcao_1a_ordem()
    if not f: return
    vals = ler_params(1)
    if not vals: return
    x, y, _, h, xf = vals

    print(f"\nResolvendo: y' = {f_str}")
    print(f"{'x':<8} | {'y':<15}")
    print("-" * 25)

    while x <= xf + 1e-9:
        print(f"{x:<8.4f} | {y:<15.6f}")
        k1 = f(x, y)
        k2 = f(x + h, y + h * k1)
        y += (h / 2) * (k1 + k2)
        x += h

def rk4():
    f, f_str = ler_funcao_1a_ordem()
    if not f: return
    vals = ler_params(1)
    if not vals: return
    x, y, _, h, xf = vals

    print(f"\nResolvendo: y' = {f_str}")
    print(f"{'x':<8} | {'y':<15}")
    print("-" * 25)

    while x <= xf + 1e-9:
        print(f"{x:<8.4f} | {y:<15.6f}")
        k1 = f(x, y)
        k2 = f(x + h/2, y + h/2 * k1)
        k3 = f(x + h/2, y + h/2 * k2)
        k4 = f(x + h, y + h * k3)
        y += (h / 6) * (k1 + 2*k2 + 2*k3 + k4)
        x += h

def euler_2a_ordem_sistema():
    f, f_str = ler_funcao_2a_ordem()
    if not f: return
    vals = ler_params(2)
    if not vals: return
    x, y, z, h, xf = vals

    print(f"\nResolvendo: y'' = {f_str}")
    print(f"{'x':<8} | {'y':<15} | {'z':<15}")
    print("-" * 42)

    while x <= xf + 1e-9:
        print(f"{x:<8.4f} | {y:<15.6f} | {z:<15.6f}")
        y_old, z_old = y, z
        y += h * z_old
        z += h * f(x, y_old, z_old)
        x += h

def main():
    while True:
        print("\n=== CÁLCULO NUMÉRICO: EDOs ===")
        print("1. Euler Simples (1a Ordem)")
        print("2. Euler Melhorado (1a Ordem)")
        print("3. RK4 (1a Ordem)")
        print("4. Euler (2a Ordem - Sistema)")
        print("0. Sair")
        
        op = input("Opção: ")
        if op == '1': euler_simples()
        elif op == '2': euler_melhorado()
        elif op == '3': rk4()
        elif op == '4': euler_2a_ordem_sistema()
        elif op == '0': break

if __name__ == "__main__":
    main()