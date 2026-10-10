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

# 🔑 CLAVE DE ADMINISTRADOR
CLAVE_ADMIN_EDWARD = "1234"

# 🖼️ Nombre exacto de la foto de fondo
NOMBRE_FOTO_FONDO = "e6a657e1-1d26-4d0c-934f-db13ac1b360f.jpeg"
bg_url = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main/{NOMBRE_FOTO_FONDO}"

GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN", None)

def get_github_file(filepath):
    if not GITHUB_TOKEN:
        return None, None
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{filepath}"
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            content = res.json()
            decoded = base64.b64decode(content["content"]).decode("utf-8")
            return json.loads(decoded), content["sha"]
    except Exception:
        pass
    return None, None

def save_github_file(filepath, data_dict, commit_message="Update data"):
    if not GITHUB_TOKEN:
        return False, "No se encontró el GITHUB_TOKEN en Streamlit Secrets."
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{filepath}"
    
    _, current_sha = get_github_file(filepath)
    
    encoded_content = base64.b64encode(json.dumps(data_dict, ensure_ascii=False, indent=2).encode("utf-8")).decode("utf-8")
    payload = {
        "message": commit_message,
        "content": encoded_content
    }
    if current_sha:
        payload["sha"] = current_sha
        
    try:
        res = requests.put(url, headers=headers, json=payload, timeout=10)
        if res.status_code in [200, 201]:
            return True, "Guardado con éxito"
        else:
            return False, f"Error {res.status_code} de GitHub: {res.text}"
    except Exception as e:
        return False, f"Excepción de conexión: {str(e)}"

def save_github_image(filename, image_bytes):
    if not GITHUB_TOKEN:
        return None, "No se encontró el GITHUB_TOKEN en Streamlit Secrets."
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    filepath = f"uploads/{filename}"
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{filepath}"
    
    _, current_sha = get_github_file(filepath)
    encoded_content = base64.b64encode(image_bytes).decode("utf-8")
    payload = {
        "message": f"Upload image {filename}",
        "content": encoded_content
    }
    if current_sha:
        payload["sha"] = current_sha
        
    try:
        res = requests.put(url, headers=headers, json=payload, timeout=10)
        if res.status_code in [200, 201]:
            raw_url = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main/{filepath}"
            return raw_url, "Imagen guardada exitosamente"
        else:
            return None, f"Error {res.status_code} al subir imagen: {res.text}"
    except Exception as e:
        return None, f"Excepción al subir imagen: {str(e)}"

def delete_github_image_file(image_url):
    if not GITHUB_TOKEN or not image_url:
        return False
    try:
        if "/main/" in image_url:
            filepath = image_url.split("/main/")[-1]
            _, sha = get_github_file(filepath)
            if sha:
                headers = {
                    "Authorization": f"token {GITHUB_TOKEN}",
                    "Accept": "application/vnd.github.v3+json"
                }
                url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{filepath}"
                payload = {"message": f"Delete image {filepath}", "sha": sha}
                res = requests.delete(url, headers=headers, json=payload, timeout=10)
                return res.status_code in [200, 201]
    except Exception:
        pass
    return False

# Carga de datos iniciales
initial_data = {
    "planes": [
        {"plan": "Ir a comer unos postres/helados ricos 🍦", "hecho": False, "fecha": datetime.now().strftime("%d/%m/%Y %I:%M %p"), "autor": "Edward ❤️"},
        {"plan": "Tarde de películas, cobijas y comida chatarra 🍿", "hecho": False, "fecha": datetime.now().strftime("%d/%m/%Y %I:%M %p"), "autor": "Edward ❤️"}
    ],
    "encuestas": [],
    "fotos": [],
    "status": {}
}

# Session State
if "app_data" not in st.session_state:
    remote_data, _ = get_github_file(DATA_FILE)
    if remote_data:
        st.session_state.app_data = remote_data
    else:
        st.session_state.app_data = initial_data

if "status" not in st.session_state.app_data:
    st.session_state.app_data["status"] = {}

if "usuario_activo" not in st.session_state:
    st.session_state.usuario_activo = None

