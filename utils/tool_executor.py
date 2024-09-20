from gadgets.weather import get_weather
from gadgets.decryptor import decrypt_message

def execute_tool(tool_name, parameters):
    if tool_name == 'weather':
        location = parameters.get('location')
        return get_weather(location)

    elif tool_name == 'decrypt':
        encrypted_message = parameters.get('encrypted_message')
        key = parameters.get('key')
        return decrypt_message(encrypted_message, key)

    else:
        return "Tool not recognized."
