# ====== Start Login Block ======
from utils.login_manager import LoginManager
LoginManager().go_to_login('Start.py') 
# ====== End Login Block ======

import streamlit as st
import pandas as pd
from datetime import datetime
from utils.data_manager import DataManager

st.title("📖 Blutzuckertagebuch")

# Initialisiere den DataManager
data_manager = DataManager()

# Lade das Blutzuckertagebuch aus der persistenten Speicherung
data_manager.load_user_data(
    session_state_key="Blutzuckertagebuch",
    file_name="blutzuckertagebuch.csv",
    initial_value=pd.DataFrame(columns=["timestamp", "blutzuckerwert"]),
    parse_dates=["timestamp"],
)

# Zugriff auf das Blutzuckertagebuch
tagebuch_df = st.session_state["Blutzuckertagebuch"]

# Eingabefeld zur Erfassung des aktuellen Blutzuckerwerts
st.subheader("Aktuellen Blutzuckerwert erfassen")
with st.form("blutzuckertagebuch_form"):
    aktueller_blutzuckerwert = st.number_input("Aktueller Blutzuckerwert (mmol/L)", value=5.5, step=0.1)
    speichern = st.form_submit_button("Speichern")

if speichern:
    # Füge den neuen Eintrag mit Timestamp hinzu
    neuer_eintrag = {"timestamp": datetime.now(), "blutzuckerwert": aktueller_blutzuckerwert}
    tagebuch_df = pd.concat([tagebuch_df, pd.DataFrame([neuer_eintrag])], ignore_index=True)
    
    # Aktualisiere den Session State und speichere die Daten
    st.session_state["Blutzuckertagebuch"] = tagebuch_df
    data_manager.save_data("Blutzuckertagebuch")
    st.success("Eintrag erfolgreich gespeichert!")

# Eingabefeld zur Nacherfassung eines Blutzuckerwerts
st.subheader("Blutzuckerwert nacherfassen")
with st.form("nacherfassung_form"):
    nacherfassen_blutzuckerwert = st.number_input("Blutzuckerwert (mmol/L)", value=5.5, step=0.1, key="nacherfassen_blutzuckerwert")
    nacherfassen_datum = st.date_input("Datum", value=datetime.now().date(), key="nacherfassen_datum")
    nacherfassen_uhrzeit = st.time_input("Uhrzeit", value=datetime.now().time(), key="nacherfassen_uhrzeit")
    nacherfassen_speichern = st.form_submit_button("Nacherfassen")

if nacherfassen_speichern:
    # Kombiniere Datum und Uhrzeit zu einem Timestamp
    nacherfassen_timestamp = datetime.combine(nacherfassen_datum, nacherfassen_uhrzeit)
    neuer_eintrag = {"timestamp": nacherfassen_timestamp, "blutzuckerwert": nacherfassen_blutzuckerwert}
    tagebuch_df = pd.concat([tagebuch_df, pd.DataFrame([neuer_eintrag])], ignore_index=True)
    
    # Sortiere den DataFrame nach Datum und Uhrzeit
    tagebuch_df = tagebuch_df.sort_values(by="timestamp").reset_index(drop=True)
    
    # Aktualisiere den Session State und speichere die Daten
    st.session_state["Blutzuckertagebuch"] = tagebuch_df
    data_manager.save_data("Blutzuckertagebuch")
    st.success("Nacherfassung erfolgreich gespeichert!")

