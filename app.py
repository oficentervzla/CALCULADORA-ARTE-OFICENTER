import streamlit as st
import requests
import json
import base64
from datetime import datetime

# 1. CONFIGURACIÓN DE LA PÁGINA Y ESTILOS INYECTADOS
st.set_page_config(page_title="Sistema Art Center", layout="wide")

st.markdown("""
    <style>
    /* Estilos globales y fuentes */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background-color: #ffffff;
    }
    
    /* Encabezados personalizados */
    .titulo-principal {
        color: #e9769d;
        font-weight: 600;
        font-size: 42px;
        margin-bottom: 5px;
    }
    
    .subtitulo-azul {
        color: #74b7d5;
        font-style: italic;
        font-size: 18px;
        margin-bottom: 25px;
    }
    
    /* Tarjetas del contenedor de Inventario */
    .tarjeta-ver {
        background-color: #f0f7f4;
        border-left: 5px solid #66c2a5;
        padding: 15px;
        border-radius: 4px;
        margin-bottom: 20px;
    }
    
    .tarjeta-editar {
        background-color: #fffdf0;
        border-left: 5px solid #ffd92f;
        padding: 15px;
        border-radius: 4px;
        margin-bottom: 20px;
    }
    
    .tarjeta-resultado {
        background-color: #fbf0f3;
        border: 1px solid #e9769d;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    
    /* Ajustes de espaciado para tablas y botones */
    .stButton>button {
        border-radius: 6px;
    }
    </style>
""", unsafe_allow_html=True) # <-- FIJO: Corrección para evitar error de pantalla rosa

# 2. CONFIGURACIÓN DE CREDENCIALES (GITHUB SECRETS)
try:
    GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
    GITHUB_REPO = st.secrets["GITHUB_REPO"]
except Exception:
    st.error("Faltan las credenciales secretas de GitHub en la configuración de Streamlit Cloud.")
    st.stop()

GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/database.json"

# 3. FUNCIONES DE PERSISTENCIA (CONEXIÓN CON GITHUB)
@st.cache_data(ttl=60)
def cargar_base_datos():
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(GITHUB_API_URL, headers=headers)
    if response.status_code == 200:
        datos_json = response.json()
        contenido_b64 = datos_json["content"]
        contenido_decodificado = base64.b64decode(contenido_b64).decode('utf-8')
        base_datos = json.loads(contenido_decodificado)
        sha = datos_json["sha"]
        return base_datos, sha
    else:
        estructura_vacia = {"materiales": {}, "productos": {}}
        return estructura_vacia, None

def guardar_base_datos(datos, sha):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    contenido_bytes = json.dumps(datos, indent=4).encode('utf-8')
    contenido_b64 = base64.b64encode(contenido_bytes).decode('utf-8')
    
    payload = {
        "message": "Actualización automática de base de datos (Calculadora)",
        "content": contenido_b64
    }
    if sha:
        payload["sha"] = sha
        
    response = requests.put(GITHUB_API_URL, headers=headers, json=payload)
    if response.status_code in [200, 201]:
        st.cache_data.clear()
        return True
    else:
        st.error(f"Error al guardar datos en GitHub: {response.text}")
        return False

# Inicializar Base de Datos en Sesión
if "db" not in st.session_state:
    base_datos, sha = cargar_base_datos()
    st.session_state.db = base_datos
    st.session_state.sha = sha

# 4. MANEJO DE NAVEGACIÓN
if "menu_actual" not in st.session_state:
    st.session_state.menu_actual = "Inicio"

col_nav1, col_nav2, col_nav3, col_nav4, col_nav5 = st.columns(5)

with col_nav1:
    if st.button("🏡 Menú Principal", use_container_width=True, type="primary" if st.session_state.menu_actual == "Inicio" else "secondary"):
        st.session_state.menu_actual = "Inicio"
        st.rerun()
with col_nav2:
    if st.button("🧮 1- Crear Presupuesto", use_container_width=True, type="primary" if st.session_state.menu_actual == "Presupuestador" else "secondary"):
        st.session_state.menu_actual = "Presupuestador"
        st.rerun()
