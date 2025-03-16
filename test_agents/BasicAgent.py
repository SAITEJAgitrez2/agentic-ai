from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools

import os
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")


agent=Agent(
    model=Groq(id="qwen-2.5-32b"),
    description="You are an assistant please reply based ont he question",
    tools=[DuckDuckGoTools()],
    markdown=True
)

agent.print_response("what is the agentic ai tech stack used in the market? and is agno used in production?")