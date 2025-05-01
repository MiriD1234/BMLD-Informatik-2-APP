import pandas as pd
from datetime import datetime, timedelta

def berechne_hba1c(data_df, tage=90, min_messwerte=20):
    """
    Berechnet den geschätzten HbA1c-Wert basierend auf Blutzuckerwerten.

    Args:
        data_df (pd.DataFrame): DataFrame mit den Blutzuckerwerten und einem 'timestamp'-Feld.
        tage (int): Anzahl der Tage, die für die Berechnung berücksichtigt werden sollen.
        min_messwerte (int): Minimale Anzahl an Messwerten für eine verlässliche Berechnung.

    Returns:
        tuple: (hba1c_gerundet, farbe, bewertung, anzahl_messwerte) oder None, wenn nicht genügend Daten vorhanden sind.
    """
    # Stelle sicher, dass 'timestamp' als datetime interpretiert wird
    data_df['timestamp'] = pd.to_datetime(data_df['timestamp'])

    # Filter: letzte `tage` Tage
    start_datum = datetime.now() - timedelta(days=tage)
    data_df_filtered = data_df[data_df['timestamp'] >= start_datum]

    if not data_df_filtered.empty and 'blutzuckerwert' in data_df_filtered.columns:
        anzahl_messwerte = len(data_df_filtered)
        if anzahl_messwerte >= min_messwerte:
            durchschnitt_bz = data_df_filtered['blutzuckerwert'].mean()
            hba1c = (durchschnitt_bz + 2.59) / 1.59
            hba1c_gerundet = round(hba1c, 1)

            # Bewertung mit Farbe/Emoji
            if hba1c_gerundet < 7.0:
                farbe = "🟢"
                bewertung = "Gut eingestellt"
            elif 7.0 <= hba1c_gerundet <= 8.0:
                farbe = "🟡"
                bewertung = "Grenzwertig"
            else:
                farbe = "🔴"
                bewertung = "Verbesserung notwendig"

            return hba1c_gerundet, farbe, bewertung, anzahl_messwerte

    return None