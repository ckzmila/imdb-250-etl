import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Ler csv
df = pd.read_csv("imdb_top_250.csv")

# Conversão da duração dos filmes
def converter_duracao(valor):
    try:
        valor = valor.lower().replace(" ", "")
        if "h" in valor:
            partes = valor.split("h")
            horas = int(partes[0])
            minutos = int(partes[1].replace("min", "")) if "min" in partes[1] else 0
            return horas * 60 + minutos
        else:
            return int(valor.replace("min", ""))
    except:
        return None

df["Duracao_min"] = df["Duration"].apply(converter_duracao)

# Criação de coluna "Década"
df["Decada"] = (df["Year"] // 10) * 10

# Análises
def top_10_filmes():
    print("\n🎬 Top 10 filmes mais bem avaliados:")
    print(df.sort_values(by="IMDB rating", ascending=False).head(10)[["Title", "Year", "IMDB rating", "Rating count"]])

def estatisticas_duracao():
    print("\n📏 Estatísticas da duração (em minutos):")
    print(df["Duracao_min"].describe())
    print("\n⏳ Top 5 filmes mais longos:")
    print(df.sort_values(by="Duracao_min", ascending=False).head(5)[["Title", "Duracao_min"]])

def media_por_decada():
    print("\n📅 Média de nota por década:")
    media_decada = df.groupby("Decada")["IMDB rating"].mean()
    print(media_decada)
    sns.barplot(x=media_decada.index, y=media_decada.values)
    plt.title("Média de notas por década")
    plt.xlabel("Década")
    plt.ylabel("Nota média")
    plt.show()

def top_5_avaliacoes():
    print("\n👥 Top 5 filmes com mais avaliações:")
    print(df.sort_values(by="Rating count", ascending=False).head(5)[["Title", "Rating count"]])

# =============================
# 3) Menu interativo
# =============================
while True:
    print("\n===== MENU DE ANÁLISES =====")
    print("1 - Top 10 filmes mais bem avaliados")
    print("2 - Estatísticas de duração")
    print("3 - Média de nota por década (com gráfico)")
    print("4 - Top 5 filmes com mais avaliações")
    print("0 - Sair")

    escolha = input("Escolha uma opção: ")

    if escolha == "1":
        top_10_filmes()
    elif escolha == "2":
        estatisticas_duracao()
    elif escolha == "3":
        media_por_decada()
    elif escolha == "4":
        top_5_avaliacoes()
    elif escolha == "0":
        print("Saindo...")
        break
    else:
        print("Opção inválida! Tente novamente.")