with col_nav3:
    if st.button("➕ 2- Crear Material", use_container_width=True, type="primary" if st.session_state.menu_actual == "NuevoMaterial" else "secondary"):
        st.session_state.menu_actual = "NuevoMaterial"
        st.rerun()
with col_nav4:
    if st.button("🎒 3- Verificar Panel de Materiales", use_container_width=True, type="primary" if st.session_state.menu_actual == "Inventario" else "secondary"):
        st.session_state.menu_actual = "Inventario"
        st.rerun()
with col_nav5:
    if st.button("📜 4- Catálogo de Productos Finales", use_container_width=True, type="primary" if st.session_state.menu_actual == "Catalogo" else "secondary"):
        st.session_state.menu_actual = "Catalogo"
        st.rerun()

st.markdown("---")

# ==========================================
# PESTAÑA: MENÚ PRINCIPAL (INICIO)
# ==========================================
if st.session_state.menu_actual == "Inicio":
    st.markdown('<div class="titulo-principal">ART CENTER</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitulo-azul">¿Qué vamos a crear hoy?</div>', unsafe_allow_html=True)
    
    num_materiales = len(st.session_state.db.get("materiales", {}))
    num_productos = len(st.session_state.db.get("productos", {}))
    
    col_inf1, col_inf2 = st.columns(2)
    with col_inf1:
        st.metric(label="Materiales en Inventario", value=num_materiales)
    with col_inf2:
        st.metric(label="Productos en Catálogo", value=num_productos)
        
    st.success("🟢 Conexión con la base de datos de GitHub activada. Tu progreso se guarda de forma permanente.")

