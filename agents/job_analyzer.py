from crewai import Agent, LLM
from dotenv import load_dotenv
import os

load_dotenv()

llm = LLM(
    model="gemini/gemini-3.1-flash-lite",
    api_key=os.getenv("GEMINI_API_KEY")
)

job_analyzer = Agent(
    role="Job Description Analyst",
    goal="Extract structured, actionable information from job descriptions",
    backstory="""You are an expert career consultant with 10 years of experience 
    analyzing government job postings. You identify exactly what employers want 
    and present it in a clear, structured way that other specialists can act on.""",
    llm=llm,
    verbose=False
)