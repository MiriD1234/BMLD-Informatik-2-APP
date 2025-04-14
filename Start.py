# ====== Start Init Block ======
import pandas as pd
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# initialize the data manager
data_manager = DataManager(fs_protocol='webdav', fs_root_folder="BMLD_GlucoBuddy")  # switch drive 

# initialize the login manager
login_manager = LoginManager(data_manager)
login_manager.login_register()  # open login/register page

# load the data from the persistent storage into the session state
data_manager.load_user_data(
    session_state_key='data_df', 
    file_name='data.csv', 
    initial_value = pd.DataFrame(), 
    parse_dates = ['timestamp']
    )
# ====== End Init Block ======

import streamlit as st

st.title("GlucoBuddy")

if st.button("🧮 Insulinbolus-Rechner"):
    st.switch_page("pages/2_Insulinbolus-Rechner.py")

if st.button("⚙️ Einstellungen"):
    st.switch_page("pages/1_Einstellungen.py")

st.info("""Diese App ersetzt keine medizinische Beratung. Änderungen Ihrer Therapie sollten nur in Absprache mit Ihrem Arzt erfolgen.""")