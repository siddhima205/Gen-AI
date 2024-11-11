from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

def handle_conversation():
    context = ""
    message = ""

    template = f"""
    You are a product description generator. Based on the following message, generate a detailed and creative product description from a promotional products industry perspective:
    
    Here is the context - {context}
    
    Input - {message}
    
    Provide information about the key features, benefits, target audience, and unique selling points.

    """

    model = OllamaLLM(model="mistral")
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    print("Welcome to Product Description Generator. Type 'exit' anytime to quit.")
    while True:
        user_input = input("Enter the product details: ")
        if user_input.lower() == "exit":
            break
        result = chain.invoke({"context": context, "message": user_input})
        print("Product Description Generator: ", result)
        context += f"\nUser: {user_input}\nAI: {result}"

if __name__ == "__main__":
    handle_conversation()
