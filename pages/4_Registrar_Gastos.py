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

# Ver gastos registrados con filtro
st.subheader("📋 Historial de gastos")

gastos_df = pd.read_csv(file_path)

# Filtro por categoría
categoria_filtro = st.selectbox("🔍 Filtrar por categoría:", ["Todos", "Packaging", "Insumos"])

if categoria_filtro != "Todos":
    gastos_filtrados = gastos_df[gastos_df["Categoría"] == categoria_filtro]
else:
    gastos_filtrados = gastos_df

# Mostrar tabla
st.dataframe(gastos_filtrados.sort_values("Fecha", ascending=False), use_container_width=True)

# Descargar CSV filtrado
csv_export = gastos_filtrados.to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️ Descargar gastos como CSV",
    data=csv_export,
    file_name=f"gastos_{categoria_filtro.lower() if categoria_filtro != 'Todos' else 'todos'}.csv",
    mime="text/csv"
)
