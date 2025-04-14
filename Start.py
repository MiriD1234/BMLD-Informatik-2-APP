import streamlit as st

st.title("GlucoBuddy")

if st.button("🧮 Insulinbolus-Rechner"):
    st.switch_page("pages/2_Insulinbolus-Rechner.py")

if st.button("⚙️ Einstellungen"):
    st.switch_page("pages/1_Einstellungen.py")

st.info("""Diese App ersetzt keine medizinische Beratung. Änderungen Ihrer Therapie sollten nur in Absprache mit Ihrem Arzt erfolgen.""")