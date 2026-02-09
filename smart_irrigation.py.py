import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Këshilltari i Mençur për Ujitje 🌱")
st.markdown("Burimi i të dhënave: **FAO Guidelines on Crop Water Requirements**")

# Input nga përdoruesi
temperatura = st.number_input("Shkruani temperaturën (°C):", min_value=-10.0, max_value=50.0, value=25.0)
reshje = st.number_input("Shkruani reshjet (mm):", min_value=0.0, max_value=500.0, value=0.0)
vlagesia = st.number_input("Lagështia e ajrit (%):", min_value=0.0, max_value=100.0, value=60.0)
dite_pa_ujitje = st.number_input("Dita pa ujitje:", min_value=0, max_value=30, value=2)
lloji_bimes = st.selectbox("Zgjidhni llojin e bimës:", [
    "Domate", "Spec", "Lulelakër", "Patate",
    "Lakër e bardhë", "Qepë", "Karrotë", "Spinaq", "Brokoli", "Kastravec"
])

# Funksioni për llogaritjen e ujit për 1 ditë
def llogarit_ujitjen(temp, reshje, vlagesia, bima, dite):
    faktorët = {
        "domate": 1.5,
        "spec": 1.2,
        "lulelakër": 1.0,
        "patate": 0.8,
        "lakër e bardhë": 1.0,
        "qepë": 0.9,
        "karrotë": 0.7,
        "spinaq": 0.6,
        "brokoli": 1.0,
        "kastravec": 1.3
    }

    baza = faktorët.get(bima.lower(), 1.0)
    koef_temp = 1 + (temp - 25) * 0.05 if temp > 25 else 1
    koef_reshje = 0.5 if reshje > 5 else 1
    koef_vlagesie = 1 + ((50 - vlagesia) * 0.01) if vlagesia < 50 else 1
    koef_kohor = 1 + (dite * 0.1)
    return round(baza * koef_temp * koef_reshje * koef_vlagesie * koef_kohor, 2)

# Butoni për llogaritje dhe grafik
if st.button("Llogarit sasinë e ujit dhe shfaq grafikun"):
    # Llogaritja për ditën e sotme
    litra_sot = llogarit_ujitjen(temperatura, reshje, vlagesia, lloji_bimes, dite_pa_ujitje)
    st.success(f"Sot, ujisni **{lloji_bimes}** me **{litra_sot} litra** ujë për metër katror.")

    # Llogaritja për 7 ditët e ardhshme
    ditet = np.arange(1, 8)
    litra_javore = [llogarit_ujitjen(temperatura, reshje, vlagesia, lloji_bimes, d) for d in ditet]

    # Grafik
    fig, ax = plt.subplots(figsize=(7,4))
    ax.plot(ditet, litra_javore, marker='o', linestyle='-', color='green')
    ax.set_title(f"Sasia e ujit për {lloji_bimes} për javën e ardhshme")
    ax.set_xlabel("Dita")
    ax.set_ylabel("Litrat / m²")
    ax.set_xticks(ditet)
    ax.grid(True)

    st.pyplot(fig)
