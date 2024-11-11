import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO
from mistralai import Mistral
from fuzzywuzzy import fuzz
from sentence_transformers import SentenceTransformer, util

def check_product_color_and_type(url):
    api_key = "K6KRQPY4DR9B1uSBzbMAg0Q8C8Hile3H"
    model = "pixtral-12b-2409"
    client = Mistral(api_key=api_key)
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Give me comma separated one word for type of product and prominent color in the image"
                },
                {
                    "type": "image_url",
                    "image_url": url
                }
            ]
        }
    ]
    chat_response = client.chat.complete(
        model=model,
        messages=messages
    )
    
    product_info = chat_response.choices[0].message.content
    product_type, product_color = product_info.split(", ")
    return product_type, product_color

model = SentenceTransformer('all-MiniLM-L6-v2')

def to_camel_case(s):
    return ''.join(word.capitalize() for word in s.split('_'))

def are_similar(word1, word2, threshold=70):
    similarity = fuzz.token_set_ratio(word1.lower(), word2.lower())
    return similarity

def are_similar_using_ai(word1, word2, threshold=0.5):
    embeddings1 = model.encode(word1, convert_to_tensor=True)
    embeddings2 = model.encode(word2, convert_to_tensor=True)

    cosine_similarity = util.pytorch_cos_sim(embeddings1, embeddings2)
    return cosine_similarity.item()

def handle_image_color_detection():
    st.title("Image Fault Detection with Pixtral")

    product_code = st.text_input("Enter the product code:")
    excel_file = st.file_uploader("Upload the Excel file with Product Codes and Paths", type=["xlsx"])

    if st.button("Find Product Details"):
        if product_code and excel_file:
            df = pd.read_excel(excel_file)
            image_row = df[df['Product Code'] == product_code]           
            
            if not image_row.empty:
                image_path = image_row.iloc[0]['Image Path']
                product_type, product_color = check_product_color_and_type(image_path)
                
                product_color = to_camel_case(product_color.lower())
                product_type = to_camel_case(product_type.lower())
                
                pim_color = to_camel_case(image_row.iloc[0]['Product Color'].lower())
                pim_type = to_camel_case(image_row.iloc[0]['Product Type'].lower())
                
                color_match =  are_similar_using_ai(product_color, pim_color) 
                type_match =  are_similar_using_ai(product_type, pim_type) 
                
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.image(image_path, caption="Product Image", use_column_width=True)
                st.subheader("Product Details Comparison:")               
                comparison_data = {
                " ": ["Product Color", "Product Type"],
                "Pixtral": [product_color, product_type],
                "PIM": [pim_color, pim_type],
                "Similar": ["Yes" if color_match>=0.5 else "No", "Yes" if type_match>=0.5 else "No"],
                "Similarity": [color_match, type_match]
                }
                #comparison_df = pd.DataFrame(comparison_data)
                
                
                st.table(comparison_data)
            
            else:
                st.error(f"Product code '{product_code}' not found in the Excel file.")
        else:
            st.warning("Please provide both an image code and an Excel file.")

def handle_image_color_detection_all_items():
    st.title("Image Fault Detection with Pixtral")

    excel_file = st.file_uploader("Upload the Excel file with Product Codes and Paths", type=["xlsx"])

    if st.button("Find Product Details"):
        if excel_file:
            df = pd.read_excel(excel_file)

            # Iterate through each product in the Excel file
            for index, row in df.iterrows():
                product_code = row['Product Code']
                image_path = row['Image Path']

                # Check if the image path exists
                if pd.isna(image_path):
                    st.warning(f"No image path found for Product Code '{product_code}'. Skipping...")
                    continue

                product_type, product_color = check_product_color_and_type(image_path)
                product_color = to_camel_case(product_color.lower())
                product_type = to_camel_case(product_type.lower())

                pim_color = to_camel_case(row['Product Color'].lower())
                pim_type = to_camel_case(row['Product Type'].lower())

                color_match = are_similar_using_ai(product_color, pim_color) 
                type_match = are_similar_using_ai(product_type, pim_type)

                # Display the image and details for each product
                st.subheader(f"Product Code: {product_code}")
                
                # Display the image
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.image(image_path, caption=f"Product Image - {product_code}", use_column_width=True)
                
                # Display the comparison details
                comparison_data = {
                    " ": ["Product Color", "Product Type"],
                    "Pixtral": [product_color, product_type],
                    "PIM": [pim_color, pim_type],
                    "Similar": ["Yes" if color_match >= 0.5 else "No", "Yes" if type_match >= 0.5 else "No"],
                    "Similarity": [color_match, type_match]
                }
                
                st.table(comparison_data)

        else:
            st.warning("Please upload an Excel file.")

if __name__ == "__main__":
    handle_image_color_detection_all_items()
