import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO
from transformers import BlipProcessor, BlipForConditionalGeneration

def find_prominent_color_with_blip(image_path):
    
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

   
    if image_path.startswith('http'):   
        response = requests.get(image_path)
        image = Image.open(BytesIO(response.content))
    else:
       
        image = Image.open(image_path)

   
    inputs = processor(image, return_tensors="pt")

   
    out = model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)      
    prominent_color = extract_color_from_caption(caption)

    return prominent_color, caption

def extract_color_from_caption(caption):
    colors = ["red", "green", "blue", "yellow", "black", "white", "orange", "purple", "pink", "brown", "gray"]
    for color in colors:
        if color in caption.lower():
            return color
    return "No prominent color found"

def handle_image_color_detection():
    st.title("Image Color Detection with BLIP")

    product_code = st.text_input("Enter the image code:")
    excel_file = st.file_uploader("Upload the Excel file with Product Codes and Paths", type=["xlsx"])

    if st.button("Find Prominent Color"):
        if product_code and excel_file:
            df = pd.read_excel(excel_file)
            image_row = df[df['Product Code'] == product_code]
            if not image_row.empty:
                image_path = image_row.iloc[0]['Image Path']
                prominent_color, caption = find_prominent_color_with_blip(image_path)
                st.subheader("Most Prominent Color in the Image (Based on Caption):")
                st.write(f"Detected Caption: {caption}")
                st.write(f"Prominent Color: {prominent_color}")
            else:
                st.error(f"Product code '{product_code}' not found in the Excel file.")
        else:
            st.warning("Please provide both an image code and an Excel file.")

if __name__ == "__main__":
    handle_image_color_detection()
