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
        
        /* Tarjetas de Gestión e Historial */
        .tarjeta-ver {
            background-color: #f4fafc; padding: 20px; border-radius: 12px;
            border: 2px solid #74b7d5; margin-top: 15px;
        }
        .tarjeta-editar {
            background-color: #fff9fb; padding: 20px; border-radius: 12px;
            border: 2px solid #e9769d; margin-top: 15px;
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

# Inicialización segura de datos para evitar errores de Attribute/Key
if 'materiales' not in st.session_state:
    st.session_state.materiales = cargar_datos('materiales.json', dict, {
        "Cartulina Escolar": {"Tipo": "Pieza (Área)", "Ancho": 50.0, "Alto": 70.0, "Costo": 0.50, "Precio": 1.00, "Marca": "Genérica", "Fecha": hoy},
        "Silicón (Barra)": {"Tipo": "Unidad (Cantidad)", "Ancho": 1.0, "Alto": 1.0, "Costo": 0.10, "Precio": 0.25, "Marca": "Genérica", "Fecha": hoy},
        "Impresion en Papel Fotográfico": {"Tipo": "Unidad (Cantidad)", "Ancho": 1.0, "Alto": 1.0, "Costo": 0.08, "Precio": 0.50, "Marca": "Genérica", "Fecha": hoy},
        "Impresion en Papel Fotográfico Carta": {"Tipo": "Unidad (Cantidad)", "Ancho": 1.0, "Alto": 1.0, "Costo": 0.08, "Precio": 0.50, "Marca": "Genérica", "Fecha": hoy}
    })

if 'productos' not in st.session_state:
    st.session_state.productos = cargar_datos('productos.json', dict, {})

if 'items_presupuesto' not in st.session_state:
    st.session_state.items_presupuesto = []

if 'tasa_bcv' not in st.session_state:
    st.session_state.tasa_bcv = 36.50

# Variables persistentes de control de acciones
if 'accion_material' not in st.session_state:
    st.session_state.accion_material = None
if 'material_focalizado' not in st.session_state:
    st.session_state.material_focalizado = None

# --- CONTROLADOR CENTRAL DE NAVEGACIÓN ---
opciones_menu = [
    "🏠 Menú Principal", 
    "🧮 1- Crear Presupuesto", 
    "➕ 2- Crear Material", 
    "🎒 3- Verificar Panel de Materiales", 
    "📜 4- Catálogo de Productos Finales"
]

if 'menu_actual' not in st.session_state:
    st.session_state.menu_actual = "🏠 Menú Principal"

# Barra de pestañas superior fija
cols_nav = st.columns(5)
for idx, opcion in enumerate(opciones_menu):
    with cols_nav[idx]:
        es_activo = st.session_state.menu_actual == opcion
        tipo_estilo = "primary" if es_activo else "secondary"
        if st.button(opcion, key=f"nav_sup_{idx}", use_container_width=True, type=tipo_estilo):
            st.session_state.menu_actual = opcion
            st.rerun()

st.divider()

# ==========================================
# 🏠 VISTA: MENÚ PRINCIPAL
# ==========================================
if st.session_state.menu_actual == "🏠 Menú Principal":
    st.markdown("<p class='titulo-principal'>ART CENTER</p>", unsafe_allow_html=True)
    st.markdown("<p class='frase-principal'>¿Qué vamos a crear hoy?</p>", unsafe_allow_html=True)
    
    st.markdown("### 🇻🇪 Control Cambiario")
    st.session_state.tasa_bcv = st.number_input("Tasa BCV del día (Bs.)", min_value=1.0, value=float(st.session_state.tasa_bcv), step=0.10, key="input_tasa_home")

# ==========================================
# 🧮 VISTA: 1- CREAR PRESUPUESTO
# ==========================================
elif st.session_state.menu_actual == "🧮 1- Crear Presupuesto":
    st.markdown("<h2 style='color: #e9769d;'>🧮 Crear Presupuesto de Produ