# ==========================================
# PESTAÑA 1: CREAR PRESUPUESTO
# ==========================================
elif st.session_state.menu_actual == "Presupuestador":
    st.markdown('<div class="titulo-principal">🧮 Creador de Presupuestos Inteligente</div>', unsafe_allow_html=True)
    
    materiales_dict = st.session_state.db.get("materiales", {})
    if not materiales_dict:
        st.warning("No puedes presupuestar porque no tienes materiales registrados en la pestaña '2- Crear Material'.")
        st.stop()
        
    if "carrito_materiales" not in st.session_state:
        st.session_state.carrito_materiales = []
        
    col_p1, col_p2 = st.columns([1.2, 1])
    
    with col_p1:
        st.subheader("🛒 Selección de Materiales para la Receta")
        
        lista_nombres_mat = sorted(list(materiales_dict.keys()))
        mat_seleccionado = st.selectbox("Selecciona un material:", lista_nombres_mat)
        
        info_mat = materiales_dict[mat_seleccionado]
        tipo_unidad = info_mat.get("tipo", "Unidad (Entero)")
        
        if tipo_unidad == "Pieza (Área)":
            st.info(f"Material por Área. Medidas originales: {info_mat['ancho']}cm x {info_mat['alto']}cm. Costo: ${info_mat['costo']:.2f}")
            c_dim1, c_dim2 = st.columns(2)
            with c_dim1:
                ancho_usar = st.number_input("Ancho a usar (cm):", min_value=0.1, value=10.0, step=1.0)
            with c_dim2:
                alto_usar = st.number_input("Alto a usar (cm):", min_value=0.1, value=10.0, step=1.0)
            cantidad_unidades = 1
        else:
            st.info(f"Material por Unidades enteras. Costo unitario: ${info_mat['costo']:.2f}")
            cantidad_unidades = st.number_input("Cantidad de unidades (und):", min_value=1, value=1, step=1)
            ancho_usar, alto_usar = 0.0, 0.0
            
        if st.button("➕ Añadir Material al Carrito", use_container_width=True):
            if tipo_unidad == "Pieza (Área)":
                area_total = info_mat['ancho'] * info_mat['alto']
                area_solicitada = ancho_usar * alto_usar
                costo_calculado = (info_mat['costo'] / area_total) * area_solicitada
                descripcion_tabla = f"{ancho_usar}x{alto_usar} cm"
            else:
                costo_calculado = info_mat['costo'] * cantidad_unidades
                descripcion_tabla = f"{cantidad_unidades} und"
                
            st.session_state.carrito_materiales.append({
                "nombre": mat_seleccionado,
                "tipo": tipo_unidad,
                "descripcion": descripcion_tabla,
                "ancho": ancho_usar,
                "alto": alto_usar,
                "cantidad": cantidad_unidades,
                "costo_parcial": costo_calculado
            })
            st.toast(f"{mat_seleccionado} agregado.")
            st.rerun()

        if st.session_state.carrito_materiales:
            st.markdown("#### Desglose Actual de Materiales:")
            total_materiales = 0.0
            for idx, item in enumerate(st.session_state.carrito_materiales):
                total_materiales += item["costo_parcial"]
                c_tab1, c_tab2, c_tab3, c_tab4 = st.columns([2, 1, 1, 0.5])
                with c_tab1:
                    st.write(f"**{item['nombre']}** ({item['tipo']})")
                with c_tab2:
                    st.write(item['descripcion'])
                with c_tab3:
                    st.write(f"${item['costo_parcial']:.2f}")
                with c_tab4:
                    if st.button("❌", key=f"del_cart_{idx}"):
                        st.session_state.carrito_materiales.pop(idx)
                        st.rerun()
            st.markdown(f"**Costo Total de Materiales Puros:** `${total_materiales:.2f}`")
        else:
            st.write("El carrito de materiales está vacío.")
            total_materiales = 0.0

    with col_p2:
        st.subheader("📊 Datos del Producto Final y Márgenes")
        
        nombre_producto_nuevo = st.text_input("Nombre del producto a cotizar (Ej: Libreta Glitter V2):").strip()
        tasa_bcv = st.number_input("Tasa BCV del Día (Bs/$):", min_value=1.0, value=36.50, step=0.1)
        mano_obra = st.number_input("Mano de Obra Directa ($):", min_value=0.0, value=2.0, step=0.5)
        
        margen_ganancia = st.number_input("Margen de Ganancia Deseado (%):", min_value=0, value=50, step=5)
        costos_indirectos_porcentaje = st.number_input("Costos Indirectos / Gastos Operativos (%):", min_value=0, value=10, step=5)
        factor_desperdicio = st.number_input("Margen de Desperdicio en Materiales por Área (%):", min_value=0, value=10, step=2)

        costo_materiales_con_desperdicio = 0.0
        for item in st.session_state.carrito_materiales:
            if item["tipo"] == "Pieza (Área)":
                costo_materiales_con_desperdicio += item["costo_parcial"] * (1 + (factor_desperdicio / 100))
            else:
                costo_materiales_con_desperdicio += item["costo_parcial"]

        costo_producción_total = costo_materiales_con_desperdicio + mano_obra
        monto_indirectos = costo_producción_total * (costos_indirectos_porcentaje / 100)
        costo_base_con_indirectos = costo_producción_total + monto_indirectos
        
        if margen_ganancia < 100:
            precio_venta_usd = costo_base_con_indirectos / (1 - (margen_ganancia / 100))
        else:
            precio_venta_usd = costo_base_con_indirectos * 2
            
        precio_venta_bs = precio_venta_usd * tasa_bcv
        
        st.markdown('<div class="tarjeta-resultado">', unsafe_allow_html=True)
        st.markdown("### 💎 Resumen Económico Resultante")
        st.markdown(f"**Costo de Fabricación Neto:** `${costo_producción_total:.2f} USD` (Con Desperdicios)")
        st.markdown(f"**Costos Indirectos Aplicados:** `${monto_indirectos:.2f} USD`")
        st.markdown(f"## Precio Sugerido Venta: `${precio_venta_usd:.2f} USD`")
        st.markdown(f"## Precio en Bolívares: `Bs. {precio_venta_bs:.2f}`")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("💾 Guardar y Registrar este Producto en el Catálogo", use_container_width=True, type="primary"):
            if not nombre_producto_nuevo:
                st.error("Por favor, ingresa un nombre válido para el producto antes de guardar.")
            elif not st.session_state.carrito_materiales:
                st.error("El producto debe tener al menos un material en su receta.")
            else:
                nuevo_prod_obj = {
                    "costo_produccion": costo_producción_total,
                    "precio_usd": precio_venta_usd,
                    "precio_bs": precio_venta_bs,
                    "tasa_bcv": tasa_bcv,
                    "mano_obra": mano_obra,
                    "margen_ganancia": margen_ganancia,
                    "costos_indirectos_porcentaje": costos_indirectos_porcentaje,
                    "factor_desperdicio": factor_desperdicio,
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "receta": st.session_state.carrito_materiales.copy()
                }
                
                st.session_state.db["productos"][nombre_producto_nuevo] = nuevo_prod_obj
                
                if guardar_base_datos(st.session_state.db, st.session_state.sha):
                    st.success(f"¡Excelente! '{nombre_producto_nuevo}' se ha guardado.")
                    st.session_state.carrito_materiales = []
                    base_datos, sha = cargar_base_datos()
                    st.session_state.db = base_datos
                    st.session_state.sha = sha
                    st.rerun()

