from crewai import Agent, LLM
from dotenv import load_dotenv
import os

load_dotenv()

llm = LLM(
    model="gemini/gemini-3.1-flash-lite",
    api_key=os.getenv("GEMINI_API_KEY")
)

outreach_specialist = Agent(
    role="LinkedIn Outreach Specialist",
    goal="Draft short, genuine LinkedIn messages that start real conversations with hiring managers",
    backstory="""You have 8 years of experience in recruitment and networking. 
    You know that the best outreach messages are brief, specific, and ask for 
    nothing more than a conversation. You never use generic templates.""",
    llm=llm,
    verbose=False
)