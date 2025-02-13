import streamlit as st
import psycopg2
from psycopg2 import sql

# Configurações do banco de dados (usando secrets do Streamlit)
DBName = st.secrets["credentials"]["db_name"]
DBUser = st.secrets["credentials"]["db_user"]
DBPassword = st.secrets["credentials"]["db_password"]
DBHost = st.secrets["credentials"]["db_host"]
DBPort = st.secrets["credentials"]["db_port"]

# Adicionar estilo CSS para tabela zebrada
st.markdown("""
<style>
    .dataframe tr:nth-child(even) {
        background-color: #f5f5f5;
    }
    .dataframe tr:hover {
        background-color: #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

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

# Função para buscar clientes por nome ou parte do nome
def buscar_clientes_por_nome(nome):
    conn = conectar_banco()
    if not conn:
        return None

    try:
        with conn.cursor() as cursor:
            query = sql.SQL("SELECT * FROM public.clientes WHERE nome ILIKE %s ORDER BY codigo ASC")
            cursor.execute(query, (f"%{nome}%",))
            resultados = cursor.fetchall()
            return resultados
    except Exception as e:
        st.error(f"Erro ao buscar clientes: {e}")
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
            query = sql.SQL("SELECT * FROM public.clientes ORDER BY codigo ASC")
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
st.title("Clientes")

# Componente de guias (tabs)
tab1, tab2, tab3 = st.tabs(["Incluir Cliente", "Alterar Cliente", "Listar Clientes"])

# Guia 1: Incluir Cliente
# Guia 1: Incluir Cliente
# Guia 1: Incluir Cliente
# Guia 1: Incluir Cliente
with tab1:
    st.header("Incluir Novo Cliente")
    st.session_state["cliente"] = None

    # Campos do formulário
    nome = st.text_input("Nome:")
    nascimento = st.date_input("Data de Nascimento:", key="nascimento_incluir")
    ba_zhi = st.text_input("Ba Zhi:")
    chamar = st.text_input("Chamar:")
    assinatura = st.text_input("Assinatura:")
    relacionamento = st.text_input("Relacionamento:")
    profissao = st.text_input("Profissão:")
    orientacao = st.text_input("Orientação:")
    inicio_assinatura = st.date_input("Início da Assinatura:", key="inicio_assinatura_incluir")
    fim_assinatura = st.date_input("Fim da Assinatura:", key="fim_assinatura_incluir")
    inicio_degustacao = st.date_input("Início da Degustação:", key="inicio_degustacao_incluir")
    fim_degustacao = st.date_input("Fim da Degustação:", key="fim_degustacao_incluir")
    nascimento_ano = st.number_input("Ano de Nascimento:", min_value=1900, max_value=2100, key="nascimento_ano_incluir")
    nascimento_mes = st.number_input("Mês de Nascimento:", min_value=1, max_value=12, key="nascimento_mes_incluir")
    nascimento_dia = st.number_input("Dia de Nascimento:", min_value=1, max_value=31, key="nascimento_dia_incluir")
    nascimento_hora = st.number_input("Hora de Nascimento:", min_value=0, max_value=23, key="nascimento_hora_incluir")
    nascimento_minuto = st.number_input("Minuto de Nascimento:", min_value=0, max_value=59, key="nascimento_minuto_incluir")
    nascimento_latitude = st.number_input("Latitude de Nascimento:", value=0.0, key="nascimento_latitude_incluir")
    nascimento_longitude = st.number_input("Longitude de Nascimento:", value=0.0, key="nascimento_longitude_incluir")

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

# Guia 2: Alterar Cliente
with tab2:
    st.header("Alterar Cliente Existente")
    nome_busca = st.text_input("Digite o nome ou parte do nome do cliente:")
    if st.button("Buscar Cliente"):
        clientes = buscar_clientes_por_nome(nome_busca)
        if clientes:
            st.session_state["clientes_encontrados"] = clientes
        else:
            st.error("Nenhum cliente encontrado.")

    if "clientes_encontrados" in st.session_state and st.session_state["clientes_encontrados"]:
        clientes = st.session_state["clientes_encontrados"]
        cliente_selecionado = st.selectbox(
            "Selecione o cliente para editar:",
            options=[f"{cliente[1]} (Código: {cliente[0]})" for cliente in clientes]
        )

        # Extrair o código do cliente selecionado
        codigo_cliente = int(cliente_selecionado.split("(Código: ")[1].replace(")", ""))

        # Buscar os dados completos do cliente selecionado
        cliente = next((c for c in clientes if c[0] == codigo_cliente), None)
        if cliente:
            st.session_state["cliente"] = cliente

    if "cliente" in st.session_state and st.session_state["cliente"]:
        cliente = st.session_state["cliente"]

        # Campos do formulário
        nome = st.text_input("Nome:", value=cliente[1])
        nascimento = st.date_input("Data de Nascimento:", value=cliente[2], key="nascimento_alterar")
        ba_zhi = st.text_input("Ba Zhi:", value=cliente[3])
        chamar = st.text_input("Chamar:", value=cliente[4])
        assinatura = st.text_input("Assinatura:", value=cliente[5])
        relacionamento = st.text_input("Relacionamento:", value=cliente[6])
        profissao = st.text_input("Profissão:", value=cliente[7])
        orientacao = st.text_input("Orientação:", value=cliente[8])
        inicio_assinatura = st.date_input("Início da Assinatura:", value=cliente[9], key="inicio_assinatura_alterar")
        fim_assinatura = st.date_input("Fim da Assinatura:", value=cliente[10], key="fim_assinatura_alterar")
        inicio_degustacao = st.date_input("Início da Degustação:", value=cliente[11], key="inicio_degustacao_alterar")
        fim_degustacao = st.date_input("Fim da Degustação:", value=cliente[12], key="fim_degustacao_alterar")
        nascimento_ano = st.number_input("Ano de Nascimento:", value=cliente[13], min_value=1900, max_value=2100, key="nascimento_ano_alterar")
        nascimento_mes = st.number_input("Mês de Nascimento:", value=cliente[14], min_value=1, max_value=12, key="nascimento_mes_alterar")
        nascimento_dia = st.number_input("Dia de Nascimento:", value=cliente[15], min_value=1, max_value=31, key="nascimento_dia_alterar")
        nascimento_hora = st.number_input("Hora de Nascimento:", value=cliente[16], min_value=0, max_value=23, key="nascimento_hora_alterar")
        nascimento_minuto = st.number_input("Minuto de Nascimento:", value=cliente[17], min_value=0, max_value=59, key="nascimento_minuto_alterar")
        nascimento_latitude = st.number_input(
            "Latitude de Nascimento:",
            value=float(cliente[18]) if cliente[18] is not None else 0.0,
            key="nascimento_latitude_alterar"
        )
        nascimento_longitude = st.number_input(
            "Longitude de Nascimento:",
            value=float(cliente[19]) if cliente[19] is not None else 0.0,
            key="nascimento_longitude_alterar"
        )

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
# Guia 3: Listar Clientes
with tab3:
    st.header("Lista de Clientes")
    clientes = listar_clientes()
    if clientes:
        # Definir nomes das colunas corrigidos
        colunas = [
            "Código", "Código", "Nome", "Data Nascimento", "Ba Zhi", "Chamar", "Assinatura", 
            "Relacionamento", "Profissão", "Orientação", "Início Assinatura", 
            "Fim Assinatura", "Início Degustação", "Fim Degustação", "Ano Nascimento",
            "Mês Nascimento", "Dia Nascimento", "Hora Nascimento", "Minuto Nascimento",
            "Latitude Nascimento", "Longitude Nascimento"
        ]

        # Formatar os dados para exibir 4 casas decimais na latitude e longitude
        clientes_formatados = []
        for cliente in clientes:
            cliente_formatado = list(cliente)
            cliente_formatado[18] = f"{float(cliente[18]):.4f}" if cliente[18] is not None else "0.0000"
            cliente_formatado[19] = f"{float(cliente[19]):.4f}" if cliente[19] is not None else "0.0000"
            clientes_formatados.append(cliente_formatado)

        # Exibir tabela com formatação aprimorada
        st.dataframe(
            clientes_formatados,
            column_config={i: col for i, col in enumerate(colunas)},
            width=900,
            height=600
        )
    else:
        st.warning("Nenhum cliente encontrado.")
