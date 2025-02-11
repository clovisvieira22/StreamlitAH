#import streamlit as st
#
#st.title("🎈 My new app")
#st.write(
#    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
#)
import streamlit as st
import psycopg2
from psycopg2 import sql

# Função para conectar ao banco de dados PostgreSQL
def conectar_banco():
    try:
        conn = psycopg2.connect(
            dbname="nome_do_banco",  # Substitua pelo nome do seu banco de dados
            user="usuario",         # Substitua pelo seu usuário
            password="senha",      # Substitua pela sua senha
            host="localhost",      # Substitua pelo host do banco de dados
            port="5432"            # Substitua pela porta do banco de dados
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
            query = sql.SQL("""
                SELECT * FROM public.clientes WHERE codigo = %s
            """)
            cursor.execute(query, (codigo,))
            resultado = cursor.fetchone()
            return resultado
    except Exception as e:
        st.error(f"Erro ao buscar cliente: {e}")
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
st.title("Formulário de Clientes")

# Selecionar entre editar ou adicionar um novo cliente
opcao = st.radio("Selecione uma opção:", ("Editar Cliente Existente", "Adicionar Novo Cliente"))

if opcao == "Editar Cliente Existente":
    codigo_cliente = st.number_input("Digite o código do cliente:", min_value=1, step=1)
    if st.button("Buscar Cliente"):
        cliente = buscar_cliente_por_codigo(codigo_cliente)
        if cliente:
            st.session_state["cliente"] = cliente
        else:
            st.error("Cliente não encontrado.")
else:
    st.session_state["cliente"] = None

# Formulário para editar ou adicionar cliente
if "cliente" in st.session_state:
    cliente = st.session_state["cliente"]

    # Campos do formulário
    nome = st.text_input("Nome:", value=cliente[1] if cliente else "")
    nascimento = st.date_input("Data de Nascimento:", value=cliente[2] if cliente else None)
    ba_zhi = st.text_input("Ba Zhi:", value=cliente[3] if cliente else "")
    chamar = st.text_input("Chamar:", value=cliente[4] if cliente else "")
    assinatura = st.text_input("Assinatura:", value=cliente[5] if cliente else "")
    relacionamento = st.text_input("Relacionamento:", value=cliente[6] if cliente else "")
    profissao = st.text_input("Profissão:", value=cliente[7] if cliente else "")
    orientacao = st.text_input("Orientação:", value=cliente[8] if cliente else "")
    inicio_assinatura = st.date_input("Início da Assinatura:", value=cliente[9] if cliente else None)
    fim_assinatura = st.date_input("Fim da Assinatura:", value=cliente[10] if cliente else None)
    inicio_degustacao = st.date_input("Início da Degustação:", value=cliente[11] if cliente else None)
    fim_degustacao = st.date_input("Fim da Degustação:", value=cliente[12] if cliente else None)
    nascimento_ano = st.number_input("Ano de Nascimento:", value=cliente[13] if cliente else 1971, min_value=1900, max_value=2100)
    nascimento_mes = st.number_input("Mês de Nascimento:", value=cliente[14] if cliente else 1, min_value=1, max_value=12)
    nascimento_dia = st.number_input("Dia de Nascimento:", value=cliente[15] if cliente else 1, min_value=1, max_value=31)
    nascimento_hora = st.number_input("Hora de Nascimento:", value=cliente[16] if cliente else 0, min_value=0, max_value=23)
    nascimento_minuto = st.number_input("Minuto de Nascimento:", value=cliente[17] if cliente else 0, min_value=0, max_value=59)
    nascimento_latitude = st.number_input("Latitude de Nascimento:", value=float(cliente[18]) if cliente else -29.1678)
    nascimento_longitude = st.number_input("Longitude de Nascimento:", value=float(cliente[19]) if cliente else -51.1794)

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

        if salvar_cliente(cliente[0] if cliente else None, dados):
            st.session_state["cliente"] = None  # Limpar o formulário após salvar
