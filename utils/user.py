import streamlit as st
from data.querys_grupoe import collaborator_access
    
def logout():
    st.session_state.clear()
    st.session_state['page'] = 'login'
    st.cache_data.clear()

def get_allowed_tabs(email):
    access_levels = collaborator_access(email)
    
    allowed_tabs = []

    if 'Basico' in access_levels:
        allowed_tabs.append("Faturamento Eshows Gerencial")
    if 'Comercial' in access_levels:
        allowed_tabs.append("Faturamento Eshows Gerencial")
    if 'Adm' in access_levels:
        allowed_tabs.append("Faturamento Eshows Gerencial")
        allowed_tabs.append("Gerenciamento de Custos")

    return allowed_tabs