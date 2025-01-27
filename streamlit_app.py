import streamlit as st
import datetime
import plotly.graph_objects as go

# Função para exibir resultados com cores
def resultado_com_cor(valor, texto):
    if valor == "bom":
        st.markdown(f"<p style='color:green; font-size: 20px; font-weight: bold;'>{texto}</p>", unsafe_allow_html=True)
    elif valor == "mediano":
        st.markdown(f"<p style='color:orange; font-size: 20px; font-weight: bold;'>{texto}</p>", unsafe_allow_html=True)
    elif valor == "ruim":
        st.markdown(f"<p style='color:red; font-size: 20px; font-weight: bold;'>{texto}</p>", unsafe_allow_html=True)

# Função para classificar o IMC
def classificar_imc(imc):
    if imc < 18.5:
        return "Abaixo do peso", "ruim"
    elif 18.5 <= imc < 24.9:
        return "Peso normal", "bom"
    elif 25 <= imc < 29.9:
        return "Sobrepeso", "mediano"
    elif 30 <= imc < 34.9:
        return "Obesidade I", "ruim"
    elif 35 <= imc < 39.9:
        return "Obesidade II (severa)", "ruim"
    else:
        return "Obesidade III (mórbida)", "ruim"

# Função para gráfico de barras de desempenho
def grafico_resultados(dados):
    fig = go.Figure()

    # Definindo os testes
    testes = ['Sentar e Levantar', 'Condicionamento Aeróbio', 'Flexibilidade']
    resultados = [
        'bom' if dados["qntd_rept"] >= 15 else 'mediano' if 10 <= dados["qntd_rept"] < 15 else 'ruim',
        'bom' if dados["distancia"] >= 100 else 'mediano' if 50 <= dados["distancia"] < 100 else 'ruim',
        'bom' if dados["flexibilidade"] >= 5 else 'mediano' if 0 <= dados["flexibilidade"] < 5 else 'ruim'
    ]

    # Definindo as cores
    cores = ['green', 'orange', 'red']

    # Adicionando as barras ao gráfico
    for i, resultado in enumerate(resultados):
        fig.add_trace(go.Bar(
            x=[testes[i]],
            y=[1],
            marker_color=cores[['bom', 'mediano', 'ruim'].index(resultado)],
            name=f'{testes[i]}: {resultado.capitalize()}'
        ))

    # Configurando o layout do gráfico
    fig.update_layout(
        title="Resultados dos Testes",
        xaxis_title="Teste",
        yaxis_title="Resultado",
        showlegend=True,
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color="white"),
        height=400
    )

    # Exibindo o gráfico
    st.plotly_chart(fig)

# Página 1
def page1():
    st.title("Protocolo de Avaliação")
    st.header('Dados do Aluno')

    # Entrada de dados do aluno
    nome = st.text_input("NOME COMPLETO")
    idade = st.slider("SELECIONE A IDADE", 0, 94)
    peso = st.slider("SELECIONE O PESO", 0, 200)
    altura = st.number_input("ALTURA DO ALUNO EM METROS, EX: 1.75", format="%.2f")
    sexo = st.selectbox("Qual é o seu sexo?", ['MASCULINO', 'FEMININO'])
    data_nascimento = st.text_input("DATA DE NASCIMENTO DO ALUNO, EX: DD/MM/AAAA")

    # Cálculo do IMC
    imc = peso / (altura ** 2) if altura > 0 else None
    if imc:
        st.write(f"O IMC do aluno é: {imc:.2f}")
    else:
        st.error("A altura deve ser maior que zero para calcular o IMC")

    # Teste de sentar e levantar
    st.header('Testes Físicos')
    st.subheader('Teste de sentar e levantar')
    qntd_rept = st.number_input('Quantas repetições você fez?', min_value=0, step=1, format="%d")

    # Teste de condicionamento aeróbio
    st.subheader("Teste de Condicionamento Aeróbio")
    distancia = st.number_input("Digite a distância percorrida pelo aluno (em metros)", min_value=0.0, format="%.2f")

    # Teste de flexibilidade
    st.subheader("Teste de Flexibilidade")
    flexibilidade = st.number_input("Digite o alcance do aluno (em cm)", format="%.2f")

    # Botão para enviar dados para a página 2
    if st.button("Clique aqui para enviar"):
        st.session_state["dados"] = {
            "nome": nome,
            "idade": idade,
            "peso": peso,
            "altura": altura,
            "sexo": sexo,
            "imc": imc,
            "qntd_rept": qntd_rept,
            "distancia": distancia,
            "flexibilidade": flexibilidade,
            "data_nascimento": data_nascimento,  # Adicionado o campo de data de nascimento
        }
        st.success("Dados enviados para a segunda página!")

