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
        
        /* Tarjetas de información y resultados */
        .tarjeta-ver {
            background-color: #f4fafc; padding: 20px; border-radius: 12px;
            border: 2px solid #74b7d5; margin-top: 15px; margin-bottom: 15px;
        }
        .tarjeta-editar {
            background-color: #fff9fb; padding: 20px; border-radius: 12px;
            border: 2px solid #e9769d; margin-top: 15px; margin-bottom: 15px;
        }
        .tarjeta-resultado {
            background-color: #f7fcf8; padding: 20px; border-radius: 12px;
            border: 2px solid #4caf50; margin-top: 15px; margin-bottom: 15px;
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
if 'carrito_presupuesto' not in st.session_state:
    st.session_state.carrito_presupuesto = []

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
            st.rerun()

st.divider()

# ==========================================
# 🏠 VISTA: MENÚ PRINCIPAL
# ==========================================
if st.session_state.menu_actual == "🏠 Menú Principal":
    st.markdown("<p class='titulo-principal'>ART CENTER</p>", unsafe_allow_html=True)
    st.markdown("<p class='frase-principal'>¿Qué vamos a crear hoy?</p>", unsafe_allow_html=True)
    
    c_m1, c_m2 = st.columns(2)
    c_m1.metric("Materiales en Inventario", len(st.session_state.materiales))
    c_m2.metric("Productos en Catálogo", len(st.session_state.productos))

# ==========================================
# 🧮 VISTA: 1- CREAR PRESUPUESTO (CORREGIDO)
# ==========================================
elif st.session_state.menu_actual == "🧮 1- Crear Presupuesto":
    st.markdown("<h2 style='color: #e9769d;'>🧮 Calculadora de Presupuestos</h2>", unsafe_allow_html=True)
    
    # Forzar recarga fresca del archivo JSON para evitar desfases
    st.session_state.materiales = cargar_datos('materiales.json')
    
    if not st.session_state.materiales:
        st.warning("Primero debes registrar materiales en la pestaña '➕ 2- Crear Material' para poder presupuestar.")
    else:
        st.session_state.tasa_bcv = st.number_input("💵 Tasa BCV para este presupuesto (Bs.)", min_value=1.0, value=float(st.session_state.tasa_bcv), step=0.10)
        st.divider()
        
        col_p1, col_p2 = st.columns([1, 1])
        
        with col_p1:
            st.markdown("### 🛒 Agregar Materiales al Diseño")
            mat_seleccionado = st.selectbox("Selecciona el material:", list(st.session_state.materiales.keys()))
            info_m = st.session_state.materiales[mat_seleccionado]
            
            st.markdown("##### ✏️ Costos Base del Material (Puedes cambiarlos para este presupuesto si deseas):")
            c_ed1, c_ed2 = st.columns(2)
            
            # CORRECCIÓN CLAVE: Usamos el nombre del material en la llave del input. 
            # Así, al cambiar de material, Streamlit se ve obligado a renderizar el nuevo costo y precio del inventario.
            costo_editado = c_ed1.number_input("Costo Proveedor ($)", min_value=0.0, value=float(info_m.get('Costo', 0.0)), step=0.01, format="%.2f", key=f"costo_{mat_seleccionado}")
            precio_editado = c_ed2.number_input("Precio Tienda ($)", min_value=0.0, value=float(info_m.get('Precio', 0.0)), step=0.01, format="%.2f", key=f"precio_{mat_seleccionado}")
            
            if info_m["Tipo"] == "Pieza (Área)":
                st.info(f"Medidas de la pieza original: {info_m['Ancho']}x{info_m['Alto']} cm.")
                ancho_usar = st.number_input("Ancho a usar (cm)", min_value=0.1, max_value=float(info_m['Ancho']), value=1.0, step=0.1)
                alto_usar = st.number_input("Alto a usar (cm)", min_value=0.1, max_value=float(info_m['Alto']), value=1.0, step=0.1)
                
                area_total = info_m['Ancho'] * info_m['Alto']
                area_usar = ancho_usar * alto_usar
                costo_proporcional = (costo_editado / area_total) * area_usar
                precio_proporcional = (precio_editado / area_total) * area_usar
                descripcion_uso = f"{ancho_usar}x{alto_usar} cm"
                detalles_calculo = {"tipo": "Pieza", "ancho_usar": ancho_usar, "alto_usar": alto_usar, "area_total": area_total}
            else:
                cantidad_items = st.number_input("Cantidad de unidades a usar", min_value=1, step=1, value=1)
                costo_proporcional = costo_editado * cantidad_items
                precio_proporcional = precio_editado * cantidad_items
                descripcion_uso = f"{cantidad_items} und"
                detalles_calculo = {"tipo": "Unidad", "cantidad": cantidad_items}
                
            if st.button("➕ Añadir este material al presupuesto"):
                st.session_state.carrito_presupuesto.append({
                    "Material": mat_seleccionado,
                    "Uso": descripcion_uso,
                    "Costo Parcial": round(costo_proporcional, 2),
                    "Precio Parcial": round(precio_proporcional, 2),
                    "Detalles_Recalculo": detalles_calculo
                })
                st.success(f"Añadido {mat_seleccionado} correctamente.")
                st.rerun()

        with col_p2:
            st.markdown("### 📋 Resumen del Diseño Actual")
            if not st.session_state.carrito_presupuesto:
                st.write("El presupuesto está vacío. Añade materiales a la izquierda.")
                total_costo_materiales = 0.0
            else:
                df_carrito = pd.DataFrame(st.session_state.carrito_presupuesto)
                st.dataframe(df_carrito[["Material", "Uso", "Costo Parcial", "Precio Parcial"]], use_container_width=True, hide_index=True)
                
                total_costo_materiales = df_carrito["Costo Parcial"].sum()
                
                if st.button("🗑️ Vaciar materiales del diseño"):
                    st.session_state.carrito_presupuesto = []
                    st.rerun()
            
            st.markdown("---")
            st.markdown("### 🛠️ Mano de Obra y Ganancia")
            nombre_producto = st.text_input("Nombre del Producto Final (Ej: Agenda Personalizada)", placeholder="Dale un nombre al producto...")
            costo_mano_obra = st.number_input("Costo de Mano de Obra Directa ($)", min_value=0.0, step=0.50, value=0.0)
            porcentaje_ganancia = st.number_input("Margen de Ganancia Deseado (%)", min_value=0.0, max_value=500.0, value=50.0, step=5.0)
            
            costo_produccion_total = total_costo_materiales + costo_mano_obra
            precio_final_venta = costo_produccion_total * (1 + (porcentaje_ganancia / 100))
            ganancia_neta = precio_final_venta - costo_produccion_total
            precio_bs = precio_final_venta * st.session_state.tasa_bcv
            
            st.markdown("---")
            st.markdown(f"""
                <div class='tarjeta-resultado'>
                    <h4 style='color:#4caf50; margin:0;'>💰 RESULTADO DE COSTOS</h4>
                    <p style='margin:5px 0;'>• <b>Costo de Producción:</b> ${costo_produccion_total:.2f}</p>
                    <p style='margin:5px 0; font-size:22px; color:#e9769d;'>• <b>Precio Final de Venta: ${precio_final_venta:.2f}</b></p>
                    <p style='margin:5px 0; font-weight:bold; color:#74b7d5;'>• Precio Final en Bolívares: Bs. {precio_bs:.2f}</p>
                    <p style='margin:5px 0; font-size:13px; color:gray;'>Tu ganancia limpia: ${ganancia_neta:.2f} ({porcentaje_ganancia}%)</p>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("💾 GUARDAR Y CREAR PRODUCTO FINAL"):
                if not nombre_producto.strip():
                    st.error("Introduce un nombre para poder registrar el producto terminado.")
                elif not st.session_state.carrito_presupuesto:
                    st.error("Debes agregar al menos un material para poder guardar el producto.")
                else:
                    st.session_state.productos[nombre_producto] = {
                        "Costo_Produccion": round(costo_produccion_total, 2),
                        "Precio_Venta": round(precio_final_venta, 2),
                        "Mano_Obra": round(costo_mano_obra, 2),
                        "Porcentaje_Ganancia": round(porcentaje_ganancia, 2),
                        "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "Receta": st.session_state.carrito_presupuesto
                    }
                    guardar_datos('productos.json', st.session_state.productos)
                    st.session_state.carrito_presupuesto = []
                    st.success(f"🎉 ¡'{nombre_producto}' se ha guardado exitosamente con su receta técnica!")
                    st.rerun()

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
# 🎒 VISTA: 3- VERIFICAR PANEL DE MATERIALES
# ==========================================
elif st.session_state.menu_actual == "🎒 3- Verificar Panel de Materiales":
    st.markdown("<h2 style='color: #e9769d;'>🎒 Panel de Control de Inventario</h2>", unsafe_allow_html=True)
    
    st.session_state.materiales = cargar_datos('materiales.json')
    st.session_state.productos = cargar_datos('productos.json')
    
    if not st.session_state.materiales:
        st.info("No hay materiales registrados en el inventario.")
    else:
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
        st.dataframe(df_materiales, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.markdown("### 🛠️ Acciones de Inventario")
        
        col_sel1, col_sel2 = st.columns([2, 1])
        with col_sel1:
            material_seleccionado = st.selectbox("Selecciona un material para interactuar:", ["-- Seleccionar --"] + list(st.session_state.materiales.keys()))
        with col_sel2:
            accion = st.radio("Acción:", ["👁️ Ver Ficha", "✏️ Editar Costos", "❌ Eliminar Material"], horizontal=True)
            
        if material_seleccionado != "-- Seleccionar --":
            info_foc = st.session_state.materiales[material_seleccionado]
            
            productos_vinculados = []
            for p_nombre, p_info in st.session_state.productos.items():
                if "Receta" in p_info:
                    for item_r in p_info["Receta"]:
                        if item_r["Material"] == material_seleccionado:
                            productos_vinculados.append(p_nombre)
                            break
            
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
                    
                    st.markdown("---")
                    st.markdown("📦 **Inclusión en Catálogo de Productos:**")
                    if productos_vinculados:
                        for prod_v in productos_vinculados:
                            st.write(f"🔹 *{prod_v}*")
                    else:
                        st.write("⚠️ *Este material no está asociado a ningún producto presupuestado actualmente.*")
                        
                with cv2:
                    st.write(f"• **Costo Unitario:** ${info_foc.get('Costo'):.2f}")
                    st.write(f"• **Precio Público:** ${info_foc.get('Precio'):.2f}")
                    st.write(f"• **Margen de Ganancia:** {info_foc.get('Ganancia_Pct')}%")
                    st.write(f"• **Último Cambio:** {info_foc.get('Fecha')}")
                    
            elif accion == "✏️ Editar Costos":
                st.markdown(f"""
                    <div class='tarjeta-editar'>
                        <h3 style='color:#e9769d; text-align:left; margin:0;'>✏️ Formulario de Modificación: {material_seleccionado}</h3>
                    </div>
                """, unsafe_allow_html=True)
                
                ce1, ce2, ce3 = st.columns(3)
                nuevo_c = ce1.number_input("Costo de Proveedor ($)", min_value=0.0, value=float(info_foc.get('Costo')), format="%.2f", key="edit_costo_val")
                nuevo_p = ce2.number_input("Precio de Tienda ($)", min_value=0.0, value=float(info_foc.get('Precio')), format="%.2f", key="edit_precio_val")
                nueva_m = ce3.text_input("Modificar Marca", value=info_foc.get('Marca', 'Genérica'), key="edit_marca_val")
                
                actualizar_global = st.checkbox("🔄 ¿Deseas actualizar automáticamente los costos en todos los productos finales que contienen este material?", value=True)
                
                if st.button("💾 Guardar Cambios e Inventario"):
                    if nuevo_p <= 0:
                        st.error("El precio debe ser mayor a 0.")
                    else:
                        nueva_ganancia = ((nuevo_p - nuevo_c) / nuevo_p * 100) if nuevo_p > 0 else 0.0
                        
                        st.session_state.materiales[material_seleccionado]["Costo"] = float(nuevo_c)
                        st.session_state.materiales[material_seleccionado]["Precio"] = float(nuevo_p)
                        st.session_state.materiales[material_seleccionado]["Marca"] = nueva_m
                        st.session_state.materiales[material_seleccionado]["Ganancia_Pct"] = round(nueva_ganancia, 1)
                        st.session_state.materiales[material_seleccionado]["Fecha"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                        
                        guardar_datos('materiales.json', st.session_state.materiales)
                        
                        if actualizar_global and productos_vinculados:
                            for p_nombre in productos_vinculados:
                                prod_data = st.session_state.productos[p_nombre]
                                nuevo_costo_materiales = 0.0
                                
                                for item_r in prod_data["Receta"]:
                                    if item_r["Material"] == material_seleccionado:
                                        detalles = item_r["Detalles_Recalculo"]
                                        if detalles["tipo"] == "Pieza":
                                            costo_prop = (float(nuevo_c) / detalles["area_total"]) * (detalles["ancho_usar"] * detalles["alto_usar"])
                                            precio_prop = (float(nuevo_p) / detalles["area_total"]) * (detalles["ancho_usar"] * detalles["alto_usar"])
                                        else:
                                            costo_prop = float(nuevo_c) * detalles["cantidad"]
                                            precio_prop = float(nuevo_p) * detalles["cantidad"]
                                            
                                        item_r["Costo Parcial"] = round(costo_prop, 2)
                                        item_r["Precio Parcial"] = round(precio_prop, 2)
                                        
                                    nuevo_costo_materiales += item_r["Costo Parcial"]
                                
                                mano_obra = prod_data.get("Mano_Obra", 0.0)
                                margen_ganancia = prod_data.get("Porcentaje_Ganancia", 50.0)
                                
                                total_costo_prod = nuevo_costo_materiales + mano_obra
                                total_precio_vent = total_costo_prod * (1 + (margen_ganancia / 100))
                                
                                st.session_state.productos[p_nombre]["Costo_Produccion"] = round(total_costo_prod, 2)
                                st.session_state.productos[p_nombre]["Precio_Venta"] = round(total_precio_vent, 2)
                                
                            guardar_datos('productos.json', st.session_state.productos)
                            st.toast(f"Sincronizados {len(productos_vinculados)} productos asociados.")
                            
                        st.success(f"¡Material '{material_seleccionado}' y productos asociados actualizados con éxito!")
                        st.rerun()

            elif accion == "❌ Eliminar Material":
                st.markdown(f"""
                    <div style='background-color: #fff5f5; padding: 20px; border-radius: 12px; border: 2px solid #ff4b4b; margin-top: 15px; margin-bottom: 15px;'>
                        <h3 style='color:#ff4b4b; text-align:left; margin:0;'>⚠️ Zona de Peligro: Eliminar '{material_seleccionado}'</h3>
                        <p style='margin-top:10px; color:#333;'>¿Estás seguro de que deseas quitar este material? Aparece en {len(productos_vinculados)} productos.</p>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"💥 Confirmar Eliminación de {material_seleccionado}", type="primary"):
                    del st.session_state.materiales[material_seleccionado]
                    guardar_datos('materiales.json', st.session_state.materiales)
                    st.success(f"El material '{material_seleccionado}' ha sido eliminado.")
                    st.rerun()

# ==========================================
# 📜 VISTA: 4- CATÁLOGO DE PRODUCTOS FINALES
# ==========================================
elif st.session_state.menu_actual == "📜 4- Catálogo de Productos Finales":
    st.markdown("<h2 style='color: #e9769d;'>📜 Catálogo de Productos Finales</h2>", unsafe_allow_html=True)
    
    st.session_state.productos = cargar_datos('productos.json')
    st.session_state.tasa_bcv = float(st.session_state.tasa_bcv)
    
    if not st.session_state.productos:
        st.info("No tienes productos guardados en el catálogo aún.")
    else:
        lista_prod = []
        for nombre_p, info_p in st.session_state.productos.items():
            precio_v = info_p.get("Precio_Venta", 0.0)
            lista_prod.append({
                "Producto Final": nombre_p,
                "Costo total ($)": info_p.get("Costo_Produccion", 0.0),
                "Precio de Venta ($)": precio_v,
                "Precio en Bs.": f"Bs. {round(precio_v * st.session_state.tasa_bcv, 2)}",
                "Fecha de Creación": info_p.get("Fecha", "No registrada")
            })
            
        df_productos = pd.DataFrame(lista_prod)
        st.dataframe(df_productos, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.markdown("### 🛠️ Acciones de Catálogo")
        
        col_ac1, col_ac2 = st.columns([2, 1])
        with col_ac1:
            prod_seleccionado = st.selectbox("Selecciona un producto para interactuar:", ["-- Seleccionar --"] + list(st.session_state.productos.keys()))
        with col_ac2:
            accion_p = st.radio("Acción:", ["👁️ Ver Detalles de Receta", "❌ Eliminar de Catálogo"], horizontal=True)
            
        if prod_seleccionado != "-- Seleccionar --":
            prod_data = st.session_state.productos[prod_seleccionado]
            
            if accion_p == "👁️ Ver Detalles de Receta":
                st.markdown(f"""
                    <div class='tarjeta-ver'>
                        <h3 style='color:#74b7d5; text-align:left; margin:0;'>📋 Estructura de Materiales: {prod_seleccionado}</h3>
                        <p style='margin: 5px 0; font-size:14px; color:gray;'>Creado el {prod_data.get('Fecha')}</p>
                    </div>
                """, unsafe_allow
