import pandas as pd
import streamlit as st
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

st.set_page_config(page_title="Meine App", page_icon=":material/home:")

dm = DataManager(fs_root_folder='Kjeldahl_Projekt')
lm = LoginManager(dm)

user_info = lm.login_register()

if user_info:
    st.sidebar.success(f"Eingeloggt als: {user_info['firstname']}")
    st.session_state['user_info'] = user_info

if 'user_info' in st.session_state and st.session_state['user_info']:
    st.sidebar.success(f"Eingeloggt als: {st.session_state['user_info']['firstname']}")

    if st.sidebar.button("Logout"):
        del st.session_state['user_info']
        lm.logout()
        st.rerun()

    if 'data_df' not in st.session_state:
        st.session_state['data_df'] = dm.load_user_data(user_info['username'])

    if st.session_state['data_df'] is None or st.session_state['data_df'].empty:
            st.session_state['data_df'] = pd.DataFrame(columns=[
            "Zeitstempel", "Volumen Probe (ml)", "Konzentration (mol/L)","Stickstoff (%)", "Protein (%)", "Faktor"])
        
    pg_home = st.Page("views/home.py", title="Home", icon=":material/home:", default=True)
    pg_second = st.Page("views/unterseite_a.py", title="Kjeldahl-Rechner", icon=":material/info:")

    pg = st.navigation([pg_home, pg_second])
    pg.run()
else:
    st.info("Bitte loggen Sie sich ein oder registrieren Sie sich, um den Kjeldahl-Rechner zu nutzen.")




