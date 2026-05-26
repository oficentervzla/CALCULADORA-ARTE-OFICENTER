import streamlit as st
import pandas as pd
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
        
        /* Tarjetas de información */
        .tarjeta-ver {
            background-color: #f4fafc; padding: 20px; border-radius: 12px;
            border: 2px solid #74b7d5; margin-top: 15px; margin-bottom: 15px;
        }
        .tarjeta-editar {
            background-color: #fff9fb; padding: 20px; border-radius: 12px;
            border: 2px solid #e9769d; margin-top: 15px; margin-bottom: 15px;
        }
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

# Variables para controlar qué material estamos viendo o editando
if 'accion_material' not in st.session_state:
    st.session_state.accion_material = None
if 'material_focalizado' not in st.session_state:
    st.session_state.material_focalizado = None

# --- BARRA DE NAVEGACIÓN SUPERIOR ---
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
            # Al cambiar de pestaña principal, cerramos cualquier edición abierta para que no se tranque
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
    
    st.subheader("🇻🇪 Control Cambiario")
    st.session_state.tasa_bcv = st.number_input("Tasa BCV del día (Bs.)", min_value=1.0, value=float(st.session_state.tasa_bcv), step=0.10)

# ==========================================
# ➕ VISTA: 2- CREAR MATERIAL
# ==========================================
elif st.session_state.menu_actual == "➕ 2- Crear Material":
    st.markdown("<h2 style='color: #e9769d;'>➕ Registrar Nuevo Insumo / Material</h2>", unsafe_allow_html=True)
    
    with st.form("formulario_nuevo_material", clear_on_submit=True):
        nombre = st.text_input("Nombre del Material (Ej: Cartulina Escolar, Silicón)", placeholder="Escribe el nombre aquí...")
        es_pieza = st.checkbox("¿Es una Pieza con medidas específicas? (Marcar si se cuenta por área en cm)", value=False)
        
        c1, c2 = st.columns(2)
        with c1:
            costo = st.number_input("Costo de Proveedor ($)", min_value=0.0, step=0.01, format="%.2f")
            marca = st.text_input("Marca (Opcional)", placeholder="Genérica")
        with c2:
            precio = st.number_input("Precio de Tienda ($)", min_value=0.0, step=0.01, format="%.2f")
            
        if es_pieza:
            st.markdown("##### 📏 Medidas de la Pieza Completa")
            cx, cy = st.columns(2)
            ancho = cx.number_input("Ancho Total (cm)", min_value=0.1, step=0.1, value=1.0)
            alto = cy.number_input("Alto Total (cm)", min_value=0.1, step=0.1, value=1.0)
            tipo_final = "Pieza (Área)"
        else:
            ancho, alto = 1.0, 1.0
            tipo_final = "Unidad (Cantidad)"
            
        guardar = st.form_submit_button("Guardar Material en Inventario")
        
        if guardar:
            if not nombre.strip():
                st.error("Por favor, introduce un nombre válido para el material.")
            elif precio <= 0:
                st.error("El precio de venta debe ser mayor a 0.")
            else:
                ganancia_porcentaje = ((precio - costo) / precio * 100) if precio > 0 else 0.0
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
                guardar_datos('materiales.json', st.session_state.materiales)
                st.success(f"🎉 ¡Material '{nombre}' registrado con éxito!")

