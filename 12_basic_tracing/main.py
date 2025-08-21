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

base_agent: Agent = Agent(
    name="Assistant",
    instructions="You are helpful assistant",
    model=model,
)

creative_agent: Agent = base_agent.clone(
    name="Creative",
    instructions="You are creative"
)
async def call_agent():

    input = "give me one business idea, concise"

    result_base = await Runner.run(
        starting_agent=base_agent,
        input=input,
    )

    result_creative = await Runner.run(
        starting_agent=creative_agent,
        input=input,
    )

    print("\n\nBase: ", result_base.final_output)
    print("\n\nCreative: ", result_creative.final_output)



asyncio.run(call_agent())


