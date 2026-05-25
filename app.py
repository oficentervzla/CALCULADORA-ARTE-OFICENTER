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
        
        /* Botones de navegación superiores con estilo de pestañas limpias */
        .boton-nav {
            display: inline-block;
            width: 100%;
        }
        
        /* Estilo interactivo para Toppers/Casillas del Menú Principal */
        div[data-testid="stColumn"] .stButton>button {
            background-color: #f7f9fa !important;
            color: #333333 !important;
            border: 2px solid #fed80c !important;
            border-radius: 15px !important;
            padding: 25px 15px !important;
            width: 100% !important;
            min-height: 180px !important;
            box-shadow: 0px 4px 8px rgba(0,0,0,0.05) !important;
            transition: all 0.3s ease !important;
            white-space: normal !important;
            display: block !important;
        }
        div[data-testid="stColumn"] .stButton>button:hover {
            border-color: #e9769d !important;
            background-color: #ffffff !important;
            transform: translateY(-3px);
            box-shadow: 0px 6px 12px rgba(0,0,0,0.1) !important;
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

# Inicialización del almacenamiento persistente en el servidor
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

# --- CONTROLADOR CENTRAL DE NAVEGACIÓN ---
# Esto garantiza que la app nunca se quede en blanco y sepa qué pestaña dibujar
opciones_menu = [
    "🏠 Menú Principal", 
    "🧮 1- Crear Presupuesto", 
    "➕ 2- Crear Material", 
    "🎒 3- Verificar Panel de Materiales", 
    "📜 4- Catálogo de Productos Finales"
]

if 'menu_actual' not in st.session_state:
    st.session_state.menu_actual = "🏠 Menú Principal"

# Render de la Barra Superior de Navegación (Botones dinámicos que actúan como pestañas)
cols_nav = st.columns(5)
for idx, opcion in enumerate(opciones_menu):
    with cols_nav[idx]:
        # El botón activo se resalta en color amarillo/azul de forma automática
        es_activo = st.session_state.menu_actual == opcion
        tipo_estilo = "primary" if es_activo else "secondary"
        if st.button(opcion, key=f"nav_sup_{idx}", use_container_width=True, type=tipo_estilo):
            st.session_state.menu_actual = opcion
            st.rerun()

st.divider()

# ==========================================
# 🏠 VISTA: MENÚ PRINCIPAL (ACCESO DESDE AMBOS SITIOS)
# ==========================================
if st.session_state.menu_actual == "🏠 Menú Principal":
    st.markdown("<p class='titulo-principal'>ART CENTER</p>", unsafe_allow_html=True)
    st.markdown("<p class='frase-principal'>¿Qué vamos a crear hoy?</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-weight: bold; color: #555;'>Selecciona una casilla o usa la barra superior para empezar:</p>", unsafe_allow_html=True)
    st.divider()
    
    st.markdown("### 🇻🇪 Control Cambiario")
    st.session_state.tasa_bcv = st.number_input("Tasa BCV del día (Bs.)", min_value=1.0, value=float(st.session_state.tasa_bcv), step=0.10, key="input_tasa_home")
    st.divider()
    
    # Render de casillas interactivas en el cuerpo principal
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("🧮 Presupuesto\n\nCalcula costos, precios de venta y desglosa tus ganancias al instante.", key="btn_home_to_pres"):
            st.session_state.menu_actual = "🧮 1- Crear Presupuesto"
            st.rerun()
    with c2:
        if st.button("➕ Crear Material\n\nRegistra nuevos insumos con sus medidas, marcas y ganancias.", key="btn_home_to_mat"):
            st.session_state.menu_actual = "➕ 2- Crear Material"
            st.rerun()
    with c3:
        if st.button("🎒 Panel Materiales\n\nMira tu inventario, edita precios en masa y revisa tus porcentajes.", key="btn_home_to_panel"):
            st.session_state.menu_actual = "🎒 3- Verificar Panel de Materiales"
            st.rerun()
    with c4:
        if st.button("📜 Catálogo Final\n\nRevisa tus productos listos, añade fotos y gestiona historiales.", key="btn_home_to_cat"):
            st.session_state.menu_actual = "📜 4- Catálogo de Productos Finales"
            st.rerun()

    st.divider()
    st.markdown("<p style='text-align: center; font-size: 12px; color: #aaa;'>Una solución desarrollada para Oficenter C.A.</p>", unsafe_allow_html=True)

# ==========================================
# 🧮 VISTA: 1- CREAR PRESUPUESTO
# ==========================================
elif st.session_state.menu_actual == "🧮 1- Crear Presupuesto":
    st.markdown("<h2 style='color: #e9769d;'>🧮 Crear Presupuesto de Production</h2>", unsafe_allow_html=True)
    
    col_izq, col_der = st.columns([1.3, 1])
    
    with col_izq:
        st.subheader("📋 Listado de Insumos del Proyecto")
        if not st.session_state.materiales:
            st.warning("Primero debes registrar materiales en la pestaña '2- Crear Material'.")
        else:
            with st.container():
                c_mat, c_cant = st.columns([2, 1])
                mat_selec = c_mat.selectbox("Selecciona un material de tu inventario:", list(st.session_state.materiales.keys()), key="sel_pres")
                mat_info = st.session_state.materiales[mat_selec]
                
                if mat_info["Tipo"] == "Pieza (Área)":
                    cx1, cx2 = st.columns(2)
                    ancho_u = cx1.number_input("Ancho a usar (cm)", min_value=0.1, value=10.0, step=1.0, key="w_pres")
                    alto_u = cx2.number_input("Alto a usar (cm)", min_value=0.1, value=10.0, step=1.0, key="h_pres")
                    cantidad_u = 1.0
                else:
                    cantidad_u = c_cant.number_input("Cantidad a usar:", min_value=0.1, value=1.0, step=1.0, key="cant_pres")
                    ancho_u, alto_u = 1.0, 1.0

                st.caption("⚙️ Valores del Insumo Seleccionado (Sincronizados automáticamente desde la base de datos):")
                ce1, ce2 = st.columns(2)
                
                # Se asigna un identificador dinámico basado en la clave del material para refrescar los montos limpios
                costo_momento = ce1.number_input("Costo unitario momentáneo ($)", min_value=0.0, value=float(mat_info["Costo"]), format="%.2f", key=f"c_mom_{mat_selec}")
                precio_momento = ce2.number_input("Precio de venta momentáneo ($)", min_value=0.0, value=float(mat_info["Precio"]), format="%.2f", key=f"p_mom_{mat_selec}")
                
                if mat_info["Tipo"] == "Pieza (Área)":
                    area_total_mat = mat_info["Ancho"] * mat_info["Alto"]
                    proporcion = (ancho_u * alto_u) / area_total_mat if area_total_mat > 0 else 0
                    costo_calculado = costo_momento * proporcion
                    precio_calculado = precio_momento * proporcion
                else:
                    costo_calculado = costo_momento * cantidad_u
                    precio_calculado = precio_momento * cantidad_u

                if st.button("➕ Añadir Insumo al Listado", key="btn_add_pres", type="primary"):
                    st.session_state.items_presupuesto.append({
                        "Material": mat_selec, "Tipo": mat_info["Tipo"], "Cantidad": cantidad_u,
                        "Ancho": ancho_u, "Alto": alto_u, "Costo Individual": costo_momento, "Precio Individual": precio_momento,
                        "Costo Calculado": round(costo_calculado, 4), "Precio Calculado": round(precio_calculado, 4)
                    })
                    st.success(f"¡Añadido: {mat_selec}!")
                    st.rerun()

        if st.session_state.items_presupuesto:
            st.markdown("### Materiales incluidos:")
            df_items = pd.DataFrame(st.session_state.items_presupuesto)
            st.dataframe(df_items[["Material", "Cantidad", "Ancho", "Alto", "Costo Calculado", "Precio Calculado"]], use_container_width=True)
            if st.button("🗑 Limpiar Lista Actual", key="btn_clear_pres"):
                st.session_state.items_presupuesto = []
                st.rerun()

    with col_der:
        st.subheader("📊 Resumen Económico")
        if st.session_state.items_presupuesto:
            total_costo_mats = sum(item["Costo Calculado"] for item in st.session_state.items_presupuesto)
            total_precio_mats = sum(item["Precio Calculado"] for item in st.session_state.items_presupuesto)
            
            margen_creativo = st.slider("Margen de Ganancia Extra (%)", min_value=0, max_value=200, value=50, step=5, key="slide_pres")
            
            precio_final_dolares = total_precio_mats * (1 + (margen_creativo / 100))
            precio_final_bolivares = precio_final_dolares * st.session_state.tasa_bcv
            
            ganancia_materiales = total_precio_mats - total_costo_mats
            ganancia_creativa_extra = precio_final_dolares - total_precio_mats
            ganancia_total_neta = ganancia_materiales + ganancia_creativa_extra

            st.markdown(f"""
                <div class="tarjeta-precio">
                    <p style="margin:0; font-size:13px; color:#555; font-weight:bold;">PRECIO DE VENTA FINAL</p>
                    <h1 style="margin:0; font-size:46px; color:#e9769d !important;">${precio_final_dolares:.2f}</h1>
                    <h3 style="margin:0; color:#74b7d5 !important;">Bs. {precio_final_bolivares:.2f}</h3>
                    <p style="margin:10px 0 0 0; font-size:14px; color:#8bcc60; font-weight:bold;">Ganancia Neta Real: ${ganancia_total_neta:.2f} ({(ganancia_total_neta * st.session_state.tasa_bcv):.2f} Bs.)</p>
                </div>
            """, unsafe_allow_html=True)
            
            with st.expander("🔎 Ver Desglose Analítico", expanded=True):
                st.write(f"• **Costo Total Insumos (Proveedor):** ${total_costo_mats:.2f}")
                st.write(f"• **Precio Total Insumos (Tienda):** ${total_precio_mats:.2f}")
                st.write(f"💸 **Ganancia por venta de materiales:** ${ganancia_materiales:.2f}")
                st.write(f"🎨 **Ganancia Creativa por encima ({margen_creativo}%):** ${ganancia_creativa_extra:.2f}")
            
            st.divider()
            st.subheader("💾 Guardar en Catálogo")
            nombre_final = st.text_input("Nombre del Producto Terminado:", placeholder="Ej: Topper San Valentín Capas", key="name_final_pres")
            
            if st.button("💾 Guardar Producto Final", key="btn_save_prod_pres"):
                if nombre_final:
                    st.session_state.productos[nombre_final] = {
                        "Precio Venta $": round(precio_final_dolares, 2),
                        "Ganancia Neta $": round(ganancia_total_neta, 2),
                        "Margen %": margen_creativo,
                        "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "Materiales Usados": st.session_state.items_presupuesto
                    }
                    guardar_datos('productos.json', st.session_state.productos)
                    st.success(f"¡El producto '{nombre_final}' se guardó en el catálogo!")
                    st.session_state.items_presupuesto = []
                    st.rerun()
                else: st.error("Ingresa un nombre para el producto.")
        else:
            st.info("Agrega materiales desde la izquierda para activar los cálculos.")

# ==========================================
# ➕ VISTA: 2- CREAR MATERIAL
# ==========================================
elif st.session_state.menu_actual == "➕ 2- Crear Material":
    st.markdown("<h2 style='color: #e9769d;'>➕ Registrar Nuevo Insumo / Material</h2>", unsafe_allow_html=True)
    
    c_n1, c_n2 = st.columns(2)
    nombre_m = c_n1.text_input("Nombre del Material:", key="n_m3")
    marca_m = c_n2.text_input("Marca (Opcional):", placeholder="Ej: Silhouette, Genérico", key="m_m3")
    
    es_pieza = st.checkbox("¿Se usa por piezas recortables en centímetros (Área)? Marca con Check si es Sí.", key="check_m3")
    tipo_m = "Pieza (Área)" if es_pieza else "Unidad (Cantidad)"
    
    ancho_m, alto_m = 1.0, 1.0
    if es_pieza:
        cx1, cx2 = st.columns(2)
        ancho_m = cx1.number_input("Ancho completo (cm)", min_value=1.0, value=50.0, key="w_m3")
        alto_m = cx2.number_input("Alto completo (cm)", min_value=1.0, value=70.0, key="h_m3")
        
    st.divider()
    cc1, cc2 = st.columns(2)
    costo_m = cc1.number_input("Costo Proveedor ($)", min_value=0.0, step=0.01, format="%.2f", key="c_m3")
    precio_m = cc2.number_input("Precio Tienda al Público ($)", min_value=0.0, step=0.01, format="%.2f", key="p_m3")
    
    if precio_m > 0:
        porcentaje_g = ((precio_m - costo_m) / precio_m) * 100
        st.info(f"📊 **Análisis directo:** Este material genera un **{porcentaje_g:.1f}% de ganancia** en tienda.")

    if st.button("💾 Guardar Material en Sistema", key="btn_save_m3", type="primary"):
        if nombre_m:
            st.session_state.materiales[nombre_m] = {
                "Tipo": tipo_m, "Ancho": ancho_m, "Alto": alto_m, "Costo": costo_m, "Precio": precio_m, "Marca": marca_m if marca_m else "Genérica", "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            guardar_datos('materiales.json', st.session_state.materiales)
            st.success(f"¡Material '{nombre_m}' creado con éxito!")
            st.rerun()
        else: st.error("El nombre es obligatorio.")

# ==========================================
# 🎒 VISTA: 3- VERIFICAR PANEL DE MATERIALES
# ==========================================
elif st.session_state.menu_actual == "🎒 3- Verificar Panel de Materiales":
    st.markdown("<h2 style='color: #e9769d;'>🎒 Verificar Panel de Materiales</h2>", unsafe_allow_html=True)
    
    if not st.session_state.materiales:
        st.info("No hay materiales registrados.")
    else:
        tabla_mats = []
        for n, d in st.session_state.materiales.items():
            usado_en = []
            for prod, p_info in st.session_state.productos.items():
                for item in p_info.get("Materiales Usados", []):
                    if item["Material"] == n:
                        usado_en.append(prod)
            
            usados_str = ", ".join(usado_en) if usado_en else "Ninguno (Sin uso)"
            porcentaje_ganancia_mat = (((d['Precio'] - d['Costo']) / d['Precio']) * 100) if d['Precio'] > 0 else 0.0
            
            tabla_mats.append({
                "Material": n, "Tipo": d["Tipo"], "Marca": d.get("Marca", "Genérica"),
                "Costo Base": f"${d['Costo']:.2f}", "Precio Base": f"${d['Precio']:.2f}",
                "Ganancia (%)": f"{porcentaje_ganancia_mat:.1f}%",
                "Última Actualización": d.get("Fecha", "Original"),
                "Utilizado en:": usados_str
            })
        
        st.dataframe(pd.DataFrame(tabla_mats), use_container_width=True)
        
        st.divider()
        st.subheader("⚙️ Modificación de Valores Individuales")
        mat_a_editar = st.selectbox("Selecciona qué material deseas visualizar o editar por separado:", list(st.session_state.materiales.keys()), key="sel_m4")
        d_ed = st.session_state.materiales[mat_a_editar]
        
        ganancia_individual_actual = d_ed["Precio"] - d_ed["Costo"]
        pct_individual_actual = ((d_ed["Precio"] - d_ed["Costo"]) / d_ed["Precio"] * 100) if d_ed["Precio"] > 0 else 0.0
        
        st.markdown(f"""
        > 🔎 **Detalles de {mat_a_editar}:**
        > * Costo actual: **${d_ed['Costo']:.2f}** | Precio actual: **${d_ed['Precio']:.2f}**
        > * Ganancia neta por unidad: **${ganancia_individual_actual:.2f}** | Porcentaje de Ganancia actual: **{pct_individual_actual:.1f}%**
        """)
        
        c_ed1, c_ed2 = st.columns(2)
        nuevo_c = c_ed1.number_input("Nuevo Costo Proveedor ($)", min_value=0.0, value=float(d_ed["Costo"]), format="%.2f", key="nc_m4")
        nuevo_p = c_ed2.number_input("Nuevo Precio Tienda ($)", min_value=0.0, value=float(d_ed["Precio"]), format="%.2f", key="np_m4")
        
        actualizar_global = st.checkbox("¿Deseas recalcular automáticamente TODOS los productos finales guardados que usen este material?", key="check_m4")
        
        if st.button("💾 Aplicar Cambios Globales", key="btn_save_m4", type="primary"):
            if actualizar_global:
                for prod, p_info in st.session_state.productos.items():
                    modificado = False
                    for item in p_info.get("Materiales Usados", []):
                        if item["Material"] == mat_a_editar:
                            if d_ed["Tipo"] == "Pieza (Área)":
                                area_tot = d_ed["Ancho"] * d_ed["Alto"]
                                prop = (item["Ancho"] * item["Alto"]) / area_tot if area_tot > 0 else 0
                                item["Costo Calculado"] = round(nuevo_c * prop, 4)
                                item["Precio Calculado"] = round(nuevo_p * prop, 4)
                            else:
                                item["Costo Calculado"] = round(nuevo_c * item["Cantidad"], 4)
                                item["Precio Calculado"] = round(nuevo_p * item["Cantidad"], 4)
                            modificado = True
                    
                    if modificado:
                        nuevo_tot_precio = sum(i["Precio Calculado"] for i in p_info["Materiales Usados"])
                        p_info["Precio Venta $"] = round(nuevo_tot_precio * (1 + (p_info["Margen %"] / 100)), 2)
                        p_info["Fecha"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                
                guardar_datos('productos.json', st.session_state.productos)
                st.info("🔄 Se recalcularon los Toppers asociados con éxito.")

            st.session_state.materiales[mat_a_editar]["Costo"] = nuevo_c
            st.session_state.materiales[mat_a_editar]["Precio"] = nuevo_p
            st.session_state.materiales[mat_a_editar]["Fecha"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            guardar_datos('materiales.json', st.session_state.materiales)
            
            st.success("¡Insumo modificado con éxito!")
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
            with st.expander(f"📦 {p_nombre} | Venta: ${p_info['Precio Venta $']} | Cambio: {(p_info['Precio Venta $'] * st.session_state.tasa_bcv):.2f} Bs. (Actualizado: {p_info['Fecha']})"):
                col_info, col_img = st.columns([2, 1])
                
                with col_info:
                    st.markdown(f"**Ganancia Neta Calculada:** ${p_info['Ganancia Neta $']} | **Margen Aplicado:** {p_info['Margen %']}%")
                    st.write("📋 **Desglose de materiales incluidos:**")
                    df_mats_prod = pd.DataFrame(p_info["Materiales Usados"])
                    st.dataframe(df_mats_prod[["Material", "Ancho", "Alto", "Cantidad", "Costo Calculado", "Precio Calculado"]], use_container_width=True)
                
                with col_img:
                    st.write("🖼 **Fotografía del Producto:**")
                    foto = st.file_uploader(f"Cargar Foto ({p_nombre})", type=["png", "jpg", "jpeg"], key=f"foto_{p_nombre}")
                    if foto:
                        st.image(foto, width=200)
                
                st.button(f"📥 Descargar Ficha Técnica PDF ({p_nombre})", key=f"pdf_{p_nombre}")
