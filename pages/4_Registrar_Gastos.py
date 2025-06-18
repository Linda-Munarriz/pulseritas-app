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
    gastos_df = pd.DataFrame(columns=["Usuario", "Categoría", "Descripción", "Cantidad", "Precio Unitario", "Monto", "Fecha"])
    gastos_df.to_csv(file_path, index=False)

# ---------------- Formulario ----------------
with st.form("gasto_form"):
    categoria = st.selectbox("Categoría", ["Packaging", "Insumos"])
    descripcion = st.text_input("Descripción (ej: hilo blanco)")
    cantidad = st.number_input("Cantidad", min_value=1, step=1)
    precio_unitario = st.number_input("Precio unitario (S/)", min_value=0.1, step=0.1)
    fecha = st.date_input("Fecha", value=date.today())
    monto_total = cantidad * precio_unitario

    st.markdown(f"**💰 Monto total:** S/ {monto_total:.2f}")

    submitted = st.form_submit_button("Registrar gasto")

    if submitted:
        new_row = {
            "Usuario": st.session_state.username,
            "Categoría": categoria,
            "Descripción": descripcion,
            "Cantidad": cantidad,
            "Precio Unitario": precio_unitario,
            "Monto": monto_total,
            "Fecha": fecha
        }
        gastos_df = pd.read_csv(file_path)
        gastos_df = pd.concat([gastos_df, pd.DataFrame([new_row])], ignore_index=True)
        gastos_df.to_csv(file_path, index=False)
        st.success("✅ Gasto registrado exitosamente.")
        try:
            st.experimental_rerun()
        except:
            pass

# ---------------- Historial ----------------
st.subheader("📋 Historial de gastos")

gastos_df = pd.read_csv(file_path)

categoria_filtro = st.selectbox("🔍 Filtrar por categoría:", ["Todos", "Packaging", "Insumos"])

if categoria_filtro != "Todos":
    gastos_filtrados = gastos_df[gastos_df["Categoría"] == categoria_filtro]
else:
    gastos_filtrados = gastos_df

# Mostrar tabla
st.dataframe(gastos_filtrados.sort_values("Fecha", ascending=False), use_container_width=True)

# Descargar CSV
csv_export = gastos_filtrados.to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️ Descargar gastos como CSV",
    data=csv_export,
    file_name=f"gastos_{categoria_filtro.lower() if categoria_filtro != 'Todos' else 'todos'}.csv",
    mime="text/csv"
)

# ---------------- Eliminar gastos ----------------
st.subheader("🗑️ Eliminar gasto por error")

if not gastos_filtrados.empty:
    gastos_filtrados = gastos_filtrados.reset_index(drop=True)
    gastos_filtrados.index += 1  # Empezar en 1

    st.write("Selecciona el número de fila que quieres eliminar:")
    st.dataframe(gastos_filtrados)

    fila_a_eliminar = st.number_input(
        "Número de fila a eliminar (ver tabla arriba)", 
        min_value=1, 
        max_value=len(gastos_filtrados), 
        step=1
    )

    if st.button("Eliminar gasto seleccionado"):
        df_original = pd.read_csv(file_path)

        # Reaplicar el filtro para alinear índice con el archivo original
        if categoria_filtro != "Todos":
            gastos_filtrados = df_original[df_original["Categoría"] == categoria_filtro]
        else:
            gastos_filtrados = df_original

        gastos_filtrados = gastos_filtrados.reset_index(drop=True)
        gastos_filtrados.index += 1  # Para que empiece en 1 igual que en la UI

        if 1 <= fila_a_eliminar <= len(gastos_filtrados):
            fila_real = gastos_filtrados.loc[fila_a_eliminar - 1]

            # Encontrar el índice real de esa fila en el CSV original
            index_real = df_original[
                (df_original["Usuario"] == fila_real["Usuario"]) &
                (df_original["Categoría"] == fila_real["Categoría"]) &
                (df_original["Descripción"] == fila_real["Descripción"]) &
                (df_original["Cantidad"].astype(float) == float(fila_real["Cantidad"])) &
                (df_original["Precio Unitario"].astype(float) == float(fila_real["Precio Unitario"])) &
                (df_original["Monto"].astype(float) == float(fila_real["Monto"])) &
                (df_original["Fecha"] == fila_real["Fecha"])
            ].index

            if not index_real.empty:
                df_actualizado = df_original.drop(index_real[0])
                df_actualizado.to_csv(file_path, index=False)
                st.success("✅ Gasto eliminado exitosamente.")
                try:
                    st.experimental_rerun()
                except:
                    pass
            else:
                st.warning("⚠️ No se encontró la fila para eliminar. Intenta de nuevo.")
        else:
            st.warning("⚠️ Número de fila inválido.")