# ==========================================
# PESTAÑA 2: CREAR MATERIAL (ESTRUCTURA ORIGINAL RESTAURADA)
# ==========================================
elif st.session_state.menu_actual == "NuevoMaterial":
    st.markdown('<div class="titulo-principal">➕ Registro de Materiales Base</div>', unsafe_allow_html=True)
    st.write("Registra la materia prima que compras para tus producciones creativas.")
    
    with st.form("form_nuevo_material"):
        nombre_mat = st.text_input("Nombre único del Material (Ej: Cartón Piedra de 2mm, Vinil Autoadhesivo):").strip()
        tipo_unidad = st.radio("Método de fraccionamiento o cálculo:", ["Unidad (Entero)", "Pieza (Área)"])
        
        costo_base = st.number_input("Costo de compra en dólares ($):", min_value=0.01, value=1.0, step=0.1)
        
        # Parámetros condicionales de área restaurados exactamente a tu lógica anterior
        st.markdown("#### Dimensiones de la lámina / pieza original completa (Solo si aplica para área):")
        ancho_orig = st.number_input("Ancho Total (cm):", min_value=0.0, value=100.0, step=5.0)
        alto_orig = st.number_input("Alto Total (cm):", min_value=0.0, value=100.0, step=5.0)
            
        btn_crear_mat = st.form_submit_button("💾 Registrar y Sincronizar Material")
        
        if btn_crear_mat:
            if not nombre_mat:
                st.error("Debes definir un nombre para el material.")
            else:
                # Asegurar guardar 0 si seleccionaron Unidad Entera para respetar la estructura original
                val_ancho = ancho_orig if tipo_unidad == "Pieza (Área)" else 0.0
                val_alto = alto_orig if tipo_unidad == "Pieza (Área)" else 0.0
                
                material_data = {
                    "tipo": tipo_unidad,
                    "costo": costo_base,
                    "ancho": val_ancho,
                    "alto": val_alto
                }
                
                st.session_state.db["materiales"][nombre_mat] = material_data
                
                if guardar_base_datos(st.session_state.db, st.session_state.sha):
                    st.success(f"Material '{nombre_mat}' guardado con éxito en el inventario.")
                    base_datos, sha = cargar_base_datos()
                    st.session_state.db = base_datos
                    st.session_state.sha = sha
                    st.rerun()

