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
        
        /* Estilos de pestañas superiores */
        button[data-baseweb="tab"] {
            font-size: 16px !important;
            font-weight: bold !important;
            color: #555555 !important;
            padding: 10px 20px !important;
        }
        button[aria-selected="true"] {
            color: #e9769d !important;
            border-bottom-color: #fed80c !important;
        }
        
        /* Botón de acción general */
        .stButton>button {
            background-color: #fed80c !important; color: #000000 !important;
            font-weight: bold !important; border-radius: 12px !important; border: none !important;
            padding: 10px 24px !important;
            display: block; margin: 0 auto;
        }
        .stButton>button:hover { background-color: #0bccd1 !important; color: #ffffff !important; }
        
        /* Tarjeta de presupuesto final destacada */
        .tarjeta-precio {
            background-color: #f7f9fa; padding: 20px; border-radius: 15px;
            border-left: 6px solid #e9769d; box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
            text-align: center;
        }
        
        /* Estilo interactivo para Toppers/Casillas del Home */
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
                if type(datos) == tipo_esperado:
                    return datos
        except:
            pass
    return defecto

def guardar_datos(archivo, datos):
    with open(archivo, 'w', encoding='utf-8') as f: 
        json.dump(datos, f, ensure_ascii=False, indent=4)

hoy = datetime.now().strftime("%Y-%m-%d %H:%M")

if 'materiales' not in st.session_state:
    st.session_state.materiales = cargar_datos('materiales.json', dict, {
        "Cartulina Escolar": {"Tipo": "Pieza (Área)", "Ancho": 50.0, "Alto": 70.0, "Costo": 0.50, "Precio": 1.00, "Marca": "Genérica", "Fecha": hoy},
        "Silicón (Barra)": {"Tipo": "Unidad (Cantidad)", "Ancho": 1.0, "Alto": 1.0, "Costo": 0.10, "Precio": 0.25, "Marca": "Genérica", "Fecha": hoy}
    })

if 'productos' not in st.session_state:
    st.session_state.productos = cargar_datos('productos.json', dict, {})

# Inicializador del estado de la pestaña activa para permitir saltos cruzados
if 'pestaña_actual' not in st.session_state:
    st.session_state.pestaña_actual = "🏠 Menú Principal"

# --- MANEJO DE REDIRECCIÓN POR CASILLAS ---
# Si el usuario hace clic en un botón del home, forzamos el renderizado en la pestaña correspondiente
def ir_a_pestaña(nombre_pestaña):
    st.session_state.pestaña_actual = nombre_pestaña
    st.rerun()

# --- BARRA DE OPCIONES SUPERIOR COMPLETA ---
opciones_menu = [
    "🏠 Menú Principal", 
    "🧮 1- Crear Presupuesto", 
    "➕ 2- Crear Material", 
    "🎒 3- Verificar Panel de Materiales", 
    "📜 4- Catálogo de Productos Finales"
]

# Buscamos el índice actual de forma segura para Streamlit
idx_inicial = opciones_menu.index(st.session_state.pestaña_actual) if st.session_state.pestaña_actual in opciones_menu else 0

# Render de la barra de navegación superior
render_tabs = st.tabs(opciones_menu)

# ==========================================
# 🏠 OPCIÓN: MENÚ PRINCIPAL (CON CASILLAS INTERACTIVAS)
# ==========================================
with render_tabs[0]:
    st.markdown("<p class='titulo-principal'>ART CENTER</p>", unsafe_allow_html=True)
    st.markdown("<p class='frase-principal'>¿Qué vamos a crear hoy?</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-weight: bold; color: #555;'>Selecciona una casilla o usa el menú de arriba para empezar:</p>", unsafe_allow_html=True)
    st.divider()
    
    st.markdown("### 🇻🇪 Control Cambiario")
    tasa_bcv = st.number_input("Tasa BCV del día (Bs.)", min_value=1.0, value=36.50, step=0.10, key="tasa_principal")
    st.divider()
    
    # Render de casillas como botones reales interactivos
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("🧮 Presupuesto\n\nCalcula costos, precios de venta y desglosa tus ganancias al instante.", key="btn_home_pres"):
            ir_a_pestaña("🧮 1- Crear Presupuesto")
    with c2:
        if st.button("➕ Crear Material\n\nRegistra nuevos insumos con sus medidas, marcas y ganancias.", key="btn_home_mat"):
            ir_a_pestaña("➕ 2- Crear Material")
    with c3:
        if st.button("🎒 Panel Materiales\n\nMira tu inventario, edita precios en masa y revisa tus porcentajes.", key="btn_home_panel"):
            ir_a_pestaña("🎒 3- Verificar Panel de Materiales")
    with c4:
        if st.button("📜 Catálogo Final\n\nRevisa tus productos listos, añade fotos y gestiona historiales.", key="btn_home_cat"):
            ir_a_pestaña("📜 4- Catálogo de Productos Finales")

    st.divider()
    st.markdown("<p style='text-align: center; font-size: 12px; color: #aaa;'>Una solución desarrollada para Oficenter C.A.</p>", unsafe_allow_html=True)

if '
