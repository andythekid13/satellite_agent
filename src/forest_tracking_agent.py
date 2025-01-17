# Forest Tracking Agent using IBM Open-Source Satellite LLM Model

# Import necessary libraries
import os
import requests
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import tensorflow as tf  # For ML model integration
from transformers import ViTForImageClassification, AutoImageProcessor
import streamlit as st  # For UI integration
import schedule
import time
import sqlite3

# Step 1: Load Satellite Data
# Using Sentinel-2 imagery as an example
def download_satellite_image(lat, lon, date, api_key):
    """
    Downloads satellite imagery for a given location and date.
    Args:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.
        date (str): Date in YYYY-MM-DD format.
        api_key (str): API key for the satellite data provider.
    Returns:
        image (PIL.Image): The satellite image.
    """
    endpoint = f"https://api.sentinel-hub.com/download?lat={lat}&lon={lon}&date={date}&key={api_key}"
    response = requests.get(endpoint)
    if response.status_code == 200:
        with open("satellite_image.tif", "wb") as f:
            f.write(response.content)
        image = Image.open("satellite_image.tif")
        return image
    else:
        raise Exception(f"Failed to download image: {response.status_code} {response.text}")

# Step 2: Load Pre-trained IBM LLM or HuggingFace Model
import logging

logging.basicConfig(level=logging.INFO)

# Use Streamlit caching to avoid reinitialization
@st.cache_resource
def load_model_and_processor():
    logging.info("Initializing the feature extractor and model...")
    # Use fast image processor
    feature_extractor = AutoImageProcessor.from_pretrained("google/vit-base-patch16-224-in21k", use_fast=True)
    # Load the Vision Transformer model
    model = ViTForImageClassification.from_pretrained(
        "google/vit-base-patch16-224-in21k",
        ignore_mismatched_sizes=True
    )
    logging.info("Model and feature extractor initialized successfully.")
    logging.info("Note: Classification head is not fine-tuned and may require training for improved accuracy.")
    return feature_extractor, model

feature_extractor, model = load_model_and_processor()

# Step 3: Process Satellite Image
def process_image(image):
    """
    Preprocess the satellite image for model inference.
    Args:
        image (PIL.Image): The satellite image.
    Returns:
        inputs (torch.Tensor): Processed image tensor.
    """
    inputs = feature_extractor(images=image, return_tensors="pt")
    return inputs

# Step 4: Analyze Forest Health
def analyze_forest_health(image):
    """
    Analyze the forest health from satellite image using the pre-trained model.
    Args:
        image (PIL.Image): The satellite image.
    Returns:
        predictions (dict): Forest health predictions.
    """
    inputs = process_image(image)
    outputs = model(**inputs)
    predictions = outputs.logits.softmax(dim=1).detach().numpy()
    return predictions

# Step 5: Visualize and Report Results
def visualize_results(image, predictions):
    """
    Visualize the results of the forest analysis.
    Args:
        image (PIL.Image): The satellite image.
        predictions (dict): Forest health predictions.
    """
    st.image(image, caption="Satellite Image", use_column_width=True)
    labels = ["Healthy", "Degraded", "Deforested"]
    prediction_dict = {label: pred for label, pred in zip(labels, predictions[0])}
    st.bar_chart(prediction_dict)

# Step 6: Save Results to Database
def save_results(date, predictions):
    """
    Save forest health predictions to a SQLite database.
    Args:
        date (str): The date of the analysis.
        predictions (list): Forest health predictions.
    """
    conn = sqlite3.connect('forest_health.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS results
                      (date TEXT, healthy REAL, degraded REAL, deforested REAL)''')
    cursor.execute('''INSERT INTO results VALUES (?, ?, ?, ?)''',
                   (date, predictions[0][0], predictions[0][1], predictions[0][2]))
    conn.commit()
    conn.close()

# Step 7: Automated Monitoring
def monitor_location(lat, lon, date, api_key):
    """
    Automate forest health monitoring for a specific location.
    Args:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.
        date (str): Date in YYYY-MM-DD format.
        api_key (str): API key for satellite data.
    """
    try:
        image = download_satellite_image(lat, lon, date, api_key)
        predictions = analyze_forest_health(image)
        save_results(date, predictions)
        print(f"[{date}] Monitoring complete for location ({lat}, {lon}).")
    except Exception as e:
        print(f"Error during monitoring: {e}")

# Schedule Monitoring
def schedule_monitoring(lat, lon, api_key):
    """
    Schedule daily monitoring for a specific location.
    Args:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.
        api_key (str): API key for satellite data.
    """
    schedule.every().day.at("08:00").do(monitor_location, lat, lon, "2024-01-01", api_key)

    while True:
        schedule.run_pending()
        time.sleep(1)

# Streamlit UI
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