# ==========================================
# PESTAÑA 3: VERIFICAR PANEL DE MATERIALES
# ==========================================
elif st.session_state.menu_actual == "Inventario":
    st.markdown('<div class="titulo-principal">🎒 Panel de Control de Inventario</div>', unsafe_allow_html=True)
    
    materiales_dict = st.session_state.db.get("materiales", {})
    if not materiales_dict:
        st.info("No hay materiales registrados en el inventario.")
        st.stop()
        
    lista_materiales = sorted(list(materiales_dict.keys()))
    mat_control = st.selectbox("Selecciona un material para auditar o modificar:", lista_materiales)
    info_mat = materiales_dict[mat_control]
    
    tab_acc1, tab_acc2, tab_acc3 = st.tabs(["👁️ Ver Ficha", "✏️ Editar Costos (Actualización en cadena)", "❌ Eliminar Material"])
    
    with tab_acc1:
        st.markdown('<div class="tarjeta-ver">', unsafe_allow_html=True)
        st.markdown(f"### Ficha Técnica: {mat_control}")
        st.write(f"**Tipo de cuantificación:** {info_mat.get('tipo', 'Unidad')}")
        st.write(f"**Costo Base Registrado:** ${info_mat['costo']:.2f} USD")
        if info_mat.get('tipo') == "Pieza (Área)":
            st.write(f"**Medidas de la pieza:** {info_mat['ancho']} cm x {info_mat['alto']} cm")
            area = info_mat['ancho'] * info_mat['alto']
            st.write(f"**Área total original:** {area:.2f} cm²")
            st.write(f"**Costo por cm²:** ${(info_mat['costo'] / area):.5f} USD")
        st.markdown('</div>', unsafe_allow_html=True)
        
        productos_dict = st.session_state.db.get("productos", {})
        usado_en = []
        for p_nombre, p_info in productos_dict.items():
            for m_item in p_info.get("receta", []):
                if m_item["nombre"] == mat_control:
                    usado_en.append(p_nombre)
                    break
                    
        st.markdown("#### 🗺️ Vinculación en Catálogo:")
        if usado_en:
            st.write(f"Este material se utiliza actualmente en: {', '.join([f'**{p}**' for p in usado_en])}")
        else:
            st.write("Este material no está asociado a ningún producto final actualmente.")

    with tab_acc2:
        st.markdown('<div class="tarjeta-editar">', unsafe_allow_html=True)
        st.markdown("### Modificación de Costo y Recálculo Automático")
        nuevo_costo_editado = st.number_input("Modificar Costo en USD ($):", min_value=0.01, value=float(info_mat['costo']), step=0.1, key="edit_cost_input")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("💾 Confirmar Cambios y Actualizar Catálogo en Cadena", type="primary"):
            st.session_state.db["materiales"][mat_control]["costo"] = nuevo_costo_editado
            productos_dict = st.session_state.db.get("productos", {})
            
            for p_nombre, p_info in productos_dict.items():
                receta_lista = p_info.get("receta", [])
                necesita_recalculo = False
                
                for item in receta_lista:
                    if item["nombre"] == mat_control:
                        necesita_recalculo = True
                        if item["tipo"] == "Pieza (Área)":
                            area_total_orig = info_mat['ancho'] * info_mat['alto']
                            area_prod_solicitada = item["ancho"] * item["alto"]
                            item["costo_parcial"] = (nuevo_costo_editado / area_total_orig) * area_prod_solicitada
                        else:
                            item["costo_parcial"] = nuevo_costo_editado * item["cantidad"]
                            
                if necesita_recalculo:
                    f_desp = p_info.get("factor_desperdicio", 10)
                    nuevo_costo_mat_total = 0.0
                    for item in receta_lista:
                        if item["tipo"] == "Pieza (Área)":
                            nuevo_costo_mat_total += item["costo_parcial"] * (1 + (f_desp / 100))
                        else:
                            nuevo_costo_mat_total += item["costo_parcial"]
                            
                    p_info["costo_produccion"] = nuevo_costo_mat_total + p_info.get("mano_obra", 0.0)
                    c_ind_porc = p_info.get("costos_indirectos_porcentaje", 10)
                    m_gan_porc = p_info.get("margen_ganancia", 50)
                    
                    monto_ind_nuevo = p_info["costo_produccion"] * (c_ind_porc / 100)
                    base_ind_nueva = p_info["costo_produccion"] + monto_ind_nuevo
                    
                    if m_gan_porc < 100:
                        p_info["precio_usd"] = base_ind_nueva / (1 - (m_gan_porc / 100))
                    else:
                        p_info["precio_usd"] = base_ind_nueva * 2
                        
                    p_info["precio_bs"] = p_info["precio_usd"] * p_info.get("tasa_bcv", 36.50)
            
            if guardar_base_datos(st.session_state.db, st.session_state.sha):
                st.success("¡Base de datos y productos recalculados en cadena con éxito!")
                base_datos, sha = cargar_base_datos()
                st.session_state.db = base_datos
                st.session_state.sha = sha
                st.rerun()

    with tab_acc3:
        st.error("⚠️ ZONA DE PELIGRO")
        if st.button(f"❌ Eliminar Definitivamente {mat_control}", use_container_width=True):
            st.session_state.db["materiales"].pop(mat_control)
            if guardar_base_datos(st.session_state.db, st.session_state.sha):
                st.success(f"Material '{mat_control}' eliminado.")
                base_datos, sha = cargar_base_datos()
                st.session_state.db = base_datos
                st.session_state.sha = sha
                st.rerun()

