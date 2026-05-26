import streamlit as st
import json
import os
from datetime import datetime

# Configuración de página con diseño limpio
st.set_page_config(page_title="Sistema Art Center", layout="wide", page_icon="🎨")

st.markdown("""
    <style>
        .stApp { background-color: #ffffff; }
        h1, h2, h3 { font-family: 'Arial', sans-serif; text-align: center; }
        .titulo-principal { color: #e9769d !important; font-size: 50px; font-weight: bold; margin-bottom: 5px; }
        .frase-principal { color: #74b7d5 !important; font-size: 28px; font-style: italic; font-weight: bold; margin-bottom: 30px; }
    </style>
""", unsafe_allow_html=True)

# --- FUNCIONES DE ALMACENAMIENTO ---
def guardar_datos(archivo, datos):
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

def cargar_datos(archivo):
    if os.path.exists(archivo):
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

# --- INICIALIZACIÓN DE DATOS ---
if 'materiales' not in st.session_state:
    st.session_state.materiales = cargar_datos('materiales.json')
if 'productos' not in st.session_state:
    st.session_state.productos = cargar_datos('productos.json')
if 'tasa_bcv' not in st.session_state:
    st.session_state.tasa_bcv = 36.50
if 'menu_actual' not in st.session_state:
    st.session_state.menu_actual = "🏠 Menú Principal"

# --- BARRA DE NAVEGACIÓN SUPERIOR (COMO TUS FOTOS) ---
opciones_menu = [
    "🏠 Menú Principal", 
    "🧮 1- Crear Presupuesto", 
    "➕ 2- Crear Material", 
    "🎒 3- Verificar Panel de Materiales", 
    "📜 4- Catálogo de Productos Finales"
]

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
    
    st.subheader("🇻🇪 Control Cambiario")
    st.session_state.tasa_bcv = st.number_input("Tasa BCV del día (Bs.)", min_value=1.0, value=float(st.session_state.tasa_bcv), step=0.10)

# ==========================================
# ➕ VISTA: 2- CREAR MATERIAL
# ==========================================
elif st.session_state.menu_actual == "➕ 2- Crear Material":
    st.markdown("<h2 style='color: #e9769d;'>➕ Registrar Nuevo Insumo / Material</h2>", unsafe_allow_html=True)
    
    # Formulario controlado para evitar reinicios innecesarios
    with st.form("formulario_nuevo_material", clear_on_submit=True):
        nombre = st.text_input("Nombre del Material (Ej: Cartulina Escolar, Silicón)", placeholder="Escribe el nombre aquí...")
        
        # Tipo de cálculo usando checkboxes limpios
        es_pieza = st.checkbox("¿Es una Pieza con medidas específicas? (Marcar si se cuenta por área en cm)", value=False)
        
        c1, c2 = st.columns(2)
        with c1:
            costo = st.number_input("Costo de Proveedor ($)", min_value=0.0, step=0.01, format="%.2f")
            marca = st.text_input("Marca (Opcional)", placeholder="Genérica")
        with c2:
            precio = st.number_input("Precio de Tienda ($)", min_value=0.0, step=0.01, format="%.2f")
            
        # Campos condicionales según el tipo elegido
        if es_pieza:
            st.markdown("##### 📏 Medidas de la Pieza Completa")
            cx, cy = st.columns(2)
            ancho = cx.number_input("Ancho Total (cm)", min_value=0.1, step=0.1, value=1.0)
            alto = cy.number_input("Alto Total (cm)", min_value=0.1, step=0.1, value=1.0)
            tipo_final = "Pieza (Área)"
        else:
            ancho, alto = 1.0, 1.0
            tipo_final = "Unidad (Cantidad)"
            
        # Botón de envío del formulario
        guardar = st.form_submit_button("Guardar Material en Inventario")
        
        if guardar:
            if not nombre.strip():
                st.error("Por favor, introduce un nombre válido para el material.")
            elif precio <= 0:
                st.error("El precio de venta debe ser mayor a 0.")
            else:
                # Calcular porcentaje de ganancia básico expuesto en el panel
                ganancia_porcentaje = ((precio - costo) / precio * 100) if precio > 0 else 0.0
                
                # Guardar en el diccionario global
                st.session_state.materiales[nombre] = {
                    "Tipo": tipo_final,
                    "Ancho": float(ancho),
                    "Alto": float(alto),
                    "Costo": float(costo),
                    "Precio": float(precio),
                    "Ganancia_Pct": round(ganancia_porcentaje, 1),
                    "Marca": marca if marca else "Genérica",
                    "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                # Guardar físicamente en el archivo de texto JSON
                guardar_datos('materiales.json', st.session_state.materiales)
                st.success(f"🎉 ¡Material '{nombre}' registrado con éxito con una ganancia del {ganancia_porcentaje:.1f}%!")

# ==========================================
# 🧮 VISTAS RESTANTES (PLUGINS VACÍOS TEMPORALES)
# ==========================================
elif st.session_state.menu_actual == "🧮 1- Crear Presupuesto":
    st.markdown("<h2 style='color: #e9769d;'>🧮 Crear Presupuesto de Producción</h2>", unsafe_allow_html=True)
    st.info("Módulo listo para ser enlazado con la base de datos.")

elif st.session_state.menu_actual == "🎒 3- Verificar Panel de Materiales":
    st.markdown("<h2 style='color: #e9769d;'>🎒 Panel de Control de Inventario</h2>", unsafe_allow_html=True)
    st.info("Aquí mostraremos la lista de lo que vayas guardando.")

elif st.session_state.menu_actual == "📜 4- Catálogo de Productos Finales":
    st.markdown("<h2 style='color: #e9769d;'>📜 Catálogo de Productos Finales</h2>", unsafe_allow_html=True)
    st.info("Catálogo en espera.")
