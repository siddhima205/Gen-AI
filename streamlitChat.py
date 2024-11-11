import streamlit as st
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate

# Streamlit-based function to handle conversation
def handle_conversation():
    st.title("Product Description Generator")

    # Create the prompt template
    template = ChatPromptTemplate(
        messages=[
            HumanMessagePromptTemplate.from_template(
                """You are a marketing expert specializing in promotional products. 
                Create a compelling product description for the following item:

                Product Type: {product_type}
                Product Name: {product_name}
                Material: {material}
                Weight: {weight}
                Diameter: {diameter}
                Colors Available: {colors}

                Focus on highlighting the benefits of this product for promotional use, 
                including how it can effectively promote a brand and engage customers. 
                The description should be persuasive and suitable for marketing purposes.
                """
            )
        ]
    )

    # Initialize the model
    model = OllamaLLM(model="mistral")

    # Collect inputs using Streamlit widgets
    product_type = st.text_input("Enter the product type:")
    product_name = st.text_input("Enter the product name:")
    material = st.text_input("Enter the product material:")
    weight = st.text_input("Enter the product weight (e.g., 12.00 oz):")
    diameter = st.text_input("Enter the product diameter (e.g., 2.75 inches):")
    colors_input = st.text_input("Enter the product colors (comma-separated, e.g., Green, Clear, Black):")

    # Create a button to generate the product description
    if st.button("Generate Product Description"):
        if product_type and product_name and material and weight and diameter and colors_input:
            colors = [color.strip() for color in colors_input.split(",")]

            # Format the prompt with the given product attributes
            formatted_prompt = {
                "product_type": product_type,
                "product_name": product_name,
                "material": material,
                "weight": weight,
                "diameter": diameter,
                "colors": ", ".join(colors),
            }

            # Create a chain using the template and model
            chain = template | model

            # Invoke the model with the formatted prompt
            result = chain.invoke(formatted_prompt)

            # Display the generated product description
            st.subheader("Generated Product Description:")
            st.write(result)
        else:
            st.warning("Please fill in all fields.")

# Main block to run the Streamlit app
if __name__ == "__main__":
    handle_conversation()
