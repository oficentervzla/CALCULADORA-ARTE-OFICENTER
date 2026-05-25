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
        
        /* Tarjeta de presupuesto final destacada */
        .tarjeta-precio {
            background-color: #f7f9fa; padding: 20px; border-radius: 15px;
            border-left: 6px solid #e9769d; box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
            text-align: center;
        }
        
        /* Tarjetas compactas de Gestión e Historial */
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

# Inicialización e historial de insumos en base de datos
if 'materiales' not in st.session_state:
    st.session_state.materiales = cargar_datos('materiales.json', dict, {
        "Cartulina Escolar": {"Tipo": "Pieza (Área)", "Ancho": 50.0, "Alto": 70.0, "Costo": 0.50, "Precio": 1.00, "Marca": "Genérica", "Fecha": hoy},
        "Silicón (Barra)": {"Tipo": "Unidad (Cantidad)", "Ancho": 1.0, "Alto": 1.0, "Costo": 0.10, "Precio": 0.25, "Marca": "Genérica", "Fecha": hoy},
        "Impresion en Papel Fotográfico": {"Tipo": "Unidad (Cantidad)", "Ancho": 1.0, "Alto": 1.0, "Costo": 0.08, "Precio": 0.50, "Marca": "Genérica", "Fecha": hoy},
        "Impresion en Papel Fotográfico Carta": {"Tipo": "Unidad (Cantidad)", "Ancho": 1.0, "Alto": 1.0, "Costo": 0.08, "Precio": 0.50, "Marca": "Genérica", "Fecha": hoy}
    })

# Corrección crítica de errores de lectura de Diccionarios vacíos
if 'productos' not in st.session_state:
    st.session_state.productos = cargar_datos('productos.json', dict, {})

if 'items_presupuesto' not in st.session_state:
    st.session_state.items_presupuesto = []

if 'tasa_bcv' not in st.session_state:
    st.session_state.tasa_bcv = 36.50

# Controladores de acción en línea desde la tabla
if 'accion_material' not in st.session_state:
    st.session_state.accion_material = None  # Puede ser "ver" o "editar"
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
    st.markdown("<h2 style='color: #e9769d;'>🧮 Crear Presupuesto de Production</h2>", unsafe_allow_html=True)
    # Lógica estándar de presupuestos...

# ==========================================
# ➕ VISTA: 2- CREAR MATERIAL
# ==========================================
elif st.session_state.menu_actual == "➕ 2- Crear Material":
    st.markdown("<h2 style='color: #e9769d;'>➕ Registrar Nuevo Insumo / Material</h2>", unsafe_allow_html=True)
    # Lógica estándar de creación...

