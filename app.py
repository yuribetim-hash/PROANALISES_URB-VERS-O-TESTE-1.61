import streamlit as st
import os
import json
from io import BytesIO
from datetime import datetime
from docxtpl import DocxTemplate, RichText

st.set_page_config(
    page_title="Proanalisis v1.3",
    page_icon="📐",
    layout="wide"
)

# ============================================
# CARREGAR TEMA
# ============================================
def carregar_tema(caminho="tema.json"):
    """Carrega o tema do arquivo JSON ou usa valores padrão"""
    tema_padrao = {
        "cores": {
            "primaria": "#0a2a3a",
            "primaria_clara": "#1a5276",
            "primaria_muito_escura": "#051a24",
            "secundaria": "#2c6b96",
            "sucesso": "#0d6e2e",
            "erro": "#b42318",
            "alerta": "#b54708",
            "info": "#175cd3",
            "fundo_claro": "#f8fafd",
            "fundo_branco": "#ffffff",
            "texto_principal": "#1a1a1a",
            "texto_secundario": "#2c3e50",
            "texto_titulo": "#051a24",
            "fundo_app": "linear-gradient(135deg, #e8f0fe 0%, #d4e4fc 100%)",
            "sidebar_fundo": "linear-gradient(180deg, #0a2a3a 0%, #051a24 100%)"
        },
        "status": {
            "conforme": {"fundo": "#ecfdf3", "borda": "#067647", "texto": "#067647", "icone": "✅"},
            "inconforme": {"fundo": "#fef3f2", "borda": "#b42318", "texto": "#7a271a", "icone": "⛔"},
            "pendente": {"fundo": "#fffaeb", "borda": "#b54708", "texto": "#7a4a0a", "icone": "⏳"},
            "nao_se_enquadra": {"fundo": "#eff6ff", "borda": "#175cd3", "texto": "#0e4a8a", "icone": "ℹ️"}
        },
        "botoes": {
            "primario_fundo": "#0d6e2e",
            "primario_fundo_hover": "#0f8a3a",
            "secundario_fundo": "#0a2a3a",
            "secundario_fundo_hover": "#1a5276",
            "texto": "#ffffff"
        },
        "fontes": {
            "titulo_principal": "24px",
            "subtitulo": "20px",
            "texto_normal": "14px",
            "texto_pequeno": "12px"
        }
    }
    
    if os.path.exists(caminho):
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                tema_custom = json.load(f)
                # Mescla com o tema padrão (preserva valores não informados)
                for key in tema_padrao:
                    if key in tema_custom:
                        if isinstance(tema_padrao[key], dict):
                            tema_padrao[key].update(tema_custom[key])
                        else:
                            tema_padrao[key] = tema_custom[key]
        except Exception as e:
            st.warning(f"Erro ao carregar tema.json: {e}. Usando tema padrão.")
    
    return tema_padrao

tema = carregar_tema()

# ============================================
# JAVASCRIPT PARA CORRIGIR O DROPDOWN
# ============================================
st.markdown("""
<script>
document.addEventListener('DOMContentLoaded', function() {
    function styleDropdowns() {
        const dropdowns = document.querySelectorAll('[data-baseweb="menu"]');
        dropdowns.forEach(dropdown => {
            dropdown.style.backgroundColor = '#1a1a2e';
            dropdown.style.border = '1px solid #2c6b96';
            dropdown.style.borderRadius = '8px';
            dropdown.style.boxShadow = '0 4px 12px rgba(0,0,0,0.3)';
            
            const options = dropdown.querySelectorAll('[role="option"]');
            options.forEach(option => {
                option.style.backgroundColor = '#1a1a2e';
                option.style.color = 'white';
                option.style.padding = '8px 16px';
                option.style.cursor = 'pointer';
                
                if (option.getAttribute('aria-selected') === 'true') {
                    option.style.backgroundColor = '#0d6e2e';
                }
                
                option.addEventListener('mouseenter', function() {
                    this.style.backgroundColor = '#2c6b96';
                    this.style.color = 'white';
                });
                option.addEventListener('mouseleave', function() {
                    if (this.getAttribute('aria-selected') === 'true') {
                        this.style.backgroundColor = '#0d6e2e';
                    } else {
                        this.style.backgroundColor = '#1a1a2e';
                    }
                    this.style.color = 'white';
                });
            });
        });
    }
    
    const observer = new MutationObserver(function(mutations) {
        styleDropdowns();
    });
    
    observer.observe(document.body, { childList: true, subtree: true });
    styleDropdowns();
});
</script>
""", unsafe_allow_html=True)

