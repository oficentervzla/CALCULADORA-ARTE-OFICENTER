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

# Inicializar carrito de presupuesto temporal si no existe
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
    
    st.subheader("🇻🇪 Control Cambiario")
    st.session_state.tasa_bcv = st.number_input("Tasa BCV del día (Bs.)", min_value=1.0, value=float(st.session_state.tasa_bcv), step=0.10)
    
    st.markdown("---")
    # Resumen rápido en el inicio
    c_m1, c_m2 = st.columns(2)
    c_m1.metric("Materiales en Inventario", len(st.session_state.materiales))
    c_m2.metric("Productos en Catálogo", len(st.session_state.productos))

# ==========================================
# 🧮 VISTA: 1- CREAR PRESUPUESTO
# ==========================================
elif st.session_state.menu_actual == "🧮 1- Crear Presupuesto":
    st.markdown("<h2 style='color: #e9769d;'>🧮 Calculadora de Presupuestos</h2>", unsafe_allow_html=True)
    
    if not st.session_state.materiales:
        st.warning("Primero debes registrar materiales en la pestaña '➕ 2- Crear Material' para poder presupuestar.")
    else:
        col_p1, col_p2 = st.columns([1, 1])
        
        with col_p1:
            st.markdown("### 🛒 Agregar Materiales al Diseño")
            mat_seleccionado = st.selectbox("Selecciona el material:", list(st.session_state.materiales.keys()))
            info_m = st.session_state.materiales[mat_seleccionado]
            
            # Formulario según el tipo de material escogido
            if info_m["Tipo"] == "Pieza (Área)":
                st.info(f"Este material se cuenta por área. Tamaño original: {info_m['Ancho']}x{info_m['Alto']} cm.")
                ancho_usar = st.number_input("Ancho a usar (cm)", min_value=0.1, max_value=float(info_m['Ancho']), value=1.0, step=0.1)
                alto_usar = st.number_input("Alto a usar (cm)", min_value=0.1, max_value=float(info_m['Alto']), value=1.0, step=0.1)
                
                # Calcular costo proporcional del área usada
                area_total = info_m['Ancho'] * info_m['Alto']
                area_usar = ancho_usar * alto_usar
                costo_proporcional = (info_m['Costo'] / area_total) * area_usar
                precio_proporcional = (info_m['Precio'] / area_total) * area_usar
                cantidad_items = 1.0
                descripcion_uso = f"{ancho_usar}x{alto_usar} cm"
            else:
                st.info(f"Este material se cuenta por unidades individuales.")
                cantidad_items = st.number_input("Cantidad de unidades a usar", min_value=1, step=1, value=1)
                costo_proporcional = info_m['Costo'] * cantidad_items
                precio_proporcional = info_m['Precio'] * cantidad_items
                descripcion_uso = f"{cantidad_items} und"
                
            if st.button("➕ Añadir este material al presupuesto"):
                st.session_state.carrito_presupuesto.append({
                    "Material": mat_seleccionado,
                    "Uso": descripcion_uso,
                    "Costo Parcial": round(costo_proporcional, 2),
                    "Precio Parcial": round(precio_proporcional, 2)
                })
                st.success(f"Añadido {mat_seleccionado} correctamente.")
                st.rerun()

        with col_p2:
            st.markdown("### 📋 Resumen del Diseño Actual")
            if not st.session_state.carrito_presupuesto:
                st.write("El presupuesto está vacío. Añade materiales a la izquierda.")
                total_costo_materiales = 0.0
                total_precio_materiales = 0.0
            else:
                df_carrito = pd.DataFrame(st.session_state.carrito_presupuesto)
                st.dataframe(df_carrito, use_container_width=True, hide_index=True)
                
                total_costo_materiales = df_carrito["Costo Parcial"].sum()
                total_precio_materiales = df_carrito["Precio Parcial"].sum()
                
                if st.button("🗑️ Vaciar materiales del diseño"):
                    st.session_state.carrito_presupuesto = []
                    st.rerun()
            
            st.markdown("---")
            st.markdown("### 🛠️ Mano de Obra y Nombre")
            nombre_producto = st.text_input("Nombre del Producto Final (Ej: Agenda Personalizada)", placeholder="Dale un nombre al producto...")
            costo_mano_obra = st.number_input("Costo de Mano de Obra Directa ($)", min_value=0.0, step=0.50, value=0.0)
            
            # CÁLCULOS FINALES INTERNOS
            costo_produccion_total = total_costo_materiales + costo_mano_obra
            precio_sugerido_tienda = total_precio_materiales + (costo_mano_obra * 2.0) # Margen sugerido sobre la mano de obra
            ganancia_neta = precio_sugerido_tienda - costo_produccion_total
            
            precio_bs = precio_sugerido_tienda * st.session_state.tasa_bcv
            
            st.markdown("---")
            st.markdown(f"""
                <div class='tarjeta-resultado'>
                    <h4 style='color:#4caf50; margin:0;'>💰 RESULTADO DE COSTOS</h4>
                    <p style='margin:5px 0;'>• <b>Costo de Producción:</b> ${costo_produccion_total:.2f}</p>
                    <p style='margin:5px 0; font-size:20px; color:#e9769d;'>• <b>Precio Venta Sugerido: ${precio_sugerido_tienda:.2f}</b></p>
                    <p style='margin:5px 0; font-weight:bold; color:#74b7d5;'>• Precio en Bolívares: Bs. {precio_bs:.2f}</p>
                    <p style='margin:5px 0; font-size:12px; color:gray;'>Ganancia estimada: ${ganancia_neta:.2f}</p>
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
                        "Precio_Venta": round(precio_sugerido_tienda, 2),
                        "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
                    }
                    guardar_datos('productos.json', st.session_state.productos)
                    st.session_state.carrito_presupuesto = [] # Limpiar carrito
                    st.success(f"🎉 ¡'{nombre_producto}' se ha guardado en el Catálogo de Productos Finales!")
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
    
    if not st.session_state.materiales:
        st.info("No hay materiales registrados en el inventario. Ve a la pestaña '➕ 2- Crear Material' para agregar el primero.")
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
            accion = st.radio("Acción:", ["👁️ Ver Ficha", "✏️ Editar Costos"], horizontal=True)
            
        if material_seleccionado != "-- Seleccionar --":
            info_foc = st.session_state.materiales[material_seleccionado]
            
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
                    
            elif accion == "✏️ Editar Costos":
                st.markdown(f"""
                    <div class='tarjeta-editar'>
                        <h3 style='color:#e9769d; text-align:left; margin:0;'>✏️ Formulario de Modificación: {material_seleccionado}</h3>
                    </div>
                """, unsafe_allow_html=True)
                
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
# 📜 VISTA: 4- CATÁLOGO DE PRODUCTOS FINALES
# ==========================================
elif st.session_state.menu_actual == "📜 4- Catálogo de Productos Finales":
    st.markdown("<h2 style='color: #e9769d;'>📜 Catálogo de Productos Finales</h2>", unsafe_allow_html=True)
    
    if not st.session_state.productos:
        st.info("No tienes productos guardados en el catálogo aún. Crea uno usando la pestaña '🧮 1- Crear Presupuesto'.")
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
        st.markdown("### 🗑️ Eliminar Producto del Catálogo")
        prod_eliminar = st.selectbox("Selecciona un producto si deseas sacarlo del catálogo:", ["-- Seleccionar --"] + list(st.session_state.productos.keys()))
        
        if prod_eliminar != "-- Seleccionar --":
            if st.button(f"❌ Eliminar '{prod_eliminar}' permanentemente"):
                del st.session_state.productos[prod_eliminar]
                guardar_datos('productos.json', st.session_state.productos)
                st.success(f"Producto '{prod_eliminar}' eliminado.")
                st.rerun()
