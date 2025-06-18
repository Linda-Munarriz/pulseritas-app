import streamlit as st
import pandas as pd
from datetime import date
import os

if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Debes iniciar sesión primero.")
    st.stop()

st.title("💸 Registrar Gastos")

file_path = "data/gastos.csv"

# Asegurar que exista el archivo
if not os.path.exists(file_path):
    gastos_df = pd.DataFrame(columns=["Usuario", "Categoría", "Descripción", "Monto", "Fecha"])
    gastos_df.to_csv(file_path, index=False)

# Formulario
with st.form("gasto_form"):
    categoria = st.selectbox("Categoría", ["Packaging", "Insumos"])
    descripcion = st.text_input("Descripción (ej: hilo blanco)")
    monto = st.number_input("Monto (S/)", min_value=0.1, step=0.1)
    fecha = st.date_input("Fecha", value=date.today())
    submitted = st.form_submit_button("Registrar gasto")

    if submitted:
        new_row = {
            "Usuario": st.session_state.username,
            "Categoría": categoria,
            "Descripción": descripcion,
            "Monto": monto,
            "Fecha": fecha
        }
        gastos_df = pd.read_csv(file_path)
        gastos_df = pd.concat([gastos_df, pd.DataFrame([new_row])], ignore_index=True)
        gastos_df.to_csv(file_path, index=False)
        st.success("✅ Gasto registrado exitosamente")

# Ver gastos recientes
st.subheader("📋 Gastos registrados")
gastos_df = pd.read_csv(file_path)
st.dataframe(gastos_df.sort_values("Fecha", ascending=False))
