import streamlit as st
import pandas as pd
import json
import os

# Configuración de la página
st.set_page_config(page_title="Calculadora Oficenter", layout="wide", page_icon="✂️")

st.title("✂️ Sistema Permanente de Costos - Papelería Creativa")
st.write("Tu calculadora personalizada con almacenamiento automático.")

# --- FUNCIONES DE ALMACENAMIENTO PERMANENTE ---
def cargar_datos(archivo, datos_por_defecto):
    if os.path.exists(archivo):
        with open(archivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    return datos_por_defecto

def guardar_datos(archivo, datos):
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

# Materiales por defecto si el archivo no existe
mats_defecto = {
    "Cartulina Escolar": {"Costo Proveedor": 0.50, "Precio Tienda": 1.00, "Ancho (cm)": 50.0, "Alto (cm)": 70.0, "Tipo": "Por Área (cm²)"},
    "Silicón (Barra)": {"Costo Proveedor": 0.10, "Precio Tienda": 0.25, "Ancho (cm)": 1.0, "Alto (cm)": 1.0, "Tipo": "Por Unidad"},
    "Palito de Madera": {"Costo Proveedor": 0.02, "Precio Tienda": 0.08, "Ancho (cm)": 1.0, "Alto (cm)": 1.0, "Tipo": "Por Unidad"}
}

# Cargar estados iniciales desde los archivos físicos
if 'materiales' not in st.session_state:
    st.session_state.materiales = cargar_datos('materiales.json', mats_defecto)

if 'productos_guardados' not in st.session_state:
    st.session_state.productos_guardados = cargar_datos('productos.json', [])

# --- PESTAÑAS ---
tab1, tab2, tab3 = st.tabs(["🧮 Calculadora de Presupuestos", "🎒 Panel de Materiales (Inventario)", "📜 Catálogo de Productos Finales"])

# ==========================================
# TAB 2: PANEL DE MATERIALES (CON GUARDADO REAL)
# ==========================================
with tab2:
    st.header("🎒 Gestión y Configuración de Materiales")
    col_inv, col_form = st.columns([2, 1])
    
    with col_inv:
        st.subheader("Tu Inventario Actual")
        tabla_visual = []
        for nombre, datos in st.session_state.materiales.items():
            if datos["Tipo"] == "Por Área (cm²)":
                area = datos["Ancho (cm)"] * datos["Alto (cm)"]
                costo_uni = datos["Costo Proveedor"] / area
                precio_uni = datos["Precio Tienda"] / area
                unidad_medida = "cm²"
            else:
                costo_uni = datos["Costo Proveedor"]
                precio_uni = datos["Precio Tienda"]
                unidad_medida = "Unidad"
                
            tabla_visual.append({
                "Material": nombre,
                "Tipo": datos["Tipo"],
                "Costo Base": f"${datos['Costo Proveedor']:.2f}",
                "Precio Tienda": f"${datos['Precio Tienda']:.2f}",
                "Medidas": f"{datos['Ancho (cm)']}x{datos['Alto (cm)']} cm" if datos["Tipo"] == "Por Área (cm²)" else "N/A",
                "Costo x " + unidad_medida: f"${costo_uni:.5f}",
                "Precio x " + unidad_medida: f"${precio_uni:.5f}"
            })
        st.dataframe(pd.DataFrame(tabla_visual), use_container_width=True)
        
    with col_form:
        st.subheader("⚙️ Configurar / Agregar Material")
        mat_nombre = st.text_input("Nombre del Material", placeholder="Ej. Silicón (Barra)")
        mat_tipo = st.selectbox("Tipo de Medición", ["Por Unidad", "Por Área (cm²)"])
        c_prov, c_tien = st.columns(2)
        mat_costo = c_prov.number_input("Costo Proveedor ($)", min_value=0.0, step=0.01, format="%.2f")
        mat_precio = c_tien.number_input("Precio Tienda ($)", min_value=0.0, step=0.01, format="%.2f")
        
        mat_ancho, mat_alto = 1.0, 1.0
        if mat_tipo == "Por Área (cm²)":
            c_an, c_al = st.columns(2)
            mat_ancho = c_an.number_input("Ancho del pliego (cm)", min_value=1.0, value=50.0)
            mat_alto = c_al.number_input("Alto del pliego (cm)", min_value=1.0, value=70.0)
            
        if st.button("💾 Guardar Cambios en Material"):
            if mat_nombre:
                st.session_state.materiales[mat_nombre] = {
                    "Costo Proveedor": mat_costo, "Precio Tienda": mat_precio,
                    "Ancho (cm)": mat_ancho, "Alto (cm)": mat_alto, "Tipo": mat_tipo
                }
                # Guardar físicamente en el archivo permanente
                guardar_datos('materiales.json', st.session_state.materiales)
                st.success(f"¡'{mat_nombre}' guardado permanentemente!")
                st.rerun()

# ==========================================
# TAB 1: CALCULADORA DE PRESUPUESTOS
# ==========================================
with tab1:
    st.header("Calcular Nuevo Proyecto")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Componentes del Producto")
        lista_mats = list(st.session_state.materiales.keys())
        
        material_1 = st.selectbox("Selecciona Material 1", lista_mats, index=0)
        row_1 = st.session_state.materiales[material_1]
        if row_1["Tipo"] == "Por Área (cm²)":
            c1, c2 = st.columns(2)
            ancho_usado = c1.number_input(f"Ancho usado de {material_1} (cm)", min_value=0.0, value=20.0)
            alto_usado = c2.number_input(f"Alto usado de {material_1} (cm)", min_value=0.0, value=20.0)
            area_total = row_1["Ancho (cm)"] * row_1["Alto (cm)"]
            costo_mat = (row_1["Costo Proveedor"] / area_total) * (ancho_usado * alto_usado)
            precio_mat = (row_1["Precio Tienda"] / area_total) * (ancho_usado * alto_usado)
        else:
            cant_usada = st.number_input(f"Cantidad de {material_1} (Unidades)", min_value=0.0, value=1.0)
            costo_mat = row_1["Costo Proveedor"] * cant_usada
            precio_mat = row_1["Precio Tienda"] * cant_usada

        material_2 = st.selectbox("Selecciona Material 2", lista_mats, index=1 if len(lista_mats)>1 else 0)
        row_2 = st.session_state.materiales[material_2]
        if row_2["Tipo"] == "Por Área (cm²)":
            c1_b, c2_b = st.columns(2)
            ancho_usado2 = c1_b.number_input(f"Ancho usado de {material_2} (cm)", min_value=0.0, value=1.0)
            alto_usado2 = c2_b.number_input(f"Alto usado de {material_2} (cm)", min_value=0.0, value=1.0)
            area_total2 = row_2["Ancho (cm)"] * row_2["Alto (cm)"]
            costo_mat2 = (row_2["Costo Proveedor"] / area_total2) * (ancho_usado2 * alto_usado2)
            precio_mat2 = (row_2["Precio Tienda"] / area_total2) * (ancho_usado2 * alto_usado2)
        else:
            cant_2 = st.number_input(f"Cantidad de {material_2} (Unidades)", min_value=0.0, value=1.0)
            costo_mat2 = row_2["Costo Proveedor"] * cant_2
            precio_mat2 = row_2["Precio Tienda"] * cant_2
        
        st.divider()
        st.subheader("⚙️ Mano de Obra y Máquinas")
        c3, c4 = st.columns(2)
        tiempo_cameo = c3.number_input("Minutos de uso de Cameo", min_value=0, value=10)
        tiempo_mano = c4.number_input("Minutos de Mano de Obra", min_value=0, value=15)
        total_fijos = (tiempo_cameo * 0.05) + (tiempo_mano * 0.10)

    with col2:
        st.subheader("📊 Resumen del Presupuesto")
        precio_tienda_insumos = precio_mat + precio_mat2
        costo_base_proyecto = precio_tienda_insumos + total_fijos
        margen_ganancia = st.slider("Margen de Ganancia Extra (%)", min_value=0, max_value=200, value=50)
        
        precio_venta_final = costo_base_proyecto * (1 + (margen_ganancia / 100))
        ganancia_total_real = (precio_venta_final - costo_base_proyecto) + (precio_tienda_insumos - (costo_mat + costo_mat2)) + (tiempo_mano * 0.10)

        st.metric(label="💰 PRECIO DE VENTA SUGERIDO", value=f"${precio_venta_final:.2f}")
        with st.expander("🔎 Ver desglose"):
            st.write(f"Insumos a Precio Público: ${precio_tienda_insumos:.2f}")
            st.write(f"Tiempo y Desgaste: ${total_fijos:.2f}")
            st.success(f"Ganancia Real Total: ${ganancia_total_real:.2f}")

        st.divider()
        st.subheader("💾 Guardar en Catálogo")
        nombre_producto = st.text_input("Nombre del producto final")
        if st.button("Registrar Producto Final"):
            if nombre_producto:
                nuevo_prod = {
                    "Producto": nombre_producto, "Precio Venta": f"${precio_venta_final:.2f}",
                    "Ganancia Real": f"${ganancia_total_real:.2f}", "Detalles": f"{tiempo_mano} min armado."
                }
                st.session_state.productos_guardados.append(nuevo_prod)
                # Guardar físicamente en el archivo permanente
                guardar_datos('productos.json', st.session_state.productos_guardados)
                st.success(f"¡'{nombre_producto}' guardado permanentemente!")
            else:
                st.error("Escribe un nombre para el producto.")

# ==========================================
# TAB 3: CATÁLOGO DE PRODUCTOS FINALIZADOS
# ==========================================
with tab3:
    st.header("📜 Catálogo de Productos Registrados")
    if len(st.session_state.productos_guardados) == 0:
        st.warning("No hay productos guardados.")
    else:
        st.dataframe(pd.DataFrame(st.session_state.productos_guardados), use_container_width=True)
