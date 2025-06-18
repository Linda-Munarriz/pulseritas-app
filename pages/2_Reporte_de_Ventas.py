import streamlit as st
import pandas as pd
import os
from datetime import date

if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Debes iniciar sesión primero.")
    st.stop()

st.title("📝 Reporte de Ventas")

bracelet_type = st.selectbox("Tipo de Pulsera", ["Pulsera Corazón", "Pulsera Power"])
quantity = st.number_input("Cantidad vendida", min_value=1, step=1)
sale_date = st.date_input("Fecha de venta", value=date.today())

if st.button("Registrar venta"):
    username = st.session_state.username
    if bracelet_type == "Pulsera Corazón":
        breakfast = 1.5 * quantity
        reinvest = 0.5 * quantity
    else:
        breakfast = 3 * quantity
        reinvest = 0

    row = {
        "Usuario": username,
        "Producto": bracelet_type,
        "Cantidad": quantity,
        "Fecha": sale_date,
        "Desayunos": breakfast,
        "Reinversión": reinvest
    }

    df = pd.DataFrame([row])
    file_path = "data/ventas.csv"
    if os.path.exists(file_path):
        df.to_csv(file_path, mode='a', header=False, index=False)
    else:
        os.makedirs("data", exist_ok=True)
        df.to_csv(file_path, index=False)

    st.success("✅ Venta registrada correctamente")
# 🗑️ Eliminar venta específica
st.subheader("🗑️ Eliminar una venta por error")

ventas_df = pd.read_csv("data/ventas.csv")
ventas_usuario = ventas_df[ventas_df["Usuario"] == st.session_state.username]

if not ventas_usuario.empty:
    ventas_usuario = ventas_usuario.reset_index(drop=True)
    ventas_usuario.index += 1  # Para que empiece en 1

    st.write("Selecciona el número de fila a eliminar:")
    st.dataframe(ventas_usuario)

    fila_a_eliminar = st.number_input(
        "Número de fila a eliminar (ver tabla arriba)", 
        min_value=1, 
        max_value=len(ventas_usuario), 
        step=1
    )

    if st.button("Eliminar venta seleccionada"):
        df_original = pd.read_csv("data/ventas.csv")
        fila_global = ventas_usuario.index[fila_a_eliminar - 1]
        fila_real = ventas_usuario.loc[fila_global]

        match = (
            (df_original["Usuario"] == fila_real["Usuario"]) &
            (df_original["Producto"] == fila_real["Producto"]) &
            (df_original["Cantidad"] == fila_real["Cantidad"]) &
            (df_original["Fecha"] == fila_real["Fecha"])
        )
        df_actualizado = df_original[~match]
        df_actualizado.to_csv("data/ventas.csv", index=False)

        st.success("✅ Venta eliminada exitosamente.")
        try:
            st.experimental_rerun()
        except:
            pass
else:
    st.info("No hay ventas registradas por ti para eliminar.")
