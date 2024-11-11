import os
import time
import requests
import pandas as pd
import streamlit as st
from runwayml import RunwayML

st.title("Image-to-Video with RunwayML")


file_path = st.file_uploader("Upload the Excel file with Product Codes and Paths", type=["xlsx"])

if file_path:
    try:
        df = pd.read_excel(file_path)
        
        required_columns = ['Image URL', 'Prompt', 'Product Code']
        if not all(col in df.columns for col in required_columns):
            st.error(f"Excel file must contain the following columns: {', '.join(required_columns)}")
        else:
            st.write("Excel file data preview:")
            st.dataframe(df)

            api_key = "key"
            client = RunwayML(api_key=api_key)

            task_results = []

            for index, row in df.iterrows():
                image_url = row['Image URL']
                prompt_text = row['Prompt']
                product_code = row['Product Code']

                try:
                   
                    st.image(image_url, caption=f"Image for Product Code: {product_code}", use_column_width=True)
                   
                    payload = {
                        "promptImage": image_url,
                        "promptText": prompt_text,
                        "model": "gen3a_turbo"
                    }
                    
                    headers = {
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {api_key}",
                        "X-Runway-Version": "2024-09-13"
                    }
                   
                    response = requests.post("https://api.dev.runwayml.com/v1/image_to_video", json=payload, headers=headers)
                    response.raise_for_status()  # Raise an error for bad responses

                    task_data = response.json()
                    task_id = task_data.get('id')
                    task_results.append((index, task_data))

                    st.write(f'Task submitted for row {index} with task ID: {task_id}')

                    
                    while True:
                        task = client.tasks.retrieve(id=task_id)
                        if task.status == 'SUCCEEDED':
                            st.write(f"Task for Product Code {product_code} completed successfully.")
                            video_url = task.output[0]
                            st.video(video_url)

                            video_response = requests.get(video_url)
                            video_filename = f"{product_code}_video.mp4"

                            st.download_button(
                                label="Download Video",
                                data=video_response.content,
                                file_name=video_filename,
                                mime="video/mp4"
                            )
                            break
                        elif task.status == 'FAILED':
                            st.error(f"Task for Product Code {product_code} failed.")
                            break
                        else:
                            st.write("Processing... Please wait.")
                            time.sleep(10)  

                except Exception as e:
                    st.error(f"Error processing image at row {index}: {e}")

            
            st.write("All tasks completed!")
            st.write(task_results)

    except Exception as e:
        st.error(f"Error loading or processing the file: {e}")
else:
    st.write("Please enter the path to your Excel file to start processing.")
