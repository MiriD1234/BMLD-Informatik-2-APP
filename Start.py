# ====== Start Init Block ======
import pandas as pd
from utils.data_manager import DataManager
from utils.login_manager import LoginManager
import streamlit as st

# initialize the data manager
data_manager = DataManager(fs_protocol='webdav', fs_root_folder="BMLD_GlucoBuddy")  # switch drive 

# initialize the login manager
login_manager = LoginManager(data_manager)
login_manager.login_register()

# Überprüfen, ob der Benutzer eingeloggt ist
if st.session_state.get("authentication_status") is True:
    # laden der nutzerspezifischen Daten von Switchdrive in die session state
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
else:
    st.warning("Bitte loggen Sie sich ein, um auf Ihre Daten zuzugreifen.")
# ====== End Init Block ======

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

# Erklärung wichtiger Begriffe
st.subheader("ℹ️ Wichtige Begriffe")
st.markdown("""
- **Blutzuckerwert (mmol/L):** Der aktuelle Zuckergehalt im Blut, gemessen in Millimol pro Liter. Ein normaler Bereich liegt typischerweise zwischen 4.0 und 8.0 mmol/L.
- **Insulinbolus:** Eine zusätzliche Insulindosis, die vor Mahlzeiten oder zur Korrektur eines hohen Blutzuckerspiegels verabreicht wird.
- **Bolusfaktor:** Gibt an, wie viel Insulin pro 10 g Kohlenhydrate benötigt wird.
- **Korrekturfaktor:** Gibt an, um wie viel mmol/l der Blutzucker durch eine Einheit Insulin gesenkt wird.
- **HbA1c:** Der HbA1c-Wert wird verwendet, um den Blutzuckerspiegel der letzten 3 Monate zu beurteilen.
            Ein höherer HbA1c-Wert bedeutet, dass der Blutzucker über einen längeren Zeitraum erhöht war. 
- **Wirkdauer Insulin:** Die Zeit, in der das Insulin aktiv im Körper wirkt.
- **Minimaler Bolusschritt:** Die kleinste Menge Insulin, die verabreicht werden kann.
""")

# Formel zur Bolusberechnung
st.subheader("Formel zur Bolusberechnung")
st.markdown(""" Die Berechnung des Insulinbolus erfolgt mit der folgenden Formel:""")
st.latex(r"""
    \frac{\text{aktueller Blutzucker} - \text{Blutzucker-Zielwert}}{\text{Korrekturfaktor}} + \frac{\text{Kohlenhydrate in g}}{10} \cdot \text{Bolusfaktor} - \text{aktives Insulin}
""")