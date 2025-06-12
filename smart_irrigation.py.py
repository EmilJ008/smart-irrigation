import streamlit as st

# Baza e të dhënave për bimët me burim të thjeshtuar
plant_water_requirements = {
    "tomato": 1.5,
    "pepper": 1.2,
    "cauliflower": 1.0,
    "potato": 0.8,
    "lettuce": 0.9,
    "onion": 0.7,
    "carrot": 0.85,
    "spinach": 1.0,
    "broccoli": 1.1,
    "cucumber": 1.3
    # Source: Adapted from FAO irrigation guidelines
}

# Funksioni për llogaritjen e nevojës për ujitje
def calculate_irrigation(temp, rainfall, humidity, plant, days_without_irrigation):
    base = plant_water_requirements.get(plant.lower(), 1.0)
    temp_coeff = 1 + (temp - 25) * 0.05 if temp > 25 else 1
    rain_coeff = 0.5 if rainfall > 5 else 1
    humidity_coeff = 1 + ((50 - humidity) * 0.01) if humidity < 50 else 1
    time_coeff = 1 + (days_without_irrigation * 0.1)
    total_water = base * temp_coeff * rain_coeff * humidity_coeff * time_coeff
    return round(total_water, 2)

# UI me Streamlit
st.set_page_config(page_title="Smart Irrigation Advisor")

st.title("Smart Irrigation Advisor 🌱")
st.write("Calculate the optimal amount of water for your crop based on weather and soil conditions.")

# Input fields
temperature = st.number_input("Temperature (°C):", min_value=-10.0, max_value=60.0, value=25.0)
rainfall = st.number_input("Rainfall in last 24h (mm):", min_value=0.0, max_value=100.0, value=0.0)
humidity = st.number_input("Air Humidity (%):", min_value=0.0, max_value=100.0, value=50.0)
days = st.number_input("Days since last irrigation:", min_value=0, max_value=30, value=0)
plant = st.selectbox("Select plant type:", options=list(plant_water_requirements.keys()))

# Button to calculate
if st.button("Calculate Water Need"):
    result = calculate_irrigation(temperature, rainfall, humidity, plant, days)
    st.success(f"Today, irrigate **{plant.title()}** with **{result} liters** of water per square meter.")

# Source information
st.markdown("**Data Source:** FAO Guidelines on Crop Water Requirements")
