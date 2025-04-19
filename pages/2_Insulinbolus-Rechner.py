# ====== Start Login Block ======
from utils.login_manager import LoginManager
LoginManager().go_to_login('Start.py') 
# ====== End Login Block ======

import streamlit as st
import pandas as pd
from utils.data_manager import DataManager
from utils import helpers
from functions.Insulinbolus import (
    berechne_korrektur_bolus,
    berechne_mahlzeiten_bolus,
    berechne_gesamt_bolus,
    berechne_gerundeter_gesamt_bolus,
    get_bolusfaktor_for_current_time  # Import der neuen Funktion
)
from datetime import datetime, timedelta

# Start Rechner

st.title("💉 Insulinbolus-Rechner")

data_manager = DataManager()

data_manager.load_user_data(
    session_state_key="user_settings",
    file_name="einstellungen.json",
    initial_value={"zielwert": 5.5, "korrekturfaktor": 0.0, "zeitfenster_bolusfaktoren": {"00:00-10:59": 0.0, "11:00-16:59": 0.0, "17:00-23:59": 0.0}, "minimaler_bolusschritt": 0.1, "wirkdauer_insulin": 4}
)

einstellungen = st.session_state["user_settings"]
zielwert = einstellungen["zielwert"]
korrekturfaktor = einstellungen["korrekturfaktor"]
minimaler_bolusschritt = einstellungen["minimaler_bolusschritt"]

# Bolusfaktor basierend auf der aktuellen Uhrzeit auswählen
zeitfenster_bolusfaktoren = einstellungen.get("zeitfenster_bolusfaktoren", {})
try:
    bolusfaktor = get_bolusfaktor_for_current_time(zeitfenster_bolusfaktoren)
except ValueError as e:
    st.error(str(e))
    bolusfaktor = 0  # Fallback, falls kein Bolusfaktor gefunden wird

# Wirkdauer des Insulins aus den Einstellungen laden
wirkdauer_insulin = einstellungen.get("wirkdauer_insulin", 4)  # Standardwert: 4 Stunden

# Berechnung des aktiven Insulins basierend auf der letzten Dosis
letzte_dosis_df = st.session_state.get("dosis_erfassung", pd.DataFrame())

# Überprüfen, ob der DataFrame nicht leer ist
if not letzte_dosis_df.empty:
    # Letzte Zeile des DataFrames abrufen
    letzte_dosis = letzte_dosis_df.iloc[-1]
    
    # Prüfen, ob der Timestamp bereits ein datetime-Objekt ist
    if isinstance(letzte_dosis["timestamp"], pd.Timestamp):
        letzte_dosis_zeitpunkt = letzte_dosis["timestamp"].to_pydatetime()  # In datetime umwandeln
    else:
        letzte_dosis_zeitpunkt = datetime.strptime(letzte_dosis["timestamp"], "%Y-%m-%d %H:%M:%S")
    
    zeit_seit_letzter_dosis = datetime.now() - letzte_dosis_zeitpunkt

    if zeit_seit_letzter_dosis > timedelta(hours=wirkdauer_insulin):
        aktives_insulin = 0  # Insulin ist nicht mehr aktiv
    else:
        aktives_insulin = letzte_dosis["gerundeter_gesamt_bolus"]  # Verwende die letzte Dosis
else:
    aktives_insulin = 0  # Keine Dosis erfasst, daher kein aktives Insulin

col1, col2 = st.columns(2)

with col1:
    with st.form("bolus_rechner_form"):
        st.subheader("Eingaben")

        aktueller_wert = st.number_input("Aktueller Blutzuckerwert (mmol/L)", value=6.0, step=0.1)
        kohlenhydrate = st.number_input("Kohlenhydratmenge (g)", value=0)

        berechnen = st.form_submit_button("Berechnen")

