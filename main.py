import streamlit as st
import random
import urllib.parse

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Impostor", page_icon="🕵️‍♂️", layout="centered")

# Estilo CSS
st.markdown("""
    <style>
    .main { background-color: #121212; }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background-color: #2E7D32;
        color: white;
        border: none;
        font-size: 18px;
        font-weight: bold;
    }
    .btn-social {
        display: inline-block;
        width: 100%;
        text-align: center;
        padding: 10px;
        border-radius: 10px;
        margin-top: 10px;
        text-decoration: none;
        font-weight: bold;
        color: white !important;
    }
    .btn-whatsapp { background-color: #25D366; }
    .btn-cafe { background-color: #FF813F; }
    .role-card {
        padding: 30px;
        border-radius: 20px;
        background-color: #1E1E1E;
        text-align: center;
        border: 2px solid #333;
        margin-bottom: 20px;
    }
    h1, h2, h3, p, span, label { color: white !important; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS (Palabra, Pista Relacionada) ---
DATOS = {
    "Lugares": [
        ("Cine", "Pantalla"), ("Hospital", "Salud"), ("Escuela", "Libros"), ("Museo", "Arte"), 
        ("Aeropuerto", "Aviones"), ("Playa", "Arena"), ("Gimnasio", "Pesas"), ("Casino", "Cartas"),
        ("Zoo", "Animales"), ("Base espacial", "Cohete"), ("Submarino", "Agua"), ("Circo", "Carpa"),
        ("Hotel", "Cama"), ("Iglesia", "Rezar"), ("Fábrica", "Humo"), ("Castillo", "Rey"),
        ("Granja", "Tractor"), ("Crucero", "Barco"), ("Desierto", "Calor"), ("Selva", "Árboles"),
        ("Banco", "Dinero"), ("Prisión", "Cárcel"), ("Teatro", "Escenario"), ("Farmacia", "Pastillas"),
        ("Spa", "Relax"), ("Cementerio", "Tumbas"), ("Discoteca", "Baile"), ("Palacio", "Lujo"),
        ("Volcán", "Lava"), ("Bosque", "Leña"), ("Pirámide", "Egipto"), ("Hogwarts", "Magia")
    ],
    "Personajes Famosos": [
        ("Lionel Messi", "Fútbol"), ("Cristiano Ronaldo", "Goles"), ("Michael Jackson", "Pop"),
        ("Albert Einstein", "Ciencia"), ("Marilyn Monroe", "Rubia"), ("Napoleón", "Guerra"),
        ("Steve Jobs", "Manzana"), ("Elon Musk", "Marte"), ("Donald Trump", "Peluquín"),
        ("Batman", "Murciélago"), ("Superman", "Capa"), ("Spider-Man", "Araña"),
        ("Harry Potter", "Gafas"), ("Sherlock Holmes", "Lupa"), ("Darth Vader", "Espada"),
        ("Mickey Mouse", "Ratón"), ("Homer Simpson", "Donut"), ("Shrek", "Ogro"),
        ("Pikachu", "Rayo"), ("Mario Bros", "Gorra")
    ],
    "Objetos": [
        ("Móvil", "Llamada"), ("Ordenador", "Teclado"), ("Televisión", "Mando"), ("Reloj", "Hora"),
        ("Gafas de sol", "Luz"), ("Llaves", "Puerta"), ("Cartera", "Monedas"), ("Paraguas", "Lluvia"),
        ("Mochila", "Espalda"), ("Bolígrafo", "Tinta"), ("Libro", "Hojas"), ("Espejo", "Reflejo"),
        ("Silla", "Asiento"), ("Sofá", "Salón"), ("Cama", "Dormir"), ("Nevera", "Frío"),
        ("Microondas", "Calentar"), ("Cafetera", "Desayuno"), ("Cuchillo", "Filo"), ("Guitarra", "Cuerdas"),
        ("Bicicleta", "Pedales"), ("Coche", "Ruedas"), ("Anillo", "Dedo"), ("Perfume", "Olor"),
        ("Zapatos", "Pies"), ("Mapa", "Ruta"), ("Brújula", "Norte"), ("Vela", "Fuego")
    ]
}

if 'paso' not in st.session_state:
    st.session_state.paso = 'config'
    st.session_state.jugador_actual = 0
    st.session_state.viendo_rol = False

# Configuración (Cambia estas URLs por las tuyas)
url_app = "https://tu-app.streamlit.app" 
msg_whatsapp = urllib.parse.quote(f"¡Mira este juego! Se llama Impostor: {url_app}")

if st.session_state.paso == 'config':
    st.title("🕵️‍♂️ Impostor")
    n_jugadores = st.number_input("¿Cuántos jugadores?", min_value=3, max_value=20, value=4)
    n_impostores = st.number_input("Número de impostores", min_value=1, max_value=max(1, n_jugadores-2), value=1)
    cat_elegida = st.selectbox("Categoría", list(DATOS.keys()))
    
    dar_pista = st.toggle("Activar pista para el Impostor", value=True)
    
    if st.button("PREPARAR PARTIDA"):
        item_elegido = random.choice(DATOS[cat_elegida]) # Elige un par (Palabra, Pista)
        palabra, pista = item_elegido
        
        roles = ["Impostor"] * n_impostores + ["Ciudadano"] * (n_jugadores - n_impostores)
        random.shuffle(roles)
        
        st.session_state.roles = roles
        st.session_state.palabra = palabra
        st.session_state.pista = pista if dar_pista else None
        st.session_state.categoria = cat_elegida
        st.session_state.paso = 'reparto'
        st.session_state.jugador_actual = 0
        st.rerun()

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1: st.markdown(f'<a href="https://wa.me/?text={msg_whatsapp}" class="btn-social btn-whatsapp">📲 Compartir</a>', unsafe_allow_html=True)
    with c2: st.markdown(f'<a href="https://paypal.me/tuusuario" class="btn-social btn-cafe">☕ Invítame</a>', unsafe_allow_html=True)

elif st.session_state.paso == 'reparto':
    actual = st.session_state.jugador_actual
    if actual < len(st.session_state.roles):
        st.subheader(f"Jugador {actual + 1}")
        if not st.session_state.viendo_rol:
            if st.button("VER MI ROL"):
                st.session_state.viendo_rol = True
                st.rerun()
        else:
            rol = st.session_state.roles[actual]
            st.markdown('<div class="role-card">', unsafe_allow_html=True)
            if rol == "Impostor":
                st.error("ERES EL IMPOSTOR")
                if st.session_state.pista:
                    st.info(f"Pista: **{st.session_state.pista}**")
            else:
                st.success("ERES CIUDADANO")
                st.write(f"Palabra: **{st.session_state.palabra}**")
            st.markdown('</div>', unsafe_allow_html=True)
            if st.button("OCULTAR"):
                st.session_state.jugador_actual += 1
                st.session_state.viendo_rol = False
                st.rerun()
    else:
        st.session_state.paso = 'juego'
        st.rerun()

elif st.session_state.paso == 'juego':
    st.title("¡A debatir!")
    st.write(f"Categoría: **{st.session_state.categoria}**")
    if st.button("NUEVA PARTIDA"):
        st.session_state.paso = 'config'
        st.rerun()
        
