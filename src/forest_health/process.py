from transformers import AutoImageProcessor

feature_extractor = AutoImageProcessor.from_pretrained("google/vit-base-patch16-224-in21k")

def process_image(image):
    """
    Preprocess the satellite image for model inference.
    """
    return feature_extractor(images=image, return_tensors="pt")