# ============================================
# CSS PERSONALIZADO COM TEMA
# ============================================
css_tema = f"""
<style>
    /* Fundo principal da aplicação */
    .stApp {{
        background: {tema["cores"]["fundo_app"]};
    }}
    
    /* Fundo dos containers principais */
    .main > div {{
        background-color: {tema["cores"]["fundo_branco"]};
        border-radius: 12px;
        padding: 1rem;
    }}
    
    /* Sidebar */
    [data-testid="stSidebar"] {{
        background: {tema["cores"]["sidebar_fundo"]};
    }}
    
    [data-testid="stSidebar"] * {{
        color: {tema["botoes"]["texto"]} !important;
    }}
    
    /* Títulos principais */
    h1 {{
        color: {tema["cores"]["texto_titulo"]} !important;
        font-weight: 700 !important;
        font-size: {tema["fontes"]["titulo_principal"]} !important;
    }}
    
    h2, h3, h4 {{
        color: {tema["cores"]["primaria"]} !important;
        font-weight: 600 !important;
    }}
    
    /* Subtítulos */
    .stCaption {{
        color: {tema["cores"]["texto_secundario"]} !important;
    }}
    
    /* Campos de input */
    .stTextInput input, .stTextArea textarea, .stNumberInput input {{
        background-color: {tema["cores"]["fundo_branco"]} !important;
        color: {tema["cores"]["texto_principal"]} !important;
        border: 1px solid #c5d5e6 !important;
        border-radius: 6px !important;
    }}
    
    /* Select box */
    .stSelectbox select {{
        background-color: {tema["cores"]["fundo_branco"]} !important;
        color: {tema["cores"]["texto_principal"]} !important;
        border: 1px solid #c5d5e6 !important;
        border-radius: 6px !important;
    }}
    
    /* Labels */
    .stTextInput label, .stSelectbox label, .stTextArea label, .stNumberInput label {{
        color: {tema["cores"]["primaria"]} !important;
        font-weight: 600 !important;
    }}
    
    /* Botões */
    .stButton > button {{
        border-radius: 8px !important;
        font-weight: 600 !important;
        color: {tema["botoes"]["texto"]} !important;
        border: none !important;
        transition: all 0.3s ease !important;
    }}
    
    .stButton > button[kind="primary"] {{
        background-color: {tema["botoes"]["primario_fundo"]} !important;
    }}
    
    .stButton > button[kind="primary"]:hover {{
        background-color: {tema["botoes"]["primario_fundo_hover"]} !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }}
    
    .stButton > button:not([kind="primary"]) {{
        background-color: {tema["botoes"]["secundario_fundo"]} !important;
    }}
    
    .stButton > button:not([kind="primary"]):hover {{
        background-color: {tema["botoes"]["secundario_fundo_hover"]} !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }}
    
    /* Progresso */
    .progress-wrap {{
        width: 100%;
        background: #e9ecef;
        border-radius: 999px;
        height: 14px;
        overflow: hidden;
        margin: 8px 0;
    }}
    
    .progress-bar {{
        height: 14px;
        border-radius: 999px;
        transition: width 0.3s ease;
    }}
    
    /* Status badges - texto escuro com fundo suave */
    .status-badge-conforme {{
        background-color: {tema["status"]["conforme"]["fundo"]};
        border-left: 4px solid {tema["status"]["conforme"]["borda"]};
        padding: 10px 12px;
        border-radius: 6px;
        margin-top: 8px;
        color: {tema["status"]["conforme"]["texto"]};
        font-weight: 600;
    }}
    
    .status-badge-inconforme {{
        background-color: {tema["status"]["inconforme"]["fundo"]};
        border-left: 4px solid {tema["status"]["inconforme"]["borda"]};
        padding: 10px 12px;
        border-radius: 6px;
        margin-top: 8px;
        color: {tema["status"]["inconforme"]["texto"]};
        font-weight: 600;
    }}
    
    .status-badge-pendente {{
        background-color: {tema["status"]["pendente"]["fundo"]};
        border-left: 4px solid {tema["status"]["pendente"]["borda"]};
        padding: 10px 12px;
        border-radius: 6px;
        margin-top: 8px;
        color: {tema["status"]["pendente"]["texto"]};
        font-weight: 600;
    }}
    
    .status-badge-na {{
        background-color: {tema["status"]["nao_se_enquadra"]["fundo"]};
        border-left: 4px solid {tema["status"]["nao_se_enquadra"]["borda"]};
        padding: 10px 12px;
        border-radius: 6px;
        margin-top: 8px;
        color: {tema["status"]["nao_se_enquadra"]["texto"]};
        font-weight: 600;
    }}
    
    /* Cards */
    .card {{
        padding: 0.8rem 1rem;
        border: 1px solid #c5d5e6;
        border-radius: 10px;
        background: {tema["cores"]["fundo_claro"]};
        margin-bottom: 0.6rem;
        color: {tema["cores"]["texto_principal"]};
    }}
    
    /* DROPDOWN */
    div[data-baseweb="menu"] {{
        background-color: #1a1a2e !important;
        border: 1px solid #2c6b96 !important;
        border-radius: 8px !important;
    }}
    
    div[data-baseweb="menu"] div {{
        background-color: #1a1a2e !important;
        color: white !important;
        padding: 8px 16px !important;
    }}
    
    div[data-baseweb="menu"] div:hover {{
        background-color: #2c6b96 !important;
        color: white !important;
    }}
    
    div[data-baseweb="menu"] div[aria-selected="true"] {{
        background-color: #0d6e2e !important;
        color: white !important;
    }}
    
    hr {{
        border-color: #c5d5e6 !important;
    }}
    
    /* Textos em geral */
    p, li, .stMarkdown, .stText {{
        color: {tema["cores"]["texto_secundario"]};
    }}
    
    /* Informações e avisos */
    .stInfo, .stSuccess, .stWarning, .stError {{
        border-radius: 8px !important;
    }}
    
    /* Métricas */
    [data-testid="stMetric"] {{
        background-color: {tema["cores"]["fundo_claro"]};
        border-radius: 8px;
        padding: 10px;
        border: 1px solid #c5d5e6;
    }}
    
    [data-testid="stMetric"] label {{
        color: {tema["cores"]["primaria"]} !important;
        font-weight: 600 !important;
    }}
    
    [data-testid="stMetric"] .stMetricValue {{
        color: {tema["cores"]["texto_principal"]} !important;
        font-weight: 700 !important;
    }}
    
    /* Expanders */
    .streamlit-expanderHeader {{
        background-color: {tema["cores"]["fundo_claro"]} !important;
        color: {tema["cores"]["primaria"]} !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
    }}
    
    .streamlit-expanderContent {{
        background-color: {tema["cores"]["fundo_branco"]} !important;
        border-radius: 0 0 8px 8px !important;
    }}
</style>
"""

