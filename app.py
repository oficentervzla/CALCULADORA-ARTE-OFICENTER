import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Sistema Art Center", layout="wide", page_icon="🎨")

# --- CSS PERSONALIZADO ---
st.markdown("""
    <style>
        .stApp { background-color: #ffffff; }
        .titulo-principal { color: #e9769d !important; font-size: 50px; font-weight: bold; text-align: center; }
        .frase-principal { color: #74b7d5 !important; font-size: 28px; font-style: italic; font-weight: bold; text-align: center; margin-bottom: 30px; }
        .tarjeta-ver { background-color: #f4fafc; padding: 20px; border-radius: 12px; border: 2px solid #74b7d5; }
        .tarjeta-editar { background-color: #fff9fb; padding: 20px; border-radius: 12px; border: 2px solid #e9769d; }
    </style>
""", unsafe_allow_html=True)

# --- FUNCIONES BASE ---
def cargar_json(archivo):
    if os.path.exists(archivo):
        with open(archivo, 'r', encoding='utf-8') as f: return json.load(f)
    return {}

def guardar_json(archivo, datos):
    with open(archivo, 'w', encoding='utf-8') as f: json.dump(datos, f, ensure_ascii=False, indent=4)

# --- INICIALIZACIÓN ---
if 'materiales' not in st.session_state: st.session_state.materiales = cargar_json('materiales.json')
if 'productos' not in st.session_state: st.session_state.productos = cargar_json('productos.json')
if 'tasa_bcv' not in st.session_state: st.session_state.tasa_bcv = 36.50
if 'menu_actual' not in st.session_state: st.session_state.menu_actual = "🏠 Menú Principal"

# --- BARRA DE NAVEGACIÓN SUPERIOR ---
opciones = ["🏠 Menú Principal", "🧮 1- Crear Presupuesto", "➕ 2- Crear Material", "🎒 3- Verificar Panel de Materiales", "📜 4- Catálogo de Productos Finales"]
cols = st.columns(5)
for i, op in enumerate(opciones):
    if cols[i].button(op, use_container_width=True, type="primary" if st.session_state.menu_actual == op else "secondary"):
        st.session_state.menu_actual = op
        st.rerun()
st.divider()

# --- 1. MENÚ PRINCIPAL ---
if st.session_state.menu_actual == "🏠 Menú Principal":
    st.markdown("<p class='titulo-principal'>ART CENTER</p>", unsafe_allow_html=True)
    st.markdown("<p class='frase-principal'>¿Qué vamos a crear hoy?</p>", unsafe_allow_html=True)
    # Placeholder para logo: st.image("logo.png") 
    st.session_state.tasa_bcv = st.number_input("Tasa BCV del día (Bs.)", value=float(st.session_state.tasa_bcv), format="%.2f")

# --- 2. CREAR MATERIAL ---
elif st.session_state.menu_actual == "➕ 2- Crear Material":
    st.subheader("➕ Registrar Nuevo Insumo")
    with st.form("form_mat"):
        nombre = st.text_input("Nombre del Material")
        tipo = st.selectbox("Tipo", ["Pieza (Área)", "Unidad (Cantidad)"])
        costo = st.number_input("Costo Proveedor ($)", min_value=0.0, format="%.2f")
        precio = st.number_input("Precio Venta ($)", min_value=0.0, format="%.2f")
        marca = st.text_input("Marca (Opcional)")
        if tipo == "Pieza (Área)":
            ancho = st.number_input("Ancho (cm)", min_value=0.1)
            alto = st.number_input("Alto (cm)", min_value=0.1)
        else:
            ancho, alto = 1.0, 1.0
        
        if st.form_submit_button("Guardar Material"):
            st.session_state.materiales[nombre] = {
                "Tipo": tipo, "Costo": costo, "Precio": precio, "Marca": marca,
                "Ancho": ancho, "Alto": alto, "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            guardar_json('materiales.json', st.session_state.materiales)
            st.success(f"Material {nombre} guardado.")

# --- 3. PANEL DE MATERIALES (GESTIÓN) ---
elif st.session_state.menu_actual == "🎒 3- Verificar Panel de Materiales":
    st.subheader("🎒 Inventario")
    if not st.session_state.materiales:
        st.info("No hay materiales.")
    else:
        # Selector de material para gestionar
        mat_sel = st.selectbox("Selecciona un material:", list(st.session_state.materiales.keys()))
        info = st.session_state.materiales[mat_sel]
        
        c1, c2 = st.columns(2)
        if c1.button("👁️ Ver Resumen"):
            st.session_state.accion = "ver"
        if c2.button("✏️ Editar"):
            st.session_state.accion = "editar"
            
        if 'accion' in st.session_state:
            if st.session_state.accion == "ver":
                st.markdown(f"<div class='tarjeta-ver'><h3>{mat_sel}</h3><p>Costo: ${info['Costo']} | Precio: ${info['Precio']}</p></div>", unsafe_allow_html=True)
                # Simulación PDF
                st.download_button("📥 Descargar PDF", f"Resumen {mat_sel}: {info}", file_name="resumen.pdf")
            
            elif st.session_state.accion == "editar":
                with st.form("edit_mat"):
                    n_costo = st.number_input("Nuevo Costo", value=float(info['Costo']))
                    n_precio = st.number_input("Nuevo Precio", value=float(info['Precio']))
                    actualizar_todo = st.checkbox("Aplicar cambios a productos vinculados")
                    if st.form_submit_button("Guardar Cambios"):
                        st.session_state.materiales[mat_sel].update({"Costo": n_costo, "Precio": n_precio, "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M")})
                        guardar_json('materiales.json', st.session_state.materiales)
                        if actualizar_todo:
                            # Lógica de actualización de productos...
                            pass
                        st.success("Actualizado")

# --- 4. CREAR PRESUPUESTO ---
elif st.session_state.menu_actual == "🧮 1- Crear Presupuesto":
    st.subheader("🧮 Nuevo Presupuesto")
    st.write("Funcionalidad en desarrollo - Usa el panel lateral para cambiar de módulo.")

# --- 5. CATÁLOGO ---
elif st.session_state.menu_actual == "📜 4- Catálogo de Productos Finales":
    st.subheader("📜 Catálogo")
    st.write("Visualización de productos guardados.")
