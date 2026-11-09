import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

# 1. Datenbank-Verbindung herstellen und Tabelle erstellen
conn = sqlite3.connect("stellvertretungen.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS stellvertretungen (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        datum DATE,
        lektion INTEGER,
        fach TEXT,
        abwesende_lp TEXT,
        vertretende_lp TEXT
    )
''')
conn.commit()

# 2. Benutzeroberfläche: Titel
st.title("Stellvertretungen Niederurnen")
st.write("Erfasse hier eine neue Stellvertretung.")

# 3. Das Eingabeformular
with st.form("eingabe_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        eingabe_datum = st.date_input("Datum", date.today())
        eingabe_lektion = st.number_input("Lektion (1-9)", min_value=1, max_value=9, step=1)
        eingabe_fach = st.selectbox("Fach", ["Mathematik", "Natur und Technik", "Deutsch", "Französisch", "Englisch", "Sport"])
    
    with col2:
        eingabe_abwesend = st.text_input("Kürzel: Abwesende Lehrperson (z.B. PS)")
        eingabe_vertreter = st.text_input("Kürzel: Vertretende Lehrperson")
    
    submitted = st.form_submit_button("Speichern")
    
    if submitted:
        cursor.execute('''
            INSERT INTO stellvertretungen (datum, lektion, fach, abwesende_lp, vertretende_lp)
            VALUES (?, ?, ?, ?, ?)
        ''', (eingabe_datum, eingabe_lektion, eingabe_fach, eingabe_abwesend, eingabe_vertreter))
        conn.commit()
        st.success("Die Stellvertretung wurde erfolgreich gespeichert!")

# 4. Dashboard für die Schulleitung (Übersicht)
st.divider() 
st.subheader("Dashboard: Alle Stellvertretungen")

# Daten aus der Datenbank auslesen
df = pd.read_sql_query("SELECT datum, lektion, fach, abwesende_lp, vertretende_lp FROM stellvertretungen", conn)

# Daten als interaktive Tabelle anzeigen
if not df.empty:
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("Bisher wurden noch keine Stellvertretungen erfasst.")