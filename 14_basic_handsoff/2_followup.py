import os, asyncio
from dotenv import load_dotenv
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner, handoff

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

analyst_agent: Agent = Agent(
    name="AnalystAgent",
    instructions=(
        "You are expert in stock analyst for Pakistan stock exchange"
        "You know how to anaylze different companies"
        "It is all about Pakistan stock exchange"
        "Give answer as per your record"
    ),
    model=llm_model    
)

main_agent: Agent = Agent(
    name="InvestmentOrchestrator",
    instructions=(
        "You are investment helper. If user asks for "
        "anything related to business, handoff to the business_agent,"
        "if analyzing company stock, handoff to the analyst_agent"
    ),
    handoffs=[
        analyst_agent,
        handoff(business_agent)
    ],
    model=llm_model
)

async def call_agent():

    r1 = await Runner.run(
        starting_agent=main_agent,
        input="What was annual D/E of FCCL in 2020",
    )
    print("\nLast Agent: ", r1.last_agent.name)
    print("\nTurn 1 Reply: \n", r1.final_output)

    specialist = r1.last_agent    

    r2_input = r1.to_input_list() + [
        { "role": "user", "content" : "What about quick ratio"}
    ]
    r2 = await Runner.run(specialist, input=r2_input)
    print("\nTurn 2 Reply: \n", r2.final_output)


asyncio.run(call_agent())


