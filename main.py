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

# --- BASE DE DATOS DE PALABRAS ---
CATEGORIAS = {
    "Lugares": ["Cine", "Gimnasio", "Hospital", "Supermercado", "Aeropuerto", "Biblioteca", "Playa", "Casino", "Escuela", "Restaurante", "Zoo", "Estación espacial", "Museo", "Base militar", "Submarino", "Circo", "Hotel", "Peluquería", "Iglesia", "Parque de atracciones", "Estadio de fútbol", "Fábrica", "Castillo", "Granja", "Crucero", "Desierto", "Selva", "Laboratorio", "Banco", "Prisión", "Teatro", "Gasolinera", "Farmacia", "Spa", "Ayuntamiento", "Comisaría", "Cementerio", "Discoteca", "Juguetería", "Tribunal", "Campamento", "Concierto", "Universidad", "Panadería", "Embajada", "Puente", "Faro", "Mina", "Jungla", "Palacio", "Rascacielos", "Estación de esquí", "Bosque", "Isla desierta", "Volcán", "Mercado", "Invernadero", "Autobús", "Tren", "Mansión", "Estación de bomberos", "Puerto", "Acuario", "Observatorio", "Estadio de tenis", "Pista de hielo", "Lavandería", "Oficina", "Garaje", "Centro comercial", "Safari", "Templo", "Cueva", "Viñedo", "Jardín", "Campo de golf", "Base antártica", "Pirámide", "Casa blanca", "Pentágono", "Coliseo", "Torre Eiffel", "Gran Muralla", "Stonehenge", "Everest", "Titanic", "El Olimpo", "Arca de Noé", "El Infierno", "El Paraíso", "Narnia", "Hogwarts", "Batcueva", "Estrella de la Muerte", "Neverland", "País de las Maravillas", "Tierra Media", "Ciudad Gótica", "Springfield", "Área 51"],
    "Personajes Famosos": ["Lionel Messi", "Cristiano Ronaldo", "Michael Jackson", "Elvis Presley", "Albert Einstein", "Marilyn Monroe", "Leonardo da Vinci", "Cleopatra", "Napoleón", "Mahatma Gandhi", "Steve Jobs", "Bill Gates", "Elon Musk", "Mark Zuckerberg", "Donald Trump", "Barack Obama", "Reina Isabel II", "Papa Francisco", "Nelson Mandela", "Marie Curie", "Pablo Picasso", "Frida Kahlo", "Salvador Dalí", "Walt Disney", "William Shakespeare", "Isaac Newton", "Charles Darwin", "Mozart", "Beethoven", "Freddie Mercury", "Madonna", "Beyoncé", "Taylor Swift", "Shakira", "Lady Gaga", "Michael Jordan", "Rafael Nadal", "Usain Bolt", "Muhammad Ali", "Tiger Woods", "Brad Pitt", "Angelina Jolie", "Tom Cruise", "Leonardo DiCaprio", "Will Smith", "Johnny Depp", "Julia Roberts", "Meryl Streep", "Jackie Chan", "Arnold Schwarzenegger", "Batman", "Superman", "Spider-Man", "Iron Man", "Harry Potter", "Sherlock Holmes", "James Bond", "Darth Vader", "Luke Skywalker", "Yoda", "Jack Sparrow", "Indiana Jones", "Lara Croft", "Mario Bros", "Pikachu", "Mickey Mouse", "Bugs Bunny", "Homer Simpson", "Bob Esponja", "Shrek", "Cenicienta", "Blancanieves", "Elsa", "El Joker", "Hannibal Lecter", "Drácula", "Frankenstein", "El Zorro", "Robin Hood", "Don Quijote", "Jesucristo", "Buda", "Cristóbal Colón", "Julio César", "Alejandro Magno", "Abraham Lincoln", "Martin Luther King", "Malala Yousafzai", "Greta Thunberg", "Neil Armstrong", "Pelé", "Maradona", "Serena Williams", "Stephen Hawking", "Vincent van Gogh", "Agatha Christie", "J.K. Rowling", "Steven Spielberg", "Oprah Winfrey", "Mr. Beast"],
    "Objetos": ["Móvil", "Ordenador", "Televisión", "Reloj", "Gafas de sol", "Llaves", "Cartera", "Paraguas", "Mochila", "Bolígrafo", "Libro", "Cuaderno", "Tijeras", "Lámpara", "Espejo", "Peine", "Cepillo de dientes", "Jabón", "Toalla", "Silla", "Mesa", "Sofá", "Cama", "Almohada", "Manta", "Ventilador", "Aire acondicionado", "Nevera", "Microondas", "Horno", "Tostadora", "Cafetera", "Sartén", "Cuchillo", "Tenedor", "Cuchara", "Plato", "Vaso", "Botella", "Martillo", "Destornillador", "Taladro", "Escalera", "Linterna", "Pilas", "Cámara", "Auriculares", "Guitarra", "Piano", "Balón", "Bicicleta", "Casco", "Patinete", "Coche", "Neumático", "Anillo", "Collar", "Pendientes", "Pintalabios", "Perfume", "Secador", "Aspiradora", "Plancha", "Máquina de coser", "Aguja", "Hilo", "Botón", "Cremallera", "Zapatos", "Calcetines", "Pantalones", "Camiseta", "Sombrero", "Guantes", "Bufanda", "Maleta", "Pasaporte", "Billete", "Moneda", "Tarjeta", "Escoba", "Cubo de basura", "Papel higiénico", "Periódico", "Diccionario", "Mapa", "Brújula", "Telescopio", "Microscopio", "Calculadora", "Mando", "Consola", "Extintor", "Botiquín", "Termómetro", "Jeringuilla", "Vela", "Cerillas", "Encendedor", "Papelera"]
}

