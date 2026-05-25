import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# Configuración de página
st.set_page_config(page_title="Sistema Art Center", layout="wide", page_icon="🎨")

# --- DISEÑO, COLORES Y ESTILOS ---
st.markdown("""
    <style>
        .stApp { background-color: #ffffff; }
        h1, h2, h3 { font-family: 'Arial', sans-serif; text-align: center; }
        .titulo-principal { color: #e9769d !important; font-size: 50px; font-weight: bold; margin-bottom: 5px; }
        .frase-principal { color: #74b7d5 !important; font-size: 28px; font-style: italic; font-weight: bold; margin-bottom: 30px; }
        .tarjeta-precio { background-color: #f7f9fa; padding: 20px; border-radius: 15px; border-left: 6px solid #e9769d; box-shadow: 0px 4px 10px rgba(0,0,0,0.05); text-align: center; }
        .tarjeta-ver { background-color: #f4fafc; padding: 20px; border-radius: 12px; border: 2px solid #74b7d5; margin-top: 15px; }
        .tarjeta-editar { background-color: #fff9fb; padding: 20px; border-radius: 12px; border: 2px solid #e9769d; margin-top: 15px; }
    </style>
""", unsafe_allow_html=True)

# --- SISTEMA DE ALMACENAMIENTO ---
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

if 'accion_material' not in st.session_state:
    st.session_state.accion_material = None
if 'material_focalizado' not in st.session_state:
    st.session_state.material_focalizado = None

# --- NAVEGACIÓN ---
opciones_menu = ["🏠 Menú Principal", "🧮 1- Crear Presupuesto", "➕ 2- Crear Material", "🎒 3- Verificar Panel de Materiales", "📜 4- Catálogo de Productos Finales"]

if 'menu_actual' not in st.session_state:
    st.session_state.menu_actual = "🏠 Menú Principal"

cols_nav = st.columns(5)
for idx, opcion in enumerate(opciones_menu):
    with cols_nav[idx]:
        es_activo = st.session_state.menu_actual == opcion
        if st.button(opcion, key=f"nav_sup_{idx}", use_container_width=True, type="primary" if es_activo else "secondary"):
            st.session_state.menu_actual = opcion
            st.rerun()

st.divider()

# --- VISTAS ---
if st.session_state.menu_actual == "🏠 Menú Principal":
    st.markdown("<p class='titulo-principal'>ART CENTER</p>", unsafe_allow_html=True)
    st.session_state.tasa_bcv = st.number_input("Tasa BCV del día (Bs.)", value=float(st.session_state.tasa_bcv))

elif st.session_state.menu_actual == "🧮 1- Crear Presupuesto":
    st.markdown("<h2 style='color: #e9769d;'>🧮 Crear Presupuesto</h2>", unsafe_allow_html=True)

elif st.session_state.menu_actual == "➕ 2- Crear Material":
    st.markdown("<h2 style='color: #e9769d;'>➕ Registrar Nuevo Insumo</h2>", unsafe_allow_html=True)

elif st.session_state.menu_actual == "🎒 3- Verificar Panel de Materiales":
    # (Tu lógica de tabla y botones aquí)
    st.write("Panel de Materiales Activo")
    # ... resto de tu código ...

elif st.session_state.menu_actual == "📜 4- Catálogo de Productos Finales":
    st.write("Catálogo Activo")
