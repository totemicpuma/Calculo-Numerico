# 📐 Algoritmos e Métodos de Cálculo Numérico em Python

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-Computa%C3%A7%C3%A3o%20Cient%C3%ADfica-013243?logo=numpy&logoColor=white)
![SymPy](https://img.shields.io/badge/SymPy-C%C3%A1lculo%20Simb%C3%B3lico-3B5526?logo=sympy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualiza%C3%A7%C3%A3o-11557c)

---

## 📌 Visão Geral

Este repositório reúne implementações completas e interativas dos principais **algoritmos clássicos de Cálculo Numérico e Computacional**, desenvolvidas em Python a partir dos fundamentos matemáticos (sem depender de *solvers* caixa-preta para a lógica matricial e iterativa).

O projeto utiliza **SymPy** para interpretação de expressões algébricas e diferenciação simbólica (cálculo automático de derivadas para Newton-Raphson e estimativa de erro de truncamento de ordem superior), **NumPy** para manipulação vetorial e **Matplotlib** para análise gráfica de convergência e ajuste de curvas.

---

## 🗂️ Catálogo de Métodos Implementados

### 🔹 Módulo 1 — Sistemas Lineares, Interpolação e Ajuste de Curvas (`codigos_A1/`)

| Arquivo | Métodos e Algoritmos Implementados | Destaques Técnicos |
| :--- | :--- | :--- |
| [**`base_conversao.py`**](./codigos_A1/base_conversao.py) | Conversão de Bases Numéricas (Base 2 até Base 36) | Conversão bidirecional generalizada ($B_1 \leftrightarrow \text{Decimal} \leftrightarrow B_2$) com validação posicional. |
| [**`met_gauss_normal.py`**](./codigos_A1/met_gauss_normal.py) | Eliminação de Gauss Clássica | Triangularização superior, substituição retroativa e cálculo do vetor resíduo $r = b - Ax$. |
| [**`met_gauss_parcial.py`**](./codigos_A1/met_gauss_parcial.py) | Eliminação de Gauss com Pivotação Parcial | Permutação de linhas pelo elemento de maior módulo na coluna para estabilidade numérica e mitigação de erros de arredondamento. |
| [**`decomposicao_LU.py`**](./codigos_A1/decomposicao_LU.py) | Fatoração $A = L \cdot U$ (Doolittle) | Resolução em duas etapas ($Ly = b$ e $Ux = y$) com verificação do vetor resíduo. |
| [**`LU_parcial.py`**](./codigos_A1/LU_parcial.py) | Fatoração $P \cdot A = L \cdot U$ com Pivotação Parcial | Rastreamento de vetor de permutação, cálculo de determinante ($\det(A)$) com ajuste de sinal e resolução pivotal. |
| [**`interpolacoes.py`**](./codigos_A1/interpolacoes.py) | **Lagrange**, **Diferenças Divididas de Newton** e **Gregory-Newton** | Construção explícita da tabela de diferenças divididas/finitas e síntese simbólica do polinômio interpolador $P_n(x)$. |
| [**`ajustes_curva.py`**](./codigos_A1/ajustes_curva.py) | Método dos Mínimos Quadrados (MMQ) | Regressão Polinomial de grau $m$, Exponencial ($y = a \cdot b^x$ e $y = a \cdot e^{bx}$) e Geométrica ($y = a \cdot x^b$), com cálculo de Coeficiente de Determinação ($R^2$), Qui-Quadrado Reduzido ($\chi^2_{\nu}$) e gráficos de dispersão. |

---

### 🔹 Módulo 2 — Zeros de Funções, Integração Numérica e EDOs (`codigos_A2/`)

| Arquivo | Métodos e Algoritmos Implementados | Destaques Técnicos |
| :--- | :--- | :--- |
| [**`metodosraiz.py`**](./codigos_A2/metodosraiz.py) | **Bisseção**, **Newton-Raphson** e **Secante** | Derivada simbólica automática via `SymPy`, plotagem gráfica do intervalo $[a, b]$ e benchmark comparativo automático de velocidade de convergência (número de iterações). |
| [**`integrais.py`**](./codigos_A2/integrais.py) | **1ª Regra de Simpson (1/3)**, **2ª Regra de Simpson (3/8)** e **Regra dos Trapézios** | Suporta tanto funções contínuas $f(x)$ quanto tabelas de pontos discretos $(x_i, y_i)$. Inclui ajuste automático de subintervalos ($n$ par ou múltiplo de 3) e **estimativa do limitante superior do erro de truncamento** via derivada de 4ª ordem ($f^{(4)}(\xi)$). |
| [**`integraisalt.py`**](./codigos_A2/integraisalt.py) | Integração Numérica Analítica Compacta | Versão enxuta para integração de funções contínuas via Simpson 1/3 e Simpson 3/8 com estimativa de erro. |
| [**`EDOS.py`**](./codigos_A2/EDOS.py) | **Euler Simples**, **Euler Melhorado (Heun / RK2)**, **Runge-Kutta de 4ª Ordem (RK4)** e **Sistemas de EDOs de 2ª Ordem** | Resolução de Problemas de Valor Inicial (PVI) de 1ª ordem ($y' = f(x, y)$) e redução de EDOs de 2ª ordem ($y'' = f(x, y, y')$) para sistemas acoplados. |

---

## 🧮 Formulações Matemáticas Destacadas

### 1. Estimativa de Erro na Integração de Simpson
Nos scripts [`integrais.py`](./codigos_A2/integrais.py) e [`integraisalt.py`](./codigos_A2/integraisalt.py), a derivada de 4ª ordem é obtida simbolicamente para limitar o erro de truncamento no intervalo $[a, b]$:

$$|E_{1/3}| \le \frac{(b - a) \cdot h^4}{180} \max_{\xi \in [a, b]} \left|f^{(4)}(\xi)\right|, \qquad |E_{3/8}| \le \frac{(b - a) \cdot h^4}{80} \max_{\xi \in [a, b]} \left|f^{(4)}(\xi)\right|$$

### 2. Runge-Kutta de 4ª Ordem (RK4) para EDOs
Implementado em [`EDOS.py`](./codigos_A2/EDOS.py):

$$y_{i+1} = y_i + \frac{h}{6}(k_1 + 2k_2 + 2k_3 + k_4)$$

---

## 🚀 Como Executar

### 1. Instalar as dependências
```bash
pip install -r requirements.txt
```

### 2. Executar qualquer módulo interativo
```bash
# Exemplo 1: Comparador de Raízes (Bisseção vs Newton-Raphson vs Secante)
python codigos_A2/metodosraiz.py

# Exemplo 2: Integração Numérica (Simpson 1/3, 3/8 e Trapézios)
python codigos_A2/integrais.py

# Exemplo 3: Equações Diferenciais Ordinárias (Euler, Heun e RK4)
python codigos_A2/EDOS.py

# Exemplo 4: Ajuste de Curvas por Mínimos Quadrados (R² e Qui-Quadrado)
python codigos_A1/ajustes_curva.py
```

---

## 👤 Autor

**Isaac Salles Gonçalves** (`@totemicpuma`)
- Instituto Federal Fluminense (IFF)
