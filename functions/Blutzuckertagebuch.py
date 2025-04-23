import pandas as pd
from datetime import datetime

def load_blutzuckertagebuch(data_manager, session_state_key, file_name):
    """Lädt das Blutzuckertagebuch aus der persistenten Speicherung."""
    return data_manager.load_user_data(
        session_state_key=session_state_key,
        file_name=file_name,
        initial_value=pd.DataFrame(columns=["timestamp", "blutzuckerwert"]),
        parse_dates=["timestamp"],
    )

def save_blutzuckertagebuch(data_manager, tagebuch_df, session_state_key):
    """Speichert das Blutzuckertagebuch und aktualisiert den Session State."""
    import streamlit as st
    st.session_state[session_state_key] = tagebuch_df
    data_manager.save_data(session_state_key)

def add_entry(tagebuch_df, blutzuckerwert):
    """Fügt einen neuen Eintrag mit aktuellem Timestamp hinzu."""
    neuer_eintrag = {"timestamp": datetime.now(), "blutzuckerwert": blutzuckerwert}
    return pd.concat([tagebuch_df, pd.DataFrame([neuer_eintrag])], ignore_index=True)

def add_manual_entry(tagebuch_df, blutzuckerwert, datum, uhrzeit):
    """Fügt einen manuell erfassten Eintrag hinzu."""
    timestamp = datetime.combine(datum, uhrzeit)
    neuer_eintrag = {"timestamp": timestamp, "blutzuckerwert": blutzuckerwert}
    tagebuch_df = pd.concat([tagebuch_df, pd.DataFrame([neuer_eintrag])], ignore_index=True)
    return tagebuch_df.sort_values(by="timestamp").reset_index(drop=True)

def check_blutzuckerwert(grenzen, aktueller_wert):
    """Prüft, ob der Blutzuckerwert innerhalb der Grenzen liegt."""
    untere_grenze, obere_grenze = grenzen
    if aktueller_wert < untere_grenze:
        return "low"
    elif aktueller_wert > obere_grenze:
        return "high"
    return "normal"