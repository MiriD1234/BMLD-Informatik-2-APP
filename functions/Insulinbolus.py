from utils import helpers
from datetime import datetime

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