st.markdown(css_tema, unsafe_allow_html=True)

# -------------------------
# USUÁRIOS VIA TXT
# -------------------------
def carregar_usuarios(caminho="usuarios.txt"):
    if not os.path.exists(caminho):
        st.error("Arquivo usuarios.txt não encontrado.")
        st.stop()

    usuarios = {}

    with open(caminho, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if not linha or ";" not in linha:
                continue
            usuario, senha = linha.split(";", 1)
            usuarios[usuario.strip()] = senha.strip()

    return usuarios


def tela_login():
    st.title("📐 Proanalisis v1.3")
    st.caption("Sistema de análise urbanística e geração de parecer técnico")

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("### Acesso ao sistema")
        usuarios = carregar_usuarios()

        user = st.text_input("Usuário", key="login_user")
        senha = st.text_input("Senha", type="password", key="login_senha")

        if st.button("Entrar", use_container_width=True, key="btn_login"):
            if user in usuarios and usuarios[user] == senha:
                st.session_state["logado"] = True
                st.session_state["usuario"] = user
                st.rerun()
            else:
                st.error("Usuário ou senha inválidos.")


if "logado" not in st.session_state:
    st.session_state["logado"] = False

if not st.session_state["logado"]:
    tela_login()
    st.stop()

# -------------------------
# SIDEBAR
# -------------------------
st.sidebar.title("📐 Proanalisis v1.3")
st.sidebar.write(f"👤 {st.session_state['usuario']}")

if st.sidebar.button("🚪 Sair", use_container_width=True, key="btn_sair"):
    st.session_state["logado"] = False
    st.session_state.pop("dados_antigos", None)
    st.rerun()

# -------------------------
# HISTÓRICO
# -------------------------
def get_pasta_protocolo(protocolo):
    protocolo_limpo = protocolo.replace("/", "-").strip()
    return os.path.join("dados", protocolo_limpo)

def listar_analises(protocolo):
    pasta = get_pasta_protocolo(protocolo)
    if not os.path.exists(pasta):
        return []

    arquivos = os.listdir(pasta)
    analises = [f for f in arquivos if f.startswith("AN") and f.endswith(".json")]

    def ordem(nome):
        try:
            return int(nome.replace("AN", "").replace(".json", ""))
        except ValueError:
            return 999999

    analises.sort(key=ordem)
    return analises

def carregar_ultima_analise(protocolo):
    analises = listar_analises(protocolo)
    if not analises:
        return None

    caminho = os.path.join(get_pasta_protocolo(protocolo), analises[-1])
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)

def sugerir_proxima_analise(protocolo):
    analises = listar_analises(protocolo)
    if not analises:
        return "0"

    ultima = analises[-1]
    try:
        numero = int(ultima.replace("AN", "").replace(".json", ""))
        return str(numero + 1)
    except ValueError:
        return "0"

def salvar_historico(dados, respostas, observacoes, conclusao, analista, n_analise, arquivo_docx, pendencias_manuais):
    pasta = get_pasta_protocolo(dados["protocolo"])
    os.makedirs(pasta, exist_ok=True)

    base = f"AN{n_analise}"

    registro = {
        "protocolo": dados["protocolo"],
        "n_analise": n_analise,
        "data": datetime.now().strftime("%d/%m/%Y"),
        "analista": analista,
        "usuario": st.session_state["usuario"],
        "dados": dados,
        "respostas": respostas,
        "observacoes": observacoes,
        "pendencias_manuais": pendencias_manuais,
        "conclusao": conclusao
    }

    with open(os.path.join(pasta, f"{base}.json"), "w", encoding="utf-8") as f:
        json.dump(registro, f, indent=4, ensure_ascii=False)

    with open(os.path.join(pasta, f"{base}.docx"), "wb") as f:
        f.write(arquivo_docx.getvalue())

