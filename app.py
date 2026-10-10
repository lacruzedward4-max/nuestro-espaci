import streamlit as st
import json
import base64
import requests
from datetime import datetime

# Configuración de página
st.set_page_config(
    page_title="El Libro de Nuestro Espacio ❤️",
    page_icon="📖",
    layout="centered"
)

# Constantes de GitHub
REPO_OWNER = "lacruzedward4-max"
REPO_NAME = "nuestro-espaci"
DATA_FILE = "data.json"
CLAVE_ADMIN_EDWARD = "1234"
NOMBRE_FOTO_FONDO = "e6a657e1-1d26-4d0c-934f-db13ac1b360f.jpeg"
bg_url = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main/{NOMBRE_FOTO_FONDO}"

GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN", None)

# Funciones de GitHub
def get_github_file(filepath, solo_sha=False):
    if not GITHUB_TOKEN: return None, None
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{filepath}"
    try:
        res = requests.get(url, headers=headers, timeout=5)
        if res.status_code == 200:
            content = res.json()
            if solo_sha: return None, content["sha"]
            decoded = base64.b64decode(content["content"]).decode("utf-8")
            return json.loads(decoded), content["sha"]
    except: pass
    return None, None

def save_github_file(filepath, data_dict, commit_message="Update data"):
    if not GITHUB_TOKEN: return False, "No token"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{filepath}"
    _, current_sha = get_github_file(filepath)
    encoded = base64.b64encode(json.dumps(data_dict, ensure_ascii=False, indent=2).encode("utf-8")).decode("utf-8")
    payload = {"message": commit_message, "content": encoded}
    if current_sha: payload["sha"] = current_sha
    try:
        res = requests.put(url, headers=headers, json=payload, timeout=10)
        if res.status_code in [200, 201]:
            st.session_state.last_sha = res.json()["content"]["sha"]
            return True, "Guardado con éxito"
    except: pass
    return False, "Error al guardar"

def save_github_image(filename, image_bytes):
    if not GITHUB_TOKEN: return None, "No token"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    filepath = f"uploads/{filename}"
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{filepath}"
    _, current_sha = get_github_file(filepath)
    encoded = base64.b64encode(image_bytes).decode("utf-8")
    payload = {"message": f"Upload image {filename}", "content": encoded}
    if current_sha: payload["sha"] = current_sha
    try:
        res = requests.put(url, headers=headers, json=payload, timeout=10)
        if res.status_code in [200, 201]:
            return f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main/{filepath}", "Éxito"
    except: pass
    return None, "Error"

def delete_github_image_file(image_url):
    if not GITHUB_TOKEN or not image_url: return False
    try:
        if "/main/" in image_url:
            filepath = image_url.split("/main/")[-1]
            _, sha = get_github_file(filepath)
            if sha:
                headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
                url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{filepath}"
                requests.delete(url, headers=headers, json={"message": f"Delete {filepath}", "sha": sha}, timeout=10)
                return True
    except: pass
    return False

# Carga inicial y control de estado (SHA)
if "last_sha" not in st.session_state:
    st.session_state.last_sha = None

if "app_data" not in st.session_state:
    remote_data, remote_sha = get_github_file(DATA_FILE)
    if remote_data:
        st.session_state.app_data = remote_data
        st.session_state.last_sha = remote_sha
    else:
        st.session_state.app_data = {"planes": [], "encuestas": [], "fotos": [], "status": {}}

if "status" not in st.session_state.app_data:
    st.session_state.app_data["status"] = {}

# Sincronización en la URL
query_user = st.query_params.get("user", None)
if query_user == "yesenia": st.session_state.usuario_activo = "Yesenia Alejandra 💕"
elif query_user == "edward": st.session_state.usuario_activo = "Edward ❤️"
elif "usuario_activo" not in st.session_state: st.session_state.usuario_activo = None

