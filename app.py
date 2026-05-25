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
        
        /* Estilos para el título y subtítulo principal */
        .titulo-principal { color: #e9769d !important; font-size: 50px; font-weight: bold; margin-bottom: 5px; }
        .frase-principal { color: #74b7d5 !important; font-size: 28px; font-style: italic; font-weight: bold; margin-bottom: 30px; }
        
        /* Botones de las pestañas superiores (Barra de opciones arriba) */
        button[data-baseweb="tab"] {
            font-size: 16px !important;
            font-weight: bold !important;
            color: #555555 !important;
            padding: 10px 20px !important;
        }
        button[aria-selected="true"] {
            color: #e9769d !important;
            border-bottom-color: #fed80c !important;
        }
        
        /* Botones de acción generales (Guardar, añadir, etc.) */
        .stButton>button {
            background-color: #fed80c !important; color: #000000 !important;
            font-weight: bold !important; border-radius: 12px !important; border: none !important;
            padding: 10px 24px !important;
            display: block; margin: 0 auto;
        }
        .stButton>button:hover { background-color: #0bccd1 !important; color: #ffffff !important; }
        
        /* Tarjeta de presupuesto final destacada */
        .tarjeta-precio {
            background-color: #f7f9fa; padding: 20px; border-radius: 15px;
            border-left: 6px solid #e9769d; box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
            text-align: center;
        }
        
        /* Bloques/Casillas de la Página de Inicio */
        .casilla-inicio {
            background-color: #f7f9fa;
            border: 2px solid #fed80c;
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            box-shadow: 0px 4px 8px rgba(0,0,0,0.05);
            margin-bottom: 20px;
            height: 180px;
        }
    </style>
""", unsafe_allow_html=True)

# --- SISTEMA DE ALMACENAMIENTO DE DATOS ---
def cargar_datos(archivo, tipo_esperado, defecto):
    if os.path.exists(archivo):
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                if type(datos) == tipo_esperado:
                    return datos
        except:
            pass
    return defecto

def guardar_datos(archivo, datos):
    with open(archivo, 'w', encoding='utf-8') as f: 
        json.dump(datos, f, ensure_ascii=False, indent=4)

hoy = datetime.now().strftime("%Y-%m-%d %H:%M")

if 'materiales' not in st.session_state:
    st.session_state.materiales = cargar_datos('materiales.json', dict, {
        "Cartulina Escolar": {"Tipo": "Pieza (Área)", "Ancho": 50.0, "Alto": 70.0, "Costo": 0.50, "Precio": 1.00, "Marca": "Genérica", "Fecha": hoy},
        "Silicón (Barra)": {"Tipo": "Unidad (Cantidad)", "Ancho": 1.0, "Alto": 1.0, "Costo": 0.10, "Precio": 0.25, "Marca": "Genérica", "Fecha": hoy}
    })

if 'productos' not in st.session_state:
    st.session_state.productos = cargar_datos('productos.json', dict, {})

# Inicializar la sección activa en el sistema si el usuario hace clic desde las casillas de inicio
if 'pes_activa' not in st.session_state:
    st.session_state.pes_activa = 0

# --- BARRA DE OPCIONES SUPERIOR (Se mantiene fija arriba en cada desglose) ---
opciones_menu = [
    "🏠 Menú Principal", 
    "🧮 1- Crear Presupuesto", 
    "➕ 2- Crear Material", 
    "🎒 3- Verificar Panel de Materiales", 
    "📜 4- Catálogo de Productos Finales"
]

# Control de navegación por pestañas superiores
pes1, pes2, pes3, pes4, pes5 = st.tabs(opciones_menu)

# ==========================================
# 🏠 OPCIÓN: MENÚ PRINCIPAL (PÁGINA DE BIENVENIDA)
# ==========================================
with pes1:
    # Logo y Frase de Bienvenida Principal
    st.markdown("<p class='titulo-principal'>ART CENTER</p>", unsafe_allow_html=True)
    st.markdown("<p class='frase-principal'>¿Qué vamos a crear hoy?</p>", unsafe_allow_html=True)
    
    st.markdown("<p style='text-align: center; font-weight: bold; color: #555;'>Selecciona una de las opciones principales para comenzar:</p>", unsafe_allow_html=True)
    st.divider()
    
    # Control de Tasa BCV integrada en el menú principal de forma cómoda
    st.markdown("### 🇻🇪 Control Cambiario")
    tasa_bcv = st.number_input("Tasa BCV del día (Bs.)", min_value=1.0, value=36.50, step=0.10, key="tasa_principal")
    st.divider()
    
    # Casillas del menú con las Opciones Principales en columnas
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown("""
            <div class='casilla-inicio'>
                <h3 style='color: #74b7d5;'>🧮 Presupuesto</h3>
                <p style='font-size: 13px; color: #666;'>Calcula costos, precios de venta y desglosa tus ganancias al instante.</p>
            </div>
        """, unsafe_allow_html=True)
        st.caption("Usa la pestaña superior **'🧮 1- Crear Presupuesto'** para ingresar.")
        
    with c2:
        st.markdown("""
            <div class='casilla-inicio'>
                <h3 style='color: #74b7d5;'>➕ Crear Material</h3>
                <p style='font-size: 13px; color: #666;'>Registra nuevos insumos con sus medidas, marcas y porcentaje de ganancia.</p>
            </div>
        """, unsafe_allow_html=True)
        st.caption("Usa la pestaña superior **'➕ 2- Crear Material'** para ingresar.")
        
    with c3:
        st.markdown("""
            <div class='casilla-inicio'>
                <h3 style='color: #74b7d5;'>🎒 Panel Materiales</h3>
                <p style='font-size: 13px; color: #666;'>Mira tu inventario, edita precios en masa y revisa en qué toppers se usan.</p>
            </div>
        """, unsafe_allow_html=True)
        st.caption("Usa la pestaña superior **'🎒 3- Verificar Panel'** para ingresar.")
        
    with c4:
        st.markdown("""
            <div class='casilla-inicio'>
                <h3 style='color: #74b7d5;'>📜 Catálogo Final</h3>
                <p style='font-size: 13px; color: #666;'>Revisa tus productos listos, añade fotos y gestiona cantidades guardadas.</p>
            </div>
        """, unsafe_allow_html=True)
        st.caption("Usa la pestaña superior **'📜 4- Catálogo Final'** para ingresar.")

    st.divider()
    st.markdown("<p style='text-align: center; font-size: 12px; color: #aaa;'>Una solución desarrollada para Oficenter C.A.</p>", unsafe_allow_html=True)

# Recuperar tasa para las siguientes pestañas
if 'tasa_principal' in st.session_state:
    tasa_bcv = st.session_state.tasa_principal
else:
    tasa_bcv = 36.50

# ==========================================
# 🧮 1- CREAR PRESUPUESTO
# ==========================================
with pes2:
    st.markdown("<h2 style='color: #e9769d;'>🧮 Crear Presupuesto de Producción</h2>", unsafe_allow_html=True)
    if 'items_presupuesto' not in st.session_state:
        st.session_state.items_presupuesto = []

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
                    area_total_mat = mat_info["Ancho"] * mat_info["Alto"]
                    proporcion = (ancho_u * alto_u) / area_total_mat
                    costo_calculado = mat_info["Costo"] * proporcion
                    precio_calculado = mat_info["Precio"] * proporcion
                else:
                    cantidad_u = c_cant.number_input("Cantidad a usar:", min_value=0.1, value=1.0, step=1.0, key="cant_pres")
                    ancho_u, alto_u = 1.0, 1.0
                    costo_calculado = mat_info["Costo"] * cantidad_u
                    precio_calculado = mat_info["Precio"] * cantidad_u

                st.caption("⚙️ Editar valores al momento (Solo para este presupuesto):")
                ce1, ce2 = st.columns(2)
                costo_momento = ce1.number_input("Costo unitario momentáneo ($)", min_value=0.0, value=float(mat_info["Costo"]), format="%.2f", key="c_mom")
                precio_momento = ce2.number_input("Precio de venta momentáneo ($)", min_value=0.0, value=float(mat_info["Precio"]), format="%.2f", key="p_mom")
                
                if costo_momento != mat_info["Costo"] or precio_momento != mat_info["Precio"]:
                    if mat_info["Tipo"] == "Pieza (Área)":
                        proporcion = (ancho_u * alto_u) / (mat_info["Ancho"] * mat_info["Alto"])
                        costo_calculado = costo_momento * proporcion
                        precio_calculado = precio_momento * proporcion
                    else:
                        costo_calculado = costo_momento * cantidad_u
                        precio_calculado = precio_momento * cantidad_u

                if st.button("➕ Añadir Insumo al Listado", key="btn_add_pres"):
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
            precio_final_bolivares = precio_final_dolares * tasa_bcv
            
            ganancia_materiales = total_precio_mats - total_costo_mats
            ganancia_creativa_extra = precio_final_dolares - total_precio_mats
            ganancia_total_neta = ganancia_materiales + ganancia_creativa_extra

            st.markdown(f"""
                <div class="tarjeta-precio">
                    <p style="margin:0; font-size:13px; color:#555; font-weight:bold;">PRECIO DE VENTA FINAL</p>
                    <h1 style="margin:0; font-size:46px; color:#e9769d !important;">${precio_final_dolares:.2f}</h1>
                    <h3 style="margin:0; color:#74b7d5 !important;">Bs. {precio_final_bolivares:.2f}</h3>
                    <p style="margin:10px 0 0 0; font-size:14px; color:#8bcc60; font-weight:bold;">Ganancia Neta Real: ${ganancia_total_neta:.2f} ({(ganancia_total_neta * tasa_bcv):.2f} Bs.)</p>
                </div>
            """, unsafe_allow_html=True)
            
            with st.expander("🔎 Ver Desglose Analítico Solicitado", expanded=True):
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
# 2- CREAR MATERIAL
# ==========================================
with pes3:
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

    if st.button("💾 Guardar Material en Sistema", key="btn_save_m3"):
        if nombre_m:
            st.session_state.materiales[nombre_m] = {
                "Tipo": tipo_m, "Ancho": ancho_m, "Alto": alto_m, "Costo": costo_m, "Precio": precio_m, "Marca": marca_m if marca_m else "Genérica", "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            guardar_datos('materiales.json', st.session_state.materiales)
            st.success(f"¡Material '{nombre_m}' creado con éxito!")
            st.rerun()
        else: st.error("El nombre es obligatorio.")

# ==========================================
# 3- VERIFICAR PANEL DE MATERIALES
# ==========================================
with pes4:
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
            
            tabla_mats.append({
                "Material": n, "Tipo": d["Tipo"], "Marca": d.get("Marca", "Genérica"),
                "Costo Base": f"${d['Costo']:.2f}", "Precio Base": f"${d['Precio']:.2f}",
                "Última Actualización": d.get("Fecha", "Original"),
                "Utilizado en:": usados_str
            })
        
        st.dataframe(pd.DataFrame(tabla_mats), use_container_width=True)
        
        st.divider()
        st.subheader("⚙️ Modificación de Valores e Impacto en Cascada")
        mat_a_editar = st.selectbox("Selecciona qué material deseas editar:", list(st.session_state.materiales.keys()), key="sel_m4")
        d_ed = st.session_state.materiales[mat_a_editar]
        
        c_ed1, c_ed2 = st.columns(2)
        nuevo_c = c_ed1.number_input("Costo Proveedor ($)", min_value=0.0, value=float(d_ed["Costo"]), format="%.2f", key="nc_m4")
        nuevo_p = c_ed2.number_input("Precio Tienda ($)", min_value=0.0, value=float(d_ed["Precio"]), format="%.2f", key="np_m4")
        
        actualizar_global = st.checkbox("¿Deseas recalcular automáticamente TODOS los productos finales guardados que usen este material?", key="check_m4")
        
        if st.button("💾 Aplicar Cambios Globales", key="btn_save_m4"):
            if actualizar_global:
                for prod, p_info in st.session_state.productos.items():
                    modificado = False
                    for item in p_info.get("Materiales Usados", []):
                        if item["Material"] == mat_a_editar:
                            if d_ed["Tipo"] == "Pieza (Área)":
                                area_tot = d_ed["Ancho"] * d_ed["Alto"]
                                prop = (item["Ancho"] * item["Alto"]) / area_tot
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
# 4- CATÁLOGO DE PRODUCTOS FINALES
# ==========================================
with pes5:
    st.markdown("<h2 style='color: #e9769d;'>📜 Catálogo de Productos Finales Guardados</h2>", unsafe_allow_html=True)
    
    if not st.session_state.productos:
        st.warning("No hay productos guardados en el catálogo.")
    else:
        for p_nombre, p_info in list(st.session_state.productos.items()):
            with st.expand_viewer if hasattr(st, "expand_viewer") else st.expander(f"📦 {p_nombre} | Venta: ${p_info['Precio Venta $']} | Cambio: {(p_info['Precio Venta $'] * tasa_bcv):.2f} Bs. (Actualizado: {p_info['Fecha']})"):
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
