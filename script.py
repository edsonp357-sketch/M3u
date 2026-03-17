import requests
import os

URL = "https://raw.githubusercontent.com/edsonp357-sketch/M3u/refs/heads/main/lista_final.m3u"

categorias = {
    "abertos_br": ["globo", "sbt", "band", "record"],
    "esportes": ["premiere", "sportv", "espn"],
}

print("Baixando lista...")
conteudo = requests.get(URL).text.splitlines()

pasta = "listas_divididas"
os.makedirs(pasta, exist_ok=True)

header = "#EXTM3U\n"

def salvar(nome, dados):
    with open(f"{pasta}/{nome}.m3u", "w", encoding="utf-8") as f:
        f.write(header + "\n".join(dados))

for nome, palavras in categorias.items():
    saida = []
    for i in range(len(conteudo)):
        linha = conteudo[i].lower()
        if linha.startswith("#extinf"):
            if any(p in linha for p in palavras):
                saida.append(conteudo[i])
                if i + 1 < len(conteudo):
                    saida.append(conteudo[i+1])
    salvar(nome, saida)

bloco = []
contador = 1
limite = 2000

for linha in conteudo:
    bloco.append(linha)
    if len(bloco) >= limite:
        salvar(f"parte_{contador}", bloco)
        bloco = []
        contador += 1

if bloco:
    salvar(f"parte_{contador}", bloco)

print("Finalizado!")
