# ==========================================
# 🎒 VISTA: 3- VERIFICAR PANEL DE MATERIALES (MEDIDAS E ICONOS EN FILA)
# ==========================================
elif st.session_state.menu_actual == "🎒 3- Verificar Panel de Materiales":
    st.markdown("<h2 style='color: #e9769d;'>🎒 Panel de Control de Inventario</h2>", unsafe_allow_html=True)
    
    if not st.session_state.materiales:
        st.info("No hay materiales registrados.")
    else:
        # Generamos la tabla con la nueva columna de dimensiones integradas
        lista_datos_tabla = []
        for n, d in st.session_state.materiales.items():
            porcentaje_ganancia_mat = (((d['Precio'] - d['Costo']) / d['Precio']) * 100) if d['Precio'] > 0 else 0.0
            
            # Formatear la medida de forma compacta y visualmente agradable
            if d.get("Tipo") == "Pieza (Área)":
                medida_str = f"{d.get('Ancho', 0.0)} x {d.get('Alto', 0.0)} cm"
            else:
                medida_str = "N/A (Unidad)"
                
            lista_datos_tabla.append({
                "Material": n,
                "Tipo": d["Tipo"],
                "Medidas (cm)": medida_str, # <--- ¡Nueva columna agregada con éxito!
                "Marca": d.get("Marca", "Genérica"),
                "Costo Base": f"${d['Costo']:.2f}",
                "Precio Base": f"${d['Precio']:.2f}",
                "Ganancia (%)": f"{porcentaje_ganancia_mat:.1f}%",
                "Última Actualización": d.get("Fecha", "Original"),
                "👁️ Ver": False,  
                "✏️ Editar": False
            })
            
        df_panel = pd.DataFrame(lista_datos_tabla)
        
        # Uso de st.data_editor para capturar los clics directamente en las filas de la tabla
        edicion_tabla = st.data_editor(
            df_panel,
            column_config={
                "👁️ Ver": st.column_config.CheckboxColumn("👁️ Ver", help="Ver ficha técnica completa y descargar PDF", default=False),
                "✏️ Editar": st.column_config.CheckboxColumn("✏️ Editar", help="Modificar precios, costos y marca", default=False)
            },
            disabled=["Material", "Tipo", "Medidas (cm)", "Marca", "Costo Base", "Precio Base", "Ganancia (%)", "Última Actualización"],
            use_container_width=True,
            key="editor_tabla_panel"
        )
        
        # Evaluar si el usuario interactuó con alguna fila de la lista
        for index, row in edicion_tabla.iterrows():
            nombre_mat_fila = row["Material"]
            if row["👁️ Ver"] == True:
                st.session_state.accion_material = "ver"
                st.session_state.material_focalizado = nombre_mat_fila
                break
            elif row["✏️ Editar"] == True:
                st.session_state.accion_material = "editar"
                st.session_state.material_focalizado = nombre_mat_fila
                break

        # ACCIÓN A: DESPLIEGUE COMPACTO DEL RESUMEN GENERAL (VER)
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
                    <h3 style="color:#74b7d5; text-align:left; margin:0;">📋 Resumen Técnico General: {mat_foc}</h3>
                </div>
            """, unsafe_allow_html=True)
            
            c_v1, c_v2, c_v3 = st.columns(3)
            with c_v1:
                st.markdown("**⚙️ Características:**")
                st.write(f"• **Tipo de medida:** {info_mat['Tipo']}")
                st.write(f"• **Marca Utilizada:** {info_mat.get('Marca', 'Genérica')}")
                if info_mat["Tipo"] == "Pieza (Área)":
                    st.write(f"• **Dimensiones:** {info_mat['Ancho']}cm x {info_mat['Alto']}cm")
            with c_v2:
                st.markdown("**💰 Datos Financieros:**")
                st.write(f"• **Costo Unitario:** ${info_mat['Costo']:.2f}")
                st.write(f"• **Precio de Venta:** ${info_mat['Precio']:.2f}")
                st.write(f"• **Ganancia Neta Real:** ${ganancia_dolares:.2f} ({pct_ganancia:.1f}%)")
            with c_v3:
                st.markdown("**🎒 Catálogo Asociado:**")
                st.write(f"• **Productos que lo usan:** `{vinculos_str}`")
                st.write(f"• **Último Registro:** {info_mat.get('Fecha', 'Original')}")
