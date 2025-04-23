# ====== Start Login Block ======
from utils.login_manager import LoginManager
LoginManager().go_to_login('Start.py') 
# ====== End Login Block ======

import streamlit as st
import pandas as pd
from datetime import datetime
from utils.data_manager import DataManager
from functions.Blutzuckertagebuch import (
    load_blutzuckertagebuch,
    save_blutzuckertagebuch,
    add_entry,
    add_manual_entry,
    check_blutzuckerwert,
)

st.title("📖 Blutzuckertagebuch")

# Initialisiere den DataManager
data_manager = DataManager()

# Lade das Blutzuckertagebuch
tagebuch_df = load_blutzuckertagebuch(
    data_manager, 
    session_state_key="Blutzuckertagebuch", 
    file_name="blutzuckertagebuch.csv"
)

# Eingabefeld zur Erfassung des aktuellen Blutzuckerwerts
st.subheader("Aktuellen Blutzuckerwert erfassen")
with st.form("blutzuckertagebuch_form"):
    aktueller_blutzuckerwert = st.number_input("Aktueller Blutzuckerwert (mmol/L)", value=5.5, step=0.1)
    speichern = st.form_submit_button("Speichern")

if speichern:
    tagebuch_df = add_entry(tagebuch_df, aktueller_blutzuckerwert)
    save_blutzuckertagebuch(data_manager, tagebuch_df, "Blutzuckertagebuch")
    st.success("Eintrag erfolgreich gespeichert!")

    # Zugriff auf die unteren und oberen Grenzen aus den Einstellungen
    einstellungen = st.session_state.get("user_settings", {})
    grenzen = (einstellungen.get("untere_grenze", 4.0), einstellungen.get("obere_grenze", 8.0))

    # Vergleiche den aktuellen Wert mit den Grenzen
    status = check_blutzuckerwert(grenzen, aktueller_blutzuckerwert)
    if status == "low":
        st.warning("⚠️ Der Blutzuckerwert ist zu niedrig. Nehmen Sie schnell wirkende Kohlenhydrate zu sich, z. B.: " \
        "15 g Traubenzucker oder 1 Glas Fruchtsaft oder 1 kleines Glas Cola (kein „light“!)")
        st.info("⏱️ Messen Sie Ihren Blutzucker nach 15 Minuten erneut.")
    elif status == "high":
        st.warning("⚠️ Der Blutzuckerwert ist zu hoch. 💉 Bitte prüfen Sie, ob eine Korrektur mit Insulin notwendig ist.")

if st.button("Zum 🧮 Insulinbolus-Rechner"):
    st.switch_page("pages/2_Insulinbolus-Rechner.py")

# Eingabefeld zur Nacherfassung eines Blutzuckerwerts
st.subheader("Blutzuckerwert nacherfassen")
with st.form("nacherfassung_form"):
    nacherfassen_blutzuckerwert = st.number_input("Blutzuckerwert (mmol/L)", value=5.5, step=0.1, key="nacherfassen_blutzuckerwert")
    nacherfassen_datum = st.date_input("Datum", value=datetime.now().date(), key="nacherfassen_datum")
    nacherfassen_uhrzeit = st.time_input("Uhrzeit", value=datetime.now().time(), key="nacherfassen_uhrzeit")
    nacherfassen_speichern = st.form_submit_button("Nacherfassen")

if nacherfassen_speichern:
    tagebuch_df = add_manual_entry(tagebuch_df, nacherfassen_blutzuckerwert, nacherfassen_datum, nacherfassen_uhrzeit)
    save_blutzuckertagebuch(data_manager, tagebuch_df, "Blutzuckertagebuch")
    st.success("Nacherfassung erfolgreich gespeichert!")

