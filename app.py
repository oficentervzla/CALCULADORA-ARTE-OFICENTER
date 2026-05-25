import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# Configuración de página
st.set_page_config(page_title="Sistema Art Center", layout="wide", page_icon="🎨")

# --- ESTILOS DE MARCA (Art Center) ---
st.markdown("""
    <style>
        .stApp { background-color: #ffffff; }
        h1, h2, h3 { color: #74b7d5 !important; font-family: 'Arial', sans-serif; }
        [data-testid="stSidebar"] { background-color: #f7f9fa; border-right: 3px solid #fed80c; }
        
        .stButton>button {
            background-color: #fed80c !important; color: #000000 !important;
            font-weight: bold !important; border-radius: 12px !important; border: none !important;
        }
        .stButton>button:hover { background-color: #0bccd1 !important; color: #ffffff !important; }
        
        .tarjeta-precio {
            background-color: #f7f9fa; padding: 20px; border-radius: 15px;
            border-left: 6px solid #e9769d; box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
        }
    </style>
""", unsafe_allow_html=True)

# --- SISTEMA DE ALMACENAMIENTO DE DATOS ---
def cargar_datos(archivo, defecto):
    if os.path.exists(archivo):
        with open(archivo, 'r', encoding='utf-8') as f: return json.load(f)
    return defecto

def guardar_datos(archivo, datos):
    with open(archivo, 'w', encoding='utf-8') as f: json.dump(datos, f, ensure_ascii=False, indent=4)

# Inicialización de bases de datos
hoy = datetime.now().strftime("%Y-%m-%d %H:%M")
if 'materiales' not in st.session_state:
    st.session_state.materiales = cargar_datos('materiales.json', {
        "Cartulina Escolar": {"Tipo": "Pieza (Área)", "Ancho": 50.0, "Alto": 70.0, "Costo": 0.50, "Precio": 1.00, "Marca": "Genérica", "Fecha": hoy},
        "Silicón (Barra)": {"Tipo": "Unidad (Cantidad)", "Ancho": 1.0, "Alto": 1.0, "Costo": 0.10, "Precio": 0.25, "Marca": "Genérica", "Fecha": hoy}
    })
if 'productos' not in st.session_state:
    st.session_state.productos = cargar_datos('productos.json', {})

# --- CONFIGURACIÓN DE TASA BCV ---
st.sidebar.markdown("<h2 style='text-align: center; color: #e9769d;'>🎨 ART CENTER</h2>", unsafe_allow_html=True)
st.sidebar.markdown("### 🇻🇪 Control Cambiario")
tasa_bcv = st.sidebar.number_input("Tasa BCV del día (Bs.)", min_value=1.0, value=36.50, step=0.10)
st.sidebar.divider()

opcion = st.sidebar.radio(
    "OPCIONES PRINCIPALES:",
    ["1- Crear Presupuesto", "2- Crear Material", "3- Verificar Panel de Materiales", "4- Catálogo de Productos Finales"]
)

st.markdown(f"<h1>{opcion}</h1>", unsafe_allow_html=True)
st.divider()

