from crewai import Agent, LLM
from dotenv import load_dotenv
import os

load_dotenv()

llm = LLM(
    model="gemini/gemini-3.1-flash-lite",
    api_key=os.getenv("GEMINI_API_KEY")
)

cover_letter_writer = Agent(
    role="Cover Letter Writer",
    goal="Write compelling, personalized cover letters that connect candidate experience to job requirements",
    backstory="""You are a senior hiring manager turned career coach. You know 
    exactly what makes a cover letter stand out — specific examples, agency 
    mission alignment, and a confident but not arrogant tone. You write in 
    first person as the candidate.""",
    llm=llm,
    verbose=False
)