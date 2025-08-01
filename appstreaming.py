import streamlit as st
import urllib.parse

# URL base de tus imágenes en GitHub
URL_BASE = "https://raw.githubusercontent.com/sebassss1218/imagenes-streaming-/main/imagenesapp/"

# Estilos personalizados
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url('{URL_BASE}DATA2.gif');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
        font-family: 'Arial', sans-serif;
        color: white;
    }}
    .app-card {{
        display: inline-block;
        width: 160px;
        margin: 10px;
        padding: 10px;
        text-align: center;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        background-color: rgba(20, 20, 20, 0.85);
        transition: 0.3s;
    }}
    .app-card:hover {{
        box-shadow: 0 6px 12px rgba(0,0,0,0.3);
    }}
    .app-img {{
        width: 100px;
        height: 100px;
        object-fit: contain;
    }}
    .price-tag {{
        font-size: 18px;
        color: #fff;
        font-weight: bold;
        margin-top: 5px;
    }}
    .checkbox-label span {{
        font-size: 20px !important;
        font-weight: bold;
        color: white !important;
    }}
    .whatsapp-btn {{
        display: inline-flex;
        align-items: center;
        background-color: #25D366;
        padding: 12px 18px;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        text-decoration: none;
        font-size: 18px;
        margin-top: 10px;
    }}
    .whatsapp-btn img {{
        width: 28px;
        height: 28px;
        margin-right: 10px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Configuración general
st.set_page_config(page_title="Combos Streaming", layout="wide")
st.title("🎬 Arma tu combo de Streaming 📱")
st.write("Selecciona las apps que quieres y obtén un combo personalizado con precio justo.")

# Precios del proveedor
precios_proveedor = {
    "Netflix": 9000,
    "Disney+": 6500,
    "Max": 4500,
    "Prime": 4500,
    "Vix": 3500,
    "Paramount+": 3500,
    "IPTV": 3800,
    "Crunchyroll": 3500,
    "YouTube Premium": 3500,
    "Plex": 3800,
    "Canva Pro": 7000,
    "Spotify": 12000
}

# Precios para el cliente
precios_cliente_unitarios = {
    "Netflix": 13000,
    "Disney+": 10500,
    "Max": 7500,
    "Prime": 7500,
    "Vix": 6500,
    "Paramount+": 6500,
    "IPTV": 6800,
    "Crunchyroll": 6500,
    "YouTube Premium": 7500,
    "Plex": 6500,
    "Canva Pro": 12000,
    "Spotify": 15000
}

# Lista de apps
apps = list(precios_cliente_unitarios.keys())
seleccionadas = []

st.markdown("## Selecciona tus apps:")
st.markdown("<div>", unsafe_allow_html=True)

cols = st.columns(4)
for i, app in enumerate(apps):
    with cols[i % 4]:
        nombre_archivo = app.replace('+', 'plus').replace(' ', '_').replace('Pro', '').lower() + ".png"
        url_imagen = URL_BASE + nombre_archivo

        clicked = st.checkbox(f"  {app}", key=app)
        st.image(url_imagen, width=100)
        st.markdown(f"<div class='price-tag'>${precios_cliente_unitarios[app]:,}</div>", unsafe_allow_html=True)
        if clicked:
            seleccionadas.append(app)

st.markdown("</div>", unsafe_allow_html=True)

# 🔧 Función de redondeo personalizada
def redondear_personalizado(valor):
    resto = valor % 1000
    base = valor - resto
    if resto < 390:
        return base
    elif 390 <= resto < 790:
        return base + 500
    else:
        return base + 1000

# Código de descuento
codigo = st.text_input("¿Tienes un código de descuento?").lower().strip()
descuento = 0
if codigo == "familia":
    descuento = 1000
elif codigo == "falla":
    descuento = 500

# Cálculo del combo
if seleccionadas:
    if len(seleccionadas) == 1:
        total_final = precios_cliente_unitarios[seleccionadas[0]]
    else:
        costo_total = sum(precios_proveedor[app] for app in seleccionadas)
        total_con_ganancia = costo_total * 1.22
        total_final = redondear_personalizado(int(total_con_ganancia))

    total_final -= descuento
    total_final = max(total_final, 0)

    st.markdown("---")
    st.subheader("📦 Resumen del Combo")
    st.write(f"**Apps seleccionadas:** {', '.join(seleccionadas)}")
    st.markdown(f"### 💰 Precio total del combo: ${int(total_final):,}")

    mensaje = f"Hola, quiero el combo con: {', '.join(seleccionadas)} por ${int(total_final):,}"
    mensaje_encoded = urllib.parse.quote(mensaje)
    url_whatsapp = f"https://wa.me/573202628338?text={mensaje_encoded}"
    st.markdown(
        f"""
        <a href="{url_whatsapp}" class="whatsapp-btn" target="_blank">
            <img src="{URL_BASE}whatsapp.png" alt="WhatsApp">
            Pedir este combo por WhatsApp
        </a>
        """,
        unsafe_allow_html=True
    )
else:
    st.info("Selecciona al menos una app para ver el precio.")


