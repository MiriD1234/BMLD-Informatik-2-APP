# ====== Start Login Block ======
from utils.login_manager import LoginManager
import streamlit as st
col3, col4, col5, col6= st.columns(4)

# ====== Start Login Block ======
from utils.login_manager import LoginManager
with col6:
    LoginManager().go_to_login('Start.py') 
# ====== End Login Block ======
with col3:
    if st.button("🏠 Home"):
        st.switch_page("Start.py")
# ====== End Login Block ======

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from utils.data_manager import DataManager
from functions.Blutzuckertagebuch import (
    create_blutzucker_figure,
)
from functions.Insulinbolus import create_insulin_dose_figure
from functions.HbA1c import berechne_hba1c

st.title("📈 Verlauf der Blutzuckerwerte")

# Initialisiere DataManager
data_manager = DataManager()

# Lade das Blutzuckertagebuch
data_df = st.session_state['Blutzuckertagebuch']
if data_df.empty:
    st.info('Keine Blutzucker Daten vorhanden. Bitte fügen Sie Blutzuckerwerte hinzu.')
    st.stop()

# Sortiere die Daten nach timestamp
data_df = data_df.sort_values(by='timestamp')

# Lade Benutzereinstellungen (Grenzwerte)
data_manager.load_user_data(
    session_state_key="user_settings",
    file_name="einstellungen.json",
    initial_value={"untere_grenze": 4.0, "obere_grenze": 8.0}
)
user_settings = st.session_state["user_settings"]
untere_grenze = user_settings.get("untere_grenze", 4.0)
obere_grenze = user_settings.get("obere_grenze", 8.0)

# Erstelle die Grafik
fig = create_blutzucker_figure(data_df, untere_grenze, obere_grenze)

# Anzeige in Streamlit
st.plotly_chart(fig, use_container_width=True)

# HbA1c-Schätzung
st.subheader("Berechnung HbA1c-Schätzungswert")

# Berechnung des HbA1c-Werts
result = berechne_hba1c(data_df)

if result:
    hba1c_gerundet, farbe, bewertung, anzahl_messwerte = result
    # Anzeige
    st.metric("🧪 Geschätzter HbA1c (aus Blutzucker ⌀)", f"{hba1c_gerundet} %")
    st.markdown(f"**{farbe} {bewertung}** – basierend auf {anzahl_messwerte} Werten in den letzten 90 Tagen")
    st.warning("ℹ️ Der HbA1c-Wert ist ein wichtiger Indikator für die Langzeitkontrolle des Blutzuckerspiegels. Diese Schätzung ist nicht für die Diagnose geeignet. Bitte konsultieren Sie Ihren Arzt für eine genaue Diagnose.")
else:
    st.info("Nicht genügend Messwerte für verlässliche HbA1c-Berechnung oder keine Blutzuckerwerte aus den letzten 3 Monaten vorhanden.")

# Verlauf der Insulin-Dosen
st.title("📈 Verlauf der verabreichten Insulin-Dosen 💉")

# Lade die verabreichten Insulin-Dosen
dosis_df = st.session_state.get("dosis_erfassung", pd.DataFrame())
if dosis_df.empty:
    st.info("ℹ️ Keine verabreichten Insulin-Dosen verfügbar.")
else:
    try:
        # Erstelle die Grafik
        fig_dosen = create_insulin_dose_figure(dosis_df)
        # Anzeige in Streamlit
        st.plotly_chart(fig_dosen, use_container_width=True)
    except ValueError as e:
        st.warning(str(e))
