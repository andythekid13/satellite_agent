import sqlite3
import schedule
import time
from .download import download_satellite_image
from .analyze import analyze_forest_health

def save_results(date, predictions):
    """
    Save forest health predictions to a SQLite database.
    """
    conn = sqlite3.connect('forest_health.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS results
                      (date TEXT, healthy REAL, degraded REAL, deforested REAL)''')
    cursor.execute('INSERT INTO results VALUES (?, ?, ?, ?)',
                   (date, predictions[0][0], predictions[0][1], predictions[0][2]))
    conn.commit()
    conn.close()

def monitor_location(lat, lon, date, api_key):
    """
    Automate forest health monitoring for a specific location.
    """
    try:
        image = download_satellite_image(lat, lon, date, api_key)
        predictions = analyze_forest_health(image)
        save_results(date, predictions)
        print(f"[{date}] Monitoring complete for location ({lat}, {lon}).")
    except Exception as e:
        print(f"Error during monitoring: {e}")

def schedule_monitoring(lat, lon, api_key):
    """
    Schedule daily monitoring for a specific location.
    """
    schedule.every().day.at("08:00").do(monitor_location, lat, lon, "2024-01-01", api_key)

    while True:
        schedule.run_pending()
        time.sleep(1)
