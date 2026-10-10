import streamlit as st
import json
import base64
import requests
from datetime import datetime

# Configuración de página
st.set_page_config(
    page_title="Para Yesenia Alejandra ❤️",
    page_icon="💖",
    layout="centered"
)

# Constantes de GitHub
REPO_OWNER = "lacruzedward4-max"
REPO_NAME = "nuestro-espaci"
DATA_FILE = "data.json"

# 🖼️ Nombre de la foto de fondo subida a tu repositorio
NOMBRE_FOTO_FONDO = "IMG_0980.png"
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

# Estructura inicial
initial_data = {
    "planes": [
        {"plan": "Ir a comer unos postres/helados ricos 🍦", "hecho": False},
        {"plan": "Tarde de películas, cobijas y comida chatarra 🍿", "hecho": False},
        {"plan": "Un picnic romántico al aire libre 🧺", "hecho": False},
        {"plan": "Salir a cenar a un sitio nuevo 🍔", "hecho": False}
    ],
    "encuestas": [],
    "fotos": []
}

# Session State
if "app_data" not in st.session_state:
    remote_data, _ = get_github_file(DATA_FILE)
    if remote_data:
        st.session_state.app_data = remote_data
    else:
        st.session_state.app_data = initial_data

# CSS para móvil Streamlit: Tarjeta blanca opaca de alto contraste
st.markdown(f"""
    <style>
    /* Fondo con foto */
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

    /* Tarjeta Blanca Sólida para el Contenido */
    [data-testid="block-container"] {{
        background-color: #ffffff !important;
        padding: 25px !important;
        border-radius: 20px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5) !important;
        margin-top: 1rem !important;
        margin-bottom: 2rem !important;
        border: 3px solid #ff4d6d !important;
    }}

    /* Forzar que TODO el texto sea NEGRO brillante */
    [data-testid="block-container"] p, 
    [data-testid="block-container"] label, 
    [data-testid="block-container"] span, 
    [data-testid="block-container"] div, 
    [data-testid="block-container"] li {{
        color: #000000 !important;
        font-weight: 600 !important;
    }}

    /* Títulos principales */
    [data-testid="block-container"] h1, 
    [data-testid="block-container"] h2, 
    [data-testid="block-container"] h3 {{
        color: #c9184a !important;
        text-align: center !important;
        font-weight: 800 !important;
    }}

    /* Frase especial estilo banner */
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

    /* Inputs de escribir */
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
    </style>
""", unsafe_allow_html=True)

if not GITHUB_TOKEN:
    st.error("⚠️ Atención: No se detectó 'GITHUB_TOKEN' en Streamlit Cloud Secrets. La app estará en modo lectura.")

st.title("💖 Nuestro Espacio Especial 💖")
st.write("<h3 style='text-align: center;'>Dedicado a Yesenia Alejandra 💕</h3>", unsafe_allow_html=True)

st.markdown("""
    <div class='frase-especial'>
        ✨ "Me gustaría ponerme al día con todos nuestros próximos planes, Yesenia Alejandra." ✨
    </div>
""", unsafe_allow_html=True)

usuario = st.selectbox("👤 ¿Quién está interactuando ahora?", ["Yesenia Alejandra 💕", "Edward ❤️"])

tab1, tab2, tab3 = st.tabs(["📌 Nuestros Planes", "📝 Encuesta Semanal", "📸 Recuerdos"])

# TAB 1: PLANES
with tab1:
    st.subheader("📌 Lista de Nuestros Próximos Planes")
    
    cambio_planes = False
    for idx, item in enumerate(st.session_state.app_data["planes"]):
        estado = st.checkbox(item["plan"], value=item["hecho"], key=f"plan_{idx}")
        if estado != item["hecho"]:
            st.session_state.app_data["planes"][idx]["hecho"] = estado
            cambio_planes = True
            
    if cambio_planes:
        ok, msg = save_github_file(DATA_FILE, st.session_state.app_data, "Update planes status")
        if ok:
            st.toast("¡Estado de plan actualizado! 💖")
            st.rerun()
        else:
            st.error(f"Error al guardar cambio: {msg}")

    st.divider()
    nuevo_plan = st.text_input("➕ Agregar nuevo plan a la lista:")
    if st.button("Guardar Plan 📝"):
        if nuevo_plan.strip():
            st.session_state.app_data["planes"].append({"plan": nuevo_plan.strip(), "hecho": False})
            ok, msg = save_github_file(DATA_FILE, st.session_state.app_data, "Add new plan")
            if ok:
                st.success("¡Plan agregado exitosamente!")
                st.rerun()
            else:
                st.error(f"Error al guardar plan: {msg}")
        else:
            st.warning("Escribe una propuesta de plan antes de guardar.")

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
                nueva_resp = {
                    "id": len(st.session_state.app_data["encuestas"]) + 1,
                    "autor": usuario,
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "p1": p1, "p2": p2, "p3": p3, "p4": p4,
                    "comentarios": []
                }
                st.session_state.app_data["encuestas"].insert(0, nueva_resp)
                ok, msg = save_github_file(DATA_FILE, st.session_state.app_data, "New survey response")
                if ok:
                    st.success("¡Respuesta registrada exitosamente!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error(f"Error al guardar encuesta: {msg}")
            else:
                st.warning("Responde al menos uno de los campos antes de enviar.")

    st.divider()
    st.subheader("💬 Respuestas y Comentarios Mutuos")
    
    if not st.session_state.app_data["encuestas"]:
        st.info("Aún no hay respuestas registradas. ¡Sé el primero en responder arriba!")
    else:
        for enc in st.session_state.app_data["encuestas"]:
            st.markdown(f"### 💌 Encuesta de {enc['autor']} ({enc['fecha']})")
            st.write(f"**1. Momento favorito:** {enc['p1']}")
            st.write(f"**2. Antojo/Plan:** {enc['p2']}")
            st.write(f"**3. Consentimiento:** {enc['p3']}")
            st.write(f"**4. Mensaje secreto:** {enc['p4']}")
            
            if enc["comentarios"]:
                st.write("**Comentarios:**")
                for c in enc["comentarios"]:
                    st.write(f"- *{c['autor']}*: {c['texto']}")
            
            nuevo_comentario = st.text_input(f"Comentar en la respuesta de {enc['autor']}:", key=f"comm_in_{enc['id']}")
            if st.button("Comentar 💬", key=f"comm_btn_{enc['id']}"):
                if nuevo_comentario.strip():
                    enc["comentarios"].append({"autor": usuario, "texto": nuevo_comentario.strip()})
                    ok, msg = save_github_file(DATA_FILE, st.session_state.app_data, "Add comment")
                    if ok:
                        st.success("Comentario publicado.")
                        st.rerun()
                    else:
                        st.error(f"Error al publicar comentario: {msg}")
            st.divider()

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
                nueva_foto = {"url": url_guardada, "caption": descripcion_foto, "autor": usuario}
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
            st.warning("Selecciona una foto de tu teléfono antes de hacer clic en guardar.")

    st.divider()
    if not st.session_state.app_data["fotos"]:
        st.info("Aún no hay fotos subidas en la galería.")
    else:
        for foto in st.session_state.app_data["fotos"]:
            st.image(foto["url"], caption=f"{foto['caption']} — Subido por {foto['autor']}", use_container_width=True)
