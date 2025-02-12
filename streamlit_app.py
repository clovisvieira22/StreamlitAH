import streamlit as st
import psycopg2
from psycopg2 import sql

# Configurações do banco de dados (usando secrets do Streamlit)
DBName = st.secrets["credentials"]["db_name"]
DBUser = st.secrets["credentials"]["db_user"]
DBPassword = st.secrets["credentials"]["db_password"]
DBHost = st.secrets["credentials"]["db_host"]
DBPort = st.secrets["credentials"]["db_port"]

# Função para conectar ao banco de dados PostgreSQL
def conectar_banco():
    try:
        conn = psycopg2.connect(
            dbname=DBName,
            user=DBUser,
            password=DBPassword,
            host=DBHost,
            port=DBPort
        )
        return conn
    except Exception as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função para buscar um cliente pelo código
def buscar_cliente_por_codigo(codigo):
    conn = conectar_banco()
    if not conn:
        return None

    try:
        with conn.cursor() as cursor:
            query = sql.SQL("SELECT * FROM public.clientes WHERE codigo = %s")
            cursor.execute(query, (codigo,))
            resultado = cursor.fetchone()
            return resultado
    except Exception as e:
        st.error(f"Erro ao buscar cliente: {e}")
        return None
    finally:
        conn.close()

# Função para listar todos os clientes
def listar_clientes():
    conn = conectar_banco()
    if not conn:
        return None

    try:
        with conn.cursor() as cursor:
            query = sql.SQL("SELECT * FROM public.clientes")
            cursor.execute(query)
            resultados = cursor.fetchall()
            return resultados
    except Exception as e:
        st.error(f"Erro ao listar clientes: {e}")
        return None
    finally:
        conn.close()

# Função para inserir ou atualizar um cliente
def salvar_cliente(codigo, dados):
    conn = conectar_banco()
    if not conn:
        return False

    try:
        with conn.cursor() as cursor:
            if codigo:  # Atualizar registro existente
                query = sql.SQL("""
                    UPDATE public.clientes
                    SET
                        nome = %s,
                        nascimento = %s,
                        ba_zhi = %s,
                        chamar = %s,
                        assinatura = %s,
                        relacionamento = %s,
                        profissao = %s,
                        orientacao = %s,
                        inicio_assinatura = %s,
                        fim_assinatura = %s,
                        inicio_degustacao = %s,
                        fim_degustacao = %s,
                        nascimento_ano = %s,
                        nascimento_mes = %s,
                        nascimento_dia = %s,
                        nascimento_hora = %s,
                        nascimento_minuto = %s,
                        nascimento_latitude = %s,
                        nascimento_longitude = %s
                    WHERE codigo = %s
                """)
                valores = (
                    dados["nome"], dados["nascimento"], dados["ba_zhi"], dados["chamar"],
                    dados["assinatura"], dados["relacionamento"], dados["profissao"],
                    dados["orientacao"], dados["inicio_assinatura"], dados["fim_assinatura"],
                    dados["inicio_degustacao"], dados["fim_degustacao"], dados["nascimento_ano"],
                    dados["nascimento_mes"], dados["nascimento_dia"], dados["nascimento_hora"],
                    dados["nascimento_minuto"], dados["nascimento_latitude"], dados["nascimento_longitude"],
                    codigo
                )
            else:  # Inserir novo registro
                query = sql.SQL("""
                    INSERT INTO public.clientes (
                        nome, nascimento, ba_zhi, chamar, assinatura, relacionamento, profissao,
                        orientacao, inicio_assinatura, fim_assinatura, inicio_degustacao, fim_degustacao,
                        nascimento_ano, nascimento_mes, nascimento_dia, nascimento_hora, nascimento_minuto,
                        nascimento_latitude, nascimento_longitude
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                """)
                valores = (
                    dados["nome"], dados["nascimento"], dados["ba_zhi"], dados["chamar"],
                    dados["assinatura"], dados["relacionamento"], dados["profissao"],
                    dados["orientacao"], dados["inicio_assinatura"], dados["fim_assinatura"],
                    dados["inicio_degustacao"], dados["fim_degustacao"], dados["nascimento_ano"],
                    dados["nascimento_mes"], dados["nascimento_dia"], dados["nascimento_hora"],
                    dados["nascimento_minuto"], dados["nascimento_latitude"], dados["nascimento_longitude"]
                )

            cursor.execute(query, valores)
            conn.commit()
            st.success("Cliente salvo com sucesso!")
            return True
    except Exception as e:
        st.error(f"Erro ao salvar cliente: {e}")
        return False
    finally:
        conn.close()

# Interface do Streamlit
st.title("Sistema de Gerenciamento de Clientes")

# Menu lateral
opcao = st.sidebar.radio(
    "Selecione uma opção:",
    ("Incluir Cliente", "Alterar Cliente", "Listar Clientes")
)

