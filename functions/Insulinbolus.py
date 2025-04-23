from utils import helpers
from datetime import datetime, timedelta
import pandas as pd

def berechne_korrektur_bolus(aktueller_wert, zielwert, korrekturfaktor):
    if korrekturfaktor <= 0:
        raise ValueError("Bolusfaktor muss größer als 0 sein.")
    result = max(0, (aktueller_wert - zielwert) / korrekturfaktor)
    return {
        "timestamp": helpers.ch_now(),
        "aktueller_wert": aktueller_wert,
        "zielwert": zielwert,
        "korrekturfaktor": korrekturfaktor,
        "korrektur_bolus": result,
    }

def berechne_mahlzeiten_bolus(kohlenhydrate, bolusfaktor):
    if kohlenhydrate == 0:
        result = 0
    elif bolusfaktor <= 0:
        raise ValueError("Bolusfaktor muss größer als 0 sein.")
    else:
        result = (kohlenhydrate / 10) * bolusfaktor
    return {
        "timestamp": helpers.ch_now(),
        "kohlenhydrate": kohlenhydrate,
        "bolusfaktor": bolusfaktor,
        "mahlzeiten_bolus": result,
    }

def berechne_gesamt_bolus(korrektur_bolus, mahlzeiten_bolus, aktives_insulin):
    result = max(0, korrektur_bolus + mahlzeiten_bolus - aktives_insulin)
    return {
        "timestamp": helpers.ch_now(),
        "korrektur_bolus": korrektur_bolus,
        "mahlzeiten_bolus": mahlzeiten_bolus,
        "aktives_insulin": aktives_insulin,
        "gesamt_bolus": result,
    }

def berechne_gerundeter_gesamt_bolus(gesamt_bolus, minimaler_bolusschritt):
    result = round(gesamt_bolus / minimaler_bolusschritt) * minimaler_bolusschritt
    return {
        "timestamp": helpers.ch_now(),
        "gesamt_bolus": gesamt_bolus,
        "minimaler_bolusschritt": minimaler_bolusschritt,
        "gerundeter_gesamt_bolus": result,
    }

def get_bolusfaktor_for_current_time(zeitfenster_bolusfaktoren):
    """
    Wählt den passenden Bolusfaktor basierend auf der aktuellen Uhrzeit aus den definierten Zeitfenstern.
    """
    current_time = datetime.now().time()
    for zeitfenster, bolusfaktor in zeitfenster_bolusfaktoren.items():
        start, end = zeitfenster.split("-")
        start_time = datetime.strptime(start, "%H:%M").time()
        end_time = datetime.strptime(end, "%H:%M").time()
        if start_time <= current_time <= end_time:
            return bolusfaktor
    raise ValueError("Kein passender Bolusfaktor für die aktuelle Uhrzeit gefunden.")

def lade_einstellungen(session_state, default_settings):
    """
    Lädt die Benutzereinstellungen aus der Session State oder verwendet Standardwerte.
    """
    return session_state.get("user_settings", default_settings)

def berechne_aktives_insulin(letzte_dosis_df, wirkdauer_insulin):
    """
    Berechnet das aktive Insulin basierend auf der letzten Dosis und der Wirkdauer.
    """
    if not letzte_dosis_df.empty:
        letzte_dosis = letzte_dosis_df.iloc[-1]
        if isinstance(letzte_dosis["timestamp"], pd.Timestamp):
            letzte_dosis_zeitpunkt = letzte_dosis["timestamp"].to_pydatetime()
        else:
            letzte_dosis_zeitpunkt = datetime.strptime(letzte_dosis["timestamp"], "%Y-%m-%d %H:%M:%S")
        
        zeit_seit_letzter_dosis = datetime.now() - letzte_dosis_zeitpunkt

        if zeit_seit_letzter_dosis > timedelta(hours=wirkdauer_insulin):
            return 0  # Insulin ist nicht mehr aktiv
        else:
            return letzte_dosis["gerundeter_gesamt_bolus"]
    return 0  # Keine Dosis erfasst, daher kein aktives Insulin