# ESTILOS CSS
st.markdown(f"""
    <style>
    [data-testid="stStatusWidget"], .stSpinner {{ display: none !important; visibility: hidden !important; }}
    
    [data-testid="stAppViewContainer"] {{
        background-image: url("{bg_url}") !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }}
    [data-testid="stHeader"] {{ background-color: transparent !important; }}

    p, label, span, div, li, h1, h2, h3 {{
        color: #ffffff !important;
        text-shadow: 2px 2px 5px rgba(0,0,0,0.9), 0px 0px 8px rgba(0,0,0,0.8) !important;
        font-weight: 700 !important;
    }}
    h1, h2, h3 {{ color: #ffccd5 !important; }}

    .stTextInput input, .stTextArea textarea {{
        background-color: rgba(0, 0, 0, 0.6) !important;
        color: white !important;
        border: 2px solid #ff4d6d !important;
        border-radius: 12px !important;
        padding: 10px !important;
    }}

    .stButton>button {{
        background-color: #ff4d6d !important;
        color: #ffffff !important;
        border-radius: 20px !important;
        border: none !important;
        font-weight: bold !important;
        padding: 8px !important;
    }}

    .whatsapp-status-box {{
        background-color: rgba(0, 0, 0, 0.5);
        border: 2px solid #25D366;
        border-radius: 15px;
        padding: 12px;
        margin-bottom: 20px;
    }}
    
    @keyframes latido {{ 0% {{ transform: scale(1); }} 14% {{ transform: scale(1.2); }} 28% {{ transform: scale(1); }} 42% {{ transform: scale(1.2); }} 70% {{ transform: scale(1); }} }}
    .corazon-animado {{ font-size: 75px !important; text-align: center; margin: 15px 0; animation: latido 1.4s infinite; display: block; }}
    </style>
""", unsafe_allow_html=True)

