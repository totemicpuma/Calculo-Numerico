def para_decimal(numero: str, base_origem: int) -> int:
    mapa_digitos = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    if not (2 <= base_origem <= 36):
        raise ValueError("A base de origem deve estar entre 2 e 36.")
        
    valor_decimal = 0
    
    for i, digito in enumerate(reversed(numero.upper())):
        valor_do_digito = mapa_digitos.index(digito)
        
        if valor_do_digito >= base_origem:
             raise ValueError(f"Dígito '{digito}' inválido para a base {base_origem}.")

        valor_decimal += valor_do_digito * (base_origem ** i)
        
    return valor_decimal

def de_decimal(numero_decimal: int, base_destino: int) -> str:
    mapa_digitos = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    if not (2 <= base_destino <= 36):
        raise ValueError("A base de destino deve estar entre 2 e 36.")

    if numero_decimal == 0:
        return "0"
    
    resultado = ""
    dividendo = numero_decimal
    
    while dividendo > 0:
        resto = dividendo % base_destino
        digito = mapa_digitos[resto]
        resultado = digito + resultado
        dividendo //= base_destino
        
    return resultado

def conversao_de_base():
    print("--- Conversor de Base Numérica (Base 2 a Base 36) ---")
    
    numero = input("Digite o número que deseja converter (ex: F, 1010, 3Z): ").strip()
    base_origem = int(input("Digite a base atual do número (ex: 16, 2, 36): "))
    base_destino = int(input("Digite a base para a qual deseja converter (ex: 10, 8, 30): "))

    valor_decimal = para_decimal(numero, base_origem)
    numero_convertido = de_decimal(valor_decimal, base_destino)
    
    print("\n--- Resultado ---")
    print(f"O número {numero} na base {base_origem} é igual a:")
    print(f"{numero_convertido} na base {base_destino}.")

if __name__ == "__main__":
    conversao_de_base()