from transformers import AutoFeatureExtractor

# Load the feature extractor
feature_extractor = AutoFeatureExtractor.from_pretrained("ibm-nasa-geospatial/prithvi-large")

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