# Opção 1: Incluir Cliente
if opcao == "Incluir Cliente":
    st.header("Incluir Novo Cliente")
    st.session_state["cliente"] = None

    # Campos do formulário
    nome = st.text_input("Nome:")
    nascimento = st.date_input("Data de Nascimento:")
    ba_zhi = st.text_input("Ba Zhi:")
    chamar = st.text_input("Chamar:")
    assinatura = st.text_input("Assinatura:")
    relacionamento = st.text_input("Relacionamento:")
    profissao = st.text_input("Profissão:")
    orientacao = st.text_input("Orientação:")
    inicio_assinatura = st.date_input("Início da Assinatura:")
    fim_assinatura = st.date_input("Fim da Assinatura:")
    inicio_degustacao = st.date_input("Início da Degustação:")
    fim_degustacao = st.date_input("Fim da Degustação:")
    nascimento_ano = st.number_input("Ano de Nascimento:", min_value=1900, max_value=2100)
    nascimento_mes = st.number_input("Mês de Nascimento:", min_value=1, max_value=12)
    nascimento_dia = st.number_input("Dia de Nascimento:", min_value=1, max_value=31)
    nascimento_hora = st.number_input("Hora de Nascimento:", min_value=0, max_value=23)
    nascimento_minuto = st.number_input("Minuto de Nascimento:", min_value=0, max_value=59)
    nascimento_latitude = st.number_input("Latitude de Nascimento:")
    nascimento_longitude = st.number_input("Longitude de Nascimento:")

    # Botão para salvar
    if st.button("Salvar Cliente"):
        dados = {
            "nome": nome,
            "nascimento": nascimento,
            "ba_zhi": ba_zhi,
            "chamar": chamar,
            "assinatura": assinatura,
            "relacionamento": relacionamento,
            "profissao": profissao,
            "orientacao": orientacao,
            "inicio_assinatura": inicio_assinatura,
            "fim_assinatura": fim_assinatura,
            "inicio_degustacao": inicio_degustacao,
            "fim_degustacao": fim_degustacao,
            "nascimento_ano": nascimento_ano,
            "nascimento_mes": nascimento_mes,
            "nascimento_dia": nascimento_dia,
            "nascimento_hora": nascimento_hora,
            "nascimento_minuto": nascimento_minuto,
            "nascimento_latitude": nascimento_latitude,
            "nascimento_longitude": nascimento_longitude
        }

        if salvar_cliente(None, dados):
            st.session_state["cliente"] = None  # Limpar o formulário após salvar

# Opção 2: Alterar Cliente
elif opcao == "Alterar Cliente":
    st.header("Alterar Cliente Existente")
    codigo_cliente = st.number_input("Digite o código do cliente:", min_value=1, step=1)
    if st.button("Buscar Cliente"):
        cliente = buscar_cliente_por_codigo(codigo_cliente)
        if cliente:
            st.session_state["cliente"] = cliente
        else:
            st.error("Cliente não encontrado.")

    if "cliente" in st.session_state and st.session_state["cliente"]:
        cliente = st.session_state["cliente"]

        # Campos do formulário
        nome = st.text_input("Nome:", value=cliente[1])
        nascimento = st.date_input("Data de Nascimento:", value=cliente[2])
        ba_zhi = st.text_input("Ba Zhi:", value=cliente[3])
        chamar = st.text_input("Chamar:", value=cliente[4])
        assinatura = st.text_input("Assinatura:", value=cliente[5])
        relacionamento = st.text_input("Relacionamento:", value=cliente[6])
        profissao = st.text_input("Profissão:", value=cliente[7])
        orientacao = st.text_input("Orientação:", value=cliente[8])
        inicio_assinatura = st.date_input("Início da Assinatura:", value=cliente[9])
        fim_assinatura = st.date_input("Fim da Assinatura:", value=cliente[10])
        inicio_degustacao = st.date_input("Início da Degustação:", value=cliente[11])
        fim_degustacao = st.date_input("Fim da Degustação:", value=cliente[12])
        nascimento_ano = st.number_input("Ano de Nascimento:", value=cliente[13], min_value=1900, max_value=2100)
        nascimento_mes = st.number_input("Mês de Nascimento:", value=cliente[14], min_value=1, max_value=12)
        nascimento_dia = st.number_input("Dia de Nascimento:", value=cliente[15], min_value=1, max_value=31)
        nascimento_hora = st.number_input("Hora de Nascimento:", value=cliente[16], min_value=0, max_value=23)
        nascimento_minuto = st.number_input("Minuto de Nascimento:", value=cliente[17], min_value=0, max_value=59)
        nascimento_latitude = st.number_input("Latitude de Nascimento:", value=float(cliente[18]))
        nascimento_longitude = st.number_input("Longitude de Nascimento:", value=float(cliente[19]))

        # Botão para salvar
        if st.button("Salvar Alterações"):
            dados = {
                "nome": nome,
                "nascimento": nascimento,
                "ba_zhi": ba_zhi,
                "chamar": chamar,
                "assinatura": assinatura,
                "relacionamento": relacionamento,
                "profissao": profissao,
                "orientacao": orientacao,
                "inicio_assinatura": inicio_assinatura,
                "fim_assinatura": fim_assinatura,
                "inicio_degustacao": inicio_degustacao,
                "fim_degustacao": fim_degustacao,
                "nascimento_ano": nascimento_ano,
                "nascimento_mes": nascimento_mes,
                "nascimento_dia": nascimento_dia,
                "nascimento_hora": nascimento_hora,
                "nascimento_minuto": nascimento_minuto,
                "nascimento_latitude": nascimento_latitude,
                "nascimento_longitude": nascimento_longitude
            }

            if salvar_cliente(cliente[0], dados):
                st.session_state["cliente"] = None  # Limpar o formulário após salvar

# Opção 3: Listar Clientes
elif opcao == "Listar Clientes":
    st.header("Lista de Clientes")
    clientes = listar_clientes()
    if clientes:
        st.table(clientes)
    else:
        st.warning("Nenhum cliente encontrado.")
