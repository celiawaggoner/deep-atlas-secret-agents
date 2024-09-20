from langchain_ollama.chat_models import ChatOllama
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
print(OPENAI_API_KEY)

MODEL_NAME = "llama2:7b"

# Initialize the ChatOllama model
chat_model = ChatOllama(model=MODEL_NAME)

gpt_model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.1, openai_api_key=OPENAI_API_KEY)

def get_llm_prompt(message, is_tool_result=False):
    if is_tool_result:
        # When passing a tool result back to the LLM for final formatting
        return f"""
        You are an assistant helping a secret agent complete a mission. You have received important intel from a tool.
        Your task is to summarize the tool result, in a concise and mission-relevant way, keeping the tone of a covert operative.
        You must respond in the following JSON format:

        {{
          "action": "respond",
          "message": <tool_result_summary>
        }}

        Tool result: {message}
        """

    else:
        # When receiving a user message, clarify tool use with specific examples
        return f"""
        You are an assistant working with a secret agent on a top-secret mission. Your job is to provide assistance in solving puzzles, retrieving information, and making decisions.

        IMPORTANT: Always respond in the following JSON format. Only invoke a tool when necessary.

        Examples of invoking a tool (like weather or decryption):

        {{
          "action": "invoke_tool",
          "tool_name": "weather",
          "parameters": {{
            "location": "Tokyo"
          }},
          "message": "Retrieving the weather for Tokyo now. Stand by, agent."
        }}

        {{
          "action": "invoke_tool",
          "tool_name": "decrypt",
          "parameters": {{
            "encrypted_message": "KHOOR DJHQW",
            "key": 3
          }},
          "message": "Decrypting the message now. Stand by, agent."
        }}

        Example of a regular response (no tool needed):

        {{
          "action": "respond",
          "message": "The answer is 4, agent."
        }}

        For subjective or creative queries, you can also respond without invoking a tool:

        Example:
        - Agent asks: "What disguise should I wear?"
          Respond with:
          {{
            "action": "respond",
            "message": "I recommend a black trench coat with sunglasses for this mission, agent."
          }}

        Agent message: {message}
        """


def send_to_llm(message, is_tool_result=False):
    # Create a custom prompt based on whether it's a user message or tool result
    prompt = get_llm_prompt(message, is_tool_result)

    # Send the message to the LLM
    messages = [HumanMessage(content=prompt)]
    response = chat_model(messages)

    return response.content  # Return the LLM's response

def send_to_gpt(message, is_tool_result=False):
    # Create a human message (user input)
    prompt = get_llm_prompt(message, is_tool_result)

    # Send the prompt to the GPT model via LangChain
    messages = [HumanMessage(content=prompt)]

    # Generate response using the GPT model
    response = gpt_model(messages)

    # Return the response content (assuming a single choice)
    return response.content
