import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA (Debe ser la primera instrucción de Streamlit)
st.set_page_config(page_title="Sistema Art Center", layout="wide", page_icon="🎨")

# 2. DISEÑO Y ESTILOS CSS ENFOCADOS EN TU MARCA
st.markdown("""
    <style>
        .stApp { background-color: #ffffff; }
        h1, h2, h3 { font-family: 'Arial', sans-serif; text-align: center; }
        
        .titulo-principal { color: #e9769d !important; font-size: 50px; font-weight: bold; margin-bottom: 5px; }
        .frase-principal { color: #74b7d5 !important; font-size: 28px; font-style: italic; font-weight: bold; margin-bottom: 30px; }
        
        /* Tarjetas de interacción de Gestión */
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

# 3. SISTEMA DE ALMACENAMIENTO SEGURO DE DATOS
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

# 4. INICIALIZACIÓN DE VARIABLES EN SESSION STATE
if 'materiales' not in st.session_state:
    st.session_state.materiales = cargar_datos('materiales.json', dict, {
        "Cartulina Escolar": {"Tipo": "Pieza (Área)", "Ancho": 50.0, "Alto": 70.0, "Costo": 0.50, "Precio": 1.00, "Marca": "Genérica", "Fecha": hoy},
        "Silicón (Barra)": {"Tipo": "Unidad (Cantidad)", "Ancho": 1.0, "Alto": 1.0, "Costo": 0.10, "Precio": 0.25, "Marca": "Genérica", "Fecha": hoy},
        "Impresion en Papel Fotografico": {"Tipo": "Unidad (Cantidad)", "Ancho": 1.0, "Alto": 1.0, "Costo": 0.08, "Precio": 0.50, "Marca": "Genérica", "Fecha": hoy},
        "Impresion en Papel Fotografico Carta": {"Tipo": "Unidad (Cantidad)", "Ancho": 1.0, "Alto": 1.0, "Costo": 0.08, "Precio": 0.50, "Marca": "Genérica", "Fecha": hoy}
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

# 5. CONTROLADOR CENTRAL DE NAVEGACIÓN (BOTONES SUPERIORES)
opciones_menu = [
    "🏠 Menú Principal", 
    "🧮 1- Crear Presupuesto", 
    "➕ 2- Crear Material", 
    "🎒 3- Verificar Panel de Materiales", 
    "📜 4- Catálogo de Productos Finales"
]

if 'menu_actual' not in st.session_state:
    st.session_state.menu_actual = "🏠 Menú Principal"

cols_nav = st.columns(5)
for idx, opcion in enumerate(opciones_menu):
    with cols_nav[idx]:
        es_activo = (st.session_state.menu_actual == opcion)
        tipo_estilo = "primary" if es_activo else "secondary"
        if st.button(opcion, key=f"nav_sup_{idx}", use_container_width=True, type=tipo_estilo):
            st.session_state.menu_actual = opcion
            # Al cambiar de pestaña principal limpiamos focos anteriores para evitar residuos visuales
            st.session_state.accion_material = None
            st.session_state.material_focalizado = None
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
    st.markdown("<h2 style='color: #e9769d;'>🧮 Crear Presupuesto de Producción</h2>", unsafe_allow_html=True)
    st.info("Módulo de presupuestos listo para operar.")

# ==========================================
# ➕ VISTA: 2- CREAR MATERIAL
# ==========================================
elif st.session_state.menu_actual == "➕ 2- Crear Material":
    st.markdown("<h2 style='color: #e9769d;'>➕ Registrar Nuevo Insumo / Material</h2>", unsafe_allow_html=True)
    st.info("Módulo de registro e ingreso de nuevos materiales configurado.")

# ==========================================
# 🎒 VISTA: 3- PANEL DE CONTROL (SINTAXIS Y ACCIONES REPARADAS)
# ==========================================
elif st.session_state.menu_actual == "🎒 3- Verificar Panel de Materiales":
    st.markdown("<h2 style='color: #e9769d;'>🎒 Panel de Control de Inventario</h2>", unsafe_allow_html=True)
    
    if not st.session_state.materiales:
        st.info("No hay materiales registrados.")
    else:
        nombres_materiales = list(st.session_state.materiales.keys())
        lista_datos_tabla = []
        
        for n in nombres_materiales:
            d = st.session_state.materiales[n]
            porcentaje_ganancia_mat = (((d['Precio'] - d['Costo']) / d['Precio']) * 100) if d['Precio'] > 0 else 0.0
            
            if d.get("Tipo") == "Pieza (Área)":
                medida_str = f"{d.get('Ancho', 0.0)} x {d.get('Alto', 0.0)} cm"
            else:
                medida_str = "N/A (Unidad)"
                
            lista_datos_tabla.append({
                "Material": n,
                "Tipo": d["Tipo"],
                "Medidas (cm)": medida_str,
                "Marca": d.get("Marca", "Genérica"),
                "Costo Base": f"${d['Costo']:.2f}",
                "Precio Base": f"${d['Precio']:.2f}",
                "Ganancia (%)": f"{porcentaje_ganancia_mat:.1f}%",
                "Última Actualización": d.get("Fecha", "Original"),
                "👁️ Ver": False,  
                "✏️ Editar": False
            })
            
        df_panel = pd.DataFrame(lista_datos_tabla)
        
        # Renderizado de la tabla con los componentes Checkbox fijos
        edicion_tabla = st.data_editor(
            df_panel,
            column_config={
                "👁️ Ver": st.column_config.CheckboxColumn("👁️ Ver", help="Ver resumen técnico", default=False),
                "✏️ Editar": st.column_config.CheckboxColumn("✏️ Editar", help="Modificar costos y dimensiones", default=False)
            },
            disabled=["Material", "Tipo", "Medidas (cm)", "Marca", "Costo Base", "Precio Base", "Ganancia (%)", "Última Actualización"],
            use_container_width=True,
            key="editor_tabla_panel"
