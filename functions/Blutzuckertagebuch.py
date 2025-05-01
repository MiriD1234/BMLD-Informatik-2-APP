import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

def load_blutzuckertagebuch(data_manager, session_state_key, file_name):
    """Lädt das Blutzuckertagebuch aus der persistenten Speicherung."""
    return data_manager.load_user_data(
        session_state_key=session_state_key,
        file_name=file_name,
        initial_value=pd.DataFrame(columns=["timestamp", "blutzuckerwert"]),
        parse_dates=["timestamp"],
    )

def add_entry(data_manager, session_state_key, blutzuckerwert):
    """Fügt einen neuen Eintrag mit aktuellem Timestamp hinzu."""
    neuer_eintrag = {"timestamp": datetime.now(), "blutzuckerwert": blutzuckerwert}
    data_manager.append_record(session_state_key, neuer_eintrag)

def check_blutzuckerwert(grenzen, aktueller_wert):
    """Prüft, ob der Blutzuckerwert innerhalb der Grenzen liegt."""
    untere_grenze, obere_grenze = grenzen
    if aktueller_wert < untere_grenze:
        return "low"
    elif aktueller_wert > obere_grenze:
        return "high"
    return "normal"

def classify_wert(wert, untere_grenze, obere_grenze):
    """Klassifiziert den Blutzuckerwert in einen Bereich."""
    if wert < untere_grenze:
        return 'Unterzucker'
    elif wert > obere_grenze:
        return 'Überzucker'
    else:
        return 'Zielbereich'

def create_blutzucker_figure(data_df, untere_grenze, obere_grenze):
    """Erstellt die interaktive Blutzuckergrafik."""
    farben = {'Unterzucker': 'blue', 'Zielbereich': 'green', 'Überzucker': 'red'}
    data_df['bereich'] = data_df['blutzuckerwert'].apply(lambda wert: classify_wert(wert, untere_grenze, obere_grenze))

    fig = go.Figure()

    # Blutzuckerlinie
    fig.add_trace(go.Scatter(
        x=data_df['timestamp'],
        y=data_df['blutzuckerwert'],
        mode='lines+markers',
        marker=dict(color=[farben[b] for b in data_df['bereich']]),
        name='Blutzuckerwert',
        hovertemplate='Zeit: %{x}<br>Wert: %{y} mmol/L<extra></extra>'
    ))

    # Zielbereich als Hintergrundband
    fig.add_shape(type="rect",
                  xref="paper", yref="y",
                  x0=0, x1=1,
                  y0=untere_grenze, y1=obere_grenze,
                  fillcolor="lightgreen", opacity=0.2,
                  layer="below", line_width=0)

    # Layout-Anpassungen
    fig.update_layout(
        title="Verlauf der Blutzuckerwerte mit Zielbereich",
        xaxis_title="Zeit",
        yaxis_title="Blutzucker (mmol/L)",
        hovermode="x unified",
        height=500
    )

    return fig