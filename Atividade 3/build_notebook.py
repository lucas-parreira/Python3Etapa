import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []

cells.append(nbf.v4.new_markdown_cell(
"""# Análise da Tabela 3 (IBGE - Tabela 10063)

Pessoas com nível superior completo, por áreas gerais de formação do curso de
graduação concluído, segundo o sexo e a Grande Região.

Fonte: IBGE/SIDRA - Tabela 10063.

Este notebook:
1. Carrega os dados brutos da Tabela 3 (`tabela3_bruta.xlsx`);
2. Filtra apenas as 5 Grandes Regiões do Brasil (Norte, Nordeste, Sudeste, Sul, Centro-Oeste);
3. Divide os dados em 3 tabelas:
   - Homens e mulheres por região com curso superior (Total);
   - Homens e mulheres por região com curso em Ciência, Tecnologia, Engenharias e Matemática (CTEM);
   - Homens e mulheres por região com curso em Educação, Serviços pessoais, Saúde e Bem-estar;
4. Salva cada tabela em `.xlsx`;
5. Apresenta as estatísticas descritivas (`describe()`) de cada uma."""
))

cells.append(nbf.v4.new_code_cell(
"""import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)"""
))

cells.append(nbf.v4.new_markdown_cell("## 1. Carregar os dados brutos da Tabela 3"))

cells.append(nbf.v4.new_code_cell(
"""df_bruto = pd.read_excel("tabela3_bruta.xlsx")
df_bruto.head(10)"""
))

cells.append(nbf.v4.new_markdown_cell(
"""## 2. Filtrar apenas as Grandes Regiões

A tabela original traz Brasil, as 5 Grandes Regiões e as 27 Unidades da Federação.
Para a análise "por região" pedida, mantemos apenas as 5 Grandes Regiões."""
))

cells.append(nbf.v4.new_code_cell(
"""grandes_regioes = ["Norte", "Nordeste", "Sudeste", "Sul", "Centro-Oeste"]
df_regioes = df_bruto[df_bruto["Regiao"].isin(grandes_regioes)].reset_index(drop=True)
df_regioes"""
))

cells.append(nbf.v4.new_markdown_cell("## 3. Dividir em 3 tabelas"))

cells.append(nbf.v4.new_code_cell(
"""# Tabela 1 - Homens e mulheres por região com curso superior (Total)
superior = df_regioes[["Regiao", "Total_Total", "Total_Homens", "Total_Mulheres"]].copy()
superior.columns = ["Regiao", "Total", "Homens", "Mulheres"]
superior"""
))

cells.append(nbf.v4.new_code_cell(
"""# Tabela 2 - Homens e mulheres por região com curso em Ciência, Tecnologia, Engenharias e Matemática
tecnologia = df_regioes[["Regiao", "CTEM_Total", "CTEM_Homens", "CTEM_Mulheres"]].copy()
tecnologia.columns = ["Regiao", "Total", "Homens", "Mulheres"]
tecnologia"""
))

cells.append(nbf.v4.new_code_cell(
"""# Tabela 3 - Homens e mulheres por região com curso em Educação, Serviços pessoais, Saúde e Bem-estar
educacao_saude = df_regioes[["Regiao", "Educ_Saude_Total", "Educ_Saude_Homens", "Educ_Saude_Mulheres"]].copy()
educacao_saude.columns = ["Regiao", "Total", "Homens", "Mulheres"]
educacao_saude"""
))

cells.append(nbf.v4.new_markdown_cell("## 4. Salvar as 3 tabelas em .xlsx"))

cells.append(nbf.v4.new_code_cell(
"""superior.to_excel("superior.xlsx", index=False)
tecnologia.to_excel("tecnologia.xlsx", index=False)
educacao_saude.to_excel("educacao_saude.xlsx", index=False)

print("Arquivos salvos: superior.xlsx, tecnologia.xlsx, educacao_saude.xlsx")"""
))

cells.append(nbf.v4.new_markdown_cell("## 5. Estatísticas descritivas (describe())"))

cells.append(nbf.v4.new_code_cell(
"""print("Curso Superior (Total)")
superior.describe()"""
))

cells.append(nbf.v4.new_code_cell(
"""print("Ciência, Tecnologia, Engenharias e Matemática")
tecnologia.describe()"""
))

cells.append(nbf.v4.new_code_cell(
"""print("Educação, Serviços pessoais, Saúde e Bem-estar")
educacao_saude.describe()"""
))

nb['cells'] = cells

with open("Analise_Tabela3.ipynb", "w", encoding="utf-8") as f:
    nbf.write(nb, f)

print("Notebook criado.")
