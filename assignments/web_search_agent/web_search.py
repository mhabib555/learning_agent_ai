import os, asyncio
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, set_tracing_disabled
# importing web search api
from tavily import TavilyClient


# Tracing Disabled
set_tracing_disabled(disabled=True)

# Importing env variables
load_dotenv(find_dotenv())
gemini_api_key=os.getenv("GEMINI_API_KEY")
tavily_api_key=os.getenv("TAVILY_API_KEY")

# Web Search Client
tavily_client: TavilyClient = TavilyClient(
    api_key=tavily_api_key
)

# LLM Service
external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# LLM Model
llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

@function_tool
def web_search(query: str) -> int:
    print(f"\nSearching....{query}")
    response = tavily_client.search(query=query)
    return response

agent: Agent = Agent(
    name="Assistant",
    instructions="You are helpful math assistant",
    model=llm_model,
    tools=[web_search]
)

async def call_agent():
    
    response = await Runner.run(
        starting_agent=agent,
        input="looking for a top 2 web development books",
    )

    print(response.final_output)
    


if __name__ == "__main__":
    asyncio.run(call_agent())
