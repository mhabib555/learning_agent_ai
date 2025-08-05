import os, asyncio 
from dotenv import load_dotenv, find_dotenv
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner, set_tracing_disabled, set_default_openai_api, set_default_openai_client

load_dotenv(find_dotenv())
api_key = os.getenv("GEMINI_API_KEY")
base_url = os.getenv("GEMINI_BASE_URL")
set_tracing_disabled(disabled=True)
set_default_openai_api("chat_completions")

client: AsyncOpenAI = AsyncOpenAI(
    api_key=api_key,
    base_url=base_url
)
set_default_openai_client(client)

async def global_level():
    
    agent: Agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant",
        model="gemini-2.5-flash"
    )

    response = await Runner.run(
        agent,
        "One line advice"
    )

    print(response.final_output)

if __name__ == "__main__":
    asyncio.run(global_level())