# -------------------------
# PERGUNTAS
# -------------------------
def carregar_perguntas_txt(caminho="perguntas.txt"):
    if not os.path.exists(caminho):
        st.error("Arquivo perguntas.txt não encontrado.")
        st.stop()

    perguntas = []
    bloco = {}

    with open(caminho, "r", encoding="utf-8") as f:
        linhas = f.readlines()

    for linha in linhas:
        linha = linha.strip()

        if not linha:
            if bloco:
                perguntas.append(bloco)
                bloco = {}
            continue

        if linha.startswith("GRUPO:"):
            bloco["grupo"] = linha.replace("GRUPO:", "").strip()
        elif linha.startswith("ID:"):
            bloco["id"] = linha.replace("ID:", "").strip()
        elif linha.startswith("PERGUNTA:"):
            bloco["pergunta"] = linha.replace("PERGUNTA:", "").strip()
        elif linha.startswith("OPCOES:"):
            bloco["opcoes"] = [op.strip() for op in linha.replace("OPCOES:", "").strip().split(";")]
        elif linha.startswith("CONFORMES:"):
            bloco["conformes"] = [op.strip() for op in linha.replace("CONFORMES:", "").strip().split(";")]
        elif linha.startswith("REGRA_"):
            chave, valor = linha.split(":", 1)
            resposta = chave.replace("REGRA_", "").strip()
            bloco.setdefault("regras", {})[resposta] = {"texto": valor.strip()}

    if bloco:
        perguntas.append(bloco)

    return perguntas


def validar_ids_repetidos(perguntas):
    ids = [p.get("id", "").strip() for p in perguntas if p.get("id", "").strip()]
    return sorted({i for i in ids if ids.count(i) > 1})


perguntas = carregar_perguntas_txt("perguntas.txt")
ids_repetidos = validar_ids_repetidos(perguntas)
if ids_repetidos:
    st.error("Há IDs repetidos no perguntas.txt: " + ", ".join(ids_repetidos))
    st.stop()

# -------------------------
# FUNÇÕES
# -------------------------
def resposta_preenchida(valor):
    return valor not in ("", None, "Selecione...")

def definir_conclusao(respostas, pendencias_manuais=None):
    for p in perguntas:
        resposta = respostas.get(p["id"])
        if not resposta_preenchida(resposta):
            continue
        conformes = p.get("conformes", ["Sim", "Não se enquadra"])
        if resposta not in conformes and resposta in p.get("regras", {}):
            return "DESFAVORÁVEL"
    
    if pendencias_manuais:
        for grupo, pendencias in pendencias_manuais.items():
            if isinstance(pendencias, list):
                for pendencia in pendencias:
                    if pendencia and pendencia.strip():
                        return "DESFAVORÁVEL"
            elif pendencias and pendencias.strip():
                return "DESFAVORÁVEL"
    
    return "FAVORÁVEL"


def montar_inconformidades_por_grupo(respostas, observacoes, pendencias_manuais=None):
    grupos = {}

    for p in perguntas:
        pid = p["id"]
        resp = respostas.get(pid)
        if not resposta_preenchida(resp):
            continue

        conformes = p.get("conformes", ["Sim", "Não se enquadra"])
        if resp not in conformes and resp in p.get("regras", {}):
            grupo = p["grupo"]
            texto = p["regras"][resp]["texto"]
            obs = observacoes.get(pid, "").strip()
            if obs:
                texto += f"\nObservação: {obs}"
            grupos.setdefault(grupo, []).append(texto)
    
    if pendencias_manuais:
        for grupo, pendencias in pendencias_manuais.items():
            if isinstance(pendencias, list):
                for pendencia in pendencias:
                    if pendencia and pendencia.strip():
                        grupos.setdefault(grupo, []).append(pendencia)
            elif pendencias and pendencias.strip():
                grupos.setdefault(grupo, []).append(pendencias)

    return grupos


def montar_inconformidades_rt(respostas, observacoes, pendencias_manuais=None):
    grupos = montar_inconformidades_por_grupo(respostas, observacoes, pendencias_manuais)

    rt = RichText()
    contador = 1

    if grupos:
        for grupo, itens in grupos.items():
            rt.add(grupo.upper(), bold=True)
            rt.add("\n\n")
            for item in itens:
                rt.add(f"{contador}. {item}")
                rt.add("\n\n")
                contador += 1
    else:
        rt.add("Não foram identificadas inconformidades.")

    return rt


def gerar_docx(dados, respostas, observacoes, conclusao, analista, matricula, setor, n_analise, pendencias_manuais=None):
    if not os.path.exists("modelo_parecer.docx"):
        st.error("Arquivo modelo_parecer.docx não encontrado.")
        st.stop()

    doc = DocxTemplate("modelo_parecer.docx")
    inconformidades_rt = montar_inconformidades_rt(respostas, observacoes, pendencias_manuais)

    matriculas_str = dados.get("matriculas", "")
    if isinstance(matriculas_str, list):
        matriculas_str = ", ".join(matriculas_str)

    context = {
        "protocolo": dados["protocolo"],
        "tipo": dados["tipo"],
        "interessado": dados["interessado"],
        "n_lotes": dados["n_lotes"],
        "matriculas": matriculas_str,
        "inconformidades": inconformidades_rt,
        "conclusao": conclusao,
        "data": f"Data: {datetime.now().strftime('%d/%m/%Y')}",
        "analista": f"Analista: {analista}",
        "matricula": matricula,
        "setor": setor,
        "n_analise": n_analise
    }

    doc.render(context)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer


