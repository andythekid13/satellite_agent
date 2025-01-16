import streamlit as st

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
