import streamlit as st

if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Debes iniciar sesión primero.")
    st.stop()

st.title("🎀 Bienvenida a Pulseritas Co")
st.write(f"Hola, {st.session_state.username}! Gracias por tu trabajo solidario 💕")
