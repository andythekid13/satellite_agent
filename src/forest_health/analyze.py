from transformers import ViTForImageClassification
from .process import process_image

model = ViTForImageClassification.from_pretrained("google/vit-base-patch16-224-in21k", ignore_mismatched_sizes=True)

def analyze_forest_health(image):
    """
    Analyze the forest health from satellite image using the pre-trained model.
    """
    inputs = process_image(image)
    outputs = model(**inputs)
    return outputs.logits.softmax(dim=1).detach().numpy()