# Estilos CSS
st.markdown(f"""
    <style>
    /* Fondo */
    [data-testid="stAppViewContainer"] {{
        background-image: url("{bg_url}") !important;
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
    }}
    
    [data-testid="stHeader"] {{
        background-color: rgba(0, 0, 0, 0) !important;
    }}

    /* Tarjeta Principal */
    [data-testid="block-container"] {{
        background-color: #ffffff !important;
        padding: 25px !important;
        border-radius: 20px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5) !important;
        margin-top: 1rem !important;
        margin-bottom: 2rem !important;
        border: 3px solid #ff4d6d !important;
    }}

    /* Forzar texto negro */
    [data-testid="block-container"] p, 
    [data-testid="block-container"] label, 
    [data-testid="block-container"] span, 
    [data-testid="block-container"] div, 
    [data-testid="block-container"] li {{
        color: #000000 !important;
        font-weight: 600 !important;
    }}

    /* Títulos */
    [data-testid="block-container"] h1, 
    [data-testid="block-container"] h2, 
    [data-testid="block-container"] h3 {{
        color: #c9184a !important;
        text-align: center !important;
        font-weight: 800 !important;
    }}

    /* Animación Corazón Latiendo */
    @keyframes latido {{
        0% {{ transform: scale(1); }}
        14% {{ transform: scale(1.2); }}
        28% {{ transform: scale(1); }}
        42% {{ transform: scale(1.2); }}
        70% {{ transform: scale(1); }}
    }}
    .corazon-animado {{
        font-size: 75px !important;
        text-align: center;
        margin: 15px 0;
        animation: latido 1.4s infinite;
        display: block;
    }}

    /* Banner Frase Especial */
    .frase-especial {{
        color: #590d22 !important;
        font-size: 1.1rem !important;
        font-weight: bold !important;
        text-align: center !important;
        background-color: #ffccd5 !important;
        padding: 16px !important;
        border-radius: 12px !important;
        border-left: 6px solid #ff4d6d !important;
        margin: 15px 0 !important;
    }}

    /* Cuadro WhatsApp Status */
    .whatsapp-status-box {{
        background-color: #f0f2f5;
        border: 2px solid #25D366;
        border-radius: 15px;
        padding: 12px;
        margin-bottom: 20px;
    }}
    .status-item {{
        font-size: 0.95rem;
        font-weight: 700;
        margin: 4px 0;
    }}

    /* Inputs */
    .stTextInput input, .stTextArea textarea {{
        color: #000000 !important;
        background-color: #f1f3f5 !important;
        border: 2px solid #ff4d6d !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }}

    /* Botones */
    .stButton>button {{
        background-color: #ff4d6d !important;
        color: #ffffff !important;
        border-radius: 25px !important;
        border: none !important;
        font-weight: bold !important;
        font-size: 1.05rem !important;
        width: 100% !important;
        padding: 12px !important;
    }}

    /* Pestañas */
    [data-baseweb="tab-list"] button {{
        background-color: #f1f3f5 !important;
        color: #000000 !important;
        border-radius: 8px !important;
        font-weight: bold !important;
    }}
    [data-baseweb="tab-list"] button[aria-selected="true"] {{
        background-color: #ff4d6d !important;
        color: #ffffff !important;
    }}
    
    .timestamp-tag {{
        font-size: 0.8rem !important;
        color: #6c757d !important;
        font-style: italic;
    }}
    </style>
""", unsafe_allow_html=True)

# 📖 PANTALLA DE ENTRADA / PORTADA DEL LIBRO DE NUESTRA HISTORIA
if st.session_state.usuario_activo is None:
    st.markdown("<h1 style='text-align: center;'>📖 Nuestro Libro de la Historia 💖</h1>", unsafe_allow_html=True)
    st.markdown("<div class='corazon-animado'>💖</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.1rem;'>Para abrir el libro y ver nuestro espacio, selecciona tu nombre:</p>", unsafe_allow_html=True)
    st.write("")

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("👸 Soy Yesenia 💕", key="btn_login_yesenia"):
            st.session_state.usuario_activo = "Yesenia Alejandra 💕"
            st.balloons()
            st.rerun()

    with col_b:
        if st.button("🤴 Soy Edward ❤️", key="btn_login_edward"):
            st.session_state.usuario_activo = "Edward ❤️"
            st.balloons()
            st.rerun()

