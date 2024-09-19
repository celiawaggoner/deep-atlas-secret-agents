from langchain_ollama.chat_models import ChatOllama
from langchain.schema import HumanMessage

MODEL_NAME = "llama2:7b"

# Initialize the ChatOllama model
chat_model = ChatOllama(model=MODEL_NAME)

def send_to_llm(message):
    # Create a human message (user input)
    messages = [HumanMessage(content=message)]

    # Generate response from Ollama model
    response = chat_model(messages)

    return response.content