def resumo_status_pergunta(p, resposta):
    if not resposta_preenchida(resposta):
        return "pendente"

    conformes = p.get("conformes", ["Sim", "Não se enquadra"])

    if resposta == "Não se enquadra":
        return "na"
    if resposta in conformes:
        return "conforme"
    if resposta in p.get("regras", {}):
        return "inconforme"
    return "neutro"


def progresso_percentual(respostas):
    total = len(perguntas)
    preenchidas = sum(1 for v in respostas.values() if resposta_preenchida(v))
    if total == 0:
        return 0, 0, 0.0
    pct = preenchidas / total
    return preenchidas, total, pct


def cor_progresso(pct):
    r = int(255 * (1 - pct))
    g = int(180 * pct + 60)
    b = 60
    return f"rgb({r},{g},{b})"


def render_progresso(preenchidas, total, pct, destino):
    cor = cor_progresso(pct)
    html = f"""
    <div><b>{preenchidas}/{total}</b> respostas preenchidas ({int(pct*100)}%)</div>
    <div class="progress-wrap">
        <div class="progress-bar" style="width:{pct*100:.1f}%; background:{cor};"></div>
    </div>
    """
    destino.markdown(html, unsafe_allow_html=True)


def render_status_badge(status):
    """Renderiza o badge de status com as cores do tema"""
    if status == "conforme":
        st.markdown(f"""
        <div class='status-badge-conforme'>
            {tema["status"]["conforme"]["icone"]} <strong>CONFORME</strong>
        </div>
        """, unsafe_allow_html=True)
    elif status == "inconforme":
        st.markdown(f"""
        <div class='status-badge-inconforme'>
            {tema["status"]["inconforme"]["icone"]} <strong>INCONFORME</strong>
        </div>
        """, unsafe_allow_html=True)
    elif status == "pendente":
        st.markdown(f"""
        <div class='status-badge-pendente'>
            {tema["status"]["pendente"]["icone"]} <strong>PENDENTE</strong>
        </div>
        """, unsafe_allow_html=True)
    elif status == "na":
        st.markdown(f"""
        <div class='status-badge-na'>
            {tema["status"]["nao_se_enquadra"]["icone"]} <strong>NÃO SE ENQUADRA</strong>
        </div>
        """, unsafe_allow_html=True)


def inicializar_estados():
    if "dados_antigos" not in st.session_state:
        st.session_state["dados_antigos"] = None
    if "etapa" not in st.session_state:
        st.session_state["etapa"] = "1. Protocolo"
    if "protocolo" not in st.session_state:
        st.session_state["protocolo"] = ""
    if "tipo" not in st.session_state:
        st.session_state["tipo"] = "Loteamento"
    if "interessado" not in st.session_state:
        st.session_state["interessado"] = ""
    if "n_lotes" not in st.session_state:
        st.session_state["n_lotes"] = 1
    if "matriculas" not in st.session_state:
        st.session_state["matriculas"] = ""
    if "analista" not in st.session_state:
        st.session_state["analista"] = ""
    if "matricula_analista" not in st.session_state:
        st.session_state["matricula_analista"] = ""
    if "setor" not in st.session_state:
        st.session_state["setor"] = ""
    if "n_analise" not in st.session_state:
        st.session_state["n_analise"] = ""
    if "pendencias_manuais" not in st.session_state:
        st.session_state["pendencias_manuais"] = {}


inicializar_estados()

# -------------------------
# CABEÇALHO
# -------------------------
st.title("📐 Proanalisis v1.3")
st.caption("Análise urbanística padronizada com geração de parecer técnico")

etapas = ["1. Protocolo", "2. Analista", "3. Análise", "4. Revisão", "5. Gerar parecer"]

etapa_atual = st.sidebar.radio("📋 Etapas", etapas, index=etapas.index(st.session_state["etapa"]))
if etapa_atual != st.session_state["etapa"]:
    st.session_state["etapa"] = etapa_atual
    st.rerun()

