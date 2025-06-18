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
