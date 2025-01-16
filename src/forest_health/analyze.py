from transformers import AutoModelForImageClassification
from .process import process_image

# Load the model
model = AutoModelForImageClassification.from_pretrained("ibm-nasa-geospatial/prithvi-large")

def analyze_forest_health(image):
    """
    Analyze the forest health from satellite image using the IBM pre-trained model.
    Args:
        image (PIL.Image): The satellite image.
    Returns:
        predictions (dict): Forest health predictions.
    """
    inputs = process_image(image)
    outputs = model(**inputs)
    predictions = outputs.logits.softmax(dim=1).detach().numpy()
    return predictions