with col2:
    st.write(f"**Blutzucker-Zielwert:** {zielwert} mmol/L")
    st.write(f"**Korrekturfaktor:** {korrekturfaktor} mmol/L pro IE Insulin")
    st.write(f"**Bolusfaktor:** {bolusfaktor} IE pro 10g Kohlenhydrate")
    st.write(f"**Minimaler Bolusschritt:** {minimaler_bolusschritt} IE")
    st.write(f"**Wirkdauer Insulin:** {wirkdauer_insulin} Stunden")
    st.write(f"**Aktives Insulin:** {aktives_insulin:.2f} IE")

if berechnen:
    if korrekturfaktor <= 0 or bolusfaktor <= 0:
        st.error("Korrekturfaktor und Bolusfaktor müssen größer als 0 sein. Bitte erfasse deine persönlichen Berechnungsfaktoren in den Einstellungen.")
    else:
        korrektur_bolus_data = berechne_korrektur_bolus(aktueller_wert, zielwert, korrekturfaktor)
        mahlzeiten_bolus_data = berechne_mahlzeiten_bolus(kohlenhydrate, bolusfaktor)
        gesamt_bolus_data = berechne_gesamt_bolus(
            korrektur_bolus_data["korrektur_bolus"],
            mahlzeiten_bolus_data["mahlzeiten_bolus"],
            aktives_insulin
        )
        gesamt_bolus_gerundet_data = berechne_gerundeter_gesamt_bolus(
            gesamt_bolus_data["gesamt_bolus"],
            minimaler_bolusschritt
        )

        # Kombiniere alle Daten in ein einziges Dictionary
        result_dict = {
            **korrektur_bolus_data,
            **mahlzeiten_bolus_data,
            **gesamt_bolus_data,
            **gesamt_bolus_gerundet_data,
        }

        # Speichere die Ergebnisse in der Session State
        st.session_state["berechnung_ergebnisse"] = result_dict
        st.session_state["berechnung_durchgefuehrt"] = True  # Markiere Berechnung als durchgeführt

        st.success("✅ Berechnung erfolgreich!")
        st.write("### Ergebnisse:")
        st.write(f"Korrektur-Bolus: {korrektur_bolus_data['korrektur_bolus']:.2f} IE")
        st.write(f"Mahlzeiten-Bolus: {mahlzeiten_bolus_data['mahlzeiten_bolus']:.2f} IE")
        st.write(f"Gesamt-Bolus (ungerundet): {gesamt_bolus_data['gesamt_bolus']:.2f} IE")
        st.write(f"**Gesamt-Bolus (gerundet): {gesamt_bolus_gerundet_data['gerundeter_gesamt_bolus']:.2f} IE**")

        if gesamt_bolus_gerundet_data["gerundeter_gesamt_bolus"] > 15:
            st.warning("⚠️ Achtung: Der berechnete Bolus ist ungewöhnlich hoch. Bitte Eingaben prüfen.")
        elif gesamt_bolus_gerundet_data["gerundeter_gesamt_bolus"] == 0:
            st.info("ℹ️ Kein Bolus notwendig auf Basis der aktuellen Eingaben.")

# Buttons nur anzeigen, wenn die Berechnung durchgeführt wurde
if st.session_state.get("berechnung_durchgefuehrt", False):
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Zurücksetzen", key="zuruecksetzen_button"):
            # Entferne die Berechnungsergebnisse aus der Session State
            del st.session_state["berechnung_ergebnisse"]
            st.session_state["berechnung_durchgefuehrt"] = False  # Setze Berechnungsstatus zurück
            st.info("🔄 Berechnungen wurden zurückgesetzt.")

    with col2:
        if st.button("Dosis erfassen", key="dosis_erfassen_button"):
            # Speichere das Dictionary in der Session State
            data_manager.append_record(session_state_key="dosis_erfassung", record_dict=st.session_state["berechnung_ergebnisse"])
            st.success("✅ Dosis erfolgreich erfasst!")



