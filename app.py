import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Para Yesenia Alejandra ❤️",
    page_icon="💖",
    layout="centered"
)

# Estilos visuales
st.markdown("""
    <style>
    .stApp { background-color: #fff0f3; }
    h1, h2, h3 { color: #c9184a !important; text-align: center; font-family: 'Segoe UI', sans-serif; }
    .frase-especial {
        color: #590d22; font-size: 1.1rem; font-weight: bold; text-align: center;
        background-color: #ffccd5; padding: 15px; border-radius: 15px;
        border-left: 6px solid #ff4d6d; margin: 15px 0;
    }
    .stButton>button {
        background-color: #ff4d6d; color: white; border-radius: 20px;
        border: none; font-weight: bold; width: 100%; padding: 10px;
    }
    .stButton>button:hover { background-color: #c9184a; color: white; }
    </style>
""", unsafe_allow_html=True)

st.title("💖 Nuestro Espacio Especial 💖")
st.write("<h3 style='text-align: center; color: #a4133c;'>Dedicado a Yesenia Alejandra 💕</h3>", unsafe_allow_html=True)

st.markdown("""
    <div class='frase-especial'>
        ✨ "Me gustaría ponerme al día con todos nuestros próximos planes, Yesenia Alejandra." ✨
    </div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📸 Nuestras Fotos", "🗓️ Nuestros Planes", "📝 Encuesta Semanal"])

with tab1:
    st.subheader("📸 Galería de Recuerdos")
    st.write("Sube las fotos que quieras desde la fototeca de tu iPhone:")
    fotos_subidas = st.file_uploader(
        "Toca aquí para seleccionar fotos 📲", 
        type=["jpg", "png", "jpeg"], 
        accept_multiple_files=True
    )
    if fotos_subidas:
        for foto in fotos_subidas:
            st.image(foto, use_container_width=True, caption="Un momento inolvidable ❤️")

with tab2:
    st.subheader("📌 Lista de Nuestros Próximos Planes")
    if "lista_planes" not in st.session_state:
        st.session_state.lista_planes = [
            {"plan": "Ir a comer unos postres/helados ricos 🍦", "hecho": False},
            {"plan": "Tarde de películas, cobijas y comida chatarra 🍿", "hecho": False},
            {"plan": "Un picnic romántico al aire libre 🧺", "hecho": False},
            {"plan": "Salir a cenar a un sitio nuevo 🍔", "hecho": False}
        ]
    
    for idx, item in enumerate(st.session_state.lista_planes):
        st.session_state.lista_planes[idx]["hecho"] = st.checkbox(
            item["plan"], value=item["hecho"], key=f"plan_{idx}"
        )
    
    st.divider()
    nuevo_plan = st.text_input("➕ ¿Tienes un nuevo plan?")
    if st.button("Agregar a la lista"):
        if nuevo_plan.strip():
            st.session_state.lista_planes.append({"plan": nuevo_plan, "hecho": False})
            st.rerun()

with tab3:
    st.subheader("📝 Encuesta Semanal")
    with st.form(key='survey_form'):
        p1 = st.text_area("1. ¿Cuál fue tu momento favorito de esta semana conmigo?")
        p2 = st.text_input("2. ¿Qué se te antoja comer o hacer este fin de semana?")
        p3 = st.select_slider("3. ¿Qué tan consentida te has sentido?", options=["Poco 🥺", "Normal 😊", "Muy Consentida 🥰", "Nivel Reina 👑"])
        p4 = st.text_area("4. Un mensajito o nota secreta para mí ❤️")
        
        if st.form_submit_button("Enviar Respuestas 💌"):
            st.success("¡Respuestas enviadas con éxito, Yesenia! Te amo ❤️")
            st.balloons()
