import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Sistema Art Center", layout="wide", page_icon="🎨")

# --- FUNCIONES DE DATOS ---
def cargar_datos(archivo, defecto):
    if os.path.exists(archivo):
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return defecto
    return defecto

def guardar_datos(archivo, datos):
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

# --- INICIALIZACIÓN ---
if 'materiales' not in st.session_state:
    st.session_state.materiales = cargar_datos('materiales.json', {})
if 'productos' not in st.session_state:
    st.session_state.productos = cargar_datos('productos.json', {})
if 'menu_actual' not in st.session_state:
    st.session_state.menu_actual = "🏠 Menú Principal"

# --- MENÚ DE NAVEGACIÓN ---
opciones = ["🏠 Menú Principal", "🧮 1- Crear Presupuesto", "➕ 2- Crear Material", "🎒 3- Verificar Panel de Materiales", "📜 4- Catálogo"]
menu = st.sidebar.selectbox("Navegación", opciones)
st.session_state.menu_actual = menu

# --- LÓGICA DE VISTAS ---

if menu == "🏠 Menú Principal":
    st.title("🎨 Sistema Art Center")
    st.write("Bienvenido al sistema de gestión.")
    st.session_state.tasa_bcv = st.number_input("Tasa BCV del día:", value=36.50)

elif menu == "➕ 2- Crear Material":
    st.subheader("Registrar Insumo")
    with st.form("nuevo_mat"):
        nombre = st.text_input("Nombre:")
        tipo = st.selectbox("Tipo:", ["Pieza (Área)", "Unidad (Cantidad)"])
        costo = st.number_input("Costo ($):", value=0.0)
        precio = st.number_input("Precio ($):", value=0.0)
        if st.form_submit_button("Guardar"):
            st.session_state.materiales[nombre] = {"Tipo": tipo, "Costo": costo, "Precio": precio, "Fecha": datetime.now().strftime("%Y-%m-%d")}
            guardar_datos('materiales.json', st.session_state.materiales)
            st.success("Guardado!")

elif menu == "🎒 3- Verificar Panel de Materiales":
    st.subheader("Inventario")
    if st.session_state.materiales:
        df = pd.DataFrame.from_dict(st.session_state.materiales, orient='index')
        st.dataframe(df)
        if st.button("Limpiar Inventario (Debug)"):
            st.session_state.materiales = {}
            guardar_datos('materiales.json', {})
            st.rerun()
    else:
        st.info("Inventario vacío.")

elif menu == "🧮 1- Crear Presupuesto":
    st.subheader("Calculadora de Toppers")
    st.write("Selecciona materiales desde el inventario para calcular.")
    # Aquí puedes añadir la lógica de suma de costos
    
elif menu == "📜 4- Catálogo":
    st.subheader("Productos Finales")
    if st.session_state.productos:
        st.json(st.session_state.productos)
    else:
        st.info("No hay productos guardados.")
