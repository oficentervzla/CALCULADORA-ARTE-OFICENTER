import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# Configuración de página
st.set_page_config(page_title="Sistema Art Center", layout="wide", page_icon="🎨")

# --- DISEÑO, COLORES Y ESTILOS ENFOCADOS EN TU MARCA ---
st.markdown("""
    <style>
        .stApp { background-color: #ffffff; }
        h1, h2, h3 { font-family: 'Arial', sans-serif; text-align: center; }
        
        .titulo-principal { color: #e9769d !important; font-size: 50px; font-weight: bold; margin-bottom: 5px; }
        .frase-principal { color: #74b7d5 !important; font-size: 28px; font-style: italic; font-weight: bold; margin-bottom: 30px; }
        
        /* Estilos de botones que actúan como pestañas superiores en el sidebar/menú */
        .stButton>button {
            border-radius: 12px !important;
            font-weight: bold !important;
        }
        
        /* Tarjeta de presupuesto final destacada */
        .tarjeta-precio {
            background-color: #f7f9fa; padding: 20px; border-radius: 15px;
            border-left: 6px solid #e9769d; box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
            text-align: center;
        }
        
        /* Estilo interactivo para los Toppers/Casillas del Home */
        div[data-testid="stColumn"] .stButton>button {
            background-color: #f7f9fa !important;
            color: #333333 !important;
            border: 2px solid #fed80c !important;
            border-radius: 15px !important;
            padding: 25px 15px !important;
            width: 100% !important;
            min-height: 180px !important;
            box-shadow: 0px 4px 8px rgba(0,0,0,0.05) !important;
            transition: all 0.3s ease !important;
            white-space: normal !important;
            display: block !important;
        }
        div[data-testid="stColumn"] .stButton>button:hover {
            border-color: #e9769d !important;
            background-color: #ffffff !important;
            transform: translateY(-3px);
            box-shadow: 0px 6px 12px rgba(0,0,0,0.1) !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- SISTEMA DE ALMACENAMIENTO DE DATOS ---
def cargar_datos(archivo, tipo_esperado, defecto):
    if os.path.exists(archivo):
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                if isinstance(datos, tipo_esperado):
                    return datos
        except:
            pass
    return defecto

def guardar_datos(archivo, datos):
    with open(archivo, 'w', encoding='utf-8') as f: 
        json.dump(datos, f, ensure_ascii=False, indent=4)

hoy = datetime.now().strftime("%Y-%m-%d %H:%M")

# Inicialización segura de Estados globales
if 'materiales' not in st.session_state:
    st.session_state.materiales = cargar_datos('materiales.json', dict, {
        "Cartulina Escolar": {"Tipo": "Pieza (Área)", "Ancho": 50.0, "Alto": 70.0, "Costo": 0.50, "Precio": 1.00, "Marca": "Genérica", "Fecha": hoy},
        "Silicón (Barra)": {"Tipo": "Unidad (Cantidad)", "Ancho": 1.0, "Alto": 1.0, "Costo": 0.10, "Precio": 0.25, "Marca": "Genérica", "Fecha": hoy}
    })

if 'productos' not in st.session_state:
    st.session_state.productos = cargar_datos('productos.json', dict, {})

if 'items_presupuesto' not in st.session_state:
    st.session_state.items_presupuesto = []

if 'tasa_bcv' not in st.session_state:
    st.session_state.tasa_bcv = 36.50

# Control estable de navegación en lugar de st.tabs que crasheaba por renderizado paralelo
opciones_menu = [
    "🏠 Menú Principal", 
    "🧮 1- Crear Presupuesto", 
    "➕ 2- Crear Material", 
    "🎒 3- Verificar Panel de Materiales", 
    "📜 4- Catálogo de Productos Finales"
]

if 'menu_actual' not in st.session_state:
    st.session_state.menu_actual = "🏠 Menú Principal"

# Barra de navegación limpia con Botones de Selección tipo Pestaña
st.write("###")
cols_nav = st.columns(5)
for i, opcion in enumerate(opciones_menu):
    with cols_nav[i]:
        # Resaltamos visualmente cuál pestaña está seleccionada actualmente
        es_activa = st.session_state.menu_actual == opcion
        tipo_boton = "primary" if es_activa else "secondary"
        if st.button(opcion, key=f"nav_tab_{i}", use_container_width=True, type=tipo_boton):
            st.session_state.menu_actual = opcion
            st.rerun()

st.divider()

# ==========================================
# 🏠 OPCIÓN: MENÚ PRINCIPAL
# ==========================================
if st.session_state.menu_actual == "🏠 Menú Principal":
    st.markdown("<p class='titulo-principal'>ART CENTER</p>", unsafe_allow_html=True)
    st.markdown("<p class='frase-principal'>¿Qué vamos a crear hoy?</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-weight: bold; color: #555;'>Selecciona una casilla o usa el menú de arriba para empezar:</p>", unsafe_allow_html=True)
    st.divider()
    
    st.markdown("### 🇲🇳 Control Cambiario")
    st.session_state.tasa_bcv = st.number_input("Tasa BCV del día (Bs.)", min_value=1.0, value=float(st.session_state.tasa_bcv), step=0.10, key="tasa_input_home")
    st.divider()
    
    # Casillas del Home interactivas como solicitaste
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("🧮 Presupuesto\n\nCalcula costos, precios de venta y desglosa tus ganancias al instante.", key="btn_home_pres"):
            st.session_state.menu_actual = "🧮 1- Crear Presupuesto"
            st.rerun()
    with c2:
        if st.button("➕ Crear Material\n\nRegistra nuevos insumos con sus medidas, marcas y ganancias.", key="btn_home_mat"):
            st.session_state.menu_actual = "➕ 2- Crear Material"
            st.rerun()
    with c3:
        if st.button("🎒 Panel Materiales\n\nMira tu inventario, edita precios en masa y revisa tus porcentajes.", key="btn_home_panel"):
            st.session_state.menu_actual = "🎒 3- Verificar Panel de Materiales"
            st.rerun()
    with c4:
        if st.button("📜 Catálogo Final\n\nRevisa tus productos listos, añade fotos y gestiona historiales.", key="btn_home_cat"):
            st.session_state.menu_actual = "📜 4- Catálogo de Productos Finales"
            st.rerun()

    st.divider()
    st.markdown("<p style='text-align: center; font-size: 12px; color: #aaa;'>Una solución desarrollada para Oficenter C.A.</p>", unsafe_allow_html=True)

# ==========================================
# 🧮 1- CREAR PRESUPUESTO
# ==========================================
elif st.session_state.menu_actual == "🧮 1- Crear Presupuesto":
    st.markdown("<h2 style='color: #e9769d;'>🧮 Crear Presupuesto de Producción</h2>", unsafe_allow_html=True)
    
    col_izq, col_der = st.columns([1.3, 1])
    
    with col_izq:
        st.subheader("📋 Listado de Insumos del Proyecto")
        if not st.session_state.materiales:
            st.warning("Primero debes registrar materiales en la pestaña '2- Crear Material'.")
        else:
            with st.container():
                c_mat, c_cant = st.columns([2, 1])
                mat_selec = c_mat.selectbox("Selecciona un material de tu inventario:", list(st.session_state.materiales.keys()), key="sel_pres")
                mat_info = st.session_state.materiales[mat_selec]
                
                if mat_info["Tipo"] == "Pieza (Área)":
                    cx1, cx2 = st.columns(2)
                    ancho_u = cx1.number_input("Ancho a usar (cm)", min_value=0.1, value=10.0, step=1.0, key="w_pres")
                    alto_u = cx2.number_input("Alto a usar (cm)", min_value=0.1, value=10.0, step=1.0, key="h_pres")
                    cantidad_u = 1.0
                else:
                    cantidad_u = c_cant.number_input("Cantidad a usar:", min_value=0.1, value=1.0, step=1.0, key="cant_pres")
                    ancho_u, alto_u = 1.0, 1.0

                st.caption("⚙️ Modificar valores al momento (Se cargan tus precios guardados automáticamente):")
                ce1, ce2 = st.columns(2)
                
                # El truco de la llave dinámica
