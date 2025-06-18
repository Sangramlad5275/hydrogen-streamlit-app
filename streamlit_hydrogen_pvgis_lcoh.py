
import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime
import matplotlib.pyplot as plt

st.title("🌞 Hydrogen Production from Solar + Electrolyser (Marienberg, Saxony)")

# --- PVGIS Parameters ---
lat, lon = 50.645, 13.242  # Approximate Marienberg
st.sidebar.header("🔧 Electrolyser & Economic Settings")

# --- User Inputs ---
efficiency = st.sidebar.slider("Electrolyser Efficiency (%)", 50, 90, 70) / 100
min_power = st.sidebar.slider("Minimum Electrolyser Power (kW)", 10, 50, 20)
capex = st.sidebar.number_input("CAPEX ($/kW)", value=900)
opex_pct = st.sidebar.number_input("OPEX (% of CAPEX/year)", value=4.0)
elec_cost = st.sidebar.number_input("Electricity Cost ($/kWh)", value=0.05)
lifetime = st.sidebar.slider("System Lifetime (years)", 5, 30, 20)
electrolyser_capacity = 50  # fixed for this model

st.write("Fetching real solar data from PVGIS for Marienberg, Saxony...")

# --- Fetch real solar data from PVGIS ---
@st.cache_data
def fetch_pvgis_data():
    url = "https://re.jrc.ec.europa.eu/api/v5_2/seriescalc"
    params = {
        "lat": lat, "lon": lon,
        "startyear": 2020, "endyear": 2020,
        "outputformat": "json", "pvcalculation": True,
        "peakpower": 50, "tilt": 20, "loss": 14
    }
    r = requests.get(url, params=params)
    data = r.json()['outputs']['hourly']
    df = pd.DataFrame(data)
    df['time'] = pd.to_datetime(df['time'])
    df['pv_kw'] = df['P']  # actual AC output from PVGIS
    return df

df = fetch_pvgis_data()
df['load_kw'] = 40  # constant load
df['surplus_kw'] = df['pv_kw'] - df['load_kw']
df.loc[df['surplus_kw'] < min_power, 'surplus_kw'] = 0

# Hydrogen calculation
lhv_h2 = 33.3  # kWh/kg
df['hydrogen_kg'] = (df['surplus_kw'] * efficiency) / lhv_h2
df['cumulative_h2'] = df['hydrogen_kg'].cumsum()

# LCOH Calculation
annual_H2 = df['hydrogen_kg'].sum() * (8760 / len(df))  # extrapolate to full year
total_CAPEX = capex * electrolyser_capacity
total_OPEX = total_CAPEX * opex_pct/100 * lifetime
total_elec_cost = df['surplus_kw'].sum() * elec_cost
LCOH = (total_CAPEX + total_OPEX + total_elec_cost) / (annual_H2 * lifetime)

# Display results
st.metric("Estimated Annual Hydrogen Production (kg)", f"{annual_H2:.1f}")
st.metric("Estimated LCOH ($/kg)", f"{LCOH:.2f}")

# Plotting
st.line_chart(df.set_index('time')[['pv_kw', 'load_kw', 'surplus_kw']])
st.line_chart(df.set_index('time')[['hydrogen_kg', 'cumulative_h2']])
st.dataframe(df[['time', 'pv_kw', 'load_kw', 'surplus_kw', 'hydrogen_kg']].head(24))