if 'paso' not in st.session_state:
    st.session_state.paso = 'config'
    st.session_state.jugador_actual = 0
    st.session_state.viendo_rol = False

# --- LÓGICA DE COMPARTIR ---
url_app = "app-impostor-joseballazn-jwgnderxxewapp86czbps4b.streamli.app"
msg_whatsapp = urllib.parse.quote(f"¡Mira este juego para fiestas! Se llama Impostor y es genial: {url_app}")

if st.session_state.paso == 'config':
    st.title("🕵️‍♂️ Impostor")
    n_jugadores = st.number_input("¿Cuántos jugadores?", min_value=3, max_value=20, value=4)
    n_impostores = st.number_input("Número de impostores", min_value=1, max_value=max(1, n_jugadores-2), value=1)
    cat_elegida = st.selectbox("Categoría", list(CATEGORIAS.keys()))
    
    if st.button("PREPARAR PARTIDA"):
        palabra = random.choice(CATEGORIAS[cat_elegida])
        roles = ["Impostor"] * n_impostores + ["Ciudadano"] * (n_jugadores - n_impostores)
        random.shuffle(roles)
        st.session_state.roles = roles
        st.session_state.palabra = palabra
        st.session_state.categoria = cat_elegida
        st.session_state.paso = 'reparto'
        st.session_state.jugador_actual = 0
        st.rerun()

    # --- SECCIÓN SOCIAL ---
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<a href="https://wa.me/?text={msg_whatsapp}" class="btn-social btn-whatsapp">📲 Compartir</a>', unsafe_allow_html=True)
    with col2:
        # CAMBIA ESTE ENLACE POR TU PAYPAL O KO-FI
        st.markdown(f'<a href="https://www.paypal.me/JoseBallesta570" class="btn-social btn-cafe">☕ Invítame</a>', unsafe_allow_html=True)

# (Resto del código de reparto y juego se mantiene igual...)
elif st.session_state.paso == 'reparto':
    actual = st.session_state.jugador_actual
    total = len(st.session_state.roles)
    if actual < total:
        st.subheader(f"Jugador {actual + 1}")
        if not st.session_state.viendo_rol:
            st.write("Pasa el móvil al siguiente.")
            if st.button("VER ROL"):
                st.session_state.viendo_rol = True
                st.rerun()
        else:
            rol = st.session_state.roles[actual]
            st.markdown('<div class="role-card">', unsafe_allow_html=True)
            if rol == "Impostor":
                st.error("ERES EL IMPOSTOR")
                st.write(f"Categoría: **{st.session_state.categoria}**")
            else:
                st.success("ERES CIUDADANO")
                st.write(f"Palabra secreta: **{st.session_state.palabra}**")
            st.markdown('</div>', unsafe_allow_html=True)
            if st.button("OCULTAR"):
                st.session_state.jugador_actual += 1
                st.session_state.viendo_rol = False
                st.rerun()
    else:
        st.session_state.paso = 'juego'
        st.rerun()

elif st.session_state.paso == 'juego':
    st.title("¡A jugar!")
    st.write(f"Categoría: **{st.session_state.categoria}**")
    st.info("Buscad al impostor.")
    if st.button("REINICIAR JUEGO"):
        st.session_state.paso = 'config'
        st.rerun()
        
