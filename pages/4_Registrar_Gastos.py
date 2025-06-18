import streamlit as st
import pandas as pd
from datetime import date
import os
import uuid

# ----------- VERIFICAR SESIÓN -----------
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Debes iniciar sesión primero.")
    st.stop()

st.title("💸 Registrar Gastos")

file_path = "data/gastos.csv"

# ----------- FUNCIONES AUXILIARES -----------
def ensure_ids(df):
    if "ID" not in df.columns:
        df["ID"] = [str(uuid.uuid4()) for _ in range(len(df))]
    elif df["ID"].isnull().any():
        df["ID"] = df["ID"].fillna(value=[str(uuid.uuid4()) for _ in range(len(df))])
    return df

# ----------- ASEGURAR EXISTENCIA DE ARCHIVO -----------
if not os.path.exists(file_path):
    gastos_df = pd.DataFrame(columns=["ID", "Usuario", "Categoría", "Descripción", "Cantidad", "Precio Unitario", "Monto", "Fecha"])
    gastos_df.to_csv(file_path, index=False)

# ----------- FORMULARIO DE GASTO -----------
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
            "ID": str(uuid.uuid4()),
            "Usuario": st.session_state.username,
            "Categoría": categoria,
            "Descripción": descripcion,
            "Cantidad": cantidad,
            "Precio Unitario": precio_unitario,
            "Monto": monto_total,
            "Fecha": fecha
        }
        gastos_df = pd.read_csv(file_path)
        gastos_df = ensure_ids(gastos_df)
        gastos_df = pd.concat([gastos_df, pd.DataFrame([new_row])], ignore_index=True)
        gastos_df.to_csv(file_path, index=False)
        st.success("✅ Gasto registrado exitosamente.")
        try:
            st.experimental_rerun()
        except:
            pass

# ----------- HISTORIAL DE GASTOS -----------
st.subheader("📋 Historial de gastos")

gastos_df = ensure_ids(pd.read_csv(file_path))
gastos_df.to_csv(file_path, index=False)

categoria_filtro = st.selectbox("🔍 Filtrar por categoría:", ["Todos", "Packaging", "Insumos"])

if categoria_filtro != "Todos":
    gastos_filtrados = gastos_df[gastos_df["Categoría"] == categoria_filtro]
else:
    gastos_filtrados = gastos_df

tabla_historial = gastos_filtrados.sort_values("Fecha", ascending=False).reset_index(drop=True)
tabla_historial.index += 1
st.dataframe(tabla_historial.drop(columns=["ID"]), use_container_width=True)

# ----------- DESCARGAR CSV -----------
csv_export = gastos_filtrados.drop(columns=["ID"]).to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️ Descargar gastos como CSV",
    data=csv_export,
    file_name=f"gastos_{categoria_filtro.lower() if categoria_filtro != 'Todos' else 'todos'}.csv",
    mime="text/csv"
)

# ----------- ELIMINAR GASTOS -----------
st.subheader("🗑️ Eliminar gasto por error")

if not gastos_filtrados.empty:
    gastos_filtrados_reset = gastos_filtrados.reset_index(drop=True)
    tabla_mostrar = gastos_filtrados_reset.drop(columns=["ID"]).copy()
    tabla_mostrar.index += 1  # Mostrar del 1 al N

    st.write("Selecciona el número de fila que quieres eliminar:")
    st.dataframe(tabla_mostrar)

    fila_a_eliminar = st.number_input(
        "Número de fila a eliminar (ver tabla arriba)", 
        min_value=1, 
        max_value=len(gastos_filtrados_reset), 
        step=1
    )

    if st.button("Eliminar gasto seleccionado"):
        fila_real = gastos_filtrados_reset.iloc[fila_a_eliminar - 1]
        id_fila = fila_real["ID"]

        df_original = ensure_ids(pd.read_csv(file_path))

        posibles = df_original[df_original["ID"] == id_fila]

        if not posibles.empty:
            df_actualizado = df_original.drop(posibles.index[0])
            df_actualizado.to_csv(file_path, index=False)
            st.success("✅ Gasto eliminado exitosamente.")
            try:
                st.experimental_rerun()
            except:
                pass
        else:
            st.warning("⚠️ No se encontró el gasto para eliminar. ¿Ya fue eliminado?")
else:
    st.info("No hay gastos para eliminar.")
