import streamlit as st
from utils.login import login_user

st.set_page_config(
    page_title="Pulseritas Co.",
    page_icon="🎀",
    layout="centered"
)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ''

if not st.session_state.logged_in:
    st.title("Pulseritas Co. – Inicio de Sesión")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Iniciar sesión"):
        if login_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Inicio de sesión exitoso 💗. Ve al menú de la izquierda.")
            st.stop()
        else:
            st.error("Credenciales incorrectas 💔")
else:
    st.switch_page("pages/1_Inicio.py")
