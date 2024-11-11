from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import pandas as pd

# Load product data from an Excel file
def load_product_data(file_path):
    product_data = pd.read_excel(file_path)
    return product_data

# Function to build the template for product recommendations
def generate_recommendation_template(context, message):
    template = f"""
    You are a product recommendation assistant. Based on the following message, provide personalized recommendations from a product catalog in the promotional products industry:
    
    Here is the context - {context}
    
    Input - {message}
    
    Recommend products by identifying the product category and mentioning key details like product name, type, and features.
    """
    return template

# Function to handle product recommendation conversation
def handle_conversation(product_data):
    context = ""

    # Initialize the AI model
    model = OllamaLLM(model="mistral")
    
    print("Welcome to the Product Recommendation System. Type 'exit' anytime to quit.")
    
    while True:
        user_input = input("Enter your product requirements or preferences: ")
        if user_input.lower() == "exit":
            break
        
        # Generate the prompt template based on the user input and context
        template = generate_recommendation_template(context, user_input)
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | model
        
        # Invoke the model to get product recommendations
        result = chain.invoke({"context": context, "message": user_input})
        
        # Display recommendations and append conversation context
        print("Product Recommendation System: ", result)
        context += f"\nUser: {user_input}\nAI: {result}"
        
        # Optionally, update product data with new recommendations or insights
        
if __name__ == "__main__":
    # Load your product catalog
    file_path = '../ProductData.xlsx'  
    product_data = load_product_data(file_path)
    
    # Start the conversation loop for product recommendation
    handle_conversation(product_data)
