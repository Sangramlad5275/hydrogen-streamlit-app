
import streamlit as st
import pandas as pd
import requests

@st.cache_data
def fetch_pvgis_data():
    url = "https://re.jrc.ec.europa.eu/api/v5_2/seriescalc?lat=50.6501&lon=13.1601&outputformat=json"
    r = requests.get(url)
    response_json = r.json()

    # Optional: Display raw JSON in Streamlit for debugging
    # st.write(response_json)

    if 'outputs' in response_json and 'hourly' in response_json['outputs']:
        data = response_json['outputs']['hourly']
        df = pd.DataFrame(data)
        return df
    else:
        st.error("⚠️ PVGIS API did not return 'hourly' data. Check location or try again later.")
        st.stop()

def main():
    st.title("Hydrogen Production from Solar + Electrolyser (Marienberg, Saxony)")
    st.write("Fetching real solar data from PVGIS for Marienberg, Saxony...")

    df = fetch_pvgis_data()

    st.subheader("Preview of PVGIS Hourly Data")
    st.dataframe(df.head())

if __name__ == "__main__":
    main()
