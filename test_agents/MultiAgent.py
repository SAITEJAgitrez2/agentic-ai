from agno.agent import Agent
from agno.models.huggingface import HuggingFace
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools

import os
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
os.environ["HF_TOKEN"]=os.getenv("HF_TOKEN")

web_agent=Agent(
    name="Web Agent",
    role="search the web for information",
    model=Groq(id="qwen-2.5-32b"),
    tools=[DuckDuckGoTools()],
    instructions="Always include the sources",
    show_tool_calls=True,
    markdown=True,
)

finance_agent = Agent(
    name="Finance Agent",
    role="Get financial data",
    model=HuggingFace(
        id="meta-llama/Meta-Llama-3-8B-Instruct",
        max_tokens=1024
    ),
    tools=[
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            stock_fundamentals=True,
            company_info=True,
        )
    ],
    instructions="Use tables to display data",
    show_tool_calls=True,
    markdown=True,
)

agent_team=Agent(
    team=[web_agent,finance_agent],
    model=Groq(id="qwen-2.5-32b"),
    instructions=["Always include sources", "Use tables to display data"],
    show_tool_calls=True,
    markdown=True,

)
#print("HF Token loaded:", os.getenv("HF_TOKEN")[:8], "******")

agent_team.print_response("Analyze companies like Tesla, NVIDIA, Apple and suggest which company is good to invest in 2025 March")