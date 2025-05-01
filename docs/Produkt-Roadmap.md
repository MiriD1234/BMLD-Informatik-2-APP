# 1️⃣ V1.0 Insulinbolus-Rechner
- Eingabe Einstellungen: persönliche Korrektur-/Bolusfaktoren, aktives Insulin anhand letzter Indulindosis aus DataFrame  
*(geplant: 3h // effektiv: 5h)*
- Insulinbolus-Rechner  
*(geplant: 3h // effektiv: 5h)*  
Formel: (aktueller BZ – BZ-Zielwert) / Korrekturfaktor + (KH in g/10g = #KE) * Bolusfaktor - aktives Insulin = Bolusvorschlag
- Datenspeicherung auf SwitchDrive, User Login und Multi-User  
*(geplant: 2h // effektiv: 3h)*

# 2️⃣ V2.0 Blutzuckertagebuch
- aktueller Blutzuckerwert erfassen, Blutzuckerwert nacherfassen  
*(geplant: 1h // effektiv: 3 h)*
- Warnhinweise zu Blutzuckerwerten (zu hoch-> direkte Verknüpfung mit Button zum Insulinbolus-Rechner, zu tief -> Hinweis)  
*(geplant: 0.5h // effektiv: 1h)*
- Grafische Darstellung der Blutzuckerwerte  
*(geplant: 1h // effektiv: 1h)*
- Grafische Darstellung der verabreichten Insulindosen  
*(geplant: 1h // effektiv: 1h)*

# 3️⃣ V3.0 HbA1c, Daten-Eport, Optimierung Login
- HbA1c berechnen: Formel (Durchschnittlicher BZ der letzten 3 Monate + 2.59) / 1.59 = HbA1c in %  
*(geplant: 2h // effektiv: 2h)*
- Export der Grafiken BZ-Werte und Insulindosen als zB. PDF -> Export als PNG implementiert
*(geplant: 1h // effektiv: 0.5h)*
- "Passwort vergessen" im Login Fenster  
*(geplant: 1h)*
- Nach Registrierung soll der Nutzer gleich angemeldet sein (sich nicht noch einloggen müssen)  
*(geplant: 1h)*

# 🔢 Priorisierung Features
- Must-have: Insulinbolus-Rechner, Blutzuckertagebuch
- Should-have: Grafische Darstellung
- Could-have: Login-Optimierungen, HbA1c, Daten-Export

