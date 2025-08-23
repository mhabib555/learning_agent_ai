import os, asyncio
from dotenv import load_dotenv
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner, RunContextWrapper, HandoffInputData, function_tool, handoff
from dataclasses import dataclass

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

@dataclass
class UserContext:
    allowed_agents: list
    
@function_tool()
def get_weather(city: str) -> str:
    """A simple function to get the weather for a user."""
    return f"The weather for {city} is sunny."

def is_agent_allowed(ctx: RunContextWrapper[UserContext], agent: Agent[UserContext]) -> bool:
    return True if agent.name in ctx.context.allowed_agents else False

news_agent: Agent = Agent(
    name="NewsAgent",
    instructions="You get latest news about tech and share it with me",
    model=llm_model
)

weather_agent: Agent = Agent(
    name="WeatherAgent",
    instructions="You are weather expert",
    model=llm_model,
    tools=[get_weather],
    handoffs=[
        handoff(news_agent, is_enabled= is_agent_allowed)
    ]
)

async def call_agent():
    
    input = "Check if there is any news related to AI"

    # User 1
    user1_ctx = UserContext(
        allowed_agents="WeatherAgent"
    )    
    result = await Runner.run(
        starting_agent=weather_agent,
        input=input,
        context=user1_ctx
    )
    print("\nAgent Output: \n", result.final_output)

    # User 2 
    user2_ctx = UserContext(
        allowed_agents="CustomerAgent"
    )    
    result2 = await Runner.run(
        starting_agent=weather_agent,
        input=input,
        context=user2_ctx
    )
    print("\nAgent 2 Output: \n", result2.final_output)



asyncio.run(call_agent())


