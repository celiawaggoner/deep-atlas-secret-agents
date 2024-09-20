from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from llm.llm_interface import send_to_llm, send_to_gpt
from utils.tool_executor import execute_tool
from utils.mission_log import load_mission_log, save_mission_log, update_mission_log
import json

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on('message')
def handle_message(user_message):
    # Step 1: Load the mission log
    mission_log = load_mission_log()

    # Step 2: Send the user message to the LLM, along with the mission log if needed
    # llm_response = send_to_llm(user_message)
    llm_response = send_to_gpt(user_message)

    try:
        # Step 3: Parse the LLM response and process tool invocations or responses
        llm_data = json.loads(llm_response)

        if llm_data.get("action") == "invoke_tool":
            emit('response', {'message': llm_data.get("message")})
            tool_name = llm_data.get("tool_name")
            parameters = llm_data.get("parameters")

            print(f"Invoking tool: {tool_name} with parameters: {parameters}")

            # Execute the tool and get the result
            tool_result = execute_tool(tool_name, parameters)

            print(f"Tool result: {tool_result}")

            # Send the tool result back to the LLM for final formatting
            # final_response = send_to_llm(tool_result, is_tool_result=True)
            final_response = send_to_gpt(tool_result, is_tool_result=True)

            print(f"Final response: {final_response}")

            # Emit the final formatted response to the user
            final_response_json = json.loads(final_response)
            emit('response', {'message': final_response_json.get("message")})

        else:
            # If no tool invocation is needed, send the LLM's response back directly
            emit('response', {'message': llm_data.get("message")})

        # Step 4: Update the mission log with the latest game state
        update_mission_log(mission_log, user_message)

    except json.JSONDecodeError:
        # If the LLM response is not in JSON format, return it as a plain message
        emit('response', {'message': llm_response})

if __name__ == '__main__':
    socketio.run(app, debug=True)
