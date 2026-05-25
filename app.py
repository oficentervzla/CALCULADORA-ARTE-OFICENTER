import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# --- CONFIGURACIÓN Y ESTILOS ---
st.set_page_config(page_title="Sistema Art Center", layout="wide", page_icon="🎨")

# [MANTIENE TUS MISMOS ESTILOS CSS AQUÍ...]
st.markdown("""
    <style>
        .tarjeta-ver { background-color: #f4fafc; padding: 20px; border-radius: 12px; border: 2px solid #74b7d5; margin-top: 15px; }
        .tarjeta-editar { background-color: #fff9fb; padding: 20px; border-radius: 12px; border: 2px solid #e9769d; margin-top: 15px; }
    </style>
""", unsafe_allow_html=True)

# --- FUNCIONES ---
def cargar_datos(archivo, tipo_esperado, defecto):
    if os.path.exists(archivo):
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                return datos if isinstance(datos, tipo_esperado) else defecto
        except: return defecto
    return defecto

def guardar_datos(archivo, datos):
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

# --- INICIALIZACIÓN ---
if 'materiales' not in st.session_state:
    st.session_state.materiales = cargar_datos('materiales.json', dict, {})
if 'productos' not in st.session_state:
    st.session_state.productos = cargar_datos('productos.json', dict, {})

# --- NAVEGACIÓN ---
opciones_menu = ["🏠 Menú Principal", "🧮 1- Crear Presupuesto", "➕ 2- Crear Material", "🎒 3- Verificar Panel de Materiales", "📜 4- Catálogo de Productos Finales"]
if 'menu_actual' not in st.session_state: st.session_state.menu_actual = "🏠 Menú Principal"

cols_nav = st.columns(5)
for idx, op in enumerate(opciones_menu):
    if cols_nav[idx].button(op, use_container_width=True, type="primary" if st.session_state.menu_actual == op else "secondary"):
        st.session_state.menu_actual = op
        st.session_state.accion_material = None # Limpiamos acciones al cambiar de menú
        st.rerun()

# ==========================================
# 🎒 VISTA: 3- PANEL DE MATERIALES (CORREGIDA)
# ==========================================
if st.session_state.menu_actual == "🎒 3- Verificar Panel de Materiales":
    st.subheader("🎒 Panel de Control de Inventario")
    
    # OPCIÓN MÁS CÓMODA: Lista desplegable para seleccionar material en lugar de checkboxes en tabla
    # Esto evita el 100% de los errores de "pantalla en blanco" o "recursión"
    mat_seleccionado = st.selectbox("Selecciona un material para gestionar:", [""] + list(st.session_state.materiales.keys()))
    
    if mat_seleccionado:
        st.session_state.material_focalizado = mat_seleccionado
        col_a, col_b = st.columns(2)
        if col_a.button("👁️ Ver Ficha Técnica"):
            st.session_state.accion_material = "ver"
        if col_b.button("✏️ Editar Costos"):
            st.session_state.accion_material = "editar"
            
        # [AQUÍ VA TU LÓGICA DE TARJETAS "ver" y "editar" QUE YA TENÍAS...]
        # Como ahora usas un selectbox, el estado es estable y no se romperá.
        
        if st.session_state.accion_material == "ver":
             # Tu lógica de despliegue de ficha (TARJETA VER)...
             st.info(f"Visualizando: {mat_seleccionado}")
             
        elif st.session_state.accion_material == "editar":
             # Tu lógica de edición (TARJETA EDITAR)...
             st.warning(f"Editando: {mat_seleccionado}")

# [RESTO DE TUS VISTAS...]
