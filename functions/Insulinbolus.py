def berechne_korrektur_bolus(aktueller_wert, zielwert, korrekturfaktor):
    if korrekturfaktor <= 0:
        raise ValueError("Bolusfaktor muss größer als 0 sein.")
    return max(0, (aktueller_wert - zielwert) / korrekturfaktor)

def berechne_mahlzeiten_bolus(kohlenhydrate, bolusfaktor):
    if kohlenhydrate == 0:
        return 0
    if bolusfaktor <= 0:
        raise ValueError("Bolusfaktor muss größer als 0 sein.")
    return (kohlenhydrate/10) * bolusfaktor

def berechne_gesamt_bolus(korrektur_bolus, mahlzeiten_bolus, aktives_insulin):
    gesamt = korrektur_bolus + mahlzeiten_bolus - aktives_insulin
    return max(0, gesamt)
