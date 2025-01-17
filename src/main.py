import streamlit as st
from forest_health.download import download_satellite_image
from forest_health.analyze import analyze_forest_health
from forest_health.visualize import visualize_results
from forest_health.monitor import save_results, schedule_monitoring

def main():
    st.title("Forest Tracking Agent")
    st.write("Monitor and analyze forest health using satellite imagery.")

    # Input fields
    lat = st.number_input("Latitude", value=48.8566)
    lon = st.number_input("Longitude", value=2.3522)
    date = st.text_input("Date (YYYY-MM-DD)", value="2024-01-01")
    api_key = st.text_input("API Key", type="password")

    if st.button("Analyze Forest Health"):
        try:
            image = download_satellite_image(lat, lon, date, api_key)
            predictions = analyze_forest_health(image)
            visualize_results(image, predictions)
            save_results(date, predictions)
        except Exception as e:
            st.error(f"Error: {e}")

    if st.button("Start Automated Monitoring"):
        try:
            st.write("Starting automated daily monitoring...")
            schedule_monitoring(lat, lon, api_key)
        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
