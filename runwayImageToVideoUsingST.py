import os
import time
import requests
import pandas as pd
import streamlit as st

st.title("Image-to-Video with RunwayML")

# File uploader
file_path = st.file_uploader("Upload the Excel file with Product Codes and Paths", type=["xlsx"])

if file_path:
    try:
        df = pd.read_excel(file_path)

        # Check for required columns
        required_columns = ['Image URL', 'Prompt', 'Product Code']
        if not all(col in df.columns for col in required_columns):
            st.error(f"Excel file must contain the following columns: {', '.join(required_columns)}")
        else:
            st.write("Excel file data preview:")
            st.dataframe(df)

            # Set your API key
            api_key = "key_32bfc791261f4e7fb13026b7d2553fb7cf24be4d960498532bd5b7c9fd7d0868879bc0d770c88c3b3ae37a09c0d6efaf4f8d62346f843fd192c7db6bb9053324"
            api_url = "https://api.dev.runwayml.com/v1/image_to_video"

            task_results = []

            for index, row in df.iterrows():
                image_url = row['Image URL']
                prompt_text = row['Prompt']
                product_code = row['Product Code']

                try:
                    # Display the image for the current row
                    st.image(image_url, caption=f"Image for Product Code: {product_code}", use_column_width=True)

                    # Prepare the payload for the API request
                    payload = {
                        "promptImage": image_url,
                        "promptText": prompt_text,
                        "model": "gen3a_turbo"
                    }

                    # Set the headers for the request
                    headers = {
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {api_key}",
                        "X-Runway-Version": "2024-09-13"
                    }

                    # Make the POST request to the API
                    response = requests.post(api_url, json=payload, headers=headers)
                    response.raise_for_status()  # Raise an error for bad responses

                    # Append task result
                    task_results.append((index, response.json()))

                    # Display task status
                    st.write(f'Task complete for row {index}:', response.json())

                except Exception as e:
                    st.error(f"Error processing image at row {index}: {e}")

            # Display all task results
            st.write("All tasks completed!")
            st.write(task_results)

    except Exception as e:
        st.error(f"Error loading or processing the file: {e}")
else:
    st.write("Please enter the path to your Excel file to start processing.")
