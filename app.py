import streamlit as st

st.set_page_config(page_title="Gestão de Estoque", page_icon="📦", layout="wide")

if "estoque" not in st.session_state:
    st.session_state.estoque = {
        "PROD001": {"nome": "Camiseta Básica", "quantidade": 15, "preco": 49.90, "categoria": "Vestuário"},
        "PROD002": {"nome": "Tênis Nike", "quantidade": 8, "preco": 199.90, "categoria": "Calçados"},
        "PROD003": {"nome": "Colar", "quantidade": 50, "preco": 80.90, "categoria": "Acessorios"},
        "PROD004": {"nome": "Relogio", "quantidade": 100, "preco": 209.90, "categoria": "Acessorios Ginez"},
        "PROD005": {"nome": "Calça Beggy Cinza Moletom", "quantidade": 35, "preco": 149.90, "categoria": "Calças"}

    }

st.title("📦 Sistema de Gestão de Estoque")

opcao = st.sidebar.selectbox("Navegação", ["Cadastrar Produto", "Visualizar Estoque", "Atualizar / Remover"])

if opcao == "Cadastrar Produto":
    st.subheader("Novo Cadastro")
    
    with st.form("form_cadastro", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            sku = st.text_input("Código (SKU)").strip().upper()
            nome = st.text_input("Nome do Produto")
            categoria = st.selectbox("Categoria", ["Vestuário", "Calçados", "Acessórios", "Outros"])
            
        with col2:
            quantidade = st.number_input("Quantidade Inicial", min_value=0, step=1)
            preco = st.number_input("Preço (R$)", min_value=0.0, step=0.50, format="%.2f")
            
        submitted = st.form_submit_button("Cadastrar no Dicionário")
        
        if submitted:
            if not sku or not nome:
                st.warning("Preencha o SKU e o Nome do produto!")
            elif sku in st.session_state.estoque:
                st.error("Já existe um produto com este código SKU.")
            else:
                st.session_state.estoque[sku] = {
                    "nome": nome,
                    "quantidade": quantidade,
                    "preco": preco,
                    "categoria": categoria
                }
                st.success(f"Produto '{nome}' cadastrado com sucesso!")

elif opcao == "Visualizar Estoque":
    st.subheader("Itens em Estoque")
    
    if not st.session_state.estoque:
        st.info("Nenhum produto cadastrado até o momento.")
    else:
        total_itens = sum(item["quantidade"] for item in st.session_state.estoque.values())
        valor_total = sum(item["quantidade"] * item["preco"] for item in st.session_state.estoque.values())
        
        col_a, col_b = st.columns(2)
        col_a.metric("Total de Itens em Estoque", total_itens)
        col_b.metric("Valor Total Armazenado", f"R$ {valor_total:,.2f}")
        
        st.divider()
        
        dados_tabela = []
        for codigo, info in st.session_state.estoque.items():
            dados_tabela.append({
                "SKU": codigo,
                "Nome": info["nome"],
                "Categoria": info["categoria"],
                "Qtd": info["quantidade"],
                "Preço Un. (R$)": f"{info['preco']:.2f}",
                "Subtotal (R$)": f"{info['quantidade'] * info['preco']:.2f}"
            })
            
        st.dataframe(dados_tabela, use_container_width=True)

elif opcao == "Atualizar / Remover":
    st.subheader("Gerenciar Produto Existente")
    
    if not st.session_state.estoque:
        st.info("Estoque vazio.")
    else:
        sku_selecionado = st.selectbox("Selecione o Código (SKU)", list(st.session_state.estoque.keys()))
        prod = st.session_state.estoque[sku_selecionado]
        
        st.write(f"**Produto atual:** {prod['nome']} | **Categoria:** {prod['categoria']}")
        
        col_esq, col_dir = st.columns(2)
        
        with col_esq:
            nova_qtd = st.number_input("Nova Quantidade", min_value=0, value=prod["quantidade"], step=1)
            if st.button("Atualizar Quantidade"):
                st.session_state.estoque[sku_selecionado]["quantidade"] = nova_qtd
                st.success("Quantidade atualizada!")
                st.rerun()
                
        with col_dir:
            st.write("---")
            if st.button("🔴 Remover Produto do Estoque", type="secondary"):
                del st.session_state.estoque[sku_selecionado]
                st.warning("Produto removido do dicionário.")
                st.rerun()