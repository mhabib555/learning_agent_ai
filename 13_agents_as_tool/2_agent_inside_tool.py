import os, asyncio
from dotenv import load_dotenv
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner, function_tool

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

business_agent: Agent = Agent(
    name="BusinessAgent",
    instructions=(
        "You are expert in business management. You know how different businesses works."
        "You know what effect its profit"
        "It is all about Pakistan stock exchange"
    ),
    model=llm_model
)

@function_tool
async def business_expert(query: str) -> str:
    result = await Runner.run(
        starting_agent=business_agent,
        input=query
    )
    return str(result.final_output)


orchestrator: Agent = Agent(
    name="InvestmentOrchestrator",
    instructions=(
        "You are investment helper."
        "Use tool as required"
    ),
    tools=[
        business_expert
    ],
    model=llm_model
)

async def call_agent():

    input = "Analyze FCCL stock, concise"

    result_base = await Runner.run(
        starting_agent=orchestrator,
        input=input,
    )

    print("\nAgent: ", result_base.final_output)



asyncio.run(call_agent())


