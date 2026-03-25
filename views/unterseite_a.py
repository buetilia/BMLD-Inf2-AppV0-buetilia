from unittest import result

import pandas as pd
import streamlit as st
import sys
import os
from utils.data_manager import DataManager

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from functions.logic import calculate_kjeldahl_results

if 'data_df' not in st.session_state:
    st.session_state['data_df'] = pd.DataFrame(columns=[
        "Zeitstempel", "Volumen Probe (ml)", "Stickstoff (%)", "Protein (%)", "Faktor"  
    ])
       
st.title("Kjeldahl Stickstoff- & Protein-Rechner")

st.divider()

st.write("""
    Dieser Rechner wurde entwickelt, um die manuelle Auswertung der **Kjeldahl-Stickstoffbestimmung** zu 
    ersetzen. Im Laboralltag fallen viele Messwerte an, die fehleranfällig berechnet werden müssen. 
    Diese App bietet eine schnelle, sichere und reproduzierbare Lösung.
    """)

tab_rechner, tab_theorie = st.tabs([" Kjeldahl-Rechner", " Anleitung & Dokumentation"])

with tab_theorie:
    st.subheader(" Hintergrund")
    st.markdown("""
    Die Bestimmung nach **Johan Kjeldahl (1883)** ist das weltweit anerkannte Referenzverfahren zur Ermittlung des Stickstoff- und Proteingehalts.
    Doch wieso misst man nicht direkt den Proteingehalt? Proteine sind chemisch sehr komplex und vielfältig (denk an Muskelgewebe, Enzyme oder Gluten). Es ist extrem schwierig, jedes einzelne Protein direkt zu wiegen. Aber fast alle Proteine haben eine gemeinsame Eigenschaft: Sie enthalten Stickstoff in ihren Aminosäuren.
    Andere Hauptbestandteile von Lebensmitteln wie Fette und Kohlenhydrate (Zucker, Stärke) enthalten hingegen keinen Stickstoff.

    Wenn man also den gesamten Stickstoff in einer Probe misst, hat man einen direkten "Fingerabdruck" der vorhandenen Proteine.
    """)

    st.header("Der Analyse-Prozess")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("🌡️ a) Aufschluss")
        st.write("""
        Die Probe wird mit konzentrierter **Schwefelsäure** bei ca. 400 °C erhitzt. 
        Dabei wird organischer Stickstoff in **Ammoniumsulfat** umgewandelt und alles andere verbrannt.
        """)

    with col2:
        st.subheader("⚗️ b) Destillation")
        st.write("""
        Durch Zugabe von **Natronlauge** wird Ammoniakgas freigesetzt und mittels Wasserdampf in eine 
        **Borsäure-Vorlage** übergetrieben.
        """)

    with col3:
        st.subheader("🧪 c) Titration")
        st.write("""
        Die aufgefangene Menge Ammoniak wird mit einer **Masslösung (HCl)** titriert. 
        Der Verbrauch gibt Aufschluss über die Stickstoffmenge. Das Verhältnis von Ammoniak und Salzsäure ist 1:1.
        """)

    st.divider()

    st.header("Mathematische Grundlagen")

    math_col1, math_col2 = st.columns([2, 1])

    with math_col1:
        st.write("**Berechnung des Stickstoffgehalts ($w_N$):**")
        st.latex(r"w_N [\%] = \frac{V_{Probe} \cdot c_{HCl} \cdot f \cdot 14.007 \cdot 0.1}{m_{Einwaage}}")
        st.write("**Umrechnung in Rohprotein:**")
        st.latex(r"Protein [\%] = w_N \cdot p\_factor")

    with math_col2:
        st.info("""
        **Legende:**
        * $V$: Volumen [ml]
        * $c$: Konzentration [mol/L]
        * $f$: Titerfaktor
        * $m$: Einwaage [g]
        * 14.007: Molmasse $N$ [g/mol]
        * 0.1: Umrechnung von ml zu L
        """)
    
    st.divider()

    st.header("Warum verschiedene Faktoren?")
    st.write("""
    Da verschiedene Proteine unterschiedliche Anteile an Stickstoff haben, nutzt man spezifische Faktoren. 
    Man geht im Durchschnitt davon aus, dass Proteine zu **16% aus Stickstoff** bestehen ($100 / 16 = 6.25$).
    """)

    st.table({
        "Proteinsorte": ["Standard / Fleisch", "Getreide (Weizen)", "Milchprodukte", "Erdnüsse"],
        "Faktor": [6.25, 5.70, 6.38, 5.46],
        "Begründung": ["Ø 16% N", "Höherer N-Anteil", "Spezifische Aminosäuren", "Niedrigerer N-Anteil"]
    })

    st.caption("Datenquelle: In Anlehnung an C. Gerhardt GmbH & Co. KG")