# 📖 MENU INICIAL
if st.session_state.usuario_activo is None:
    st.markdown("<h1 style='text-align: center;'>📖 Nuestro Libro 💖</h1>", unsafe_allow_html=True)
    st.markdown("<div class='corazon-animado'>💖</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Selecciona tu nombre para abrir:</p>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("👸 Soy Yesenia 💕"):
            st.session_state.usuario_activo = "Yesenia Alejandra 💕"
            st.query_params["user"] = "yesenia"
            st.session_state.app_data["status"]["Yesenia Alejandra 💕"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_github_file(DATA_FILE, st.session_state.app_data, "Login Yesenia")
            st.rerun()
    with col_b:
        if st.button("🤴 Soy Edward ❤️"):
            st.session_state.usuario_activo = "Edward ❤️"
            st.query_params["user"] = "edward"
            st.session_state.app_data["status"]["Edward ❤️"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_github_file(DATA_FILE, st.session_state.app_data, "Login Edward")
            st.rerun()

# 💖 APLICACIÓN PRINCIPAL
else:
    usuario = st.session_state.usuario_activo

    @st.fragment(run_every="4s")
    def motor_sincronizacion_silenciosa():
        if GITHUB_TOKEN:
            _, remote_sha = get_github_file(DATA_FILE, solo_sha=True)
            if remote_sha and st.session_state.last_sha and remote_sha != st.session_state.last_sha:
                st.rerun()
    
    motor_sincronizacion_silenciosa()

    # Barra Superior
    c1, c2 = st.columns([0.65, 0.35])
    with c1:
        st.markdown(f"<b>Hola, {usuario}</b>", unsafe_allow_html=True)
    with c2:
        if st.button("🔄 Salir"):
            st.session_state.usuario_activo = None
            st.query_params.clear()
            st.rerun()

    # PANEL ADMIN PRIMERO (Para habilitar opciones exclusivas)
    es_admin = False
    if usuario == "Edward ❤️":
        with st.expander("🛠️ Admin"):
            if st.text_input("Clave:", type="password") == CLAVE_ADMIN_EDWARD: 
                es_admin = True

    # ESTADOS "EN LÍNEA" (SOLO VISIBLE SI ES ADMIN)
    if es_admin:
        def obtener_badge_estado(nombre_user):
            last_str = st.session_state.app_data["status"].get(nombre_user, "")
            if not last_str: return "⚪ Desconectado/a"
            try:
                dt = datetime.strptime(last_str, "%Y-%m-%d %H:%M:%S")
                diferencia = (datetime.now() - dt).total_seconds()
                if diferencia < 300:
                    return "🟢 Reciente"
                else:
                    return f"⚪ Última vez: {dt.strftime('%d/%m %I:%M %p')}"
            except: return "⚪ Desconectado/a"

        st.markdown(f"""
            <div class='whatsapp-status-box'>
                <div>👸 <b>Yesenia:</b> {obtener_badge_estado("Yesenia Alejandra 💕")}</div>
                <div>🤴 <b>Edward:</b> {obtener_badge_estado("Edward ❤️")}</div>
            </div>
        """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📌 Planes", "📝 Encuesta", "📸 Fotos"])

    # TAB 1: PLANES
    with tab1:
        cambio_planes, idx_borrar = False, None
        for idx, item in enumerate(st.session_state.app_data["planes"]):
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                estado = st.checkbox(f"{item['plan']} ({item.get('autor','')} {item.get('fecha','')})", value=item["hecho"], key=f"plan_{idx}")
                if estado != item["hecho"]:
                    st.session_state.app_data["planes"][idx]["hecho"] = estado
                    cambio_planes = True
            with col2:
                if es_admin and st.button("🗑️", key=f"del_plan_{idx}"): idx_borrar = idx
                        
        if idx_borrar is not None:
            st.session_state.app_data["planes"].pop(idx_borrar)
            save_github_file(DATA_FILE, st.session_state.app_data, "Delete plan")
            st.rerun()
        if cambio_planes:
            save_github_file(DATA_FILE, st.session_state.app_data, "Update plan")
            st.rerun()

        st.divider()
        nuevo_plan = st.text_input("➕ Agregar plan:")
        if st.button("Guardar Plan 📝") and nuevo_plan.strip():
            st.session_state.app_data["planes"].append({"plan": nuevo_plan.strip(), "hecho": False, "fecha": datetime.now().strftime("%d/%m %I:%M %p"), "autor": usuario})
            save_github_file(DATA_FILE, st.session_state.app_data, "Add plan")
            st.rerun()

    # TAB 2: ENCUESTA
    with tab2:
        with st.expander("➕ Responder la encuesta", expanded=False):
            p1 = st.text_area("1. Momento favorito de la semana:")
            p2 = st.text_input("2. Antojo de este finde:")
            p3 = st.text_area("3. Mensajito secreto ❤️:")
            if st.button("Enviar Respuestas 💌") and (p1.strip() or p2.strip() or p3.strip()):
                st.session_state.app_data["encuestas"].insert(0, {
                    "id": len(st.session_state.app_data["encuestas"]) + 1, "autor": usuario,
                    "fecha": datetime.now().strftime("%d/%m %I:%M %p"), "p1": p1, "p2": p2, "p3": p3, "comentarios": []
                })
                save_github_file(DATA_FILE, st.session_state.app_data, "New survey")
                st.rerun()

        st.divider()
        idx_borrar_enc = None
        for enc_idx, enc in enumerate(st.session_state.app_data["encuestas"]):
            st.markdown(f"### 💌 Encuesta de {enc['autor']} ({enc.get('fecha','')})")
            st.write(f"**1. Momento:** {enc['p1']}")
            st.write(f"**2. Antojo:** {enc['p2']}")
            st.write(f"**3. Mensaje:** {enc['p3']}")
            
            if es_admin and st.button(f"🗑️ Eliminar Encuesta", key=f"del_enc_{enc_idx}"): idx_borrar_enc = enc_idx

            for c_idx, c in enumerate(enc["comentarios"]):
                st.write(f"- *{c['autor']}* ({c.get('fecha','')}): {c['texto']}")
                if es_admin and st.button(f"🗑️", key=f"del_c_{enc_idx}_{c_idx}"):
                    enc["comentarios"].pop(c_idx)
                    save_github_file(DATA_FILE, st.session_state.app_data, "Del comment")
                    st.rerun()

            n_com = st.text_input(f"Comentar a {enc['autor']}:", key=f"comm_{enc['id']}")
            if st.button("Comentar 💬", key=f"btn_c_{enc['id']}") and n_com.strip():
                st.session_state.app_data["status"][usuario] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                enc["comentarios"].append({"autor": usuario, "texto": n_com.strip(), "fecha": datetime.now().strftime("%d/%m %I:%M %p")})
                save_github_file(DATA_FILE, st.session_state.app_data, "Add comment")
                st.rerun()
            st.divider()

        if idx_borrar_enc is not None:
            st.session_state.app_data["encuestas"].pop(idx_borrar_enc)
            save_github_file(DATA_FILE, st.session_state.app_data, "Del survey")
            st.rerun()

    # TAB 3: RECUERDOS
    with tab3:
        foto_archivo = st.file_uploader("Sube una foto 📲", type=["jpg", "png", "jpeg"])
        desc = st.text_input("Pie de foto:")
        if st.button("Guardar Foto 🖼️") and foto_archivo:
            url, _ = save_github_image(f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{foto_archivo.name}", foto_archivo.getvalue())
            if url:
                st.session_state.app_data["fotos"].insert(0, {"url": url, "caption": desc, "autor": usuario, "fecha": datetime.now().strftime("%d/%m %I:%M %p")})
                save_github_file(DATA_FILE, st.session_state.app_data, "Add photo")
                st.rerun()

        st.divider()
        for idx_foto, foto in enumerate(st.session_state.app_data["fotos"]):
            st.image(foto["url"], caption=f"{foto['caption']} - {foto['autor']} ({foto.get('fecha','')})", use_container_width=True)
            if es_admin and st.button(f"🗑️ Eliminar foto", key=f"del_p_{idx_foto}"):
                delete_github_image_file(foto["url"])
                st.session_state.app_data["fotos"].pop(idx_foto)
                save_github_file(DATA_FILE, st.session_state.app_data, "Del photo")
                st.rerun()
            st.divider()

                save_github_file(DATA_FILE, st.session_state.app_data, "Del photo")
                st.rerun()
            st.divider()
