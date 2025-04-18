# ====== Start Login Block ======
from utils.login_manager import LoginManager
LoginManager().go_to_login('Start.py') 
# ====== End Login Block ======


import streamlit as st
from utils.data_manager import DataManager

st.title("⚙️ Einstellungen")

data_manager = DataManager()

# Lade die gespeicherten Einstellungen (nur beim ersten Mal)
data_manager.load_user_data(
    session_state_key="user_settings",
    file_name="einstellungen.json",
    initial_value={"zielwert": 5.5, "korrekturfaktor": 0.0, "bolusfaktor": 0.0, "minimaler_bolusschritt": 0.1}
)

# Zugriff auf die gespeicherten Werte
user_settings = st.session_state["user_settings"]

# Anzeige und Bearbeitung
zielwert = st.number_input("Zielwert (mmol/L)", value=user_settings.get("zielwert", 5.5), step=0.1)
korrekturfaktor = st.number_input("Korrekturfaktor (mmol/L pro IE)", value=user_settings.get("korrekturfaktor", 1.5), step=0.1)
bolusfaktor = st.number_input("Bolusfaktor (IE pro 10g KH)", value=user_settings.get("bolusfaktor", 1.0), step=0.1)
minimaler_bolusschritt = st.selectbox("Minimaler Bolusschritt (IE)", [0.05, 0.1, 0.2, 0.5])

if st.button("💾 Speichern"):
    st.session_state["user_settings"] = {
        "zielwert": round(zielwert, 1),
        "korrekturfaktor": round(korrekturfaktor, 1),
        "bolusfaktor": round(bolusfaktor, 1),
        "minimaler_bolusschritt": round(minimaler_bolusschritt, 1)
    }

    data_manager.save_data("user_settings")
    st.success("Einstellungen wurden gespeichert.")