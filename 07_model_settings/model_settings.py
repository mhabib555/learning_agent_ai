import os
from dotenv import load_dotenv
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner, ModelSettings, function_tool, set_tracing_disabled

set_tracing_disabled(disabled=True)
load_dotenv()
api_key=os.getenv("GEMINI_API_KEY")
base_url=os.getenv("GEMINI_BASE_URL")

client: AsyncOpenAI = AsyncOpenAI(
    api_key=api_key,
    base_url=base_url
)

model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=client
)


creative_agent: Agent = Agent(
    name="Creative",
    instructions="You are helpful assistant",
    model_settings=ModelSettings(temperature=0.8),
    model= model
)

focused_agent: Agent = Agent(
    name="Focused",
    instructions="You are helpful assistant",
    model_settings=ModelSettings(temperature=0.2),
    model= model
)

creative_result = Runner.run_sync(
    creative_agent,
    "tell me a short story"
)
print("Creative answer")
print(creative_result.final_output)
print("\n\n")

creative_result = Runner.run_sync(
    focused_agent,
    "tell me a short story"
)
print("Focused answer")
print(creative_result.final_output)
