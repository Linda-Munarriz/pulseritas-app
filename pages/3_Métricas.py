import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Debes iniciar sesión primero.")
    st.stop()

st.title("📊 Dashboard de Métricas")

file_path = "data/ventas.csv"

# Verifica si hay datos
if not os.path.exists(file_path):
    st.warning("Aún no se han registrado ventas.")
    st.stop()

# Cargar datos
ventas = pd.read_csv(file_path)
ventas['Fecha'] = pd.to_datetime(ventas['Fecha'])

# Cálculos
total_desayunos_soles = ventas['Desayunos'].sum()
total_desayunos = int(total_desayunos_soles // 3)  # Solo contar desayunos completos
gastos_file = "data/gastos.csv"
if os.path.exists(gastos_file):
    gastos = pd.read_csv(gastos_file)
    total_gastos = gastos["Monto"].sum()
else:
    total_gastos = 0

total_reinversion_bruto = ventas['Reinversión'].sum()
total_reinversion = total_reinversion_bruto - total_gastos
total_ventas = ventas['Cantidad'].sum()
dinero_para_desayunos = total_desayunos * 3  # En soles

# Mostrar métricas
col1, col2 = st.columns(2)
col1.metric("🍞 Total Desayunos Financiados", f"{total_desayunos} desayunos")
col2.metric("💰 Fondo Reinv. Acumulado", f"S/ {total_reinversion:.2f}")

col3, col4 = st.columns(2)
corazon_count = ventas[ventas["Producto"] == "Pulsera Corazón"]["Cantidad"].sum()
power_count = ventas[ventas["Producto"] == "Pulsera Power"]["Cantidad"].sum()

col3.metric("📦 Ventas Totales", f"{total_ventas} pulseras")
col3.caption(f"💖 Corazón: {corazon_count} | 💪 Power: {power_count}")
col4.metric("🧾 Dinero para desayunos", f"S/ {dinero_para_desayunos:.2f}")

st.divider()

# 📆 Gráfica de líneas: Ventas por día
st.subheader("📆 Ventas por día")
diarias = ventas.groupby('Fecha')["Cantidad"].sum()
st.line_chart(diarias)

# 📊 Histograma: por tipo de pulsera
st.subheader("📊 Ventas por tipo de pulsera")

if not ventas['Producto'].dropna().empty:
    fig, ax = plt.subplots(figsize=(6, 4))
    ventas['Producto'].value_counts().plot(kind='bar', color=['#ffb6c1', '#f08080'], ax=ax)
    ax.set_xlabel("Tipo de pulsera")
    ax.set_ylabel("Cantidad")
    ax.set_title("Ventas por tipo de pulsera")
    st.pyplot(fig)
else:
    st.info("📭 No hay datos suficientes para mostrar esta gráfica.")

# 🗑️ Eliminar última venta
st.subheader("❌ Eliminar última venta (en caso de error)")
if st.button("Eliminar la última venta registrada"):
    ventas = ventas[:-1]
    ventas.to_csv(file_path, index=False)
    st.success("Última venta eliminada con éxito. Recarga la página.")