# 💖 APLICACIÓN PRINCIPAL (LIBRO ABIERTO)
else:
    usuario = st.session_state.usuario_activo

    # Barra Superior de Bienvenida
    c1, c2 = st.columns([0.65, 0.35])
    with c1:
        st.markdown(f"<b>Hola, {usuario}</b>", unsafe_allow_html=True)
    with c2:
        if st.button("🔄 Cerrar Libro", key="btn_logout"):
            st.session_state.usuario_activo = None
            st.rerun()

    st.title("💖 Nuestro Espacio Especial 💖")
    st.write("<h3 style='text-align: center;'>Dedicado a Yesenia Alejandra 💕</h3>", unsafe_allow_html=True)

    st.markdown("""
        <div class='frase-especial'>
            ✨ "Me gustaría ponerme al día con todos nuestros próximos planes, Yesenia Alejandra." ✨
        </div>
    """, unsafe_allow_html=True)

    # Actualizar estado "En Línea"
    ahora_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.app_data["status"][usuario] = ahora_str

    if GITHUB_TOKEN:
        save_github_file(DATA_FILE, st.session_state.app_data, f"Status update {usuario}")

    def obtener_badge_estado(nombre_user):
        last_str = st.session_state.app_data["status"].get(nombre_user, "")
        if not last_str:
            return "⚪ Desconectado/a"
        try:
            dt = datetime.strptime(last_str, "%Y-%m-%d %H:%M:%S")
            diferencia = (datetime.now() - dt).total_seconds()
            if diferencia < 180:
                return "🟢 En línea"
            else:
                return f"⚪ Última vez: {dt.strftime('%d/%m/%Y %I:%M %p')}"
        except:
            return "⚪ Desconectado/a"

    status_yesenia = obtener_badge_estado("Yesenia Alejandra 💕")
    status_edward = obtener_badge_estado("Edward ❤️")

    # Recuadro de Estados WhatsApp
    st.markdown(f"""
        <div class='whatsapp-status-box'>
            <div class='status-item'>👸 <b>Yesenia Alejandra:</b> {status_yesenia}</div>
            <div class='status-item'>🤴 <b>Edward:</b> {status_edward}</div>
        </div>
    """, unsafe_allow_html=True)

    # Panel de Administrador Global para Edward
    es_admin = False
    if usuario == "Edward ❤️":
        with st.expander("🛠️ Panel Administrador (Edward)"):
            clave_input = st.text_input("Clave de Administrador:", type="password", key="pwd_admin_global")
            if clave_input == CLAVE_ADMIN_EDWARD:
                es_admin = True
                st.success("🔓 Permisos de Administrador Activos: Puedes eliminar elementos en todas las secciones.")
            elif clave_input:
                st.error("❌ Clave incorrecta.")

    tab1, tab2, tab3 = st.tabs(["📌 Nuestros Planes", "📝 Encuesta Semanal", "📸 Recuerdos"])

    # TAB 1: PLANES
    with tab1:
        st.subheader("📌 Lista de Nuestros Próximos Planes")
        
        cambio_planes = False
        idx_a_borrar_plan = None
        
        for idx, item in enumerate(st.session_state.app_data["planes"]):
            fecha_text = item.get("fecha", "Hace tiempo")
            autor_text = item.get("autor", "")
            
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                estado = st.checkbox(f"{item['plan']}", value=item["hecho"], key=f"plan_{idx}")
                st.markdown(f"<span class='timestamp-tag'>📅 Agregado: {fecha_text} {f'por {autor_text}' if autor_text else ''}</span>", unsafe_allow_html=True)
                if estado != item["hecho"]:
                    st.session_state.app_data["planes"][idx]["hecho"] = estado
                    cambio_planes = True
            with col2:
                if es_admin:
                    if st.button("🗑️", key=f"del_plan_{idx}"):
                        idx_a_borrar_plan = idx
                        
        if idx_a_borrar_plan is not None:
            st.session_state.app_data["planes"].pop(idx_a_borrar_plan)
            save_github_file(DATA_FILE, st.session_state.app_data, "Delete plan item")
            st.success("Plan eliminado.")
            st.rerun()

        if cambio_planes:
            ok, msg = save_github_file(DATA_FILE, st.session_state.app_data, "Update planes status")
            if ok:
                st.toast("¡Plan actualizado! 💖")
                st.rerun()

        st.divider()
        nuevo_plan = st.text_input("➕ Agregar nuevo plan a la lista:")
        if st.button("Guardar Plan 📝"):
            if nuevo_plan.strip():
                fecha_actual = datetime.now().strftime("%d/%m/%Y %I:%M %p")
                st.session_state.app_data["planes"].append({
                    "plan": nuevo_plan.strip(),
                    "hecho": False,
                    "fecha": fecha_actual,
                    "autor": usuario
                })
                ok, msg = save_github_file(DATA_FILE, st.session_state.app_data, "Add new plan")
                if ok:
                    st.success("¡Plan agregado exitosamente!")
                    st.rerun()
                else:
                    st.error(f"Error al guardar plan: {msg}")
            else:
                st.warning("Escribe una propuesta antes de guardar.")

    # TAB 2: ENCUESTA
    with tab2:
        st.subheader("📝 Encuesta e Interacción Semanal")
        
        with st.expander("➕ Responder la encuesta de esta semana", expanded=True):
            p1 = st.text_area("1. ¿Cuál fue tu momento favorito de esta semana juntos?")
            p2 = st.text_input("2. ¿Qué se te antoja comer o hacer este fin de semana?")
            p3 = st.select_slider("3. ¿Qué tan consentido/a te has sentido?", options=["Poco 🥺", "Normal 😊", "Muy Consentido/a 🥰", "Nivel Reina/Rey 👑"])
            p4 = st.text_area("4. Un mensajito o nota secreta ❤️")
            
            if st.button("Enviar Respuestas 💌"):
                if p1.strip() or p2.strip() or p4.strip():
                    fecha_actual = datetime.now().strftime("%d/%m/%Y %I:%M %p")
                    nueva_resp = {
                        "id": len(st.session_state.app_data["encuestas"]) + 1,
                        "autor": usuario,
                        "fecha": fecha_actual,
                        "p1": p1, "p2": p2, "p3": p3, "p4": p4,
                        "comentarios": []
                    }
                    st.session_state.app_data["encuestas"].insert(0, nueva_resp)
                    ok, msg = save_github_file(DATA_FILE, st.session_state.app_data, "New survey response")
                    if ok:
                        st.success("¡Respuesta registrada!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(f"Error al guardar encuesta: {msg}")
                else:
                    st.warning("Responde al menos un campo antes de enviar.")

        st.divider()
        st.subheader("💬 Respuestas y Comentarios Mutuos")
        
        if not st.session_state.app_data["encuestas"]:
            st.info("Aún no hay respuestas registradas. ¡Sé el primero en responder arriba!")
        else:
            idx_borrar_encuesta = None
            for enc_idx, enc in enumerate(st.session_state.app_data["encuestas"]):
                st.markdown(f"### 💌 Encuesta de {enc['autor']}")
                st.markdown(f"<span class='timestamp-tag'>📅 Fecha: {enc.get('fecha', 'Reciente')}</span>", unsafe_allow_html=True)
                st.write(f"**1. Momento favorito:** {enc['p1']}")
                st.write(f"**2. Antojo/Plan:** {enc['p2']}")
                st.write(f"**3. Consentimiento:** {enc['p3']}")
                st.write(f"**4. Mensaje secreto:** {enc['p4']}")
                
                if es_admin:
                    if st.button(f"🗑️ Eliminar Encuesta de {enc['autor']}", key=f"del_enc_{enc_idx}"):
                        idx_borrar_encuesta = enc_idx

                if enc["comentarios"]:
                    st.write("**Comentarios:**")
                    idx_borrar_comentario = None
                    for c_idx, c in enumerate(enc["comentarios"]):
                        f_com = c.get("fecha", "")
                        st.write(f"- *{c['autor']}* ({f_com}): {c['texto']}")
                        if es_admin:
                            if st.button(f"🗑️ Eliminar Comentario #{c_idx+1}", key=f"del_comm_{enc_idx}_{c_idx}"):
                                idx_borrar_comentario = c_idx
                    
                    if idx_borrar_comentario is not None:
                        enc["comentarios"].pop(idx_borrar_comentario)
                        save_github_file(DATA_FILE, st.session_state.app_data, "Delete comment")
                        st.success("Comentario eliminado.")
                        st.rerun()

                nuevo_comentario = st.text_input(f"Comentar en la respuesta de {enc['autor']}:", key=f"comm_in_{enc['id']}")
                if st.button("Comentar 💬", key=f"comm_btn_{enc['id']}"):
                    if nuevo_comentario.strip():
                        f_comentario = datetime.now().strftime("%d/%m/%Y %I:%M %p")
                        enc["comentarios"].append({"autor": usuario, "texto": nuevo_comentario.strip(), "fecha": f_comentario})
                        ok, msg = save_github_file(DATA_FILE, st.session_state.app_data, "Add comment")
                        if ok:
                            st.success("Comentario publicado.")
                            st.rerun()
                        else:
                            st.error(f"Error al publicar comentario: {msg}")
                st.divider()

            if idx_borrar_encuesta is not None:
                st.session_state.app_data["encuestas"].pop(idx_borrar_encuesta)
                save_github_file(DATA_FILE, st.session_state.app_data, "Delete survey response")
                st.success("Encuesta eliminada.")
                st.rerun()

    # TAB 3: RECUERDOS
    with tab3:
        st.subheader("📸 Galería de Recuerdos")
        
        foto_archivo = st.file_uploader("Selecciona una foto 📲", type=["jpg", "png", "jpeg"])
        descripcion_foto = st.text_input("Pie de foto o recuerdo:")
        
        if st.button("Guardar en la Galería 🖼️"):
            if foto_archivo is not None:
                bytes_data = foto_archivo.getvalue()
                nombre_foto = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{foto_archivo.name}"
                
                with st.spinner("Guardando foto en la galería..."):
                    url_guardada, msg_img = save_github_image(nombre_foto, bytes_data)
                    
                if url_guardada:
                    fecha_foto = datetime.now().strftime("%d/%m/%Y %I:%M %p")
                    nueva_foto = {"url": url_guardada, "caption": descripcion_foto, "autor": usuario, "fecha": fecha_foto}
                    st.session_state.app_data["fotos"].insert(0, nueva_foto)
                    ok_json, msg_json = save_github_file(DATA_FILE, st.session_state.app_data, "Add new photo")
                    if ok_json:
                        st.success("¡Foto guardada en la galería compartida!")
                        st.rerun()
                    else:
                        st.error(f"Error al actualizar la lista de fotos: {msg_json}")
                else:
                    st.error(f"Error al subir la imagen: {msg_img}")
            else:
                st.warning("Selecciona una foto antes de guardar.")

        st.divider()
        if not st.session_state.app_data["fotos"]:
            st.info("Aún no hay fotos subidas en la galería.")
        else:
            for idx_foto, foto in enumerate(st.session_state.app_data["fotos"]):
                f_foto = foto.get("fecha", "Reciente")
                st.image(foto["url"], caption=f"{foto['caption']} — Subido por {foto['autor']} (📅 {f_foto})", use_container_width=True)
                
                if es_admin:
                    if st.button(f"🗑️ Eliminar esta foto", key=f"del_photo_{idx_foto}"):
                        with st.spinner("Eliminando foto..."):
                            delete_github_image_file(foto["url"])
                            st.session_state.app_data["fotos"].pop(idx_foto)
                            ok, msg = save_github_file(DATA_FILE, st.session_state.app_data, "Delete photo")
                            if ok:
                                st.success("Foto eliminada correctamente.")
                                st.rerun()
                            else:
                                st.error(f"Error al guardar cambios: {msg}")
                st.divider()