# ==========================================
# PESTAÑA 4: CATÁLOGO DE PRODUCTOS FINALES
# ==========================================
elif st.session_state.menu_actual == "Catalogo":
    st.markdown('<div class="titulo-principal">📜 Catálogo de Productos Guardados</div>', unsafe_allow_html=True)
    
    productos_dict = st.session_state.db.get("productos", {})
    if not productos_dict:
        st.info("No tienes productos guardados en el catálogo aún.")
        st.stop()
        
    lista_productos_guardados = sorted(list(productos_dict.keys()))
    
    tabla_resumen = []
    for prod_name, prod_info in productos_dict.items():
        tabla_resumen.append({
            "Producto": prod_name,
            "Costo Fab ($)": f"${prod_info['costo_produccion']:.2f}",
            "Precio Venta ($)": f"${prod_info['precio_usd']:.2f}",
            "Precio Venta (Bs)": f"Bs. {prod_info['precio_bs']:.2f}",
            "Fecha Registro": prod_info.get("fecha", "N/A")
        })
    st.dataframe(tabla_resumen, use_container_width=True)
    
    st.markdown("---")
    st.subheader("🔍 Ver Detalles y Receta Específica")
    prod_seleccionado = st.selectbox("Selecciona un producto para auditar su receta:", lista_productos_guardados)
    detalles_prod = productos_dict[prod_seleccionado]
    
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.markdown(f"### Configuración de: {prod_seleccionado}")
        st.write(f"**Mano de Obra Directa asignada:** ${detalles_prod.get('mano_obra', 0.0):.2f} USD")
        st.write(f"**Margen de Ganancia Neto:** {detalles_prod.get('margen_ganancia', 0)}%")
        st.write(f"**Costos Indirectos:** {detalles_prod.get('costos_indirectos_porcentaje', 0)}%")
        st.write(f"**Tasa de Cambio de referencia:** {detalles_prod.get('tasa_bcv', 0.0)} Bs/$")
    
    with col_d2:
        st.markdown("#### 📦 Receta de Materiales Utilizados:")
        receta_lista = detalles_prod.get("receta", [])
        for item in receta_lista:
            st.write(f"• **{item['nombre']}**: {item['descripcion']} | Subtotal: ${item['costo_parcial']:.2f} USD")
            
    if st.button(f"🗑️ Eliminar '{prod_seleccionado}' del Catálogo", type="secondary"):
        st.session_state.db["productos"].pop(prod_seleccionado)
        if guardar_base_datos(st.session_state.db, st.session_state.sha):
            st.success(f"Producto '{prod_seleccionado}' eliminado con éxito.")
            base_datos, sha = cargar_base_datos()
            st.session_state.db = base_datos
            st.session_state.sha = sha
            st.rerun()
