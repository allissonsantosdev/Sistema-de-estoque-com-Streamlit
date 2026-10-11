import streamlit as st
import database as db
import base64
import sys
from pathlib import Path

# Suporte para caminhos em modo congelado (PyInstaller) e desenvolvimento
if getattr(sys, "frozen", False):
    BASE_DIR = Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
else:
    BASE_DIR = Path(__file__).parent.resolve()

# Configuração da página
def img_tag(caminho: str, tamanho: int = 25) -> str:
    path = BASE_DIR / caminho
    if path.exists():
        b64 = base64.b64encode(path.read_bytes()).decode("utf-8")
        return f'<img src="data:image/png;base64,{b64}" width="{tamanho}" style="vertical-align: middle; margin-right: 8px;">'
    return ""

icone_janela = str(BASE_DIR / "icones" / "wrench.png") if (BASE_DIR / "icones" / "wrench.png").exists() else "wrench"
st.set_page_config(page_title="Sistema de Estoque", 
page_icon=icone_janela,
layout="wide")

st.markdown("""
    <style>
    /* Altera o fundo da área principal da aplicação */
    .stApp {
        background-color: #d3d3d3; /* Cor de fundo principal */
    }
    
    /* Opcional: ajustar os cards para destacar do fundo */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #1A1C23;
        border-color: #2E3340;
    }
    </style>
""", unsafe_allow_html=True)
st.markdown("""
    <style>
    /* Cor global para textos, parágrafos e elementos gerais */
    html, body, [class*="css"], .stApp {
        color: #5c5c5c !important; /* Branco suave / cinza claro */
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    /* Texto das Abas superiores (Consultar, Cadastrar, Atualizar...) */
    button[data-baseweb="tab"] div p {
        color: #ff6600 !important;
        font-size: 16px;
    }
    /* Aba selecionada / ativa */
    button[data-baseweb="tab"][aria-selected="true"] div p {
        color: #ff0000 !important; /* Dourado / Laranja */
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)
# Inicializa a estrutura do banco
db.init_db()

# Cabeçalho centralizado (Logotipo + Título)
logo_html = img_tag("icones/engrenagem.png", tamanho=55)
st.markdown(
    f"""
    <div style="display: flex; align-items: center; justify-content: center; gap: 12px; margin-top: 5px; margin-bottom: 25px;">
        {logo_html}
        <h1 style="margin: 0; padding: 0; font-size: 2.3rem; font-weight: 700; line-height: 1.2;">
            Sistema de Estoque
        </h1>
    </div>
    """,
    unsafe_allow_html=True
)

tabs = st.tabs([
    "Consultar Estoque", 
    "Cadastrar Novo Item", 
    "Entrada de Itens", 
    "Saída de Itens", 
    "Atualizar Item"
])
tab_consulta, tab_cadastro, tab_entrada_item, tab_saida_item, tab_atualizar = tabs

# ----------------------------------------------------
# 1. CONSULTA
# ----------------------------------------------------
with tab_consulta:
    st.subheader("Itens em Estoque")
    pesquisa = st.text_input("Pesquisar por descrição ou localização...","")
    
    df = db.listar_itens()

    if not df.empty:
        if pesquisa.strip():
            df_filtro = df[
                df["descricao"].str.contains(pesquisa, case=False, na=False) |
                df["localizacao"].str.contains(pesquisa, case=False, na=False)
            ]
            df_filtro.rename(columns={"id":"Código", "descricao": "Descrição", "quantidade": "Quantidade", "estado": "Estado", "localizacao": "Localização"}, inplace=True)
            st.dataframe(df_filtro, use_container_width=True, hide_index=True)
            st.caption(f"Itens encontrados: {len(df_filtro)}")
        else:
            df.rename(columns={"id":"Código", "descricao": "Descrição", "quantidade": "Quantidade", "estado": "Estado", "localizacao": "Localização"}, inplace=True)
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.caption(f"Total de itens cadastrados: {len(df)}")
    else:
        st.info("Nenhum item cadastrado no banco de dados.")

        # Excluir Itens
    with st.expander("Gerenciar / Excluir Itens"):
        df_itens = db.listar_itens()

        if df_itens.empty:
            st.info("Nenhum item cadastrado no momento.")
        else:
            with st.form("form_excluir_item", clear_on_submit=True):
            # Mapeia descrição para ID
                opcoes = {f"ID {row['id']} - {row['descricao']}": row['id'] for _, row in df_itens.iterrows()}
                item_selecionado = st.selectbox("Selecione o Item para Excluir*", list(opcoes.keys()))
            
            # Checkbox de confirmação por segurança operacional
                confirmar = st.checkbox("Confirmo que desejo apagar permanentemente este item")
            
            
                btn_excluir = st.form_submit_button("Excluir Item", type="primary")

                if btn_excluir:
                    if not confirmar:
                        st.warning("Marque a caixa de confirmação para poder excluir.")
                    else:
                        id_item = opcoes[item_selecionado]
                        try:
                            db.deletar_item(id_item)
                            st.success("Item excluído com sucesso!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erro ao excluir: {e}")
# ----------------------------------------------------
# 2. NOVO CADASTRO
# ----------------------------------------------------
with tab_cadastro:
    st.subheader("Novo Cadastro")

    with st.form("form_novo_item", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            descricao = st.text_input("Descrição *", placeholder="Ex: Disjuntor Tripolar 63A Curva C")
            estado = st.selectbox("Estado do item", ["Novo", "Usado", "Recondicionado", "Danificado"])

        with col2:
            quantidade = st.number_input("Quantidade Inicial", min_value=0, step=1, value=1)
            localizacao = st.selectbox("Localização *", [
                "Prateleira A",
                "Prateleira B",
                "Prateleira C",
                "Prateleira D",
                "Armário A",
                "Armário B",
                "Armário C",
                "Armário D",
                "Gaveta A",
                "Gaveta B",
                "Gaveta C",
                "Gaveta D",
                "Armário Geral",
                "Gaveta Geral"
            ])

        enviado = st.form_submit_button("Salvar no estoque", use_container_width=True)

        if enviado:
            if not descricao.strip():
                st.error("O campo 'Descrição' é obrigatório!")
            else:
                try:
                    db.adicionar_item(descricao.strip(), int(quantidade), estado.strip(), localizacao.strip())
                    st.success(f"Item '{descricao}' cadastrado com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao salvar no estoque: {e}")

# ----------------------------------------------------
# 3. ENTRADA DE ITENS
# ----------------------------------------------------
with tab_entrada_item:
    st.subheader("Entrada de Itens")
    df_itens = db.listar_itens()

    if not df_itens.empty:
        opcoes = {f"ID {row['id']} - {row['descricao']} (Saldo atual: {row['quantidade']})": row['id'] for _, row in df_itens.iterrows()}
        
        with st.form("form_entrada_item", clear_on_submit=True):
            item_selecionado = st.selectbox("Selecione o Item para Adicionar Saldo*", list(opcoes.keys()))
            qtd_entrada = st.number_input("Quantidade a Adicionar", min_value=1, step=1, value=1)

            btn_adicionar = st.form_submit_button("Confirmar Entrada", use_container_width=True)

            if btn_adicionar:
                id_item = opcoes[item_selecionado]
                try:
                    db.incrementar_item(id_item, int(qtd_entrada))
                    st.success("Saldo atualizado com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao atualizar: {e}")
    else:
        st.info("Cadastre itens no estoque primeiro para registrar entradas.")

# ----------------------------------------------------
# 4. SAÍDA DE ITENS (CORRIGIDO PARA BLOQUEAR)
# ----------------------------------------------------
with tab_saida_item:
    st.subheader("Saída de Itens (Baixa)")
    df_itens = db.listar_itens()
    if not df_itens.empty:
        opcoes = {f"ID {row['id']} - {row['descricao']} (Saldo atual: {row['quantidade']})": (row['id'], int(row['quantidade'])) for _, row in df_itens.iterrows()}
        
        with st.form("form_saida_item", clear_on_submit=False):
            item_selecionado = st.selectbox("Selecione o Item para Dar Baixa*", list(opcoes.keys()))
            qtd_saida = st.number_input("Quantidade a Retirar", min_value=1, step=1, value=1)
            btn_remover = st.form_submit_button("Confirmar Saída", use_container_width=True)
            
            if btn_remover:
                id_item, saldo_atual = opcoes[item_selecionado]
                if saldo_atual <= 0:
                    st.error("❌ Operação cancelada! Este item não possui unidades disponíveis em estoque.")
                elif qtd_saida > saldo_atual:
                    st.error(f"❌ Operação cancelada! Quantidade solicitada ({qtd_saida}) é maior que o saldo em estoque ({saldo_atual}).")
                else:
                    try:
                        db.decrementar_item(id_item, int(qtd_saida))
                        st.success(f"✅ Baixa de {qtd_saida} unidade(s) realizada com sucesso!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao registrar baixa: {e}")
    else:
        st.info("Nenhum item cadastrado para realizar baixa.")

# ----------------------------------------------------
# 5. ATUALIZAR ITEM
# ----------------------------------------------------
with tab_atualizar:
    st.subheader("Atualizar Item")
    df_itens = db.listar_itens()

    if not df_itens.empty:
        opcoes = {
            f"ID {row['id']} - {row['descricao']} (Saldo: {row['quantidade']})": row['id']
            for _, row in df_itens.iterrows()
        }

        item_selecionado = st.selectbox(
            "Selecione o Item para Atualizar*",
            list(opcoes.keys()),
            key="select_item_atualizar"
        )

        id_selecionado = opcoes[item_selecionado]
        item_dados = df_itens[df_itens["id"] == id_selecionado].iloc[0]

        lista_estados = ["Novo", "Usado", "Recondicionado", "Danificado"]
        lista_localizacoes = [
            "Prateleira A",
            "Prateleira B",
            "Prateleira C",
            "Prateleira D",
            "Armário A",
            "Armário B",
            "Armário C",
            "Armário D",
            "Gaveta A",
            "Gaveta B",
            "Gaveta C",
            "Gaveta D",
            "Armário Geral",
            "Gaveta Geral"
        ]

        idx_estado = lista_estados.index(item_dados["estado"]) if item_dados["estado"] in lista_estados else 0
        if item_dados["localizacao"] not in lista_localizacoes:
            lista_localizacoes.insert(0, str(item_dados["localizacao"]))
            idx_loc = 0
        else:
            idx_loc = lista_localizacoes.index(item_dados["localizacao"])

        with st.form("form_atualizar_item"):
            col1, col2 = st.columns(2)
            with col1:
                nova_descricao = st.text_input(
                    "Descrição *",
                    value=str(item_dados["descricao"]),
                    key=f"edit_desc_{id_selecionado}"
                )
                novo_estado = st.selectbox(
                    "Estado do item",
                    lista_estados,
                    index=idx_estado,
                    key=f"edit_estado_{id_selecionado}"
                )

            with col2:
                nova_quantidade = st.number_input(
                    "Quantidade em Estoque",
                    min_value=0,
                    step=1,
                    value=int(item_dados["quantidade"]),
                    key=f"edit_qtd_{id_selecionado}"
                )
                nova_localizacao = st.selectbox(
                    "Localização *",
                    lista_localizacoes,
                    index=idx_loc,
                    key=f"edit_loc_{id_selecionado}"
                )

            btn_atualizar = st.form_submit_button("Salvar Alterações", use_container_width=True, type="primary")

            if btn_atualizar:
                if not nova_descricao.strip():
                    st.error("O campo 'Descrição' não pode ficar vazio!")
                else:
                    try:
                        db.atualizar_item(
                            id_selecionado,
                            nova_descricao.strip(),
                            int(nova_quantidade),
                            novo_estado.strip(),
                            nova_localizacao.strip()
                        )
                        st.success(f"Item #{id_selecionado} atualizado com sucesso!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao atualizar o item: {e}")
    else:
        st.info("Nenhum item cadastrado no estoque para atualizar.")



