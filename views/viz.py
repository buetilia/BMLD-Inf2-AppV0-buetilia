import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

st.dataframe(st.session_state['data_df'].set_index(st.session_state['data_df'].index + 1))

st.title("Analyse-Ergebnisse")

if 'data_df' in st.session_state and not st.session_state['data_df'].empty:
    df = st.session_state['data_df']

    st.subheader("Übersicht Proteingehalt")
    fig, ax = plt.subplots(figsize=(10, 5))

    x_labels = [f"P{i+1}" for i in range(len(df))]
    y_values = df["Protein (%)"]

    bars = ax.bar(x_labels, y_values, color='#007acc', edgecolor='black')

    ax.set_ylabel("Protein [%]", fontsize=12)
    ax.set_xlabel("Proben-Nummer", fontsize=12)
    ax.set_title("Vergleich der Messergebnisse", fontsize=14)

    max_val = df["Protein (%)"].max()
    
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + (max_val * 0.01), 
            f"{yval:.2f}%", 
            ha='center', va='bottom', fontweight='bold', color='black')
        
    if max_val > 0:
        ax.set_ylim(0, max_val * 1.05)
    else:
        ax.set_ylim(0, 10)

    st.pyplot(fig)

    st.divider()
    col1, col2 = st.columns(2)
    col1.metric("Durchschnitt Protein", f"{df['Protein (%)'].mean():.2f} %")
    col2.metric("Höchster Wert", f"{df['Protein (%)'].max():.2f} %")

else:
    st.info("Noch keine Daten vorhanden. Bitte berechne zuerst eine Probe im Rechner.")

st.divider()

st.subheader("Daten-Export")

if 'data_df' in st.session_state and not st.session_state['data_df'].empty:
    df_export = st.session_state['data_df']

    @st.cache_data
    def convert_df_to_excel_csv(df):
        return df.to_csv(sep=';', index=False).encode('utf-8-sig')

    csv_data = convert_df_to_excel_csv(df_export)
    col_btn, col_info = st.columns([1, 2])
    with col_btn:
        st.download_button(
            label="📊 CSV für Excel exportieren",
            data=csv_data,
            file_name='Kjeldahl_Laborprotokoll.csv',
            mime='text/csv',
        )
    with col_info:
        st.info("Tipp: Diese Datei lässt sich direkt in Excel öffnen")
else:
    st.write("Sobald Daten im Rechner gespeichert wurden, erscheint hier der Export-Button.")