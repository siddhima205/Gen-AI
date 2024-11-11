from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import pandas as pd

# Load product data from an Excel file
def load_product_data(file_path):
    try:
        product_data = pd.read_excel(file_path)
        print("Product data loaded successfully.")
        print(product_data.head())  # Print the first few rows of the DataFrame for verification
        print("Columns in DataFrame:", product_data.columns)  # Print columns to verify names
        return product_data
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to recommend products based on the product catalog, user input, and color preference
def recommend_products(product_data, query):
    query = query.lower()
    
    # Debug: Print the query to see what the user input was
    print(f"User Query: '{query}'")

    # Filter products where the query matches product name, type, or color
    matching_products = product_data[
        product_data['Product Name'].str.contains(query, case=False, na=False) |
        product_data['Product Type'].str.contains(query, case=False, na=False) |
        product_data['Color'].str.contains(query, case=False, na=False)
    ]
    
    # Debug: Print the matching products for verification
    print("Matching Products Found:")
    print(matching_products)

    if matching_products.empty:
        return "Sorry, no products matched your query."
    
    recommendations = "Here are some products we recommend based on your input:\n"
    for index, row in matching_products.iterrows():
        recommendations += f"- {row['Product Name']} ({row['Product Type']}, Color: {row['Color']}) - Code: {row['Product Code']}\n"
    
    return recommendations

# Function to build the template for product recommendations
def generate_recommendation_template(context, message):
    template = f"""
    You are a product recommendation assistant. Based on the following message, provide personalized recommendations from a product catalog in the promotional products industry:
    
    Here is the context - {context}
    
    Input - {message}
    
    Recommend products by identifying the product category, color, and mentioning key details like product name, type, and features.
    """
    return template

# Function to handle product recommendation conversation
def handle_conversation(product_data):
    context = ""
    model = OllamaLLM(model="llama3")
    
    print("Welcome to the Product Recommendation System. Type 'exit' anytime to quit.")
    
    while True:
        user_input = input("Enter your product requirements or preferences (e.g., product type, color): ")
        if user_input.lower() == "exit":
            break
        
        product_recommendations = recommend_products(product_data, user_input)
        context += f"\nUser: {user_input}\nAI: {product_recommendations}"
        
        template = generate_recommendation_template(context, user_input)
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | model
        
        ai_response = chain.invoke({"context": context, "message": user_input})
        
        print("Product Recommendation System: ", ai_response)
        context += f"\nAI: {ai_response}"

if __name__ == "__main__":
    # Load your product catalog
    file_path = '../ProductData.xlsx'  # Update this path to your Excel file
    product_data = load_product_data(file_path)
    
    # Start the conversation loop for product recommendation
    if product_data is not None:
        handle_conversation(product_data)
