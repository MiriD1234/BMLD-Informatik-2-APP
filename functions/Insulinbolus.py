from utils import helpers

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