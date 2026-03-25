import pandas as pd 
import streamlit as st

st.set_page_config(page_title="Kjeldahl-Rechner")

from utils.data_manager import DataManager
from utils.login_manager import LoginManager

data_manager = DataManager(       # initialize data manager
    fs_protocol='webdav',         
    fs_root_folder="Kjeldahl-Rechner (2)"  # folder on switch drive where the data is stored
    ) 
login_manager = LoginManager(data_manager) # handles user login and registration
login_manager.login_register() 

if 'data_df' not in st.session_state:
    st.session_state['data_df'] = data_manager.load_user_data(
        "data.csv",                    
        initial_value=pd.DataFrame()    
   )

pg_home = st.Page("views/home.py", title="Home", icon=":material/home:", default=True)
pg_calculator = st.Page("views/unterseite_a.py", title="Kjeldahl-Rechner", icon=":material/science:")
pg_viz = st.Page("views/viz.py", title="Kjeldahl Grafik", icon=":material/show_chart:")

pg = st.navigation([pg_home, pg_calculator, pg_viz])
pg.run()
