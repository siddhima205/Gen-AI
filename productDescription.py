from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate

def handle_conversation():
    print("Welcome to Product Description Generator. Type 'exit' anytime to quit.")
    
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

    while True:
        # Collect user inputs
        product_type = input("Enter the product type: ")
        product_name = input("Enter the product name: ")
        material = input("Enter the product material: ")
        weight = input("Enter the product weight (e.g., 12.00 oz): ")
        diameter = input("Enter the product diameter (e.g., 2.75 inches): ")
        colors_input = input("Enter the product colors (comma-separated, e.g., Green, Clear, Black): ")
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
        print("Product Description Generator: ", result)

if __name__ == "__main__":
    handle_conversation()
