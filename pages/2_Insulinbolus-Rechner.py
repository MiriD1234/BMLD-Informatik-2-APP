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
    berechne_gerundeter_gesamt_bolus
)

st.title("💉 Insulin-Bolus-Rechner")

data_manager = DataManager()

data_manager.load_user_data(
    session_state_key="user_settings",
    file_name="einstellungen.json",
    initial_value={"zielwert": 5.5, "korrekturfaktor": 1.5, "bolusfaktor": 1.0}
)

einstellungen = st.session_state["user_settings"]
zielwert = einstellungen["zielwert"]
korrekturfaktor = einstellungen["korrekturfaktor"]
bolusfaktor = einstellungen["bolusfaktor"]
minimaler_bolusschritt = einstellungen["minimaler_bolusschritt"]

col1, col2 = st.columns(2)

with col1:
    with st.form("bolus_rechner_form"):
        st.subheader("Eingaben")

        aktueller_wert = st.number_input("Aktueller Blutzuckerwert (mmol/L)", value=6.0, step=0.1)
        kohlenhydrate = st.number_input("Kohlenhydratmenge (g)", value=0)
        aktives_insulin = st.number_input("Aktives Insulin (IE)", value=0.0, step=0.1)

        berechnen = st.form_submit_button("Berechnen")

with col2:
    st.write(f"**Blutzucker-Zielwert:** {zielwert} mmol/L")
    st.write(f"**Korrekturfaktor:** {korrekturfaktor} mmol/L pro IE Insulin")
    st.write(f"**Bolusfaktor:** {bolusfaktor} IE pro 10g Kohlenhydrate")
    st.write(f"**Minimaler Bolusschritt:** {minimaler_bolusschritt} IE")

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