# -------------------------
# ETAPA 1 - PROTOCOLO
# -------------------------
if st.session_state["etapa"] == "1. Protocolo":
    st.header("📋 Dados do protocolo")

    protocolo = st.text_input("N° Protocolo", value=st.session_state["protocolo"], key="protocolo_input")
    if protocolo != st.session_state["protocolo"]:
        st.session_state["protocolo"] = protocolo

    st.subheader("🏢 Dados do empreendimento")
    
    tipo = st.selectbox("Tipo do Empreendimento", ["Loteamento", "Condomínio fechado de lotes"], 
                        index=0 if st.session_state["tipo"] == "Loteamento" else 1, key="tipo_select")
    st.session_state["tipo"] = tipo
    
    interessado = st.text_input("Requerente", value=st.session_state["interessado"], key="interessado_input")
    st.session_state["interessado"] = interessado
    
    n_lotes = st.number_input("Número de Lotes", min_value=1, value=st.session_state["n_lotes"], key="n_lotes_input")
    st.session_state["n_lotes"] = n_lotes
    
    matriculas = st.text_area("Matrícula(s) do Empreendimento", value=st.session_state["matriculas"], 
                               key="matriculas_input", placeholder="Digite a(s) matrícula(s) separadas por vírgula")
    st.session_state["matriculas"] = matriculas

    st.markdown("---")
    
    if st.session_state["protocolo"]:
        ultima = carregar_ultima_analise(st.session_state["protocolo"])
        if ultima:
            st.info(f"📋 Última análise encontrada: AN{ultima['n_analise']}")
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("▶️ Continuar análise", use_container_width=True):
                    st.session_state["dados_antigos"] = ultima
                    st.session_state["tipo"] = ultima["dados"].get("tipo", "Loteamento")
                    st.session_state["interessado"] = ultima["dados"].get("interessado", "")
                    st.session_state["n_lotes"] = int(ultima["dados"].get("n_lotes", 1))
                    st.session_state["matriculas"] = ultima["dados"].get("matriculas", "")
                    st.session_state["etapa"] = "2. Analista"
                    st.rerun()
            with col_b:
                if st.button("➕ Iniciar nova análise", use_container_width=True):
                    st.session_state["dados_antigos"] = None
                    st.session_state["etapa"] = "2. Analista"
                    st.rerun()
        else:
            st.success("✅ Nenhum histórico encontrado para este protocolo.")
            if st.button("Prosseguir →", use_container_width=True, type="primary"):
                if st.session_state["protocolo"] and st.session_state["interessado"]:
                    st.session_state["etapa"] = "2. Analista"
                    st.rerun()
                else:
                    st.error("⚠️ Preencha o protocolo e o requerente")
    else:
        st.warning("⚠️ Informe o número do protocolo para continuar.")

# -------------------------
# ETAPA 2 - ANALISTA
# -------------------------
elif st.session_state["etapa"] == "2. Analista":
    st.header("👤 Dados do analista")
    
    st.info(f"📌 Protocolo: **{st.session_state['protocolo']}** | Empreendimento: **{st.session_state['interessado']}**")

    analista = st.text_input("Nome do Analista", value=st.session_state["analista"], key="analista_input")
    st.session_state["analista"] = analista
    
    matricula_analista = st.text_input("Matrícula do Analista", value=st.session_state["matricula_analista"], key="matricula_analista_input")
    st.session_state["matricula_analista"] = matricula_analista
    
    setor = st.text_input("Setor", value=st.session_state["setor"], key="setor_input")
    st.session_state["setor"] = setor
    
    n_analise_sugerida = sugerir_proxima_analise(st.session_state["protocolo"]) if st.session_state["protocolo"] else "1"
    if not st.session_state["n_analise"]:
        st.session_state["n_analise"] = n_analise_sugerida
    
    n_analise = st.text_input("Nº da Análise", value=st.session_state["n_analise"], key="n_analise_input")
    st.session_state["n_analise"] = n_analise

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Voltar", use_container_width=True):
            st.session_state["etapa"] = "1. Protocolo"
            st.rerun()
    with col2:
        if st.button("Prosseguir →", use_container_width=True, type="primary"):
            if st.session_state["analista"] and st.session_state["n_analise"]:
                st.session_state["etapa"] = "3. Análise"
                st.rerun()
            else:
                st.error("⚠️ Preencha todos os campos")

