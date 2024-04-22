import openai
import os
import tools_handler as th

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

messages = []
messages.append({"role": "system", "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."})
messages.append({"role": "user", "content": "What's the weather like today in Buenos Aires"})
chat_response = chat_completion_request(
    messages, tools=th.get_tools()
)
assistant_message = chat_response.choices[0].message
messages.append(assistant_message)
print(assistant_message)