import openai
import os
import tools_handler as th
import json

openai.api_key = os.environ["OPENAI_API_KEY"]
client = openai.OpenAI()

assistant = client.chat.completions.create(
  model="gpt-4-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who won the world series in 2020?"},
    {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    {"role": "user", "content": "Where was it played?"}
  ],
  tools=th.get_tools()
)

def chat_completion_request(messages, tools=None, tool_choice=None, model="gpt-4-turbo"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e

def execute_function(assistant_message):
    function_name = assistant_message.tool_calls[0].function.name
    if function_name == "get_current_temperature":
        arguments = json.loads(assistant_message.tool_calls[0].function.arguments)
        location = arguments["location"]
        unit = arguments["unit"]
        results = th.get_rain(location, unit)
    else:
        results = f"Error: function {function_name} does not exist"
    return results

messages = []
messages.append({"role": "system", "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."})

user_input = ""
while user_input != "bye":
    user_input = input("You: ")

    messages.append({"role": "user", "content": user_input})
    chat_response = chat_completion_request(
        messages, tools=th.get_tools()
    )
    assistant_message = chat_response.choices[0].message
    if assistant_message.tool_calls:
        results = execute_function(assistant_message)
        messages.append({"role": "function", "tool_call_id": assistant_message.tool_calls[0].id,
                         "name": assistant_message.tool_calls[0].function.name, "content": results})
        print(f"Chatbot: {results}")
    else:
        messages.append(assistant_message)
        print(f"Chatbot: {assistant_message}")