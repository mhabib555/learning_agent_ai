import os, asyncio
from dotenv import load_dotenv
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner

load_dotenv()
api_key=os.getenv("GEMINI_API_KEY")
base_url=os.getenv("GEMINI_BASE_URL")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

gemini_client: AsyncOpenAI = AsyncOpenAI(
    api_key=api_key,
    base_url=base_url
) 

model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model= "gemini-2.5-flash",
    openai_client=gemini_client
)

agent: Agent = Agent(
    name="Assistant",
    instructions="You are helpful assistant",
    model=model,
)

async def call_agent():

    input = "give me one business idea, concise"

    result_base = await Runner.run(
        starting_agent=agent,
        input=input,
    )

    print("\nAgent: ", result_base.final_output)



asyncio.run(call_agent())


