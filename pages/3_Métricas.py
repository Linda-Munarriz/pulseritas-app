import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Debes iniciar sesión primero.")
    st.stop()

st.title("📊 Dashboard de Métricas")

file_path = "data/ventas.csv"
if not os.path.exists(file_path):
    st.warning("Aún no se han registrado ventas.")
    st.stop()

ventas = pd.read_csv(file_path)
ventas['Fecha'] = pd.to_datetime(ventas['Fecha'])

st.metric("🍞 Total Desayunos Financiados", f"{ventas['Desayunos'].sum():.2f} soles")
st.metric("💰 Fondo de Reinv. Acumulado", f"{ventas['Reinversión'].sum():.2f} soles")
st.metric("📦 Total Ventas", f"{ventas['Cantidad'].sum()} pulseras")

# 📆 Gráfica de líneas: Ventas por día
diarias = ventas.groupby('Fecha')["Cantidad"].sum()
st.line_chart(diarias)

# 📊 Histograma: por tipo de pulsera
fig, ax = plt.subplots()
ventas['Producto'].value_counts().plot(kind='bar', ax=ax)
ax.set_title("Frecuencia por Tipo de Pulsera")
ax.set_ylabel("Cantidad de ventas")
st.pyplot(fig)
