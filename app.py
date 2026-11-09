import streamlit as st

st.title("Stellvertretungen - Übersicht")
st.write("Willkommen im neuen Dashboard! Hier entsteht unser System.")

import pandas as pd

# 5. Dashboard für die Schulleitung (Übersicht)
st.divider() 
st.subheader("Dashboard: Alle Stellvertretungen")

# Daten aus der Datenbank auslesen
df = pd.read_sql_query("SELECT datum, lektion, fach, abwesende_lp, vertretende_lp FROM stellvertretungen", conn)

# Daten als interaktive Tabelle anzeigen
if not df.empty:
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("Bisher wurden noch keine Stellvertretungen erfasst.")