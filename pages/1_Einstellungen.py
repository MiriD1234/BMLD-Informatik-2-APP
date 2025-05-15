# ====== Start Login Block ======
from utils.login_manager import LoginManager
import streamlit as st

col3, col4, col5, col6= st.columns(4)

with col6:
    LoginManager().go_to_login('Start.py') 
# ====== End Login Block ======
with col3:
    if st.button("🏠 Home"):
        st.switch_page("Start.py")

from utils.data_manager import DataManager

st.title("⚙️ Einstellungen")

# Initialisiere den DataManager
data_manager = DataManager()

# Zugriff auf die gespeicherten Werte
user_settings = st.session_state["user_settings"]

# Anzeige und Bearbeitung
st.subheader("Blutzuckerwerte")
zielwert = st.number_input("Zielwert (mmol/L)", value=user_settings.get("zielwert", 5.5), step=0.1)
untere_grenze = st.number_input("Untere Grenze (mmol/L)", value=user_settings.get("untere_grenze", 4.0), step=0.1)
obere_grenze = st.number_input("Obere Grenze (mmol/L)", value=user_settings.get("obere_grenze", 8.0), step=0.1)

# Erfassen von Bolusfaktoren für drei feste Zeitfenster
st.subheader("Bolusfaktoren")
bolusfaktor_1 = st.number_input("Bolusfaktor für 00:00-10:59 Uhr (IE pro 10g KH)", value=user_settings.get("zeitfenster_bolusfaktoren", {}).get("00:00-10:59", 1.0), step=0.1)
bolusfaktor_2 = st.number_input("Bolusfaktor für 11:00-16:59 Uhr (IE pro 10g KH)", value=user_settings.get("zeitfenster_bolusfaktoren", {}).get("11:00-16:59", 1.0), step=0.1)
bolusfaktor_3 = st.number_input("Bolusfaktor für 17:00-23:59 Uhr (IE pro 10g KH)", value=user_settings.get("zeitfenster_bolusfaktoren", {}).get("17:00-23:59", 1.0), step=0.1)

# Eingabefeld für die Wirkdauer des Insulins
st.subheader("Insulin")
wirkdauer_insulin = st.number_input(
    "Wirkdauer Insulin in Stunden", 
    value=user_settings.get("wirkdauer_insulin", 4), 
    step=1
)
minimaler_bolusschritt = st.selectbox("Minimaler Bolusschritt (IE)", [0.05, 0.1, 0.2, 0.5])
korrekturfaktor = st.number_input("Korrekturfaktor (mmol/L pro IE)", value=user_settings.get("korrekturfaktor", 1.5), step=0.1)


# Speichern der Einstellungen
if st.button("💾 Speichern"):
    st.session_state["user_settings"] = {
        "zielwert": round(zielwert, 1),
        "korrekturfaktor": round(korrekturfaktor, 1),
        "minimaler_bolusschritt": round(minimaler_bolusschritt, 1),
        "zeitfenster_bolusfaktoren": {
            "00:00-10:59": round(bolusfaktor_1, 1),
            "11:00-16:59": round(bolusfaktor_2, 1),
            "17:00-23:59": round(bolusfaktor_3, 1),
        },
        "wirkdauer_insulin": wirkdauer_insulin,
        "untere_grenze": round(untere_grenze, 1),
        "obere_grenze": round(obere_grenze, 1),
    }

    data_manager.save_data("user_settings")
    st.success("Einstellungen wurden gespeichert.")