with st.sidebar:
    st.header("⚙️ Einstellungen")
    c_hcl = st.number_input("Konzentration HCl", value=0.1)

    st.divider()

    f_titer = st.number_input("Titer (f):", value=1.0000, format="%.4f")

    st.divider()

    sorte = st.selectbox(
        "Proteinsorte wählen:",
        ["Fleisch / Eier", "Getreide (Weizen)", "Milchprodukte", "Erdnüsse", "Andere"]
    )
    if sorte == "Fleisch / Eier":
        wert = 6.25
    elif sorte == "Getreide (Weizen)":
        wert = 5.70
    elif sorte == "Milchprodukte":
        wert = 6.38
    elif sorte == "Erdnüsse":
        wert = 5.46
    else:
        wert = 1.00
    p_factor = st.number_input(
        "Zugehöriger Faktor:",
        value=wert,
        step=0.01,
        format="%.2f",
        help="Dieser Wert wird für die Berechnung des Rohproteins verwendet.")

with tab_rechner:
    st.subheader("Messdaten der Titration")

    with st.form("inputs"):
        m_e = st.number_input("Einwaage (g)", format="%.4f")
        v_p = st.number_input("Verbrauch HCl (ml)", format="%.4f")
        submit = st.form_submit_button("Berechnen")

    if submit:
        try:
            if 'user_info' not in st.session_state or st.session_state['user_info'] is None:
                st.error("Login-Daten nicht gefunden. Bitte auf der Home-Seite neu einloggen.")
                st.stop()
            
            if 'dm' not in st.session_state:
                from utils.data_manager import DataManager
                st.session_state['dm'] = DataManager(fs_protocol='webdav', fs_root_folder="Kjeldahl-Rechner")

            dm = st.session_state['dm']
            username = st.session_state['user_info']['username']

            raw_result = calculate_kjeldahl_results(v_p, c_hcl, f_titer, m_e, p_factor)
            result = {
                "Zeitstempel": pd.Timestamp.now().strftime("%d.%m.%Y %H:%M"),
                "Volumen Probe (ml)": v_p,
                "Stickstoff (%)": raw_result['Stickstoff (%)'], # Namen aus deiner logic.py
                "Protein (%)": raw_result['Protein (%)'],       # Namen aus deiner logic.py
                "Faktor": p_factor
            }
            result['Zeitstempel'] = pd.Timestamp.now().strftime("%d.%m.%Y %H:%M")

            new_row = pd.DataFrame([result])
            new_row.index = [len(st.session_state['data_df']) + 1]
            st.session_state['data_df'] = pd.concat([st.session_state['data_df'], new_row])

            dm.save_user_data(username, st.session_state['data_df'])

            st.success(f"Probe {len(st.session_state['data_df'])} erfolgreich gespeichert!")
            
            col1, col2 = st.columns(2)
            col1.metric("Stickstoffgehalt", f"{result['Stickstoff (%)']} %")
            col2.metric("Rohproteingehalt", f"{result['Protein (%)']} %")

        except ValueError as e:
            st.error(f"Fehler bei der Berechnung: {e}")
        except Exception as e:
            st.error(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

st.subheader("Verlauf der Analysen")
st.dataframe(st.session_state['data_df'])