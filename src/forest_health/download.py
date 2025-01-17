def download_satellite_image(lat, lon, date, token):
    """
    Downloads satellite imagery for a given location and date from NASA Earthdata.
    Args:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.
        date (str): Date in YYYY-MM-DD format.
        token (str): NASA Earthdata token for authentication.
    Returns:
        image (PIL.Image): The satellite image.
    """
    # NASA Earthdata API endpoint
    endpoint = "https://api.nasa.gov/planetary/earth/assets"
    
    # Parameters for the API request
    params = {
        "lon": lon,
        "lat": lat,
        "date": date,
        "dim": 0.1,  # Spatial resolution in degrees
        "api_key": token,
    }
    
    # Make the API request
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        try:
            # Extract the image URL from the response
            image_url = response.json().get("url")
            if not image_url:
                raise Exception("No image URL found in the API response.")
            
            # Download the image from the URL
            image_response = requests.get(image_url)
            image_response.raise_for_status()
            
            # Open the image
            return Image.open(BytesIO(image_response.content))
        except Exception as e:
            raise Exception(f"Error processing the image: {e}")
    else:
        raise Exception(f"Failed to download image: {response.status_code} {response.text}")
