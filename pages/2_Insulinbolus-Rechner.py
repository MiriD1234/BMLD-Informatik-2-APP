# ====== Start Login Block ======
from utils.login_manager import LoginManager
LoginManager().go_to_login('Start.py') 
# ====== End Login Block ======

import streamlit as st
from functions.Insulinbolus import (berechne_korrektur_bolus, berechne_mahlzeiten_bolus, berechne_gesamt_bolus)

# Form für Eingaben und Berechnung
st.title("💉 Insulin-Bolus-Rechner")

with st.form("bolus_rechner_form"):
    st.subheader("Eingaben")

    zielwert = st.number_input("Blutzucker-Zielwert (mmol/L)", value=5.5, step=0.1)
    aktueller_wert = st.number_input("Aktueller Blutzuckerwert (mmol/L)", value=6.0, step=0.1)
    korrekturfaktor = st.number_input("Korrekturfaktor (mmol/L pro IE Insulin)", value=1.5, step=0.1)
    kohlenhydrate = st.number_input("Kohlenhydratmenge (g)", value=0)
    bolusfaktor = st.number_input("Bolusfaktor (Insulin pro 10g Kohlenhydrate)", value=1.0, step=0.1)
    aktives_insulin = st.number_input("Aktives Insulin (IE)", value=0.0, step=0.1)
    minimaler_bolusschritt = st.selectbox("Minimaler Bolusschritt (IE)", [0.05, 0.1, 0.2, 0.5])

    berechnen = st.form_submit_button("Berechnen")

if berechnen:
    try:
        korrektur_bolus = berechne_korrektur_bolus(aktueller_wert, zielwert, korrekturfaktor)
        mahlzeiten_bolus = berechne_mahlzeiten_bolus(kohlenhydrate, bolusfaktor)
        gesamt_bolus = berechne_gesamt_bolus(korrektur_bolus, mahlzeiten_bolus, aktives_insulin)

        gerundeter_gesamt_bolus = round(gesamt_bolus / minimaler_bolusschritt) * minimaler_bolusschritt

        st.success("✅ Berechnung erfolgreich!")
        st.write("### Ergebnisse:")
        st.write(f"Korrektur-Bolus: {korrektur_bolus:.2f} IE")
        st.write(f"Mahlzeiten-Bolus: {mahlzeiten_bolus:.2f} IE")
        st.write(f"Gesamt-Bolus (ungerundet): {gesamt_bolus:.2f} IE")
        st.write(f"**Gesamt-Bolus (gerundet): {gerundeter_gesamt_bolus:.2f} IE**")

        if gerundeter_gesamt_bolus > 15:
            st.warning("⚠️ Achtung: Der berechnete Bolus ist ungewöhnlich hoch. Bitte Eingaben prüfen.")
        elif gerundeter_gesamt_bolus == 0:
            st.info("ℹ️ Kein Bolus notwendig auf Basis der aktuellen Eingaben.")

    except ValueError as e:
        st.error(f"Fehler: {e}")

st.markdown("---")