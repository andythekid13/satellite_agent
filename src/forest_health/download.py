import requests
from PIL import Image
from io import BytesIO

def download_satellite_image(lat, lon, date, api_key):
    """
    Downloads satellite imagery for a given location and date from NASA Earthdata.
    Args:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.
        date (str): Date in YYYY-MM-DD format.
        api_key (str): API key for NASA Earthdata.
    Returns:
        image (PIL.Image): The satellite image.
    """
    endpoint = f"https://api.nasa.gov/planetary/earth/assets"
    params = {
        "lon": lon,
        "lat": lat,
        "date": date,
        "dim": 0.1,  # Resolution in degrees
        "api_key": api_key
    }
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        url = response.json().get("url")
        image_response = requests.get(url)
        return Image.open(BytesIO(image_response.content))
    else:
        raise Exception(f"Failed to fetch image: {response.status_code} {response.text}")
