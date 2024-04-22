import openai
import os
import tools_handler as th
import event_handler

openai.api_key = os.environ["OPENAI_API_KEY"]
client = openai.OpenAI()

assistant = client.beta.assistants.create(
  instructions="You are a weather bot. Use the provided functions to answer questions.",
  model="gpt-4-turbo",
  tools=th.get_tools()
)

thread = client.beta.threads.create()
message = client.beta.threads.messages.create(
  thread_id=thread.id,
  role="user",
  content="What's the weather in San Francisco today and the likelihood it'll rain?",
)

print(message.content)

with client.beta.threads.runs.stream(
        thread_id=thread.id,
        assistant_id=assistant.id,
        event_handler=event_handler.EventHandler()
) as stream:
    stream.until_done()