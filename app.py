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
        
        /* Tarjeta de gestión técnica de materiales */
        .tarjeta-gestion {
            background-color: #fcfcfc; padding: 25px; border-radius: 15px;
            border: 2px solid #74b7d5; box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
            margin-top: 15px;
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

# Inicialización segura de datos
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

# Estado para recordar qué material se está gestionando activamente en la Opción A
if 'material_seleccionado' not in st.session_state:
    st.session_state.material_seleccionado = None

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

# Barra superior tipo pestaña
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
    # Encabezado estético con branding doble
    c_logo1, c_logo2 = st.columns([1, 1])
    with c_logo1:
        st.markdown("<p style='text-align: center; font-size: 14px; color: #aaa; margin:0;'>DEPARTAMENTO CREATIVO</p>", unsafe_allow_html=True)
        st.markdown("<h2 style='color: #e9769d; margin:0;'>🎨 ART CENTER</h2>", unsafe_allow_html=True)
    with c_logo2:
        st.markdown("<p style='text-align: center; font-size: 14px; color: #aaa; margin:0;'>SEDE PRINCIPAL</p>", unsafe_allow_html=True)
        st.markdown("<h2 style='color: #74b7d5; margin:0;'>📎 OFICENTER C.A.</h2>", unsafe_allow_html=True)
        
    st.markdown("<p class='titulo-principal' style='margin-top:20px;'>ART CENTER</p>", unsafe_allow_html=True)
    st.markdown("<p class='frase-principal'>¿Qué vamos a crear hoy?</p>", unsafe_allow_html=True)
    
    st.markdown("### 🇻🇪 Control Cambiario")
    st.session_state.tasa_bcv = st.number_input("Tasa BCV del día (Bs.)", min_value=1.0, value=float(st.session_state.tasa_bcv), step=0.10, key="input_tasa_home")
    st.divider()
    
    # Casillas del Home
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

# ==========================================
# 🧮 VISTA: 1- CREAR PRESUPUESTO
# ==========================================
elif st.session_state.menu_actual == "🧮 1- Crear Presupuesto":
    st.markdown("<h2 style='color: #e9769d;'>🧮 Crear Presupuesto de Producción</h2>", unsafe_allow_html=True)
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

                st.caption("⚙️ Valores del Insumo Seleccionado:")
                ce1, ce2 = st.columns(2)
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
                    <p style="margin:10px 0 0 0; font-size:14px; color:#8bcc60; font-weight:bold;">Ganancia Neta Real: ${ganancia_total_neta:.2f}</p>
                </div>
            """, unsafe_allow_html=True)
            
            nombre_final = st.text_input("Nombre del Producto Terminado:", key="name_final_pres")
            if st.button("💾 Guardar Producto Final", key="btn_save_prod_pres"):
                if nombre_final:
                    st.session_state.productos[nombre_final] = {
                        "Precio Venta $": round(precio_final_dolares, 2), "Ganancia Neta $": round(ganancia_total_neta, 2),
                        "Margen %": margen_creativo, "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"), "Materiales Usados": st.session_state.items_presupuesto
                    }
                    guardar_datos('productos.json', st.session_state.productos)
                    st.success(f"¡El producto '{nombre_final}' se guardó con éxito!")
                    st.session_state.items_presupuesto = []
                    st.rerun()

# ==========================================
# ➕ VISTA: 2- CREAR MATERIAL
# ==========================================
elif st.session_state.menu_actual == "➕ 2- Crear Material":
    st.markdown("<h2 style='color: #e9769d;'>➕ Registrar Nuevo Insumo / Material</h2>", unsafe_allow_html=True)
    c_n1, c_n2 = st.columns(2)
    nombre_m = c_n1.text_input("Nombre del Material:", key="n_m3")
    marca_m = c_n2.text_input("Marca (Opcional):", key="m_m3")
    
    es_pieza = st.checkbox("¿Se usa por piezas recortables en centímetros (Área)?", key="check_m3")
    tipo_m = "Pieza (Área)" if es_pieza else "Unidad (Cantidad)"
    
    ancho_m, alto_m = 1.0, 1.0
    if es_pieza:
        cx1, cx2 = st.columns(2)
        ancho_m = cx1.number_input("Ancho completo (cm)", min_value=1.0, value=50.0, key="w_m3")
        alto_m = cx2.number_input("Alto completo (cm)", min_value=1.0, value=70.0, key="h_m3")
        
    cc1, cc2 = st.columns(2)
    costo_m = cc1.number_input("Costo Proveedor ($)", min_value=0.0, step=0.01, format="%.2f", key="c_m3")
    precio_m = cc2.number_input("Precio Tienda al Público ($)", min_value=0.0, step=0.01, format="%.2f", key="p_m3")
    
    if st.button("💾 Guardar Material en Sistema", key="btn_save_m3", type="primary"):
        if nombre_m:
            st.session_state.materiales[nombre_m] = {
                "Tipo": tipo_m, "Ancho": ancho_m, "Alto": alto_m, "Costo": costo_m, "Precio": precio_m, "Marca": marca_m if marca_m else "Genérica", "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            guardar_datos('materiales.json', st.session_state.materiales)
            st.success(f"¡Material '{nombre_m}' creado con éxito!")
            st.rerun()

# ==========================================
# 🎒 VISTA: 3- VERIFICAR PANEL DE MATERIALES (OPCIÓN A CONFIGURADA)
# ==========================================
elif st.session_state.menu_actual == "🎒 3- Verificar Panel de Materiales":
    st.markdown("<h2 style='color: #e9769d;'>🎒 Panel de Control de Inventario</h2>", unsafe_allow_html=True)
    
    if not st.session_state.materiales:
        st.info("No hay materiales registrados.")
    else:
        # 1. Tabla Resumen Principal
        tabla_mats = []
        for n, d in st.session_state.materiales.items():
            porcentaje_ganancia_mat = (((d['Precio'] - d['Costo']) / d['Precio']) * 100) if d['Precio'] > 0 else 0.0
            tabla_mats.append({
                "Material": n, "Tipo": d["Tipo"], "Marca": d.get("Marca", "Genérica"),
                "Costo Base": f"${d['Costo']:.2f}", "Precio Base": f"${d['Precio']:.2f}",
                "Ganancia (%)": f"{porcentaje_ganancia_mat:.1f}%", "Última Actualización": d.get("Fecha", "Original")
            })
        
        st.dataframe(pd.DataFrame(tabla_mats), use_container_width=True)
        st.divider()
        
        # 2. IMPLEMENTACIÓN OPCIÓN A: Fila de Botones para Gestionar cada Material
        st.write("### 🔍 Acceder al Centro de Gestión Individual")
        st.write("<p style='color:#666; font-size:14px; margin-top:-10px;'>Haz clic en el botón del material que deseas analizar, verificar en qué Toppers se usa o actualizar sus costos de tienda:</p>", unsafe_allow_html=True)
        
        # Generar fila ordenada de botones dinámicos
        lista_nombres_mats = list(st.session_state.materiales.keys())
        cols_botones = st.columns(min(len(lista_nombres_mats), 6)) # Máximo 6 botones por fila visual
        
        for i, nombre_mat in enumerate(lista_nombres_mats):
            col_destino = cols_botones[i % 6]
            with col_destino:
                # Si el material está seleccionado actualmente, resaltar el botón en rosa/primario
                es_este = st.session_state.material_seleccionado == nombre_mat
                tipo_btn_mat = "primary" if es_este else "secondary"
                if st.button(f"🔎 {nombre_mat}", key=f"btn_panel_gest_{nombre_mat}", use_container_width=True, type=tipo_btn_mat):
                    st.session_state.material_seleccionado = nombre_mat
                    st.rerun()
                    
        # 3. Panel de Gestión de Información Desplegado (Solo se muestra cuando se selecciona uno)
        if st.session_state.material_seleccionado and st.session_state.material_seleccionado in st.session_state.materiales:
            mat_actual = st.session_state.material_seleccionado
            info_mat = st.session_state.materiales[mat_actual]
            
            # Cálculos financieros del Insumo
            ganancia_dolares = info_mat["Precio"] - info_mat["Costo"]
            pct_ganancia = (ganancia_dolares / info_mat["Precio"] * 100) if info_mat["Precio"] > 0 else 0.0
            
            # Buscar en qué Toppers/Diseños se utiliza este material exactamente
            productos_vinculados = []
            for prod_name, prod_detalles in st.session_state.productos.items():
                for item in prod_detalles.get("Materiales Usados", []):
                    if item["Material"] == mat_actual:
                        productos_vinculados.append(prod_name)
            
            vinculos_str = ", ".join(productos_vinculados) if productos_vinculados else "Ninguno actualmente (Insumo libre)"
            
            # Renderizado de la Tarjeta Técnica Estilizada
            st.markdown(f"""
                <div class="tarjeta-gestion">
                    <h3 style="color:#e9769d; text-align:left; margin-top:0;">📋 Resumen de Información Completa: {mat_actual}</h3>
                    <hr style="border:1px solid #74b7d5; margin-bottom:15px;"/>
                </div>
            """, unsafe_allow_html=True)
            
            # Cuadrícula de Información Técnica
            c_inf1, c_inf2, c_inf3 = st.columns(3)
            with c_inf1:
                st.markdown("##### ⚙️ Propiedades Físicas")
                st.write(f"• **Tipo de Consumo:** {info_mat['Tipo']}")
                st.write(f"• **Marca Registrada:** {info_mat.get('Marca', 'Genérica')}")
                if info_mat["Tipo"] == "Pieza (Área)":
                    st.write(f"• **Medidas Pliego:** {info_mat['Ancho']} cm x {info_mat['Alto']} cm")
                    st.write(f"• **Área Total:** {info_mat['Ancho'] * info_mat['Alto']:.1f} cm²")
            
            with c_inf2:
                st.markdown("##### 💵 Rendimiento Comercial")
                st.write(f"• **Costo Proveedor:** ${info_mat['Costo']:.2f}")
                st.write(f"• **Precio Venta Tienda:** ${info_mat['Precio']:.2f}")
                st.write(f"• **Ganancia Neta:** ${ganancia_dolares:.2f} por unidad")
                st.write(f"• **Margen Insumo:** {pct_ganancia:.1f}% de utilidad")
                
            with c_inf3:
                st.markdown("##### 📦 Historial de Uso en Art Center")
                st.write(f"• **Último cambio de costos:** {info_mat.get('Fecha', 'Original')}")
                st.write(f"• **Utilizado en los productos:** `{vinculos_str}`")
            
            st.markdown("---")
            
            # Formulario de Modificación de Costos integrado directamente en la tarjeta
            st.markdown("##### ✏️ Modificar Valores y Recalcular Automáticamente")
            c_mod1, c_mod2 = st.columns(2)
            nuevo_costo = c_mod1.number_input("Actualizar Costo Proveedor ($)", min_value=0.0, value=float(info_mat["Costo"]), format="%.2f", key="edit_c_panel")
            nuevo_precio = c_mod2.number_input("Actualizar Precio Tienda ($)", min_value=0.0, value=float(info_mat["Precio"]), format="%.2f", key="edit_p_panel")
            
            actualizar_cadena = st.checkbox(f"Recalcular automáticamente el costo y precio final de todos los Toppers que usan `{mat_actual}`", value=True, key="chk_cadena_panel")
            
            c_save1, c_save2 = st.columns([1, 4])
            with c_save1:
                if st.button("💾 Guardar Cambios", key="btn_save_cambios_panel", type="primary", use_container_width=True):
                    # Si el usuario quiere actualizar la cadena, recalculamos todos los productos guardados
                    if actualizar_cadena:
                        for p_key, p_val in st.session_state.productos.items():
                            cambiado = False
                            for item in p_val.get("Materiales Usados", []):
                                if item["Material"] == mat_actual:
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
                    
                    # Guardar datos del material propiamente dicho
                    st.session_state.materiales[mat_actual]["Costo"] = nuevo_costo
                    st.session_state.materiales[mat_actual]["Precio"] = nuevo_precio
                    st.session_state.materiales[mat_actual]["Fecha"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                    guardar_datos('materiales.json', st.session_state.materiales)
                    
                    st.success(f"¡Material '{mat_actual}' y productos derivados actualizados!")
                    st.rerun()
            with c_save2:
                if st.button("❌ Cerrar Ficha", key="btn_close_panel"):
                    st.session_state.material_seleccionado = None
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
                    if foto: st.image(foto, width=200)
                st.button(f"📥 Descargar Ficha Técnica PDF ({p_nombre})", key=f"pdf_{p_nombre}")
