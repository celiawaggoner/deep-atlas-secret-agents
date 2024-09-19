from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from llm.llm_interface import send_to_llm
from utils.tool_executor import execute_tool
from utils.mission_log import load_mission_log, save_mission_log

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on('message')
def handle_message(message):
    # Send user message to the LLM
    llm_response = send_to_llm(message)

    # Send the response to the user
    emit('response', {'message': llm_response['message']})

if __name__ == '__main__':
    socketio.run(app, debug=True)
