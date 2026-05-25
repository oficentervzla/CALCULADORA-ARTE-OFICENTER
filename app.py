import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Sistema Art Center", layout="wide", page_icon="🎨")

# 2. DISEÑO Y ESTILOS CSS ENFOCADOS EN TU MARCA
st.markdown("""
    <style>
        .stApp { background-color: #ffffff; }
        h1, h2, h3 { font-family: 'Arial', sans-serif; text-align: center; }
        
        .titulo-principal { color: #e9769d !important; font-size: 50px; font-weight: bold; margin-bottom: 5px; }
        .frase-principal { color: #74b7d5 !important; font-size: 28px; font-style: italic; font-weight: bold; margin-bottom: 30px; }
        
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
        "Impresion en Papel Fotografico": {"Tipo": "Unidad (Cantidad)", "Ancho": 1.0, "Alto": 1.0, "Costo": 0.08, "Precio": 0.50, "Marca": "Genérica", "Fecha": hoy}
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

# 5. CONTROLADOR CENTRAL DE NAVEGACIÓN
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
    
    st.write("---")
    st.markdown("### ⚡ Acceso Rápido")
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("🧮 Ir a Calculadora", use_container_width=True):
        st.session_state.menu_actual = "🧮 1- Crear Presupuesto"
        st.rerun()
    if c2.button("➕ Añadir Insumo", use_container_width=True):
        st.session_state.menu_actual = "➕ 2- Crear Material"
        st.rerun()
    if c3.button("🎒 Ver Inventario", use_container_width=True):
        st.session_state.menu_actual = "🎒 3- Verificar Panel de Materiales"
        st.rerun()
    if c4.button("📜 Ver Catálogo", use_container_width=True):
        st.session_state.menu_actual = "📜 4- Catálogo de Productos Finales"
        st.rerun()

# ==========================================
# 🧮 VISTA: 1- CREAR PRESUPUESTO (CALCULADORA INTERACTIVA)
# ==========================================
elif st.session_state.menu_actual == "🧮 1- Crear Presupuesto":
    st.markdown("<h2 style='color: #e9769d;'>🧮 Calculadora de Producción de Toppers</h2>", unsafe_allow_html=True)
    
    if not st.session_state.materiales:
        st.warning("Primero debes registrar materiales en el inventario.")
    else:
        with st.form("form_añadir_item"):
            st.markdown("### 🛠️ Agregar Insumo al Presupuesto Actual")
            mat_seleccionado = st.selectbox("Selecciona el Material / Insumo:", list(st.session_state.materiales.keys()))
            info_m = st.session_state.materiales[mat_seleccionado]
            
            if info_m["Tipo"] == "Pieza (Área)":
                st.caption(f"Formato original de este material: {info_m['Ancho']} x {info_m['Alto']} cm (Área total: {info_m['Ancho']*info_m['Alto']} cm²)")
                c_p1, c_p2 = st.columns(2)
                ancho_usar = c_p1.number_input("Ancho a utilizar (cm):", min_value=0.1, value=10.0, step=0.5)
                alto_usar = c_p2.number_input("Alto a utilizar (cm):", min_value=0.1, value=10.0, step=0.5)
                cantidad_m = 1
            else:
                st.caption("Este material se calcula por unidades físicas enteras.")
                cantidad_m = st.number_input("Cantidad de unidades a usar:", min_value=1, value=1, step=1)
                ancho_usar, alto_usar = 1.0, 1.0
                
            if st.form_submit_button("➕ Agregar Insumo al Topper"):
                if info_m["Tipo"] == "Pieza (Área)":
                    area_total_mat = info_m["Ancho"] * info_m["Alto"]
                    area_usada = ancho_usar * alto_usar
                    proporcion = area_usada / area_total_mat
                    costo_calc = round(info_m["Costo"] * proporcion, 4)
                    precio_calc = round(info_m["Precio"] * proporcion, 4)
                    cant_str = f"{ancho_usar}x{alto_usar} cm"
                else:
                    costo_calc = round(info_m["Costo"] * cantidad_m, 4)
                    precio_calc = round(info_m["Precio"] * cantidad_m, 4)
                    cant_str = f"{cantidad_m} Unid."
                    
                st.session_state.items_presupuesto.append({
                    "Material": mat_seleccionado,
                    "Cantidad": cant_str,
                    "Ancho": ancho_usar if info_m["Tipo"] == "Pieza (Área)" else 1.0,
                    "Alto": alto_usar if info_m["Tipo"] == "Pieza (Área)" else 1.0,
                    "Costo Calculado": costo_calc,
                    "Precio Calculado": precio_calc
                })
                st.success(f"¡{mat_seleccionado} añadido!")
                st.rerun()

        # MOSTRAR TABLA DE ITEMS ACTUALES
        if st.session_state.items_presupuesto:
            st.markdown("### 📋 Desglose de Materiales del Diseño")
            df_items = pd.DataFrame(st.session_state.items_presupuesto)
            st.dataframe(df_items[["Material", "Cantidad", "Costo Calculado", "Precio Calculado"]], use_container_width=True)
            
            costo_materiales = sum(item["Costo Calculado"] for item in st.session_state.items_presupuesto)
            precio_materiales_base = sum(item["Precio Calculado"] for item in st.session_state.items_presupuesto)
            
            st.markdown("### 💰 Configuración del Margen de Ganancia del Topper")
            c_g1, c_g2 = st.columns(2)
            nombre_topper = c_g1.text_input("Nombre o Modelo del Topper (Ej: Topper Cumpleaños Karol G):", value="Nuevo Topper Creativo")
            margen_diseño = c_g2.number_input("Margen de Ganancia sobre materiales (%):", min_value=0.0, value=30.0, step=5.0)
            
            precio_venta_final = round(precio_materiales_base * (1 + (margen_diseño / 100)), 2)
            ganancia_neta = round(precio_venta_final - costo_materiales, 2)
            precio_bs = round(precio_venta_final * st.session_state.tasa_bcv, 2)
            
            # PANEL DE RESULTADOS FINALES
            st.markdown("---")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Costo Real Materiales", f"${costo_materiales:.2f}")
            m2.metric("Precio Sugerido ($)", f"${precio_venta_final:.2f}")
            m3.metric("Precio en Bolívares", f"{precio_bs:.2f} Bs.")
            m4.metric("Ganancia Neta Limpia", f"${ganancia_neta:.2f}")
            
            cb1, cb2 = st.columns(2)
            if cb1.button("💾 Guardar y Publicar en Catálogo", type="primary", use_container_width=True):
                st.session_state.productos[nombre_topper] = {
                    "Materiales Usados": st.session_state.items_presupuesto.copy(),
                    "Margen %": margen_diseño,
                    "Precio Venta $": precio_venta_final,
                    "Ganancia Neta $": ganancia_neta,
                    "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                guardar_datos('productos.json', st.session_state.productos)
                st.success(f"¡El producto '{nombre_topper}' se guardó exitosamente en el Catálogo!")
                st.session_state.items_presupuesto = []
                st.rerun()
                
            if cb2.button("🗑️ Borrar Presupuesto Actual", use_container_width=True):
                st.session_state.items_presupuesto = []
                st.rerun()

# ==========================================
# ➕ VISTA: 2- CREAR MATERIAL (FORMULARIO OPERATIVO)
# ==========================================
elif st.session_state.menu_actual == "➕ 2- Crear Material":
    st.markdown("<h2 style='color: #e9769d;'>➕ Registrar Nuevo Insumo / Material</h2>", unsafe_allow_html=True)
    
    with st.form("form_crear_material_nuevo"):
        nombre_m = st.text_input("Nombre del Material (Ej: Cartulina Metalizada Dorada):")
        tipo_m = st.radio("Método de cálculo en taller:", ["Pieza (Área)", "Unidad (Cantidad)"])
        
        c_m1, c_m2 = st.columns(2)
        costo_m = c_m1.number_input("Costo de compra del proveedor ($):", min_value=0.01, value=1.00, step=0.10, format="%.2f")
        precio_m = c_m2.number_input("Precio base de venta asignado ($):", min_value=0.01, value=2.00, step=0.10, format="%.2f")
        
        marca_m = st.text_input("Marca / Proveedor del material:", value="Genérica")
        
        ancho_m, alto_m = 1.0, 1.0
        if tipo_m == "Pieza (Área)":
            st.markdown("#### 📐 Dimensiones de la pieza original completa")
            c_d1, c_d2 = st.columns(2)
            ancho_m = c_d1.number_input("Ancho original (cm):", min_value=1.0, value=50.0, step=1.0)
            alto_m = c_d2.number_input("Alto original (cm):", min_value=1.0, value=70.0, step=1.0)
            
        if st.form_submit_button("💾 Registrar Insumo en Inventario", type="primary"):
            if not nombre_m.strip():
                st.error("Por favor introduce un nombre válido para el material.")
            else:
                st.session_state.materiales[nombre_m] = {
                    "Tipo": tipo_m,
                    "Ancho": float(ancho_m),
                    "Alto": float(alto_m),
                    "Costo": float(costo_m),
                    "Precio": float(precio_m),
                    "Marca": marca_m,
                    "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                guardar_datos('materiales.json', st.session_state.materiales)
                st.success(f"¡Material '{nombre_m}' registrado correctamente!")
                st.balloons()

# ==========================================
# 🎒 VISTA: 3- PANEL DE CONTROL (TABLA INTERACTIVA)
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
            costo_base = d.get('Costo', 0.0)
            precio_base = d.get('Precio', 0.0)
            porcentaje_ganancia_mat = (((precio_base - costo_base) / precio_base) * 100) if precio_base > 0 else
