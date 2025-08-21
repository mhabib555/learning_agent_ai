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

llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model= "gemini-2.5-flash",
    openai_client=gemini_client
)

business_agent: Agent = Agent(
    name="BusinessAgent",
    instructions=(
        "You are expert in business management. You know how different businesses works."
        "You know what effect its profit"
    ),
    model=llm_model
)

analyst_agent: Agent = Agent(
    name="AnalystAgent",
    instructions=(
        "You are expert in stock analyst for Pakistan stock exchange"
        "You know how to anaylze different companies"
    ),
    model=llm_model    
)

orchestrator: Agent = Agent(
    name="InvestmentOrchestrator",
    instructions=(
        "You are investment helper. If user asks for "
        "anything related to business, call business_agent,"
        "if analyzing company stock, call analyst_agent"
    ),
    tools=[
        business_agent.as_tool(
            tool_name="business_agent",
            tool_description="Analyze company business"
        ),
        analyst_agent.as_tool(
            tool_name="analyst_agent",
            tool_description="Analyze company stock"
        )

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


