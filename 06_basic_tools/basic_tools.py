import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner, function_tool, set_tracing_disabled

set_tracing_disabled(disabled=True)
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
base_url = os.getenv('GEMINI_BASE_URL')

client: AsyncOpenAI = AsyncOpenAI(
    api_key=api_key,
    base_url=base_url
)


model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=client
)

@function_tool
def add(a: int, b: int) -> int:
    print("Adding .....")
    return a + b

@function_tool
def multiply(a: int, b: int) -> int:
    print("Multiplying...")
    return a * b


agent: Agent = Agent(
    name="Assistant",
    instructions="You are helpful assistant",
    model=model,
    tools=[add, multiply]
)

result = Runner.run_sync(
    agent,
    "Add 2 and 5 and multiply by 2"
)

print(result.final_output)