# Página 2
def page2():
    if "dados" not in st.session_state or not st.session_state["dados"]:
        st.warning("Nenhum dado disponível. Preencha a página 1 primeiro.")
        return

    dados = st.session_state["dados"]

    # Título da página 2
    st.title("Perfil do Aluno")

    # Dividindo a página em duas colunas
    col1, col2 = st.columns([1, 2])

    with col1:
        st.image("https://www.pngitem.com/pimgs/m/52-522046_user-profile-icon-png-user-profile-icon-vector.png", width=150)
        st.subheader(f"Nome: {dados['nome']}")
        st.text(f"Idade: {dados['idade']} anos")
        st.text(f"Sexo: {dados['sexo']}")

    with col2:
        st.subheader(f"Data de Nascimento: {dados['data_nascimento']}")
        st.text(f"Peso: {dados['peso']} kg")
        st.text(f"Altura: {dados['altura']} metros")
        
        # Classificação do IMC
        if dados["imc"]:
            imc_classificacao, cor = classificar_imc(dados["imc"])
            resultado_com_cor(cor, f"IMC: {dados['imc']:.2f} - {imc_classificacao}")
        
        st.text(f"Teste de Sentar e Levantar: {dados['qntd_rept']} repetições")
        st.text(f"Distância Percorrida: {dados['distancia']} metros")
        st.text(f"Alcance de Flexibilidade: {dados['flexibilidade']} cm")

        st.header("Resultados dos Testes")
        # Exibindo o gráfico de barras
        grafico_resultados(dados)

        # Avaliação do teste de sentar e levantar
        if dados["qntd_rept"] >= 15:
            resultado_com_cor("bom", "Teste de Sentar e Levantar: Resultado Bom")
        elif 10 <= dados["qntd_rept"] < 15:
            resultado_com_cor("mediano", "Teste de Sentar e Levantar: Resultado Mediano")
        else:
            resultado_com_cor("ruim", "Teste de Sentar e Levantar: Resultado Ruim")

        # Avaliação do teste de condicionamento aeróbio
        if dados["distancia"] >= 100:
            resultado_com_cor("bom", "Teste de Condicionamento Aeróbio: Resultado Bom")
        elif 50 <= dados["distancia"] < 100:
            resultado_com_cor("mediano", "Teste de Condicionamento Aeróbio: Resultado Mediano")
        else:
            resultado_com_cor("ruim", "Teste de Condicionamento Aeróbio: Resultado Ruim")

        # Avaliação do teste de flexibilidade
        if dados["flexibilidade"] >= 5:
            resultado_com_cor("bom", "Teste de Flexibilidade: Resultado Bom")
        elif 0 <= dados["flexibilidade"] < 5:
            resultado_com_cor("mediano", "Teste de Flexibilidade: Resultado Mediano")
        else:
            resultado_com_cor("ruim", "Teste de Flexibilidade: Resultado Ruim")

# Configuração do menu na barra lateral
st.sidebar.title("Menu")
selected_page = st.sidebar.radio("Selecione a página", ["Protocolo de Avaliação", "Perfil do Aluno"])

# Controle de navegação
if selected_page == "Protocolo de Avaliação":
    page1()
elif selected_page == "Perfil do Aluno":
    page2()
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
