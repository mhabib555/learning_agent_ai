import os, asyncio
from dotenv import load_dotenv
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner, RunContextWrapper, function_tool
import random
from dataclasses import dataclass

load_dotenv()
api_key=os.getenv("GEMINI_API_KEY")
base_url=os.getenv("GEMINI_BASE_URL")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

@dataclass
class UserContext:
    name: str
    is_admin: bool = False

gemini_client: AsyncOpenAI = AsyncOpenAI(
    api_key=api_key,
    base_url=base_url
) 

llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model= "gemini-2.5-flash",
    openai_client=gemini_client
)

def is_admin(cntxt: RunContextWrapper[UserContext], agent: Agent[UserContext]) -> bool :
    return cntxt.context.is_admin

@function_tool(is_enabled=is_admin)
def get_random_number() -> int: 
    print("Generating random numbers by tool ...\n")
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
    
    habib_context = UserContext(
        name="Habib",
        is_admin=True
    )
    print("\n===== User is admin so tool is enabled =====\n")
    result = await Runner.run(
        starting_agent=main_agent,
        input="Get me 4 random numbers",
        context=habib_context
    )
    print("\nAgent Output: \n", result.final_output)


    abdullah_context = UserContext(
        name="Abdullah",
    )
    print("\n===== User is not admin so tool is disabled =====\n")
    result2 = await Runner.run(
        starting_agent=main_agent,
        input="Get me 4 random numbers",
        context=abdullah_context
    )
    print("\nAgent Output: \n", result2.final_output)

asyncio.run(call_agent())