# ==========================================
# 🎒 VISTA: 3- VERIFICAR PANEL DE MATERIALES (BOTONES EN TABLA INTEGRADOS)
# ==========================================
elif st.session_state.menu_actual == "🎒 3- Verificar Panel de Materiales":
    st.markdown("<h2 style='color: #e9769d;'>🎒 Panel de Control de Inventario</h2>", unsafe_allow_html=True)
    
    if not st.session_state.materiales:
        st.info("No hay materiales registrados.")
    else:
        # Generamos la tabla con columnas interactivas utilizando st.dataframe avanzado
        lista_datos_tabla = []
        for n, d in st.session_state.materiales.items():
            porcentaje_ganancia_mat = (((d['Precio'] - d['Costo']) / d['Precio']) * 100) if d['Precio'] > 0 else 0.0
            lista_datos_tabla.append({
                "Material": n,
                "Tipo": d["Tipo"],
                "Marca": d.get("Marca", "Genérica"),
                "Costo Base": f"${d['Costo']:.2f}",
                "Precio Base": f"${d['Precio']:.2f}",
                "Ganancia (%)": f"{porcentaje_ganancia_mat:.1f}%",
                "Última Actualización": d.get("Fecha", "Original"),
                "👁️ Ver Resumen": False,  # Configurado como interactivo
                "✏️ Editar Costos": False
            })
            
        df_panel = pd.DataFrame(lista_datos_tabla)
        
        # Uso de st.data_editor para capturar los clics directamente en las filas de la tabla
        edicion_tabla = st.data_editor(
            df_panel,
            column_config={
                "👁️ Ver Resumen": st.column_config.CheckboxColumn("👁️ Ver", help="Ver ficha completa y PDF", default=False),
                "✏️ Editar Costos": st.column_config.CheckboxColumn("✏️ Editar", help="Modificar precios e insumos", default=False)
            },
            disabled=["Material", "Tipo", "Marca", "Costo Base", "Precio Base", "Ganancia (%)", "Última Actualización"],
            use_container_width=True,
            key="editor_tabla_panel"
        )
        
        # Evaluar si el usuario interactuó con alguna fila de la lista
        for index, row in edicion_tabla.iterrows():
            nombre_mat_fila = row["Material"]
            if row["👁️ Ver Resumen"] == True:
                st.session_state.accion_material = "ver"
                st.session_state.material_focalizado = nombre_mat_fila
                st.component_value = False # Reset momentáneo
                break
            elif row["✏️ Editar Costos"] == True:
                st.session_state.accion_material = "editar"
                st.session_state.material_focalizado = nombre_mat_fila
                break

        # ACCIÓN A: DESPLIEGUE COMPACTO DEL RESUMEN GENERAL (VER)
        if st.session_state.accion_material == "ver" and st.session_state.material_focalizado in st.session_state.materiales:
            mat_foc = st.session_state.material_focalizado
            info_mat = st.session_state.materiales[mat_foc]
            
            ganancia_dolares = info_mat["Precio"] - info_mat["Costo"]
            pct_ganancia = (ganancia_dolares / info_mat["Precio"] * 100) if info_mat["Precio"] > 0 else 0.0
            
            # Buscar Toppers donde se usa este insumo
            productos_vinculados = [p_name for p_name, p_detalles in st.session_state.productos.items() 
                                    if any(item["Material"] == mat_foc for item in p_detalles.get("Materiales Usados", []))]
            vinculos_str = ", ".join(productos_vinculados) if productos_vinculados else "Ninguno (Insumo libre)"
            
            st.markdown(f"""
                <div class="tarjeta-ver">
                    <h3 style="color:#74b7d5; text-align:left; margin:0;">📋 Resumen Técnico General: {mat_foc}</h3>
                </div>
            """, unsafe_allow_html=True)
            
            c_v1, c_v2, c_v3 = st.columns(3)
            with c_v1:
                st.markdown("**⚙️ Características:**")
                st.write(f"• **Tipo de medida o cantidad:** {info_mat['Tipo']}")
                st.write(f"• **Marca Utilizada:** {info_mat.get('Marca', 'Genérica')}")
                if info_mat["Tipo"] == "Pieza (Área)":
                    st.write(f"• **Dimensiones:** {info_mat['Ancho']}cm x {info_mat['Alto']}cm")
            with c_v2:
                st.markdown("**💰 Datos Financieros:**")
                st.write(f"• **Costo Unitario:** ${info_mat['Costo']:.2f}")
                st.write(f"• **Precio de Venta:** ${info_mat['Precio']:.2f}")
                st.write(f"• **Ganancia Neta Real:** ${ganancia_dolares:.2f} ({pct_ganancia:.1f}%)")
            with c_v3:
                st.markdown("**🎒 Catálogo Asociado:**")
                st.write(f"• **Productos que lo usan:** `{vinculos_str}`")
                st.write(f"• **Último Registro:** {info_mat.get('Fecha', 'Original')}")
            
            # Botones de Acción de la Ficha
            c_btn_v1, c_btn_v2, c_btn_v3 = st.columns([1, 1, 3])
            with c_btn_v1:
                # Creación simulada del archivo plano para simular descarga de ficha PDF limpia
                data_pdf_simulada = f"FICHA TÉCNICA - {mat_foc}\nMarca: {info_mat.get('Marca', 'Genérica')}\nCosto: ${info_mat['Costo']}\nPrecio: ${info_mat['Precio']}"
                st.download_button("📥 Descargar PDF", data=data_pdf_simulada, file_name=f"Ficha_{mat_foc}.pdf", mime="text/plain", use_container_width=True)
            with c_btn_v2:
                if st.button("✏️ Cambiar a Editar", key="btn_switch_edit"):
                    st.session_state.accion_material = "editar"
                    st.rerun()
            with c_btn_v3:
                if st.button("❌ Cerrar Vista", key="btn_close_v"):
                    st.session_state.accion_material = None
                    st.session_state.material_focalizado = None
                    st.rerun()

        # ACCIÓN B: DESPLIEGUE COMPACTO FORMULARIO DE EDICIÓN (EDITAR)
        elif st.session_state.accion_material == "editar" and st.session_state.material_focalizado in st.session_state.materiales:
            mat_foc = st.session_state.material_focalizado
            info_mat = st.session_state.materiales[mat_foc]
            
            st.markdown(f"""
                <div class="tarjeta-editar">
                    <h3 style="color:#e9769d; text-align:left; margin:0;">✏️ Formulario de Modificación Rápida: {mat_foc}</h3>
                </div>
            """, unsafe_allow_html=True)
            
            c_e1, c_e2, c_e3 = st.columns(3)
            nuevo_costo = c_e1.number_input("Actualizar Costo Proveedor ($)", min_value=0.0, value=float(info_mat["Costo"]), format="%.2f", key="edit_c_tabla")
            nuevo_precio = c_e2.number_input("Actualizar Precio Público ($)", min_value=0.0, value=float(info_mat["Precio"]), format="%.2f", key="edit_p_tabla")
            nueva_marca = c_e3.text_input("Actualizar Marca Utilizada", value=info_mat.get("Marca", "Genérica"), key="edit_m_tabla")
            
            actualizar_cadena = st.checkbox("Recalcular automáticamente el costo y precio final de todos los Toppers que incluyan este material", value=True)
            
            c_btn_e1, c_btn_e2 = st.columns([1, 4])
            with c_btn_e1:
                if st.button("💾 Guardar", key="btn_save_e", type="primary", use_container_width=True):
                    # Recalcular el árbol de productos si corresponde para mantener la consistencia
                    if actualizar_cadena:
                        for p_key, p_val in st.session_state.productos.items():
                            cambiado = False
                            for item in p_val.get("Materiales Usados", []):
                                if item["Material"] == mat_foc:
                                    if info_mat["Tipo"] == "Pieza (Área)":
                                        area_tot = info_mat["Ancho"] * info_mat["Alto"]
                                        prop = (item["Ancho"] * item["Alto"]) / area_tot if area_tot > 0 else 0
                                        item["Costo Calculado"] = round(nuevo_costo * prop, 4)
                                        item["Precio Calculado"] = round(nuevo_precio * prop, 4)
                                    else:
                                        item["Costo Calculado"] = round(nuevo_costo * item["Cantidad"], 4)
                                        item["Precio Calculado"] = round(nuevo_precio * item["Cantidad"], 4)
                                    cambiado = True
                            if cambiado:
                                nuevo_precio_mats = sum(i["Precio Calculado"] for i in p_val["Materiales Usados"])
                                p_val["Precio Venta $"] = round(nuevo_precio_mats * (1 + (p_val["Margen %"] / 100)), 2)
                                p_val["Fecha"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                        guardar_datos('productos.json', st.session_state.productos)
                    
                    # Actualizar maestro de materiales
                    st.session_state.materiales[mat_foc]["Costo"] = nuevo_costo
                    st.session_state.materiales[mat_foc]["Precio"] = nuevo_precio
                    st.session_state.materiales[mat_foc]["Marca"] = nueva_marca
                    st.session_state.materiales[mat_foc]["Fecha"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                    guardar_datos('materiales.json', st.session_state.materiales)
                    
                    st.success("¡Insumo actualizado con éxito!")
                    st.session_state.accion_material = None
                    st.session_state.material_focalizado = None
                    st.rerun()
            with c_btn_e2:
                if st.button("❌ Cancelar", key="btn_cancel_e"):
                    st.session_state.accion_material = None
                    st.session_state.material_focalizado = None
                    st.rerun()

# ==========================================
# 📜 VISTA: 4- CATÁLOGO DE PRODUCTOS FINALES
# ==========================================
elif st.session_state.menu_actual == "📜 4- Catálogo de Productos Finales":
    st.markdown("<h2 style='color: #e9769d;'>📜 Catálogo de Productos Finales Guardados</h2>", unsafe_allow_html=True)
    
    if not st.session_state.productos:
        st.warning("No hay productos guardados en el catálogo.")
    else:
        # El catálogo ahora lee de manera segura el diccionario sin romper la app por variables nulas
        for p_nombre, p_info in list(st.session_state.productos.items()):
            with st.expander(f"📦 {p_nombre} | Venta: ${p_info.get('Precio Venta $', 0.00)} | {(p_info.get('Precio Venta $', 0.00) * st.session_state.tasa_bcv):.2f} Bs."):
                st.write(f"**Ganancia Neta Real:** ${p_info.get('Ganancia Neta $', 0.00)}")
                if "Materiales Usados" in p_info:
                    st.dataframe(pd.DataFrame(p_info["Materiales Usados"])[["Material", "Cantidad", "Costo Calculado", "Precio Calculado"]], use_container_width=True)
