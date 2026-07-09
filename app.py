import streamlit as st
import scraper_engine as wolf_engine

# Configuración de la página web de Wolf
st.set_page_config(page_title="Proyecto Wolf - Apuestas Deportivas", layout="wide")

st.title("🐺 Proyecto Wolf - Comparador en Tiempo Real (Lima, Perú)")
st.caption("Filtro de cuotas optimizado para Bet365, Betano, Betsson, 1xBet, Inkabet y Doradobet.")

# Botón para forzar la actualización de datos
if st.button("🔄 Actualizar Cuotas y Partidos"):
    st.cache_data.clear()

# Obtener los datos organizados del motor
datos_partidos = wolf_engine.simular_datos_casas()

# Crear las 3 pestañas solicitadas
tab_en_vivo, tab_hoy, tab_manana = st.tabs([
    "🔴 EN VIVO AHORA", 
    "📅 PARTIDOS DE HOY", 
    "⏳ PARTIDOS DE MAÑANA"
])

def renderizar_tabla_cuotas(cuotas):
    """Genera una tabla comparativa limpia para las 6 casas"""
    st.write("**Comparativa de Casas de Apuestas:**")
    
    # Crear columnas para simular tabla
    col_casa, col_1, col_x, col_2 = st.columns([2, 1, 1, 1])
    col_casa.markdown("**Casa de Apuesta**")
    col_1.markdown("🔴 **Gana Local (1)**")
    col_x.markdown("⚪ **Empate (X)**")
    col_2.markdown("🔵 **Gana Visita (2)**")
    
    for casa, valores in cuotas.items():
        c_casa, c_1, c_x, c_2 = st.columns([2, 1, 1, 1])
        c_casa.text(casa)
        c_1.info(f"{valores['1']:.2f}")
        c_x.info(f"{valores['X']:.2f}")
        c_2.info(f"{valores['2']:.2f}")

# ----------------- PESTAÑA: EN VIVO -----------------
with tab_en_vivo:
    partidos_vivo = [p for p in datos_partidos if p["categoria"] == "en_vivo"]
    if not partidos_vivo:
        st.info("No hay partidos jugándose en este momento.")
    for p in partidos_vivo:
        with st.container(border=True):
            # Formato En Vivo: Nombre, Marcador y Tiempo
            st.subheader(f"🏟️ {p['local']} {p['marcador']} {p['visitante']}")
            st.markdown(f"⏱️ **Tiempo Transcurrido:** :red[{p['tiempo']}]")
            renderizar_tabla_cuotas(p["cuotas"])

# ----------------- PESTAÑA: HOY -----------------
with tab_hoy:
    partidos_hoy = [p for p in datos_partidos if p["categoria"] == "hoy"]
    if not partidos_hoy:
        st.info("No hay más partidos programados para hoy.")
    for p in partidos_hoy:
        with st.container(border=True):
            # Formato Hoy: Nombre y Hora Local
            st.subheader(f"⚽ {p['local']} vs {p['visitante']}")
            st.markdown(f"🕒 **Hora de Lima:** {p['hora_inicio']}")
            renderizar_tabla_cuotas(p["cuotas"])

# ----------------- PESTAÑA: MAÑANA -----------------
with tab_manana:
    partidos_manana = [p for p in datos_partidos if p["categoria"] == "manana"]
    if not partidos_manana:
        st.info("No hay partidos registrados para mañana aún.")
    for p in partidos_manana:
        with st.container(border=True):
            # Formato Mañana: Nombre y Hora Local
            st.subheader(f"📅 {p['local']} vs {p['visitante']}")
            st.markdown(f"🕒 **Hora de Lima:** {p['hora_inicio']}")
            renderizar_tabla_cuotas(p["cuotas"])