# Análise da Tabela 3 (IBGE - Tabela 10063)

Pessoas com nível superior completo, por áreas gerais de formação do curso de
graduação concluído, segundo o sexo e a Grande Região.

**Fonte dos dados:** IBGE/SIDRA - Tabela 10063.

## Conteúdo

- `dados_tabela3.py` — script que gera `tabela3_bruta.xlsx` a partir dos dados originais da Tabela 3.
- `tabela3_bruta.xlsx` — tabela original (Brasil, Grandes Regiões e Unidades da Federação).
- `Analise_Tabela3.ipynb` — notebook com a análise: filtra as 5 Grandes Regiões, divide os
  dados em 3 tabelas e calcula estatísticas descritivas (`describe()`).
- `superior.xlsx` — homens e mulheres por região com curso superior (Total).
- `tecnologia.xlsx` — homens e mulheres por região com curso em Ciência, Tecnologia,
  Engenharias e Matemática.
- `educacao_saude.xlsx` — homens e mulheres por região com curso em Educação, Serviços
  pessoais, Saúde e Bem-estar.

## Como executar

```bash
pip install pandas openpyxl nbformat nbconvert
jupyter nbconvert --to notebook --execute --inplace Analise_Tabela3.ipynb
```

## Observação

A tabela original também traz os dados por Unidade da Federação (estado); para a análise
"por região", foram consideradas apenas as 5 Grandes Regiões (Norte, Nordeste, Sudeste,
Sul e Centro-Oeste).
