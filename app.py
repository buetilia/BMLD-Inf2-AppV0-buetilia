import pandas as pd 
import streamlit as st

st.set_page_config(page_title="Kjeldahl-Rechner")

from utils.data_manager import DataManager
from utils.login_manager import LoginManager

if 'dm' not in st.session_state:
    st.session_state['dm'] = DataManager(       
        fs_protocol='webdav',         
        fs_root_folder="Kjeldahl-Rechner"
    )

dm_object = st.session_state['dm']

login_manager = LoginManager(dm_object)

with st.sidebar:
    user_info = login_manager.login_register()

if user_info:
    st.session_state['user_info'] = user_info

    if 'data_df' not in st.session_state:
        st.session_state['data_df'] = dm_object.load_user_data(
            user_info['username'],                    
            initial_value=pd.DataFrame(columns=["Zeitstempel", "Volumen Probe (ml)", "Stickstoff (%)", "Protein (%)", "Faktor"]),   
            parse_dates=['timestamp']       
        )

pg_home = st.Page("views/home.py", title="Home", icon=":material/home:", default=True)
pg_calculator = st.Page("views/unterseite_a.py", title="Kjeldahl-Rechner", icon=":material/science:")
pg_viz = st.Page("views/viz.py", title="Kjeldahl Grafik", icon=":material/show_chart:")

pg = st.navigation([pg_home, pg_calculator, pg_viz])
pg.run()
