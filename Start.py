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
    session_state_key="dosis_erfassung",
    file_name="dosis_erfassung.csv",
    initial_value=pd.DataFrame(),
    parse_dates=["timestamp"],
    )

data_manager.load_user_data(
    session_state_key="Blutzuckertagebuch",
    file_name="blutzuckertagebuch.csv",
    initial_value=pd.DataFrame(),
    parse_dates=["timestamp"],
    )

data_manager.load_user_data(
    session_state_key="user_settings",
    file_name="einstellungen.json",
    initial_value={"zielwert": 5.5, "korrekturfaktor": 0.0, "zeitfenster_bolusfaktoren": {"00:00-10:59": 0.0, "11:00-16:59": 0.0, "17:00-23:59": 0.0}, "minimaler_bolusschritt": 0.1, "wirkdauer_insulin": 4, "untere_grenze": 4.0, "obere_grenze": 8.0}
)
# ====== End Init Block ======

import streamlit as st

st.image("docs/Fotos/Logo_Version_1.jpg", width=400)

if st.button("📖 Blutzuckertagebuch"):
    st.switch_page("pages/3_Blutzuckertagebuch.py")

if st.button("🧮 Insulinbolus-Rechner"):
    st.switch_page("pages/2_Insulinbolus-Rechner.py")

if st.button("📈 Verlauf"):
    st.switch_page("pages/4_Verlauf.py")

if st.button("⚙️ Einstellungen"):
    st.switch_page("pages/1_Einstellungen.py")

st.info("""Diese App ersetzt keine medizinische Beratung. Änderungen Ihrer Therapie sollten nur in Absprache mit Ihrem Arzt erfolgen.""")