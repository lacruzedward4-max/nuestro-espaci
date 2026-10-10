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

# Integración con GitHub API
REPO_OWNER = "lacruzedward4-max"
REPO_NAME = "nuestro-espaci"
DATA_FILE = "data.json"

GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN", None)

def get_github_file(filepath):
    if not GITHUB_TOKEN:
        return None, None
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{filepath}"
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        content = res.json()
        decoded = base64.b64decode(content["content"]).decode("utf-8")
        return json.loads(decoded), content["sha"]
    return None, None

def save_github_file(filepath, data_dict, sha=None, commit_message="Update data"):
    if not GITHUB_TOKEN:
        return False
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{filepath}"
    encoded_content = base64.b64encode(json.dumps(data_dict, ensure_ascii=False, indent=2).encode("utf-8")).decode("utf-8")
    payload = {
        "message": commit_message,
        "content": encoded_content
    }
    if sha:
        payload["sha"] = sha
    res = requests.put(url, headers=headers, json=payload)
    return res.status_code in [200, 201]

def save_github_image(filename, image_bytes):
    if not GITHUB_TOKEN:
        return None
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    filepath = f"uploads/{filename}"
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{filepath}"
    encoded_content = base64.b64encode(image_bytes).decode("utf-8")
    payload = {
        "message": f"Upload image {filename}",
        "content": encoded_content
    }
    res = requests.put(url, headers=headers, json=payload)
    if res.status_code in [200, 201]:
        return f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main/{filepath}"
    return None

# Datos iniciales
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

remote_data, file_sha = get_github_file(DATA_FILE)
app_data = remote_data if remote_data else initial_data

# Foto de fondo personalizada (IMG_0980.png)
bg_url = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main/IMG_0980.png"

st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("{bg_url}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .main .block-container {{
        background-color: rgba(255, 255, 255, 0.95);
        padding: 25px;
        border-radius: 20px;
        margin-top: 15px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.25);
    }}
    h1, h2, h3, p, label, span, div {{
        color: #1a1a1a !important;
    }}
    h1, h2, h3 {{
        color: #c9184a !important;
        text-align: center;
    }}
    .frase-especial {{
        color: #590d22 !important;
        font-size: 1.1rem;
        font-weight: bold;
        text-align: center;
        background-color: #ffccd5;
        padding: 15px;
        border-radius: 15px;
        border-left: 6px solid #ff4d6d;
        margin: 15px 0;
    }}
    .stTextInput input, .stTextArea textarea {{
        color: #000000 !important;
        background-color: #ffffff !important;
        border: 2px solid #ff4d6d !important;
        border-radius: 10px !important;
    }}
    .stCheckbox label p {{
        color: #000000 !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
    }}
    .stButton>button {{
        background-color: #ff4d6d;
        color: white !important;
        border-radius: 20px;
        border: none;
        font-weight: bold;
        width: 100%;
        padding: 10px;
    }}
    </style>
""", unsafe_allow_html=True)

st.title("💖 Nuestro Espacio Especial 💖")
st.write("<h3 style='text-align: center; color: #a4133c;'>Dedicado a Yesenia Alejandra 💕</h3>", unsafe_allow_html=True)

st.markdown("""
    <div class='frase-especial'>
        ✨ "Me gustaría ponerme al día con todos nuestros próximos planes, Yesenia Alejandra." ✨
    </div>
""", unsafe_allow_html=True)

usuario = st.selectbox("👤 ¿Quién está en la app ahora?", ["Yesenia Alejandra 💕", "Edward ❤️"])

tab1, tab2, tab3 = st.tabs(["📌 Nuestros Planes", "📝 Encuesta Semanal", "📸 Recuerdos"])

# TAB 1: PLANES
with tab1:
    st.subheader("📌 Lista de Nuestros Próximos Planes")
    
    cambio_planes = False
    for idx, item in enumerate(app_data["planes"]):
        estado = st.checkbox(item["plan"], value=item["hecho"], key=f"plan_{idx}")
        if estado != item["hecho"]:
            app_data["planes"][idx]["hecho"] = estado
            cambio_planes = True
            
    if cambio_planes and GITHUB_TOKEN:
        save_github_file(DATA_FILE, app_data, file_sha, "Update planes status")
        st.rerun()

    st.divider()
    nuevo_plan = st.text_input("➕ Agregar nuevo plan a la lista:")
    if st.button("Guardar Plan 📝"):
        if nuevo_plan.strip():
            app_data["planes"].append({"plan": nuevo_plan.strip(), "hecho": False})
            if GITHUB_TOKEN:
                save_github_file(DATA_FILE, app_data, file_sha, "Add new plan")
            st.success("¡Plan agregado exitosamente!")
            st.rerun()

# TAB 2: ENCUESTA
with tab2:
    st.subheader("📝 Encuesta e Interacción Semanal")
    
    with st.expander("➕ Responder la encuesta de esta semana", expanded=True):
        p1 = st.text_area("1. ¿Cuál fue tu momento favorito de esta semana juntos?")
        p2 = st.text_input("2. ¿Qué se te antoja comer o hacer este fin de semana?")
        p3 = st.select_slider("3. ¿Qué tan consentido/a te has sentido?", options=["Poco 🥺", "Normal 😊", "Muy Consentido/a 🥰", "Nivel Reina/Rey 👑"])
        p4 = st.text_area("4. Un mensajito o nota secreta ❤️")
        
        if st.button("Enviar Respuestas 💌"):
            nueva_resp = {
                "id": len(app_data["encuestas"]) + 1,
                "autor": usuario,
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "p1": p1, "p2": p2, "p3": p3, "p4": p4,
                "comentarios": []
            }
            app_data["encuestas"].insert(0, nueva_resp)
            if GITHUB_TOKEN:
                save_github_file(DATA_FILE, app_data, file_sha, "New survey response")
            st.success("¡Respuesta registrada!")
            st.balloons()
            st.rerun()

    st.divider()
    st.subheader("💬 Respuestas y Comentarios Mutuos")
    
    if not app_data["encuestas"]:
        st.info("Aún no hay respuestas registradas. ¡Sé el primero en responder arriba!")
    else:
        for enc in app_data["encuestas"]:
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
            if st.button(f"Comentar 💬", key=f"comm_btn_{enc['id']}"):
                if nuevo_comentario.strip():
                    enc["comentarios"].append({"autor": usuario, "texto": nuevo_comentario.strip()})
                    if GITHUB_TOKEN:
                        save_github_file(DATA_FILE, app_data, file_sha, "Add comment")
                    st.success("Comentario publicado.")
                    st.rerun()
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
            
            url_guardada = save_github_image(nombre_foto, bytes_data)
            if url_guardada:
                app_data["fotos"].insert(0, {"url": url_guardada, "caption": descripcion_foto, "autor": usuario})
                save_github_file(DATA_FILE, app_data, file_sha, "Add new photo")
                st.success("¡Foto guardada en la galería compartida!")
                st.rerun()

    st.divider()
    if not app_data["fotos"]:
        st.info("Aún no hay fotos subidas en la galería.")
    else:
        for foto in app_data["fotos"]:
            st.image(foto["url"], caption=f"{foto['caption']} — Subido por {foto['autor']}", use_container_width=True)
