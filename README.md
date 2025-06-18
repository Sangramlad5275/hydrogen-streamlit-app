
# Hydrogen Production from Grid-Connected Electrolyser (Marienberg, Saxony)

This Streamlit app simulates green hydrogen production using real solar PV data from PVGIS (for Marienberg, Saxony) and a PEM electrolyser connected to the electricity grid.

## 🌍 Features

- Real-time hourly solar data fetched from PVGIS
- Electrolyser logic based on surplus solar power
- Interactive sliders to adjust:
  - Electrolyser efficiency
  - Minimum operational power
  - CAPEX, OPEX, and electricity cost
- Calculates LCOH (Levelized Cost of Hydrogen)
- Graphs for PV output, surplus power, and hydrogen output
- Data table for first 24 hours

## 🧪 System Model

- 50 kW fixed-tilt PV system
- 40 kW constant load demand
- PEM electrolyser operates only when surplus > minimum threshold

## 🧰 Tech Stack

- Python
- Streamlit
- Requests (for PVGIS API)
- Pandas, NumPy, Matplotlib

## 🚀 How to Run

1. Clone the repo
2. Install dependencies:
   ```
   pip install streamlit pandas numpy matplotlib requests
   ```
3. Run the app:
   ```
   streamlit run streamlit_hydrogen_pvgis_lcoh.py
   ```

## 🌐 Deployment (Streamlit Cloud)

1. Push code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Link your repo and select `streamlit_hydrogen_pvgis_lcoh.py` as the main file
4. Done! Share your public app URL

## 📍 Location Config

Currently set for: Marienberg, Saxony (lat=50.645, lon=13.242)  
You can edit coordinates in the script to simulate other locations.

## 📄 License

MIT License

---

Created with ❤️ for portfolio and academic learning.
