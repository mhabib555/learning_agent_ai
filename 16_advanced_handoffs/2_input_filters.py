import os, asyncio
from dotenv import load_dotenv
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner, HandoffInputData, function_tool, handoff

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

def summarized_news_transfer(data: HandoffInputData) -> HandoffInputData:
    print("\n\nHandoff: Summarizing news transfer..\n\n")
    
    summarized_conversation = "Get latest tech news"
    
    print("\n\nItem 1: ", data.input_history)
    print("\n\nItem 2: ", data.pre_handoff_items)
    print("\n\nItem 3: ", data.new_items)
    
    return HandoffInputData(
        input_history=summarized_conversation,
        pre_handoff_items=(),
        new_items=(),
    )
    
    
@function_tool()
def get_weather(city: str) -> str:
    """A simple function to get the weather for a user."""
    return f"The weather for {city} is sunny."

    

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
        handoff(news_agent, input_filter= summarized_news_transfer)
    ]
)

async def call_agent():
    
    result = await Runner.run(
        starting_agent=weather_agent,
        input="Check if there is any news related to AI",
    )
    print("\nAgent Output: \n", result.final_output)



asyncio.run(call_agent())


