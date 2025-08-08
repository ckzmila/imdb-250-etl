import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Função para converter duração
def converter_duracao(valor):
    try:
        valor = valor.lower().replace(" ", "")
        if "min" in valor:
            return int(valor.replace("min", ""))
    except:
        return None
    return None

# Carregar dados
df = pd.read_csv("imdb_top_250.csv")
df["Duracao_min"] = df["Duration"].apply(converter_duracao)
df["Decada"] = (df["Year"] // 10) * 10

# Configuração do Streamlit
st.set_page_config(page_title="IMDb Top 250", layout="wide")
st.title("🎬 Dashboard Interativo - IMDb Top 250")

# Filtros na barra lateral
st.sidebar.header("Filtros")

# Filtro de gênero
todos_generos = sorted({g.strip() for sublist in df["Genre"].dropna().str.split(",") for g in sublist})
genero_escolhido = st.sidebar.multiselect("Selecione o(s) gênero(s):", todos_generos)

# Filtro de ano
min_ano = int(df["Year"].min())
max_ano = int(df["Year"].max())
ano_range = st.sidebar.slider("Selecione o intervalo de anos:", min_ano, max_ano, (min_ano, max_ano))

# Aplicar filtros
df_filtrado = df.copy()
if genero_escolhido:
    df_filtrado = df_filtrado[df_filtrado["Genre"].apply(lambda x: any(g in x for g in genero_escolhido))]
df_filtrado = df_filtrado[(df_filtrado["Year"] >= ano_range[0]) & (df_filtrado["Year"] <= ano_range[1])]

# Menu lateral
menu = st.sidebar.selectbox(
    "Escolha o indicador:",
    [
        "Visão geral",
        "Top 10 filmes mais bem avaliados",
        "Top 5 filmes mais longos",
        "Média de nota por década",
        "Top 5 filmes com mais avaliações"
    ]
)

# Visão geral dos filmes
if menu == "Visão geral":
    st.subheader("📊 Estatísticas gerais (com filtros aplicados)")
    st.dataframe(df_filtrado.head(10))
    st.write(df_filtrado.describe())

# Top 10: melhores filmes
elif menu == "Top 10 filmes mais bem avaliados":
    top10 = df_filtrado.sort_values(by="IMDB rating", ascending=False).head(10)
    st.subheader("🏆 Top 10 filmes mais bem avaliados")
    st.dataframe(top10[["Title", "Year", "IMDB rating", "Rating count"]])

    fig, ax = plt.subplots()
    ax.barh(top10["Title"], top10["IMDB rating"], color="gold")
    ax.invert_yaxis()
    ax.set_xlabel("Nota IMDb")
    st.pyplot(fig)

# Top 5: filmes mais longos
elif menu == "Top 5 filmes mais longos":
    longos = df_filtrado.dropna(subset=["Duracao_min"]).sort_values(by="Duracao_min", ascending=False).head(5)
    st.subheader("⏳ Top 5 filmes mais longos")
    st.dataframe(longos[["Title", "Duracao_min"]])

    fig, ax = plt.subplots()
    ax.barh(longos["Title"], longos["Duracao_min"], color="skyblue")
    ax.invert_yaxis()
    ax.set_xlabel("Duração (min)")
    st.pyplot(fig)

# ----------------------------
# MÉDIA DE NOTA POR DÉCADA
# -----------