# ==========================================
# 🎒 VISTA: 3- VERIFICAR PANEL DE MATERIALES (ESTABLE)
# ==========================================
elif st.session_state.menu_actual == "🎒 3- Verificar Panel de Materiales":
    st.markdown("<h2 style='color: #e9769d;'>🎒 Panel de Control de Inventario</h2>", unsafe_allow_html=True)
    
    if not st.session_state.materiales:
        st.info("No hay materiales registrados en el inventario. Ve a la pestaña '➕ 2- Crear Material' para agregar el primero.")
    else:
        # Generar los datos para la tabla de forma segura
        lista_tabla = []
        for nombre_m, info_m in st.session_state.materiales.items():
            lista_tabla.append({
                "Material": nombre_m,
                "Tipo": info_m.get("Tipo", "Unidad (Cantidad)"),
                "Marca": info_m.get("Marca", "Genérica"),
                "Costo ($)": info_m.get("Costo", 0.0),
                "Precio ($)": info_m.get("Precio", 0.0),
                "Ganancia (%)": f"{info_m.get('Ganancia_Pct', 0.0)}%",
                "Última Actualización": info_m.get("Fecha", "No registrada")
            })
            
        df_materiales = pd.DataFrame(lista_tabla)
        
        # Mostramos la tabla limpia (Sin edición directa interna para que no rompa la navegación)
        st.dataframe(df_materiales, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.markdown("### 🛠️ Acciones de Inventario")
        
        # Selectores externos súper estables para elegir qué hacer
        col_sel1, col_sel2 = st.columns([2, 1])
        with col_sel1:
            material_seleccionado = st.selectbox("Selecciona un material para interactuar:", ["-- Seleccionar --"] + list(st.session_state.materiales.keys()))
        with col_sel2:
            accion = st.radio("Acción:", ["👁️ Ver Ficha", "✏️ Editar Costos"], horizontal=True)
            
        if material_seleccionado != "-- Seleccionar --":
            info_foc = st.session_state.materiales[material_seleccionado]
            
            # ACCIÓN: VER FICHA
            if accion == "👁️ Ver Ficha":
                st.markdown(f"""
                    <div class='tarjeta-ver'>
                        <h3 style='color:#74b7d5; text-align:left; margin:0;'>📋 Ficha Técnica: {material_seleccionado}</h3>
                    </div>
                """, unsafe_allow_html=True)
                
                cv1, cv2 = st.columns(2)
                with cv1:
                    st.write(f"• **Tipo de Medida:** {info_foc.get('Tipo')}")
                    st.write(f"• **Marca:** {info_foc.get('Marca')}")
                    if info_foc.get('Tipo') == "Pieza (Área)":
                        st.write(f"• **Dimensiones:** {info_foc.get('Ancho')}cm x {info_foc.get('Alto')}cm")
                with cv2:
                    st.write(f"• **Costo Unitario:** ${info_foc.get('Costo'):.2f}")
                    st.write(f"• **Precio Público:** ${info_foc.get('Precio'):.2f}")
                    st.write(f"• **Margen de Ganancia:** {info_foc.get('Ganancia_Pct')}%")
                    st.write(f"• **Último Cambio:** {info_foc.get('Fecha')}")
                    
            # ACCIÓN: EDITAR COSTOS
            elif accion == "✏️ Editar Costos":
                st.markdown(f"""
                    <div class='tarjeta-editar'>
                        <h3 style='color:#e9769d; text-align:left; margin:0;'>✏️ Formulario de Modificación: {material_seleccionado}</h3>
                    </div>
                """, unsafe_allow_html=True)
                
                # Formulario dedicado para guardar la edición de forma segura
                with st.form("form_edicion_panel"):
                    ce1, ce2, ce3 = st.columns(3)
                    nuevo_c = ce1.number_input("Costo de Proveedor ($)", min_value=0.0, value=float(info_foc.get('Costo')), format="%.2f")
                    nuevo_p = ce2.number_input("Precio de Tienda ($)", min_value=0.0, value=float(info_foc.get('Precio')), format="%.2f")
                    nueva_m = ce3.text_input("Modificar Marca", value=info_foc.get('Marca', 'Genérica'))
                    
                    guardar_cambios = st.form_submit_button("💾 Guardar Cambios")
                    
                    if guardar_cambios:
                        if nuevo_p <= 0:
                            st.error("El precio debe ser mayor a 0.")
                        else:
                            nueva_ganancia = ((nuevo_p - nuevo_c) / nuevo_p * 100) if nuevo_p > 0 else 0.0
                            st.session_state.materiales[material_seleccionado]["Costo"] = nuevo_c
                            st.session_state.materiales[material_seleccionado]["Precio"] = nuevo_p
                            st.session_state.materiales[material_seleccionado]["Marca"] = nueva_m
                            st.session_state.materiales[material_seleccionado]["Ganancia_Pct"] = round(nueva_ganancia, 1)
                            st.session_state.materiales[material_seleccionado]["Fecha"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                            
                            guardar_datos('materiales.json', st.session_state.materiales)
                            st.success(f"¡Material '{material_seleccionado}' actualizado con éxito!")
                            st.rerun()

# ==========================================
# 🧮 VISTAS RESTANTES (TEMPORALES)
# ==========================================
elif st.session_state.menu_actual == "🧮 1- Crear Presupuesto":
    st.markdown("<h2 style='color: #e9769d;'>🧮 Crear Presupuesto de Producción</h2>", unsafe_allow_html=True)
    st.info("Módulo listo para ser enlazado con la base de datos.")

elif st.session_state.menu_actual == "📜 4- Catálogo de Productos Finales":
    st.markdown("<h2 style='color: #e9769d;'>📜 Catálogo de Productos Finales</h2>", unsafe_allow_html=True)
    st.info("Catálogo en espera.")
