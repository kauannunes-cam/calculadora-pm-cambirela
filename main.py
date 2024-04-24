import streamlit as st
import pandas as pd

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Chame a função com o caminho do seu arquivo CSS personalizado
local_css("style.css")

def add_custom_css():
    st.markdown("""
        <style>
            /* Altera a cor do texto de toda a página */
            body, h1, h2, h3, h4, h5, h6, p, div, label, input, button, table {
                color: #1F4741; /* Cor secundária para texto */
            }

        </style>
    """, unsafe_allow_html=True)

# Adiciona o CSS personalizado ao app
add_custom_css()

# Função para calcular o preço médio e a quantidade de lotes em aberto
def calcular_preco_medio_e_lotes(transacoes):
    if not transacoes.empty:
        # Calcula o preço médio
        transacoes['Total'] = transacoes['Preço'] * transacoes['Quantidade']
        total_compras = transacoes[transacoes['Tipo'] == 'Compra']['Total'].sum()
        total_vendas = transacoes[transacoes['Tipo'] == 'Venda']['Total'].sum()
        quantidade_compras = transacoes[transacoes['Tipo'] == 'Compra']['Quantidade'].sum()
        quantidade_vendas = transacoes[transacoes['Tipo'] == 'Venda']['Quantidade'].sum()
        
        quantidade_lotes_em_aberto = quantidade_compras - quantidade_vendas
        total_quantidade = quantidade_compras + quantidade_vendas

        if total_quantidade > 0:
            preco_medio = (total_compras - total_vendas) / quantidade_lotes_em_aberto if quantidade_lotes_em_aberto != 0 else 0
        else:
            preco_medio = 0

        return preco_medio, quantidade_lotes_em_aberto
    else:
        return 0, 0

st.title('Calculadora de Preço Médio')

# Tabela interativa para entrada de dados das transações
st.subheader('Insira os preços e quantidades:')
# Inicializar a tabela se ela não existir
if 'transacoes' not in st.session_state:
    st.session_state.transacoes = pd.DataFrame(columns=['Preço', 'Quantidade', 'Tipo'])

# Cria campos para inserção de novas transações
preco_input = st.number_input('Preço', min_value=0.0, value=0.0, format='%f', key='preco')
quantidade_input = st.number_input('Quantidade', min_value=0, value=0, format='%d', key='quantidade')
tipo_transacao = st.radio("Tipo de Transação", ('Compra', 'Venda'))

# Botão para adicionar transação à tabela
add_button = st.button('Adicionar Transação')

if add_button:
    # Adiciona nova transação à tabela existente
    new_transaction = pd.DataFrame({
        'Preço': [preco_input],
        'Quantidade': [quantidade_input],
        'Tipo': [tipo_transacao]
    })
    st.session_state.transacoes = pd.concat([st.session_state.transacoes, new_transaction], ignore_index=True)


# Mostrando a tabela de transações
st.write('Transações:')
st.table(st.session_state.transacoes)

# Botão para limpar a tabela de transações
clear_button = st.button('Limpar Transações')

if clear_button:
    # Reseta a tabela de transações para um DataFrame vazio
    st.session_state.transacoes = pd.DataFrame(columns=['Preço', 'Quantidade', 'Tipo'])
    
# Calculando e exibindo o preço médio e a quantidade de lotes em aberto
preco_medio, quantidade_lotes_em_aberto = calcular_preco_medio_e_lotes(st.session_state.transacoes)

# Usando st.write para alinhar métricas horizontalmente
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Preço Médio", value=f"R$ {preco_medio:,.2f}")
with col2:
    st.metric(label="Quantidade de Lotes em Aberto", value=f"{quantidade_lotes_em_aberto}")
