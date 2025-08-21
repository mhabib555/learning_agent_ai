import os, asyncio
from dotenv import load_dotenv
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner, function_tool, set_tracing_disabled

set_tracing_disabled(disabled=True)
load_dotenv()
api_key=os.getenv("GEMINI_API_KEY")
base_url=os.getenv("GEMINI_BASE_URL")

gemini_client: AsyncOpenAI = AsyncOpenAI(
    api_key=api_key,
    base_url=base_url
) 

model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model= "gemini-2.5-flash",
    openai_client=gemini_client
)

@function_tool
def add( a: int, b: int) -> int:
    return a + b

@function_tool
def subtract( a: int, b: int) -> int:
    return a - b

@function_tool
def multiply( a: int, b: int) -> int:
    return a * b


base_agent: Agent = Agent(
    name="Assistant",
    instructions="You are helpful assistant",
    model=model,
    tools=[add]
)

shared_clone: Agent = base_agent.clone(
    name="SharedClone",
    instructions="You are creative",
)

base_agent.tools.append(subtract)

print("Base tools: ", len(base_agent.tools))
print("SharedClone tools: ", len(shared_clone.tools))


independent_clone: Agent = base_agent.clone(
    name="independentClone",
    instructions="You are creative",
    tools=[multiply] 
)

base_agent.tools.append(subtract)

print("IndependentClone tools: ", len(independent_clone.tools))
