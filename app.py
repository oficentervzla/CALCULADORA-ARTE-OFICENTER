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
    st.markdown("<h2 style='color: #e9769d;'>🧮 Crear Presupuesto de Production</h2>", unsafe_allow_html=True)
    st.info("Módulo de presupuestos listo para operar.")

# ==========================================
# ➕ VISTA: 2- CREAR MATERIAL
# ==========================================
elif st.session_state.menu_actual == "➕ 2- Crear Material":
    st.markdown("<h2 style='color: #e9769d;'>➕ Registrar Nuevo Insumo / Material</h2>", unsafe_allow_html=True)
    st.info("Módulo de registro e ingreso de nuevos materiales configurado.")

# ==========================================
# 🎒 VISTA: 3- PANEL DE CONTROL (REPARADO)
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
            
            # Cálculo seguro de la ganancia
            costo_base = d.get('Costo', 0.0)
            precio_base = d.get('Precio', 0.0)
            porcentaje_ganancia_mat = (((precio_base - costo_base) / precio_base) * 100) if precio_base > 0 else 0.0
            
            if d.get("Tipo") == "Pieza (Área)":
                medida_str = f"{d.get('Ancho', 0.0)} x {d.get('Alto', 0.0)} cm"
            else:
                medida_str = "N/A (Unidad)"
                
            lista_datos_tabla.append({
                "Material": n,
                "Tipo": d.get("Tipo", "Unidad (Cantidad)"),
                "Medidas (cm)": medida_str,
                "Marca": d.get("Marca", "Genérica"),
                "Costo Base": f"${costo_base:.2f}",
                "Precio Base": f"${precio_base:.2f}",
                "Ganancia (%)": f"{porcentaje_ganancia_mat:.1f}%",
                "Última Actualización": d.get("Fecha", "Original"),
                "👁️ Ver": False,  
                "✏️ Editar": False
            })
            
        df_panel = pd.DataFrame(lista_datos_tabla)
        
        # Columnas deshabilitadas para edición directa
        columnas_bloqueadas = ["Material", "Tipo", "Medidas (cm)", "Marca", "Costo Base", "Precio Base", "Ganancia (%)", "Última Actualización"]
        
        # Configuración explícita de las columnas interactivas
        configuracion_columnas = {
            "👁️ Ver": st.column_config.CheckboxColumn("👁️ Ver", help="Ver resumen técnico", default=False),
            "✏️ Editar": st.column_config.CheckboxColumn("✏️ Editar", help="Modificar costos y dimensiones", default=False)
        }
        
        # Renderizado limpio del editor de datos
        edicion_tabla = st.data_editor(
            df_panel,
            column_config=configuracion_columnas,
            disabled=columnas_bloqueadas,
            use_container_width=True,
            key="editor_tabla_panel"
        )
        
        # DETECTAR ACCIONES INMEDIATAS
        if "editor_tabla_panel" in st.session_state:
            estado_editor = st.session_state.editor_tabla_panel
            if estado_editor.get("edited_rows"):
                filas_cambiadas = estado_editor["edited_rows"]
                for idx_fila_str, cambios in filas_cambiadas.items():
                    idx_fila = int(idx_fila_str)
                    nombre_mat_fila = nombres_materiales[idx_fila]
                    
                    if cambios.get("👁️ Ver") is True:
                        st.session_state.accion_material = "ver"
                        st.session_state.material_focalizado = nombre_mat_fila
                        st.rerun()
                    elif cambios.get("✏️ Editar") is True:
                        st.session_state.accion_material = "editar"
                        st.session_state.material_focalizado = nombre_mat_fila
                        st.rerun()

        # BLOQUE DE ACCIÓN A: VER DETALLES
        if st.session_state.accion_material == "ver" and st.session_state.material_focalizado in st.session_state.materiales:
            mat_foc = st.session_state.material_focalizado
            info_mat = st.session_state.materiales[mat_foc]
            
            ganancia_dolares = info_mat["Precio"] - info_mat["Costo"]
            pct_ganancia = (ganancia_dolares / info_mat["Precio"] * 100) if info_mat["Precio"] > 0 else 0.0
            
            productos_vinculados = [p_name for p_name, p_detalles in st.session_state.productos.items() 
                                    if any(item["Material"] == mat_foc for item in p_detalles.get("Materiales Usados", []))]
            vinculos_str = ", ".join(productos_vinculados) if productos_vinculados else "Ninguno (Insumo libre)"
            
            st.markdown(f"""
                <div class="tarjeta-ver">
                    <h3 style="color:#74b7d5; text-align:left; margin:0;">📋 Resumen Técnico: {mat_foc}</h3>
                </div>
            """, unsafe_allow_html=True)
            
            c_v1, c_v2, c_v3 = st.columns(3)
            with c_v1:
                st.markdown("**⚙️ Características:**")
                st.write(f"• **Tipo de medida:** {info_mat['Tipo']}")
                st.write(f"• **Marca:** {info_mat.get('Marca', 'Genérica')}")
                if info_mat["Tipo"] == "Pieza (Área)":
                    st.write(f"• **Formato:** {info_mat['Ancho']}cm x {info_mat['Alto']}cm")
            with c_v2:
                st.markdown("**💰 Estructura Financiera:**")
                st.write(f"• **Costo Proveedor:** ${info_mat['Costo']:.2f}")
                st.write(f"• **Precio Venta:** ${info_mat['Precio']:.2f}")
                st.write(f"• **Utilidad:** ${ganancia_dolares:.2f} ({pct_ganancia:.1f}%)")
            with c_v3:
                st.markdown("**🎒 Vínculos:**")
                st.write(f"• **Usado en:** `{vinculos_str}`")
                st.write(f"• **Actualizado:** {info_mat.get('Fecha', 'Original')}")
            
            c_btn_v1, c_btn_v2, c_btn_v3 = st.columns([1, 1, 3])
            with c_btn_v1:
                medida_pdf = f"{info_mat.get('Ancho')}x{info_mat.get('Alto')} cm" if info_mat["Tipo"] == "Pieza (Área)" else "N/A"
                data_pdf_simulada = (
                    f"FICHA TÉCNICA - ART CENTER\n\nMaterial: {mat_foc}\nTipo: {info_mat['Tipo']}\n"
                    f"Medidas: {medida_pdf}\nMarca: {info_mat.get('Marca', 'Genérica')}\n"
                    f"Costo: ${info_mat['Costo']:.2f}\nPrecio: ${info_mat['Precio']:.2f}\nMargen: {pct_ganancia:.1f}%"
                )
                st.download_button("📥 Descargar Info", data=data_pdf_simulada, file_name=f"Ficha_{mat_foc.replace(' ', '_')}.txt", mime="text/plain", use_container_width=True)
            with c_btn_v2:
                if st.button("✏️ Editar Insumo", key="btn_switch_edit"):
                    st.session_state.accion_material = "editar"
                    st.rerun()
            with c_btn_v3:
                if st.button("❌ Cerrar Ficha", key="btn_close_v"):
                    st.session_state.accion_material = None
                    st.session_state.material_focalizado = None
                    st.rerun()

        # BLOQUE DE ACCIÓN B: FORMULARIO DE EDICIÓN RAPIDA
        elif st.session_state.accion_material == "editar" and st.session_state.material_focalizado in st.session_state.materiales:
            mat_foc = st.session_state.material_focalizado
            info_mat = st.session_state.materiales[mat_foc]
            
            st.markdown(f"""
                <div class="tarjeta-editar">
                    <h3 style="color:#e9769d; text-align:left; margin:0;">✏️ Modificación Rápida: {mat_foc}</h3>
                </div>
            """, unsafe_allow_html=True)
            
            c_e1, c_e2, c_e3 = st.columns(3)
            nuevo_costo = c_e1.number_input("Costo Proveedor ($)", min_value=0.0, value=float(info_mat["Costo"]), format="%.2f", key="edit_c_tabla")
            nuevo_precio = c_e2.number_input("Precio Público ($)", min_value=0.0, value=float(info_mat["Precio"]), format="%.2f", key="edit_p_tabla")
            nueva_marca = c_e3.text_input("Marca", value=info_mat.get("Marca", "Genérica"), key="edit_m_tabla")
            
            if info_mat["Tipo"] == "Pieza (Área)":
                c_m1, c_m2 = st.columns(2)
                nuevo_ancho = c_m1.number_input("Ancho (cm)", min_value=1.0, value=float(info_mat.get("Ancho", 1.0)), key="edit_ancho_tabla")
                nuevo_alto = c_m2.number_input("Alto (cm)", min_value=1.0, value=float(info_mat.get("Alto", 1.0)), key="edit_alto_tabla")
            
            actualizar_cadena = st.checkbox("Recalcular costos en Toppers vinculados", value=True)
            
            c_btn_e1, c_btn_e2 = st.columns([1, 4])
            with c_btn_e1:
                if st.button("💾 Guardar", key="btn_save_e", type="primary", use_container_width=True):
                    if actualizar_cadena:
                        for p_key, p_val in st.session_state.productos.items():
                            cambiado = False
                            for item in p_val.get("Materiales Usados", []):
                                if item["Material"] == mat_foc:
                                    if info_mat["Tipo"] == "Pieza (Área)":
                                        area_tot = nuevo_ancho * nuevo_alto
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
                    
                    st.session_state.materiales[mat_foc]["Costo"] = nuevo_costo
                    st.session_state.materiales[mat_foc]["Precio"] = nuevo_precio
                    st.session_state.materiales[mat_foc]["Marca"] = nueva_marca
                    if info_mat["Tipo"] == "Pieza (Área)":
                        st.session_state.materiales[mat_foc]["Ancho"] = nuevo_ancho
                        st.session_state.materiales[mat_foc]["Alto"] = nuevo_alto
                        
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
        for p_nombre, p_info in list(st.session_state.productos.items()):
            with st.expander(f"📦 {p_nombre} | Venta: ${p_info.get('Precio Venta $', 0.00)} | {(p_info.get('Precio Venta $', 0.00) * st.session_state.tasa_bcv):.2f} Bs."):
                st.write(f"**Ganancia Neta Real:** ${p_info.get('Ganancia Neta $', 0.00)}")
                if "Materiales Usados" in p_info:
                    st.dataframe(pd.DataFrame(p_info["Materiales Usados"])[["Material", "Cantidad", "Costo Calculado", "Precio Calculado"]], use_container_width=True)
