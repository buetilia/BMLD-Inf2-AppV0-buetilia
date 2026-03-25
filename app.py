import pandas as pd
import streamlit as st
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

st.set_page_config(page_title="Kjeldahl App", page_icon="🧪")

dm = DataManager(fs_root_folder='Kjeldahl-Rechner')
lm = LoginManager(dm)

user_info = lm.login_register()

if user_info:
    st.session_state['user_info'] = user_info
    st.sidebar.success(f"Eingeloggt als: {user_info['firstname']}")

    if st.sidebar.button("Logout"):
        lm.logout()
        if 'user_info' in st.session_state:
            del st.session_state['user_info']
        st.rerun()

    if 'data_df' not in st.session_state:
        fetched_data = dm.load_user_data(user_info['username'])
        if fetched_data is not None and not fetched_data.empty:
            st.session_state['data_df'] = fetched_data
        else:
            st.session_state['data_df'] = pd.DataFrame(columns=[
                "Zeitstempel", "Volumen Probe (ml)", "Stickstoff (%)", "Protein (%)", "Faktor"
            ])

    pg_home = st.Page("views/home.py", title="Home", icon="🏠", default=True)
    pg_rechner = st.Page("views/unterseite_a.py", title="Kjeldahl-Rechner", icon="🧪")

    pg = st.navigation([pg_home, pg_rechner])
    pg.run()

else:
    st.info("Bitte loggen Sie sich ein oder registrieren Sie sich, um den Kjeldahl-Rechner zu nutzen.")

    try:
        pg_home = st.Page("views/home.py", title="Home", icon="🏠", default=True)
        pg_rechner = st.Page("views/unterseite_a.py", title="Kjeldahl-Rechner", icon="🧪")

        pg = st.navigation([pg_home, pg_rechner])
        pg.run()
    except Exception as e:
        st.error(f"Fehler beim Laden der Seiten: {e}")