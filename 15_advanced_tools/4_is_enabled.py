import os, asyncio
from dotenv import load_dotenv
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner, MaxTurnsExceeded, function_tool
import random

load_dotenv()
api_key=os.getenv("GEMINI_API_KEY")
base_url=os.getenv("GEMINI_BASE_URL")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

gemini_client: AsyncOpenAI = AsyncOpenAI(
    api_key=api_key,
    base_url=base_url
) 

llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model= "gemini-2.5-flash",
    openai_client=gemini_client
)

@function_tool(is_enabled=False)
def get_random_number() -> int: 
    """This tool is temporary unavailable"""
    return random.randint(1, 100)
    

main_agent: Agent = Agent(
    name="Assistant",
    instructions="You are assistant to help user",
    tools=[
        get_random_number,
    ],
    model=llm_model
)

async def call_agent():

    result = await Runner.run(
        starting_agent=main_agent,
        input="Get me 4 random numbers",
    )

    print("\nAgent Output: \n", result.final_output)


asyncio.run(call_agent())


