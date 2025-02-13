import streamlit as st
import psycopg2
from datetime import datetime

# Título da aplicação
st.title("Formulário de Cadastro de Prospects")

# Função para conectar ao banco de dados PostgreSQL
def conectar_banco():
    try:
        conn = psycopg2.connect(
            dbname="nome_do_banco",  # Substitua pelo nome do seu banco de dados
            user="usuario",          # Substitua pelo seu usuário do PostgreSQL
            password="senha",        # Substitua pela sua senha do PostgreSQL
            host="localhost",        # Substitua pelo host do seu banco de dados
            port="5432"             # Substitua pela porta do seu banco de dados
        )
        return conn
    except Exception as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função para inserir dados na tabela prospects
def inserir_prospect(dados):
    conn = conectar_banco()
    if not conn:
        return False

    try:
        with conn.cursor() as cursor:
            query = """
                INSERT INTO prospects (
                    codigo, nome_completo, data_de_nascimento, hora_de_nascimento,
                    cidade_de_nascimento, em_relacionamento, profissao, genero
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s
                )
            """
            cursor.execute(query, dados)
            conn.commit()
            st.success("Prospect cadastrado com sucesso!")
            return True
    except Exception as e:
        st.error(f"Erro ao inserir prospect: {e}")
        return False
    finally:
        conn.close()

# Formulário de cadastro
with st.form("formulario_prospect"):
    st.header("Preencha os dados do Prospect")

    # Campos do formulário
    codigo = st.number_input("Código:", min_value=1, step=1)
    nome_completo = st.text_input("Nome Completo:")
    data_nascimento = st.date_input("Data de Nascimento:")
    hora_nascimento = st.time_input("Hora de Nascimento:")
    cidade_nascimento = st.text_input("Cidade de Nascimento:")
    em_relacionamento = st.selectbox("Em Relacionamento?", options=["Sim", "Não"])
    profissao = st.text_input("Profissão:")
    genero = st.selectbox("Gênero:", options=["Homem", "Mulher", "Outro"])

    # Botão para enviar o formulário
    if st.form_submit_button("Cadastrar Prospect"):
        # Converter os dados para o formato adequado
        em_relacionamento_bool = True if em_relacionamento == "Sim" else False
        dados = (
            codigo, nome_completo, data_nascimento, hora_nascimento,
            cidade_nascimento, em_relacionamento_bool, profissao, genero
        )

        # Inserir os dados no banco de dados
        if inserir_prospect(dados):
            st.balloons()  # Animação de confetes para indicar sucesso