# ==========================================
# 1- CREAR PRESUPUESTO (DINÁMICO SIN LÍMITE)
# ==========================================
if opcion == "1- Crear Presupuesto":
    if 'items_presupuesto' not in st.session_state:
        st.session_state.items_presupuesto = []

    col_izq, col_der = st.columns([1.3, 1])
    
    with col_izq:
        st.subheader("📋 Listado de Materiales e Insumos")
        
        # Formulario rápido para ir agregando items a la lista
        with st.container():
            c_mat, c_cant = st.columns([2, 1])
            mat_selec = c_mat.selectbox("Selecciona un material o servicio de tu inventario:", list(st.session_state.materiales.keys()))
            mat_info = st.session_state.materiales[mat_selec]
            
            # Formulario adaptativo dinámico según el tipo de material
            if mat_info["Tipo"] == "Pieza (Área)":
                cx1, cx2 = st.columns(2)
                ancho_u = cx1.number_input("Ancho a usar (cm)", min_value=0.1, value=10.0, step=1.0)
                alto_u = cx2.number_input("Alto a usar (cm)", min_value=0.1, value=10.0, step=1.0)
                cantidad_u = 1.0
                # Cálculo de área proporcional
                area_total_mat = mat_info["Ancho"] * mat_info["Alto"]
                proporcion = (ancho_u * alto_u) / area_total_mat
                costo_calculado = mat_info["Costo"] * proporcion
                precio_calculado = mat_info["Precio"] * proporcion
            else:
                cantidad_u = c_cant.number_input("Cantidad a usar:", min_value=0.1, value=1.0, step=1.0)
                ancho_u, alto_u = 1.0, 1.0
                costo_calculado = mat_info["Costo"] * cantidad_u
                precio_calculado = mat_info["Precio"] * cantidad_u

            # --- EDICIÓN AL MOMENTO (Sin ir al inventario) ---
            st.caption("⚙️ Editar valores solo para este presupuesto:")
            ce1, ce2 = st.columns(2)
            costo_momento = ce1.number_input("Costo unitario momentáneo ($)", min_value=0.0, value=float(mat_info["Costo"]), format="%.2f")
            precio_momento = ce2.number_input("Precio unitario momentáneo ($)", min_value=0.0, value=float(mat_info["Precio"]), format="%.2f")
            
            # Recalcular si el usuario editó en el acto
            if costo_momento != mat_info["Costo"] or precio_momento != mat_info["Precio"]:
                if mat_info["Tipo"] == "Pieza (Área)":
                    proporcion = (ancho_u * alto_u) / (mat_info["Ancho"] * mat_info["Alto"])
                    costo_calculado = costo_momento * proporcion
                    precio_calculado = precio_momento * proporcion
                else:
                    costo_calculado = costo_momento * cantidad_u
                    precio_calculado = precio_momento * cantidad_u

            if st.button("➕ Añadir al Listado"):
                st.session_state.items_presupuesto.append({
                    "Material": mat_selec, "Tipo": mat_info["Tipo"], "Cantidad": cantidad_u,
                    "Ancho": ancho_u, "Alto": alto_u, "Costo Individual": costo_momento, "Precio Individual": precio_momento,
                    "Costo Calculado": costo_calculado, "Precio Calculado": precio_calculado
                })
                st.success(f"Añadido: {mat_selec}")
                st.rerun()

        # Mostrar tabla del listado actual
        if st.session_state.items_presupuesto:
            st.markdown("### Insumos añadidos hasta el momento:")
            df_items = pd.DataFrame(st.session_state.items_presupuesto)
            st.dataframe(df_items[["Material", "Cantidad", "Ancho", "Alto", "Costo Calculado", "Precio Calculado"]], use_container_width=True)
            if st.button("🗑 Limpiar Lista"):
                st.session_state.items_presupuesto = []
                st.rerun()

    with col_der:
        st.subheader("📊 Resumen del Presupuesto Final")
        if st.session_state.items_presupuesto:
            total_costo_mats = sum(item["Costo Calculado"] for item in st.session_state.items_presupuesto)
            total_precio_mats = sum(item["Precio Calculado"] for item in st.session_state.items_presupuesto)
            
            margen_creativo = st.slider("Margen de Ganancia Creativa Extra (%)", min_value=0, max_value=200, value=50, step=5)
            
            # Cálculos finales
            precio_final_dolares = total_precio_mats * (1 + (margen_creativo / 100))
            precio_final_bolivares = precio_final_dolares * tasa_bcv
            
            ganancia_materiales = total_precio_mats - total_costo_mats
            ganancia_creativa_extra = precio_final_dolares - total_precio_mats
            ganancia_total_neta = ganancia_materiales + ganancia_creativa_extra

            # Tarjeta de venta
            st.markdown(f"""
                <div class="tarjeta-precio">
                    <p style="margin:0; font-size:13px; color:#555; font-weight:bold;">PRECIO AL CLIENTE</p>
                    <h1 style="margin:0; font-size:46px; color:#e9769d !important;">${precio_final_dolares:.2f}</h1>
                    <h3 style="margin:0; color:#74b7d5 !important;">Bs. {precio_final_bolivares:.2f}</h3>
                    <p style="margin:10px 0 0 0; font-size:14px; color:#8bcc60; font-weight:bold;">Ganancia Total Real: ${ganancia_total_neta:.2f} ({ganancia_total_neta * tasa_bcv:.2f} Bs.)</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Desglose ultra detallado solicitado
            with st.expander("🔎 Ver Desglose Analítico Completo", expanded=True):
                st.write(f"• **Costo Total Insumos (Proveedor):** ${total_costo_mats:.2f}")
                st.write(f"• **Precio Total Insumos (Tienda):** ${total_precio_mats:.2f}")
                st.write(f"💸 **Ganancia retenida por venta de materiales:** ${ganancia_materiales:.2f}")
                st.write(f"🎨 **Ganancia por encima (Margen Creativo {margen_creativo}%):** ${ganancia_creativa_extra:.2f}")
            
            st.divider()
            st.subheader("💾 Registrar en Catálogo")
            nombre_final = st.text_input("Nombre del Producto Terminado:", placeholder="Ej: Topper Happy Birthday Rosa")
            
            if st.button("💾 Guardar Producto Final"):
                if nombre_final:
                    st.session_state.productos[nombre_final] = {
                        "Precio Venta $": round(precio_final_dolares, 2),
                        "Ganancia Neta $": round(ganancia_total_neta, 2),
                        "Margen %": margen_creativo,
                        "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "Materiales Usados": st.session_state.items_presupuesto
                    }
                    guardar_datos('productos.json', st.session_state.productos)
                    st.success(f"¡{nombre_final} guardado con éxito en el Catálogo!")
                    st.session_state.items_presupuesto = []
                    st.rerun()
                else: st.error("Escribe un nombre para el producto terminado.")
        else:
            st.info("Agrega materiales en el listado izquierdo para generar el presupuesto.")

# ==========================================
# 2- CREAR MATERIAL
# ==========================================
elif opcion == "2- Crear Material":
    st.subheader("Formulario de Registro de Insumos")
    
    c_n1, c_n2 = st.columns(2)
    nombre_m = c_n1.text_input("Nombre del Material (Ej: Cartulina Escolar 2, Cartulina Glitter Oro)")
    marca_m = c_n2.text_input("Marca (Opcional)", placeholder="Ej: Silhouette, Genérico")
    
    es_pieza = st.checkbox("¿El material se usa por piezas recortables (área en cm)? Marcar con Check si es Sí. Dejar vacío si es por Unidad entera.")
    tipo_m = "Pieza (Área)" if es_pieza else "Unidad (Cantidad)"
    
    ancho_m, alto_m = 1.0, 1.0
    if es_pieza:
        cx1, cx2 = st.columns(2)
        ancho_m = cx1.number_input("Ancho completo del pliego (cm)", min_value=1.0, value=50.0)
        alto_m = cx2.number_input("Alto completo del pliego (cm)", min_value=1.0, value=70.0)
        
    st.divider()
    cc1, cc2 = st.columns(2)
    costo_m = cc1.number_input("Costo de Compra Proveedor ($)", min_value=0.0, step=0.01, format="%.2f")
    precio_m = cc2.number_input("Precio de Venta Tienda ($)", min_value=0.0, step=0.01, format="%.2f")
    
    if precio_m > 0:
        porcentaje_g = ((precio_m - costo_m) / precio_m) * 100
        total_m_area = ancho_m * alto_m if es_pieza else 1.0
        st.info(f"📊 **Análisis automático:** Este material genera un **{porcentaje_g:.1f}% de ganancia** por venta directa. Tamaño registrado: {total_m_area} unidades/cm².")

    if st.button("💾 Registrar Material"):
        if nombre_m:
            st.session_state.materiales[nombre_m] = {
                "Tipo": tipo_m, "Ancho": ancho_m, "Alto": alto_m, "Costo": costo_m, "Precio": precio_m, "Marca": marca_m if marca_m else "Genérica", "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            guardar_datos('materiales.json', st.session_state.materiales)
            st.success(f"Material '{nombre_m}' guardado permanentemente en el sistema.")
        else: st.error("Ingresa el nombre del material.")

# ==========================================
# 3- VERIFICAR PANEL DE MATERIALES
# ==========================================
elif opcion == "3- Verificar Panel de Materiales":
    st.subheader("Inventario de Insumos Activos e Historial de Usos")
    
    # Renderizar la lista
    tabla_mats = []
    for n, d in st.session_state.materiales.items():
        # Buscar en qué productos finales se usa este material
        usado_en = []
        for prod, p_info in st.session_state.productos.items():
            for item in p_info.get("Materiales Usados", []):
                if item["Material"] == n:
                    usado_en.append(prod)
        
        usados_str = ", ".join(usado_en) if usado_en else "Ninguno (Sin asignar)"
        
        tabla_mats.append({
            "Material": n, "Tipo": d["Tipo"], "Marca": d.get("Marca", "Genérica"),
            "Costo $": f"${d['Costo']:.2f}", "Precio $": f"${d['Precio']:.2f}",
            "Última Actualización": d.get("Fecha", "Original"),
            "Utilizado en:": usados_str
        })
    
    st.dataframe(pd.DataFrame(tabla_mats), use_container_width=True)
    
    st.divider()
    st.subheader("⚙️ Editar Material Existente")
    mat_a_editar = st.selectbox("Selecciona qué material deseas modificar:", list(st.session_state.materiales.keys()))
    d_ed = st.session_state.materiales[mat_a_editar]
    
    c_ed1, c_ed2 = st.columns(2)
    nuevo_c = c_ed1.number_input("Modificar Costo ($)", min_value=0.0, value=float(d_ed["Costo"]), format="%.2f")
    nuevo_p = c_ed2.number_input("Modificar Precio ($)", min_value=0.0, value=float(d_ed["Precio"]), format="%.2f")
    
    # --- CHECK DE ACTUALIZACIÓN INTELIGENTE ---
    actualizar_global = st.checkbox("¿Deseas actualizar el costo/precio automáticamente en TODOS tus productos finales guardados que contengan este material?")
    
    if st.button("💾 Guardar Cambios"):
        # Si se marca la actualización global, se recalculan los Toppers en cascada
        if actualizar_global:
            for prod, p_info in st.session_state.productos.items():
                modificado = False
                for item in p_info.get("Materiales Usados", []):
                    if item["Material"] == mat_a_editar:
                        # Sacar proporción o cantidad vieja
                        if d_ed["Tipo"] == "Pieza (Área)":
                            area_tot = d_ed["Ancho"] * d_ed["Alto"]
                            prop = (item["Ancho"] * item["Alto"]) / area_tot
                            item["Costo Calculado"] = nuevo_c * prop
                            item["Precio Calculado"] = nuevo_p * prop
                        else:
                            item["Costo Calculado"] = nuevo_c * item["Cantidad"]
                            item["Precio Calculado"] = nuevo_p * item["Cantidad"]
                        modificado = True
                
                if modificado:
                    # Recalcular totales del producto final de forma automática
                    nuevo_tot_costo = sum(i["Costo Calculado"] for i in p_info["Materiales Usados"])
                    nuevo_tot_precio = sum(i["Precio Calculado"] for i in p_info["Materiales Usados"])
                    p_info["Precio Venta $"] = round(nuevo_tot_precio * (1 + (p_info["Margen %"] / 100)), 2)
                    p_info["Ganancia Neta $"] = round((p_info["Precio Venta $"] - (nuevo_tot_precio + (p_info["Precio Venta $"] - nuevo_tot_precio))), 2) # recalculado simple
                    p_info["Fecha"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            guardar_datos('productos.json', st.session_state.productos)
            st.info("¡Se actualizaron todos los productos vinculados!")

        # Guardar en el propio material
        st.session_state.materiales[mat_a_editar]["Costo"] = nuevo_c
        st.session_state.materiales[mat_a_editar]["Precio"] = nuevo_p
        st.session_state.materiales[mat_a_editar]["Fecha"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        guardar_datos('materiales.json', st.session_state.materiales)
        
        st.success("¡Material modificado con éxito!")
        st.rerun()

# ==========================================
# 4- CATÁLOGO DE PRODUCTOS FINALES
# ==========================================
elif opcion == "4- Catálogo de Productos Finales":
    st.subheader("Catálogo de Diseños Registrados")
    
    if not st.session_state.productos:
        st.warning("No hay productos finales guardados en el catálogo aún.")
    else:
        for p_nombre, p_info in st.session_state.productos.items():
            with st.expander(f"📦 {p_nombre} | Venta: ${p_info['Precio Venta $']} | Tasa Bs: {p_info['Precio Venta $']*tasa_bcv:.2f} Bs. (Última actualización: {p_info['Fecha']})"):
                
                col_info, col_img = st.columns([2, 1])
                
                with col_info:
                    st.markdown(f"**Ganancia Neta Calculada:** ${p_info['Ganancia Neta $']} | **Margen de ganancia aplicada:** {p_info['Margen %']}%")
                    st.write("📋 **Desglose de materiales que componen este producto:**")
                    df_mats_prod = pd.DataFrame(p_info["Materiales Usados"])
                    st.dataframe(df_mats_prod[["Material", "Ancho", "Alto", "Cantidad", "Costo Calculado", "Precio Calculado"]], use_container_width=True)
                
                with col_img:
                    # --- CARGA DE FOTO PARA EL TOPPER ---
                    st.write("🖼 **Fotografía del Producto:**")
                    foto = st.file_uploader(f"Subir foto para {p_nombre}", type=["png", "jpg", "jpeg"], key=f"foto_{p_nombre}")
                    if foto:
                        st.image(foto, width=200)
                
                # Botón de simulación para PDF informativo
                st.button(f"📥 Descargar Ficha Técnica PDF ({p_nombre})", key=f"pdf_{p_nombre}")
