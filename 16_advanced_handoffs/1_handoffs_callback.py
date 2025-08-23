import os, asyncio
from dotenv import load_dotenv
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner, RunContextWrapper, function_tool, handoff
from pydantic import BaseModel

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

class NewsRequest(BaseModel):
    topic: str
    reason: str

@function_tool()
def get_weather(city: str) -> str:
    """A simple function to get the weather for a user."""
    return f"The weather for {city} is sunny."

def handoff_process(ctx: RunContextWrapper, input_data: NewsRequest) -> None:
    print(input_data)
    

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
        handoff(news_agent, on_handoff=handoff_process, input_type= NewsRequest)
    ]
)

async def call_agent():
    
    result = await Runner.run(
        starting_agent=weather_agent,
        input="Check if there is any news related to AI",
    )
    print("\nAgent Output: \n", result.final_output)



asyncio.run(call_agent())


