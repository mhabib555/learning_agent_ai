import os, asyncio
from dotenv import load_dotenv, find_dotenv
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner, function_tool, set_tracing_disabled
from tavily import TavilyClient


set_tracing_disabled(disabled=True)
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
base_url = os.getenv('GEMINI_BASE_URL')
tavily_api_key = os.getenv("TAVILY_API_KEY")

tavily_client = TavilyClient(tavily_api_key)

client: AsyncOpenAI = AsyncOpenAI(
    api_key=api_key,
    base_url=base_url
)


model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=client
)

@function_tool 
def search_web(query: str) -> object: 

    print('Searching web using tavily.') 
    print(f'Search query: {query} \n\n')

    response = tavily_client.search(
        query=query
    )
    return response

agent: Agent = Agent(
    name="Assistant",
    instructions="You are helpful assistant",
    model=model,
    tools=[search_web]
)

async def call_agent(): 

    result = await Runner.run(
        agent,
        "Weather in city Lahore"
    )

    print(result.final_output)

asyncio.run(call_agent())