# -------------------------
# ETAPA 3 - ANÁLISE
# -------------------------
elif st.session_state["etapa"] == "3. Análise":
    st.header("🔍 Análise técnica")
    st.info(f"📌 Protocolo: **{st.session_state['protocolo']}** | Analista: **{st.session_state['analista']}**")

    respostas = {}
    observacoes = {}
    pendencias_manuais = st.session_state.get("pendencias_manuais", {})
    inconformes_sidebar = []

    for grupo in sorted(set(p["grupo"] for p in perguntas)):
        with st.expander(f"📁 {grupo}", expanded=False):
            for p in [p for p in perguntas if p["grupo"] == grupo]:
                pid = p["id"]
                chave_resp = f"resp_{pid}"
                chave_obs = f"obs_{pid}"

                if chave_resp not in st.session_state:
                    valor_padrao = st.session_state["dados_antigos"]["respostas"].get(pid) if st.session_state["dados_antigos"] else "Selecione..."
                    st.session_state[chave_resp] = valor_padrao if valor_padrao in p["opcoes"] else "Selecione..."
                if chave_obs not in st.session_state:
                    st.session_state[chave_obs] = st.session_state["dados_antigos"]["observacoes"].get(pid, "") if st.session_state["dados_antigos"] else ""

                opcoes = ["Selecione..."] + p["opcoes"]
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    resposta = st.selectbox(p["pergunta"], opcoes, key=chave_resp)
                    respostas[pid] = resposta
                with col2:
                    status = resumo_status_pergunta(p, resposta)
                    render_status_badge(status)
                    if status == "inconforme":
                        inconformes_sidebar.append(p["pergunta"])
                
                obs = st.text_area("Observação", key=chave_obs, height=68, 
                                   placeholder="Registre detalhes adicionais sobre esta resposta...")
                observacoes[pid] = obs
                st.markdown("---")
            
            # Inconformidades diversas
            st.markdown("### 📝 Inconformidades Diversas")
            st.caption("Registre aqui quaisquer inconformidades adicionais não cobertas pelas perguntas acima")
            
            if grupo not in pendencias_manuais:
                pendencias_manuais[grupo] = []
            elif not isinstance(pendencias_manuais[grupo], list):
                if pendencias_manuais[grupo] and pendencias_manuais[grupo].strip():
                    pendencias_manuais[grupo] = [pendencias_manuais[grupo]]
                else:
                    pendencias_manuais[grupo] = []
            
            # Exibir inconformidades existentes
            if pendencias_manuais[grupo]:
                for i, pendencia in enumerate(pendencias_manuais[grupo]):
                    if pendencia and pendencia.strip():
                        col_p, col_b = st.columns([10, 1])
                        with col_p:
                            st.markdown(f"""
                            <div style="background-color: #fff3e0; border-left: 4px solid #ff9800; 
                                        padding: 10px; margin: 5px 0; border-radius: 5px;">
                                <strong>Inconformidade {i+1}:</strong> {pendencia}
                            </div>
                            """, unsafe_allow_html=True)
                        with col_b:
                            if st.button("🗑️", key=f"remove_{grupo}_{i}"):
                                pendencias_manuais[grupo].pop(i)
                                st.rerun()
            
            # Botão para adicionar
            if st.button(f"+ Adicionar Inconformidade Diversa", key=f"add_{grupo}", use_container_width=True):
                pendencias_manuais[grupo].append("")
                st.rerun()
            
            # Campo para nova inconformidade
            if pendencias_manuais[grupo] and not pendencias_manuais[grupo][-1]:
                nova = st.text_area("Nova inconformidade", key=f"new_{grupo}", height=80,
                                    placeholder="Descreva a inconformidade encontrada...")
                if nova and nova.strip():
                    pendencias_manuais[grupo][-1] = nova
                    st.rerun()
            elif pendencias_manuais[grupo] and pendencias_manuais[grupo][-1]:
                ultima = pendencias_manuais[grupo][-1]
                nova = st.text_area("Editar inconformidade (última adicionada)", value=ultima, 
                                    key=f"edit_{grupo}", height=80)
                if nova != ultima:
                    pendencias_manuais[grupo][-1] = nova
            
            for pendencia in pendencias_manuais[grupo]:
                if pendencia and pendencia.strip():
                    inconformes_sidebar.append(f"{grupo} - Inconformidade Diversa")
            
            st.markdown("---")

    st.session_state["pendencias_manuais"] = pendencias_manuais
    preenchidas, total, pct = progresso_percentual(respostas)
    render_progresso(preenchidas, total, pct, st)

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Progresso")
    render_progresso(preenchidas, total, pct, st.sidebar)
    
    st.sidebar.markdown("### ⚠️ Inconformidades")
    if inconformes_sidebar:
        for item in inconformes_sidebar[:20]:
            st.sidebar.write(f"- {item}")
    else:
        st.sidebar.write("Nenhuma até o momento.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Voltar", use_container_width=True):
            st.session_state["etapa"] = "2. Analista"
            st.rerun()
    with col2:
        if st.button("Prosseguir para revisão →", use_container_width=True, type="primary"):
            st.session_state["respostas_temp"] = respostas
            st.session_state["observacoes_temp"] = observacoes
            st.session_state["etapa"] = "4. Revisão"
            st.rerun()

