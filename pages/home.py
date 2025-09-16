import streamlit as st
from menu.cost_management import CostManagement
from menu.management_billing import ManegementBilling
from utils.components import *
from utils.user import *
from data.get_data import *
# Theme functionality removed - using Streamlit's built-in theming

def render():
    user_id = st.session_state['user_data']["data"]["user_id"]
    user_name = st.session_state['user_data']["data"]['full_name']
    user_email = st.session_state['user_data']["data"]["session"]["username"]
    # Theme detection - using default theme
    st.session_state["base_theme"] = "default"
    col1, col2, col3 = st.columns([3.5,0.4,0.3])
    
    col1.write(f"## Olá, "+user_name)
    col2.image("./assets/imgs/eshows100x100.png")
    col3.markdown("<p style='padding-top:0.7em'></p>", unsafe_allow_html=True)
    col3.button(label="Logout", on_click=logout)
    
    component_effect_underline()
    st.write('## Resultados Consolidados')
    st.markdown('<div class="full-width-line-white"></div>', unsafe_allow_html=True)
    st.markdown('<div class="full-width-line-black"></div>', unsafe_allow_html=True)

    col6, col7, col8, = st.columns([3.4,0.2,0.4])
    col8.button(label="Atualizar", on_click = st.cache_data.clear)
    
    data = initialize_data(user_id)
    # data = get_data(data) 

    allowed_tabs = get_allowed_tabs(user_email)
    
    if not allowed_tabs:
        st.warning("⚠ Você não possui acesso a nenhuma aba.")
    else:
        tabs = st.tabs(allowed_tabs)
        tab_list = {
            "Faturamento Eshows Gerencial": ManegementBilling,
            "Gerenciamento de Custos": CostManagement,
        }
        for tab, tab_name in zip(tabs, allowed_tabs):
            with tab:
                if tab_name in tab_list:
                    page = tab_list[tab_name]()
                    page.render()

if __name__ == "__main__":
    if 'jwt_token' not in st.session_state:
        st.switch_page("main.py")
    
    st.set_page_config(page_title="Home | Relatorio Eshows",page_icon="./assets/imgs/eshows-logo100x100.png", layout="wide")

    component_hide_sidebar()
    component_fix_tab_echarts()

    if 'user_data' in st.session_state:
        render()
    else:
        st.switch_page("main.py")