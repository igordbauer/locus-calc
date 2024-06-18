import numpy as np
import plotly.graph_objects as go
import cmath
import re


def criar_funcao_equacao():
    """
    Cria uma função a partir da equação complexa fornecida pelo usuário.
    """
    # Recebe a equação complexa do usuário
    equacao = input(
        "Digite a equação complexa (e.g., I = 28.284+28.284j/(j + 1 - j*X)): "
    )

    # Extraímos o lado direito da equação
    lados = equacao.split("=")
    if len(lados) != 2:
        raise ValueError(
            "Formato de equação inválido. Certifique-se de que há um sinal de igualdade."
        )

    lado_direito = lados[1].strip()

    # Extrai a variável da equação
    variavel = re.findall(r"\b[A-Za-z]\b", lado_direito)
    variavel = [v for v in variavel if v not in ["i", "j"]]
    if len(variavel) != 1:
        raise ValueError("A equação deve conter exatamente uma variável.")
    variavel = variavel[0]

    # Definindo a função usando eval() e lambda
    funcao = lambda C: eval(
        lado_direito,
        {"__builtins__": None, "cmath": cmath, "np": np},
        {variavel: C, "j": 1j, "i": 1j},
    )

    return funcao, variavel, equacao


def plot_locus_complex(func, variavel, equacao, var_min, var_max, num_points=1000):
    """
    Plota o Lócus da Função Complexa (parte real versus parte imaginária).

    Args:
    - func: Função a ser plotada. Deve aceitar um array numpy como entrada.
    - variavel: Nome da variável usada na função.
    - equacao: Equação complexa fornecida pelo usuário.
    - var_min: Valor mínimo da variável.
    - var_max: Valor máximo da variável.
    - num_points: Número de pontos para interpolação (default é 1000).
    """
    var_values = np.logspace(var_min, var_max, num=num_points)
    try:
        y_values = [func(C) for C in var_values]
    except Exception as e:
        raise ValueError(f"A função fornecida não pôde ser avaliada: {e}")

    V_real = [V.real for V in y_values]
    V_imag = [V.imag for V in y_values]

    fig1 = go.Figure()

    # Plotando o Lócus da Função Complexa (parte real versus parte imaginária)
    fig1.add_trace(
        go.Scatter(
            x=V_real,
            y=V_imag,
            mode="lines",
            name="Lócus da Função Complexa",
            hoverinfo="text",
            text=[f"{variavel}={C:.3f}" for C in var_values],
            hovertemplate="Real=%{x:.2f}<br>Imag=%{y:.2f}<extra>%{text}</extra>",
        )
    )

    fig1.update_layout(
        title=f"Lócus da Função Complexa: {equacao}",
        xaxis_title="Parte Real",
        yaxis_title="Parte Imaginária",
        hovermode="closest",
    )

    fig1.show()


def plot_variavel_complex(func, variavel, equacao, var_min, var_max, num_points=1000):
    """
    Plota a variável da esquerda (parte real e imaginária) versus a variável da direita.

    Args:
    - func: Função a ser plotada. Deve aceitar um array numpy como entrada.
    - variavel: Nome da variável usada na função.
    - equacao: Equação complexa fornecida pelo usuário.
    - var_min: Valor mínimo da variável.
    - var_max: Valor máximo da variável.
    - num_points: Número de pontos para interpolação (default é 1000).
    """
    var_values = np.logspace(var_min, var_max, num=num_points)
    try:
        y_values = [func(C) for C in var_values]
    except Exception as e:
        raise ValueError(f"A função fornecida não pôde ser avaliada: {e}")

    V_real = [V.real for V in y_values]
    V_imag = [V.imag for V in y_values]

    fig2 = go.Figure()

    # Plotando a parte real da variável da esquerda versus a variável da direita
    fig2.add_trace(
        go.Scatter(
            x=var_values,
            y=V_real,
            mode="lines",
            name=f"Real({variavel})",
            hoverinfo="text",
            text=[f"{variavel}={C:.3f}" for C in var_values],
            hovertemplate=f"{variavel}=%{{text}}<br>Real=%{{y:.2f}}",
        )
    )

    # Plotando a parte imaginária da variável da esquerda versus a variável da direita
    fig2.add_trace(
        go.Scatter(
            x=var_values,
            y=V_imag,
            mode="lines",
            name=f"Imag({variavel})",
            hoverinfo="text",
            text=[f"{variavel}={C:.3f}" for C in var_values],
            hovertemplate=f"{variavel}=%{{text}}<br>Imag=%{{y:.2f}}",
        )
    )

    fig2.update_layout(
        title=f"Eixo Y vs. {variavel}",
        xaxis_title=f"{variavel}",
        yaxis_title="Eixo Y",
        hovermode="closest",
    )

    fig2.show()


if __name__ == "__main__":
    # Criando a função a partir da equação complexa fornecida pelo usuário
    minha_funcao, variavel, equacao = criar_funcao_equacao()

    if minha_funcao:
        # Plotando o Lócus da Função Complexa
        plot_locus_complex(minha_funcao, variavel, equacao, -4, 4)

        # Plotando a variável da esquerda versus a variável da direita
        plot_variavel_complex(minha_funcao, variavel, equacao, -4, 4)
