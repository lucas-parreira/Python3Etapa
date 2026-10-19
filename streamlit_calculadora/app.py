import streamlit as st

st.set_page_config(page_title="Calculadora de Compras", page_icon="🛒", layout="centered")

precos_itens = {
    "Arroz (5kg)": 25.90,
    "Feijão (1kg)": 8.50,
    "Macarrão (500g)": 4.99,
    "Açúcar (1kg)": 4.79,
    "Café (500g)": 17.90,
    "Óleo de soja (900ml)": 7.49,
    "Leite (1L)": 5.29,
    "Pão de forma": 8.90,
    "Ovos (dúzia)": 12.50,
    "Frango (1kg)": 14.99,
    "Carne moída (1kg)": 32.90,
    "Banana (1kg)": 6.49,
    "Tomate (1kg)": 7.99,
    "Sabão em pó (1kg)": 13.90,
    "Papel higiênico (12 rolos)": 19.90,
}


def calcular_preco_total(itens_selecionados):
    total = sum(precos_itens[item] for item in itens_selecionados)
    return total


def calcular_troco(total, valor_pago):
    return valor_pago - total


def decompor_troco(troco):
    cedulas_e_moedas = [100, 50, 20, 10, 5, 2, 1, 0.50, 0.25, 0.10, 0.05]
    restante = round(troco * 100)
    resultado = {}
    for valor in cedulas_e_moedas:
        centavos = round(valor * 100)
        quantidade, restante = divmod(restante, centavos)
        if quantidade:
            resultado[valor] = quantidade
    return resultado, restante / 100


def formatar_valor(valor):
    if valor >= 1:
        return f"R$ {valor:.0f}" if valor == int(valor) else f"R$ {valor:.2f}"
    return f"R$ {valor:.2f}"


st.title("🛒 Calculadora de Compras")
st.caption("Selecione os itens do supermercado, veja o total e calcule o troco.")

itens_selecionados = st.multiselect(
    label="Selecione os itens do supermercado:",
    options=list(precos_itens.keys()),
)

if itens_selecionados:
    st.subheader("Itens Selecionados:")
    for item in itens_selecionados:
        st.write(f"- {item}: R$ {precos_itens[item]:.2f}")

    total_compra = calcular_preco_total(itens_selecionados)

    st.divider()
    st.metric(label="Total da Compra", value=f"R$ {total_compra:.2f}")

    st.subheader("💵 Calculadora de Troco")
    valor_pago = st.number_input(
        "Valor pago pelo cliente (R$):",
        min_value=0.0,
        value=0.0,
        step=1.0,
        format="%.2f",
    )

    if valor_pago > 0:
        troco = calcular_troco(total_compra, valor_pago)

        if troco < 0:
            st.error(f"Valor insuficiente! Faltam R$ {abs(troco):.2f}.")
        elif troco == 0:
            st.success("Pagamento exato. Não há troco!")
        else:
            st.metric(label="Troco", value=f"R$ {troco:.2f}")

            cedulas, sobra = decompor_troco(troco)
            st.write("Sugestão de cédulas e moedas:")
            for valor, quantidade in cedulas.items():
                tipo = "cédula" if valor >= 2 else "moeda"
                plural = "s" if quantidade > 1 else ""
                st.write(f"- {quantidade} {tipo}{plural} de {formatar_valor(valor)}")
else:
    st.info("Nenhum item selecionado. Marque os produtos acima para ver o valor total.")