# -------------------------
# ETAPA 4 - REVISÃO
# -------------------------
elif st.session_state["etapa"] == "4. Revisão":
    st.header("📋 Revisão da análise")
    
    respostas = st.session_state.get("respostas_temp", {})
    observacoes = st.session_state.get("observacoes_temp", {})
    pendencias_manuais = st.session_state.get("pendencias_manuais", {})
    
    preenchidas, total, pct = progresso_percentual(respostas)
    render_progresso(preenchidas, total, pct, st)
    
    conclusao = definir_conclusao(respostas, pendencias_manuais)
    grupos_inconformes = montar_inconformidades_por_grupo(respostas, observacoes, pendencias_manuais)
    
    col1, col2 = st.columns([1.4, 1])
    
    with col1:
        st.subheader("📌 Resumo geral")
        st.write(f"**Protocolo:** {st.session_state.get('protocolo', '')}")
        st.write(f"**Requerente:** {st.session_state.get('interessado', '')}")
        st.write(f"**Tipo:** {st.session_state.get('tipo', '')}")
        st.write(f"**Matrícula(s):** {st.session_state.get('matriculas', '')}")
        st.write(f"**Analista:** {st.session_state.get('analista', '')}")
        st.write(f"**Nº da análise:** {st.session_state.get('n_analise', '')}")
        
        if conclusao == "FAVORÁVEL":
            st.success(f"✅ **Conclusão preliminar:** {conclusao}")
        else:
            st.error(f"❌ **Conclusão preliminar:** {conclusao}")
    
    with col2:
        st.subheader("📊 Contagem")
        total_inconformes = sum(len(v) for v in grupos_inconformes.values())
        st.metric("Perguntas", len(perguntas))
        st.metric("Respondidas", preenchidas)
        st.metric("Inconformidades", total_inconformes)
    
    st.subheader("⚠️ Inconformidades identificadas")
    if grupos_inconformes:
        for grupo, itens in grupos_inconformes.items():
            st.markdown(f"#### {grupo}")
            for i, item in enumerate(itens, start=1):
                st.markdown(f"""
                <div style="background-color: #f8fafd; border: 1px solid #c5d5e6; 
                            border-radius: 10px; padding: 12px 16px; margin: 8px 0;">
                    <b style="color: #1a5276;">{i}.</b> 
                    <span style="color: #1a1a1a;">{item.replace(chr(10), '<br>')}</span>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.success("✅ Não foram identificadas inconformidades.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Voltar para análise", use_container_width=True):
            st.session_state["etapa"] = "3. Análise"
            st.rerun()
    with col2:
        if st.button("Prosseguir para geração →", use_container_width=True, type="primary"):
            st.session_state["etapa"] = "5. Gerar parecer"
            st.rerun()

# -------------------------
# ETAPA 5 - GERAR PARECER
# -------------------------
elif st.session_state["etapa"] == "5. Gerar parecer":
    st.header("📄 Geração do parecer")
    
    respostas = st.session_state.get("respostas_temp", {})
    observacoes = st.session_state.get("observacoes_temp", {})
    pendencias_manuais = st.session_state.get("pendencias_manuais", {})
    
    dados = {
        "protocolo": st.session_state.get("protocolo", ""),
        "tipo": st.session_state.get("tipo", ""),
        "interessado": st.session_state.get("interessado", ""),
        "n_lotes": st.session_state.get("n_lotes", 1),
        "matriculas": st.session_state.get("matriculas", "")
    }
    
    conclusao = definir_conclusao(respostas, pendencias_manuais)
    
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**📌 Protocolo:** {dados['protocolo']}")
        st.write(f"**👤 Requerente:** {dados['interessado']}")
        st.write(f"**🏢 Tipo:** {dados['tipo']}")
    with col2:
        st.write(f"**🔢 Nº Lotes:** {dados['n_lotes']}")
        st.write(f"**👨‍💼 Analista:** {st.session_state.get('analista', '')}")
        st.write(f"**🔍 Nº Análise:** {st.session_state.get('n_analise', '')}")
    
    if conclusao == "FAVORÁVEL":
        st.success(f"✅ **Conclusão final:** {conclusao}")
    else:
        st.error(f"❌ **Conclusão final:** {conclusao}")
    
    # Validações
    if not dados["protocolo"]:
        st.error("❌ Protocolo não informado")
    elif not st.session_state.get("analista"):
        st.error("❌ Analista não informado")
    elif not st.session_state.get("n_analise"):
        st.error("❌ Número da análise não informado")
    elif not os.path.exists("modelo_parecer.docx"):
        st.error("❌ Arquivo 'modelo_parecer.docx' não encontrado")
    else:
        if st.button("📄 Gerar Parecer Técnico", use_container_width=True, type="primary"):
            try:
                with st.spinner("Gerando parecer técnico... Aguarde."):
                    arquivo = gerar_docx(
                        dados=dados, respostas=respostas, observacoes=observacoes,
                        conclusao=conclusao, analista=st.session_state["analista"],
                        matricula=st.session_state["matricula_analista"], setor=st.session_state["setor"],
                        n_analise=st.session_state["n_analise"], pendencias_manuais=pendencias_manuais
                    )
                    
                    salvar_historico(dados, respostas, observacoes, conclusao, 
                                    st.session_state["analista"], st.session_state["n_analise"], 
                                    arquivo, pendencias_manuais)
                    
                    protocolo_limpo = dados["protocolo"].replace("/", "-")
                    data_arquivo = datetime.now().strftime("%d-%m-%Y")
                    analise_str = f"AN{st.session_state['n_analise']}"
                    nome_arquivo = f"PU_{protocolo_limpo}_{data_arquivo}_{analise_str}.docx"
                    
                    st.success("✅ Parecer gerado e histórico salvo com sucesso!")
                    st.download_button("⬇️ Baixar parecer (.docx)", data=arquivo, 
                                      file_name=nome_arquivo, use_container_width=True)
            except Exception as e:
                st.error(f"❌ Erro ao gerar o parecer: {str(e)}")
    
    if st.button("← Voltar para revisão", use_container_width=True):
        st.session_state["etapa"] = "4. Revisão"
        st.rerun()