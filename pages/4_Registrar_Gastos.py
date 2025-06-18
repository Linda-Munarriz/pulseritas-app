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
# 🗑️ Sección para eliminar gastos
st.subheader("🗑️ Eliminar gasto por error")

if not gastos_filtrados.empty:
    gastos_filtrados = gastos_filtrados.reset_index(drop=True)
    gastos_filtrados.index += 1  # Empezar en 1 para usuarios

    st.write("Selecciona el número de fila que quieres eliminar:")
    st.dataframe(gastos_filtrados)

    fila_a_eliminar = st.number_input(
        "Número de fila a eliminar (ver tabla arriba)", 
        min_value=1, 
        max_value=len(gastos_filtrados), 
        step=1
    )

    if st.button("Eliminar gasto seleccionado"):
        # Leer archivo original completo
        df_original = pd.read_csv(file_path)

        # Localizar fila exacta en archivo original por índice absoluto
        fila_global = gastos_filtrados.index[fila_a_eliminar - 1]  # -1 porque el índice empieza en 1
        fila_real = gastos_filtrados.loc[fila_global]

        # Buscar en df original y eliminar esa fila exacta
        match = (
            (df_original["Usuario"] == fila_real["Usuario"]) &
            (df_original["Categoría"] == fila_real["Categoría"]) &
            (df_original["Descripción"] == fila_real["Descripción"]) &
            (df_original["Monto"] == fila_real["Monto"]) &
            (df_original["Fecha"] == fila_real["Fecha"])
        )
        df_actualizado = df_original[~match]

        df_actualizado.to_csv(file_path, index=False)
        st.success("✅ Gasto eliminado exitosamente.")
try:
    st.experimental_rerun()
except:
    pass

else:
    st.info("No hay gastos para eliminar.")
