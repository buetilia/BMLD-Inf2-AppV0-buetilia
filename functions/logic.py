import pytz
from datetime import datetime

def calculate_kjeldahl_results(v_p, c_hcl, f_titer, m_e, p_factor):
    if m_e <= 0:
        raise ValueError("Die Einwaage muss grösser als 0 sein.")

    n_percent = (v_p * c_hcl * f_titer * 14.007 * 0.1) / m_e

    p_percent = n_percent * p_factor

    swiss_tz = pytz.timezone('Europe/Zurich')
    
    return {
        "Zeitstempel": datetime.now(swiss_tz).strftime("%d.%m.%Y %H:%M:%S"),
        "Proben Volumen (ml)": v_p,
        "Konzentration (mol/L)": c_hcl,
        "Stickstoff (%)": round(n_percent, 3),
        "Protein (%)": round(p_percent, 2),
        "Faktor": p_factor
    }