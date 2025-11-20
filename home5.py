import streamlit as st

st.title("Login")

logged_in = False
if st.button("Log in"):
    logged_in = True

if logged_in:
    st.wrtie("Welcome")
