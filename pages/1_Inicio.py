import streamlit as st

if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Debes iniciar sesión primero.")
    st.stop()

st.title("🎀 Bienvenida a Pulseritas Co")
st.markdown(f"Hola, **{st.session_state.username}** 👋")

st.subheader("¿Qué deseas hacer hoy?")

# Menú de navegación con botones
col1, col2 = st.columns(2)

with col1:
    if st.button("📝 Reportar venta"):
        st.switch_page("pages/2_Reporte_de_Ventas.py")

    if st.button("📊 Ver métricas"):
        st.switch_page("pages/3_Métricas.py")

with col2:
    if st.button("💸 Registrar gasto"):
        st.switch_page("pages/4_Registrar_Gastos.py")

    if st.button("🔒 Cerrar sesión"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.success("Sesión cerrada. Recarga la página.")
        st.stop()
