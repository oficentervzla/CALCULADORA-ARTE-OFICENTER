import streamlit as st
import pandas as pd
import json
import os

# Configuración de la página
st.set_page_config(page_title="Sistema Art Center", layout="wide", page_icon="🎨")

# --- DISEÑO Y ESTILOS DE TU MARCA ---
st.markdown("""
    <style>
        .stApp { background-color: #ffffff; }
        h1, h2, h3 { color: #74b7d5 !important; font-family: 'Arial', sans-serif; }
        
        /* Menú lateral de opciones principales */
        [data-testid="stSidebar"] {
            background-color: #f7f9fa;
            border-right: 3px solid #fed80c;
        }
        
        /* Botón de guardar y acciones */
        .stButton>button {
            background-color: #fed80c !important;
            color: #000000 !important;
            font-weight: bold !important;
            border-radius: 12px !important;
            border: none !important;
            padding: 8px 20px !important;
        }
        .stButton>button:hover {
            background-color: #0bccd1 !important;
            color: #ffffff !important;
        }
        
        /* Tarjeta de precio final destacada */
        .tarjeta-precio {
            background-color: #f7f9fa;
            padding: 25px;
            border-radius: 15px;
            border-left: 6px solid #e9769d;
            text-align: center;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
        }
    </style>
""", unsafe_allow_html=True)

# --- SISTEMA DE ALMACENAMIENTO ---
def cargar_datos(archivo, defecto):
    if os.path.exists(archivo):
        with open(archivo, 'r', encoding='utf-8') as f: return json.load(f)
    return defecto

def guardar_datos(archivo, datos):
    with open(archivo, 'w', encoding='utf-8') as f: json.dump(datos, f, ensure_ascii=False, indent=4)

mats_defecto = {
    "Cartulina Escolar": {"Costo Proveedor": 0.50, "Precio Tienda": 1.00, "Ancho (cm)": 50.0, "Alto (cm)": 70.0, "Tipo": "Por Área (cm²)", "Marca": "Generica"},
    "Silicón (Barra)": {"Costo Proveedor": 0.10, "Precio Tienda": 0.25, "Ancho (cm)": 1.0, "Alto (cm)": 1.0, "Tipo": "Por Unidad", "Marca": "Generica"},
    "Palito de Madera": {"Costo Proveedor": 0.02, "Precio Tienda": 0.08, "Ancho (cm)": 1.0, "Alto (cm)": 1.0, "Tipo": "Por Unidad", "Marca": "Generica"}
}

if 'materiales' not in st.session_state: st.session_state.materiales = cargar_datos('materiales.json', mats_defecto)
if 'productos_guardados' not in st.session_state: st.session_state.productos_guardados = cargar_datos('productos.json', [])

# --- MENÚ LATERAL: OPCIONES PRINCIPALES ---
st.sidebar.markdown("<h2 style='color: #e9769d !important; text-align: center;'>🎨 ART CENTER</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; font-size: 12px; font-weight: bold; color: #74b7d5;'>MENÚ PRINCIPAL</p>", unsafe_allow_html=True)
st.sidebar.divider()

opcion = st.sidebar.radio(
    "Selecciona una acción:",
    ["🧮 Crear Presupuesto", "➕ Crear Material", "🎒 Verificar Panel de Materiales", "📜 Catálogo de Productos Finales"]
)

# Encabezado superior dinámico
st.markdown(f"<h1 style='color: #e9769d !important;'>{opcion}</h1>", unsafe_allow_html=True)
st.divider()

