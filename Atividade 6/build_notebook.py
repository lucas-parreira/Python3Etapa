import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []

cells.append(nbf.v4.new_markdown_cell(
"""# Desocupação por sexo (2012 x 2026) x Afazeres domésticos (Tabela 1.1.1)

Fontes:
- `Tabela5-sem_emprego_2012.csv` e `Tabela5-sem_emprego_2026.csv` — composição da
  desocupação por sexo, 1º trimestre de 2012 e de 2026, por UF;
- `Tabela_1_1_1.xls` — horas semanais dedicadas a cuidados e afazeres domésticos,
  por sexo/cor, 2022 (mesma tabela da Aula 2).

Este notebook:
1. Abre e trata as duas Tabelas 5 (2012 e 2026);
2. Junta as duas Tabelas 5 num único dataframe (`comp`);
3. Trata a Tabela 1.1.1 (código da Aula 2), mantendo apenas os estados (sem Brasil e sem as Grandes Regiões);
4. Junta `comp` com a Tabela 1.1.1 tratada;
5. Ordena, derrete (`melt`) e plota a participação feminina na desocupação em 2012 T1 x 2026 T1, por estado."""
))

cells.append(nbf.v4.new_code_cell(
"""# python -m pip install pandas matplotlib seaborn xlrd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)"""
))

cells.append(nbf.v4.new_markdown_cell("## 1. Abrir as duas Tabelas 5 (2012 e 2026)"))

cells.append(nbf.v4.new_code_cell(
"""# encoding="utf-8-sig" porque os CSVs têm BOM (ï»¿) no início
t2012 = pd.read_csv(
    "Tabela5-sem_emprego_2012.csv", sep=";", decimal=",", encoding="utf-8-sig"
)
t2026 = pd.read_csv(
    "Tabela5-sem_emprego_2026.csv", sep=";", decimal=",", encoding="utf-8-sig"
)
t2012.head()"""
))

cells.append(nbf.v4.new_code_cell(
"""# Renomeia para colunas curtas, já indicando o ano
t2012 = t2012.rename(columns={
    "Desocupados - homens (2012 T1)": "homens_2012",
    "Desocupados - mulheres (2012 T1)": "mulheres_2012",
})
t2026 = t2026.rename(columns={
    "Desocupados - homens (2026 T1)": "homens_2026",
    "Desocupados - mulheres (2026 T1)": "mulheres_2026",
})
t2026.head()"""
))

cells.append(nbf.v4.new_markdown_cell("## 2. Juntar as duas Tabelas 5"))

cells.append(nbf.v4.new_code_cell(
"""comp = t2012.merge(t2026, on=["Sigla", "Código", "Estado"], how="inner")
comp["variacao_mulheres_pp"] = comp["mulheres_2026"] - comp["mulheres_2012"]
comp.sort_values("variacao_mulheres_pp")"""
))

cells.append(nbf.v4.new_markdown_cell(
"""## 3. Tratar a Tabela 1.1.1 (código da Aula 2), só estados

A tabela original traz Brasil, as 5 Grandes Regiões e os 27 estados/UFs, nessa ordem
(Brasil, Norte, seus estados, Nordeste, seus estados...). Para cruzar com a Tabela 5
(que só tem estados), removemos a linha "Brasil" e as 5 linhas de região."""
))

cells.append(nbf.v4.new_code_cell(
"""bruto = pd.read_excel("Tabela_1_1_1.xls", engine="xlrd", header=None)

indicador_1 = bruto.iloc[8:41].copy()
indicador_1.columns = [
    "uf_regiao",
    "total",
    "total_branca",
    "total_preta_parda",
    "homem_branca",
    "homem_preta_parda",
    "mulher_branca",
    "mulher_preta_parda",
]

regioes = ["Norte", "Nordeste", "Sudeste", "Sul", "Centro-Oeste"]
indicador_estados = indicador_1[~indicador_1["uf_regiao"].isin(["Brasil"] + regioes)].copy()
indicador_estados = indicador_estados.rename(columns={"uf_regiao": "Estado"})
indicador_estados"""
))

cells.append(nbf.v4.new_markdown_cell("## 4. Juntar `comp` com a Tabela 1.1.1 (só estados)"))

cells.append(nbf.v4.new_code_cell(
"""comp = comp.merge(indicador_estados, on="Estado", how="inner")
comp"""
))

cells.append(nbf.v4.new_markdown_cell("## 5. Gráfico — participação feminina na desocupação, 2012 T1 x 2026 T1"))

cells.append(nbf.v4.new_code_cell(
"""ordem = comp.sort_values("mulheres_2026")["Estado"]

longo = comp.melt(
    id_vars=["Sigla", "Código", "Estado"],
    value_vars=["mulheres_2012", "mulheres_2026"],
    var_name="Ano",
    value_name="Participacao_mulheres",
)
longo["Ano"] = longo["Ano"].map({"mulheres_2012": "2012 T1", "mulheres_2026": "2026 T1"})
longo.head()"""
))

cells.append(nbf.v4.new_code_cell(
"""fig, ax = plt.subplots(figsize=(10, 10))
sns.barplot(
    data=longo,
    y="Estado",
    x="Participacao_mulheres",
    hue="Ano",
    order=ordem,
    ax=ax,
)
ax.axvline(50, color="gray", linestyle="--", linewidth=1)
ax.set_xlabel("Participação das mulheres entre as pessoas desocupadas (%)")
ax.set_ylabel("")
ax.set_title("Desocupação: participação feminina em 2012 T1 e 2026 T1")
ax.legend(title="Trimestre")
fig.tight_layout()
plt.savefig("graficos/desocupacao_mulheres_2012_2026.png", dpi=150)
plt.show()"""
))

nb['cells'] = cells

with open("Analise_Tabela5_Desocupacao.ipynb", "w", encoding="utf-8") as f:
    nbf.write(nb, f)

print("Notebook criado com", len(cells), "células.")
