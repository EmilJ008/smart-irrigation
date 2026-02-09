import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Këshilltari i Mençur për Ujitje 🌱")
st.markdown("Burimi i të dhënave: **FAO Guidelines on Crop Water Requirements**")

# Input nga përdoruesi
temperatura = st.number_input("Shkruani temperaturën (°C):", -10.0, 50.0, 25.0)
reshje = st.number_input("Shkruani reshjet (mm):", 0.0, 500.0, 0.0)
vlagesia = st.number_input("Lagështia e ajrit (%):", 0.0, 100.0, 60.0)
dite_pa_ujitje = st.number_input("Dita pa ujitje:", 0, 30, 2)
lloji_bimes = st.selectbox("Zgjidhni llojin e bimës:", [
    "Domate","Spec","Lulelakër","Patate","Lakër e bardhë","Qepë","Karrotë","Spinaq","Brokoli","Kastravec"
])

# Këshilla dhe foto për bimët
keshilla_foto = {
    "domate": {
        "keshilla": "Domatet kanë nevojë për ujitje të rregullt, rreth 1-2 litra për m² çdo ditë gjatë rritjes aktive. Mos i ujitni gjethet direkt për të shmangur sëmundjet fungale. Vendosni mbulimin e tokës për të ruajtur lagështinë dhe kontrolloni që toka të mos thahet plotësisht midis ujitjeve.",
        "foto": "images/Domate.jpg"
    },
    "spec": {
        "keshilla": "Specat duan tokë të ngrohtë dhe ujitje të moderuar. Mbajeni tokën të lagësht gjatë periudhës së lulëzimit dhe shtoni pak pleh organik për të përmirësuar prodhimin. Kujdes që të mos ujitni gjethet gjatë mesditës për të shmangur djegien.",
        "foto": "images/Spec.jpg"
    },
    "lulelakër": {
        "keshilla": "Lulelakra kërkon tokë të pasur me lëndë ushqyese dhe ujitje të qëndrueshme. Lagështia e njëtrajtshme ndihmon për kokrra të forta dhe të shëndetshme. Mbajeni tokën të mbuluar për të parandaluar tharjen e shpejtë.",
        "foto": "images/Lulelakër.jpg"
    },
    "patate": {
        "keshilla": "Patatet duan tokë të lagësht, por jo të përmbytur. Ujitja e rregullt është e rëndësishme gjatë formimit të gungave. Evitoni ujitjen e tepërt që mund të shkaktojë myk të patates.",
        "foto": "images/Patate.jpg"
    },
    "lakër e bardhë": {
        "keshilla": "Lakra e bardhë kërkon ujitje të qëndrueshme dhe tokë të pasur. Mbajeni sipërfaqen e tokës të lagësht, por shmangni ujitjen e tepërt që mund të sjellë rrënjë të kalbura.",
        "foto": "images/Lakër e bardhë.jpg"
    },
    "qepë": {
        "keshilla": "Qepët kanë nevojë për ujitje të moderuar. Lagështia e tokës ndihmon në rritjen e kokrrave të mëdha dhe të forta. Evitoni ujitjen e gjetheve për të parandaluar sëmundjet fungale.",
        "foto": "images/Qepë.jpg"
    },
    "karrotë": {
        "keshilla": "Karrotat duan tokë të butë dhe lagësht për rritjen e rrënjëve të shëndetshme. Lagështia e njëtrajtshme ndihmon për rrënjë të gjata dhe të ëmbla. Mos e përmbysni tokën gjatë ujitjes.",
        "foto": "images/Karrotë.jpg"
    },
    "spinaq": {
        "keshilla": "Spinaqi rritet më mirë në tokë të lagësht dhe të ftohtë. Lagështia e qëndrueshme ndihmon në gjethe të mëdha dhe të shëndetshme. Mbajeni tokën të mbuluar për të shmangur tharjen e shpejtë.",
        "foto": "images/Spinaq.jpg"
    },
    "brokoli": {
        "keshilla": "Brokoli kërkon ujitje të rregullt, sidomos gjatë formimit të kokrrave. Lagështia e njëtrajtshme parandalon që kokrrat të jenë të forta dhe të shëndetshme. Mbajeni tokën të pasur me pleh organik.",
        "foto": "images/Brokoli.jpg"
    },
    "kastravec": {
        "keshilla": "Kastravecët duan tokë të lagësht dhe shumë diell. Ujitja e rregullt siguron rrënjë dhe fruta të shëndetshme. Mbajeni tokën të mbuluar për të ruajtur lagështinë dhe shmangni ujitjen e tepërt që shkakton myk.",
        "foto": "images/Kastravec.jpg"
    }
}

# Funksioni për llogaritjen e ujit për 1 ditë
def llogarit_ujitjen(temp, reshje, vlagesia, bima, dite):
    faktorët = {
        "domate": 1.5,"spec": 1.2,"lulelakër": 1.0,"patate": 0.8,
        "lakër e bardhë": 1.0,"qepë": 0.9,"karrotë": 0.7,"spinaq": 0.6,"brokoli": 1.0,"kastravec": 1.3
    }
    baza = faktorët.get(bima.lower(),1.0)
    koef_temp = 1 + (temp - 25)*0.05 if temp>25 else 1
    koef_reshje = 0.5 if reshje>5 else 1
    koef_vlagesie = 1 + ((50 - vlagesia)*0.01) if vlagesia<50 else 1
    koef_kohor = 1 + (dite*0.1)
    return round(baza*koef_temp*koef_reshje*koef_vlagesie*koef_kohor,2)

if st.button("Llogarit sasinë e ujit dhe shfaq grafikun"):
    # Llogaritja për ditën e sotme
    litra_sot = llogarit_ujitjen(temperatura, reshje, vlagesia, lloji_bimes, dite_pa_ujitje)
    st.success(f"Sot, ujisni **{lloji_bimes}** me **{litra_sot} litra** ujë për metër katror.")

    # Llogaritja për 7 ditët e ardhshme
    ditet = np.arange(1,8)
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

    # Shfaq keshillat dhe foton
    info = keshilla_foto.get(lloji_bimes.lower())
    if info:
        st.markdown(f"**Këshilla për {lloji_bimes}:** {info['keshilla']}")
        st.image(info['foto'], caption=lloji_bimes, use_column_width=True)