# ==========================================
# 1. CREAR PRESUPUESTO
# ==========================================
if opcion == "🧮 Crear Presupuesto":
    col_izq, col_der = st.columns([1.2, 1])
    lista_mats = list(st.session_state.materiales.keys())
    
    with col_izq:
        st.subheader("Selecciona los insumos usados:")
        
        # Insumo 1
        mat1 = st.selectbox("Material Principal", lista_mats, index=0)
        d1 = st.session_state.materiales[mat1]
        if d1["Tipo"] == "Por Área (cm²)":
            c1, c2 = st.columns(2)
            w1 = c1.number_input("Ancho usado (cm)", min_value=0.0, value=20.0, key="w1")
            h1 = c2.number_input("Alto usado (cm)", min_value=0.0, value=20.0, key="h1")
            area = d1["Ancho (cm)"] * d1["Alto (cm)"]
            c_m1 = (d1["Costo Proveedor"] / area) * (w1 * h1)
            p_m1 = (d1["Precio Tienda"] / area) * (w1 * h1)
        else:
            cant1 = st.number_input("Cantidad utilizada (Unidades)", min_value=0.0, value=1.0, key="v1")
            c_m1 = d1["Costo Proveedor"] * cant1
            p_m1 = d1["Precio Tienda"] * cant1

        st.markdown("---")
        
        # Insumo 2
        mat2 = st.selectbox("Segundo Material / Accesorio", lista_mats, index=1 if len(lista_mats)>1 else 0)
        d2 = st.session_state.materiales[mat2]
        if d2["Tipo"] == "Por Área (cm²)":
            c3, c4 = st.columns(2)
            w2 = c3.number_input("Ancho usado (cm)", min_value=0.0, value=5.0, key="w2")
            h2 = c4.number_input("Alto usado (cm)", min_value=0.0, value=5.0, key="h2")
            area2 = d2["Ancho (cm)"] * d2["Alto (cm)"]
            c_m2 = (d2["Costo Proveedor"] / area2) * (w2 * h2)
            p_m2 = (d2["Precio Tienda"] / area2) * (w2 * h2)
        else:
            cant2 = st.number_input("Cantidad utilizada (Unidades)", min_value=0.0, value=1.0, key="v2")
            c_m2 = d2["Costo Proveedor"] * cant2
            p_m2 = d2["Precio Tienda"] * cant2

        st.markdown("---")
        st.subheader("⏱ Dificultad y Ensamblaje")
        dificultad = st.radio("Complejidad del Topper:", ["Sencillo (15 min)", "Intermedio (30 min)", "Muy Detallado / Capas (60 min)"], horizontal=True)
        minutos = 15 if "Sencillo" in dificultad else (30 if "Intermedio" in dificultad else 60)
        costo_tiempo = minutos * 0.15

    with col_der:
        st.subheader("📊 Resultado del Presupuesto")
        precio_materiales_tienda = p_m1 + p_m2
        costo_materiales_proveedor = c_m1 + c_m2
        costo_base_topper = precio_materiales_tienda + costo_tiempo
        
        margen = st.slider("Ganancia Creativa Extra (%)", min_value=0, max_value=150, value=40, step=10)
        precio_cliente = costo_base_topper * (1 + (margen / 100))
        ganancia_real = (precio_cliente - costo_base_topper) + (precio_materiales_tienda - costo_materiales_proveedor) + (costo_tiempo * 0.6)

        st.markdown(f"""
            <div class="tarjeta-precio">
                <p style="margin:0; font-size:14px; color:#555; font-weight:bold;">PRECIO DE VENTA DEL TOPPER</p>
                <h1 style="margin:0; font-size:52px; color:#e9769d !important;">${precio_cliente:.2f}</h1>
                <p style="margin:8px 0 0 0; font-size:15px; color:#8bcc60; font-weight:bold;">✨ Ganancia Total Real: ${ganancia_real:.2f}</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.expander("🔎 Ver desglose detallado"):
            st.write(f"• Materiales (a precio de tienda): **${precio_materiales_tienda:.2f}**")
            st.write(f"• Costo real de esos materiales (proveedor): **${costo_materiales_proveedor:.2f}**")
            st.write(f"• Tu tiempo y uso de máquinas: **${costo_tiempo:.2f}**")
            st.write(f"• Margen creativo aplicado: **{margen}%**")

        st.divider()
        st.subheader("💾 Guardar como Producto Terminado")
        nombre_top = st.text_input("Nombre del producto final", placeholder="Ej: Topper 2 capas 15cm")
        if st.button("Guardar en Catálogo"):
            if nombre_top:
                st.session_state.productos_guardados.append({
                    "Producto Final": nombre_top, "Precio Venta": f"${precio_cliente:.2f}",
                    "Ganancia Neta": f"${ganancia_real:.2f}", "Complejidad": dificultad
                })
                guardar_datos('productos.json', st.session_state.productos_guardados)
                st.success(f"¡'{nombre_top}' guardado con éxito!")
                st.rerun()
            else: st.error("Escribe un nombre para el producto.")

# ==========================================
# 2. CREAR MATERIAL
# ==========================================
elif opcion == "➕ Crear Material":
    st.subheader("Registra un nuevo insumo para el sistema")
    
    col_f1, col_f2 = st.columns([1, 1])
    with col_f1:
        n_m = st.text_input("Nombre del Material (Ej: Cartulina Glitter Oro)")
        t_m = st.selectbox("Tipo de Medición / Venta", ["Por Área (cm²)", "Por Unidad"])
        marca = st.text_input("Marca del Material (Opcional)", placeholder="Ej: Silhouette, Cricut, Genérico")
    
    with col_f2:
        c_p = st.number_input("Costo de Compra Proveedor ($)", min_value=0.0, step=0.01, format="%.2f")
        p_t = st.number_input("Precio de Venta Tienda al Público ($)", min_value=0.0, step=0.01, format="%.2f")
        
        an, al = 1.0, 1.0
        if t_m == "Por Área (cm²)":
            c_an, c_al = st.columns(2)
            an = c_an.number_input("Ancho completo del pliego (cm)", min_value=1.0, value=50.0)
            al = c_al.number_input("Alto completo del pliego (cm)", min_value=1.0, value=70.0)

    st.divider()
    if st.button("💾 Registrar Nuevo Material"):
        if n_m:
            st.session_state.materiales[n_m] = {
                "Costo Proveedor": c_p, "Precio Tienda": p_t, 
                "Ancho (cm)": an, "Alto (cm)": al, "Tipo": t_m, "Marca": marca if marca else "Genérico"
            }
            guardar_datos('materiales.json', st.session_state.materiales)
            st.success(f"¡Material '{n_m}' agregado con éxito al sistema!")
        else: st.error("Por favor, introduce al menos el nombre del material.")

# ==========================================
# 3. VERIFICAR PANEL DE MATERIALES
# ==========================================
elif opcion == "🎒 Verificar Panel de Materiales":
    st.subheader("Consulta, analiza y edita tus insumos existentes")
    
    tabla_v = []
    for n, d in st.session_state.materiales.items():
        u = "cm²" if d["Tipo"] == "Por Área (cm²)" else "Unidad"
        fact = (d["Ancho (cm)"] * d["Alto (cm)"]) if d["Tipo"] == "Por Área (cm²)" else 1
        ganancia_tienda = d["Precio Tienda"] - d["Costo Proveedor"]
        
        tabla_v.append({
            "Material": n, "Marca": d.get("Marca", "Genérico"), "Medición": d["Tipo"], 
            "Tamaño Original": f"{d['Ancho (cm)']}x{d['Alto (cm)']} cm" if d["Tipo"] == "Por Área (cm²)" else "1 Unidad",
            "Costo Proveedor": f"${d['Costo Proveedor']:.2f}", "Precio Tienda": f"${d['Precio Tienda']:.2f}",
            "Ganancia Papelería": f"${ganancia_tienda:.2f}",
            "Precio x "+u: f"${(d['Precio Tienda']/fact):.4f}"
        })
    st.dataframe(pd.DataFrame(tabla_v), use_container_width=True)
    st.info("💡 Consejo: Si deseas modificar los precios de un material existente, ve a la sección 'Crear Material', escribe su mismo nombre exacto y guarda los nuevos costos.")

# ==========================================
# 4. CATÁLOGO DE PRODUCTOS FINALES
# ==========================================
elif opcion == "📜 Catálogo de Productos Finales":
    st.subheader("Tus productos terminados y guardados de papelería creativa")
    
    if len(st.session_state.productos_guardados) == 0:
        st.warning("Aún no tienes ningún producto final guardado en el catálogo. Calcula uno y regístralo.")
    else:
        st.dataframe(pd.DataFrame(st.session_state.productos_guardados), use_container_width=True)
