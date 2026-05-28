from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv
import os

load_dotenv()

llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)

# ── Job description we're targeting ──────────────────────────────────
job_description = """
Position: Data Analyst
Agency: Department of Health and Human Services
Duties: Analyze health data using Python and SQL. Build dashboards in Tableau.
Write reports for senior stakeholders. Collaborate with engineering teams.
Required: 2 years experience, proficiency in Python, SQL, data visualization.
"""

# ── Candidate's base resume ───────────────────────────────────────────
base_resume = """
Jane Smith | jane@email.com | linkedin.com/in/janesmith

EXPERIENCE
Junior Data Analyst, ABC Corp (2022-2024)
- Wrote SQL queries to extract sales data
- Created Excel dashboards for weekly reports
- Collaborated with marketing team on campaign analysis

EDUCATION
B.S. Computer Science, State University, 2022

SKILLS
Python, SQL, Excel, basic Tableau, data cleaning
"""

# ═══════════════════════════════════════════════════════════════════════
# AGENTS — each is a specialist with a distinct persona
# ═══════════════════════════════════════════════════════════════════════

job_analyzer = Agent(
    role="Job Description Analyst",
    goal="Extract structured, actionable information from job descriptions",
    backstory="""You are an expert career consultant with 10 years of experience 
    analyzing government job postings. You identify exactly what employers want 
    and present it in a clear, structured way that other specialists can act on.""",
    llm=llm,
    verbose=False  # turned off now that we know it works
)

resume_customizer = Agent(
    role="Resume Customization Specialist",
    goal="Tailor resumes to match specific job requirements without fabricating experience",
    backstory="""You are a professional resume writer who has helped hundreds of 
    candidates land government jobs. You reframe existing experience using the 
    exact language and keywords employers are scanning for, while staying 
    completely truthful about the candidate's background.""",
    llm=llm,
    verbose=False
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

outreach_specialist = Agent(
    role="LinkedIn Outreach Specialist",
    goal="Draft short, genuine LinkedIn messages that start real conversations with hiring managers",
    backstory="""You have 8 years of experience in recruitment and networking. 
    You know that the best outreach messages are brief, specific, and ask for 
    nothing more than a conversation. You never use generic templates.""",
    llm=llm,
    verbose=False
)

# ═══════════════════════════════════════════════════════════════════════
# TASKS — what each agent actually does
# Note: context=[] links tasks together — output flows forward
# ═══════════════════════════════════════════════════════════════════════

task_analyze = Task(
    description=f"""
    Analyze this job description thoroughly:
    
    {job_description}
    
    Extract:
    - Required technical skills
    - Soft skills and qualities
    - Experience level and years required
    - Key responsibilities
    - Top 5 resume keywords
    - What the agency seems to value most
    """,
    expected_output="""A structured job analysis covering skills, experience level,
    key responsibilities, top keywords, and agency priorities.""",
    agent=job_analyzer
)

task_resume = Task(
    description=f"""
    Using the job analysis provided, customize this resume to better match the role.
    
    Base resume:
    {base_resume}
    
    Instructions:
    - Rewrite bullet points using keywords from the job analysis
    - Reorder skills to put the most relevant ones first
    - Strengthen weak descriptions with more impact-focused language
    - Do NOT invent experience or skills the candidate doesn't have
    - Keep the same overall structure
    """,
    expected_output="""A fully rewritten resume tailored to the job, using 
    relevant keywords and stronger impact language.""",
    agent=resume_customizer,
    context=[task_analyze]  # receives job analysis as input
)

task_cover_letter = Task(
    description="""
    Using the job analysis and customized resume, write a cover letter.
    
    Requirements:
    - Address it to the hiring team at the agency from the job analysis
    - Opening paragraph: why this specific role and agency
    - Middle paragraph: connect 2-3 specific experiences to job requirements  
    - Closing paragraph: confident call to action
    - Tone: professional but human, not stiff
    - Length: 3 paragraphs, under 300 words
    """,
    expected_output="""A 3-paragraph cover letter under 300 words, tailored 
    to the specific role and agency.""",
    agent=cover_letter_writer,
    context=[task_analyze, task_resume]  # receives both previous outputs
)

task_outreach = Task(
    description="""
    Write a LinkedIn connection request message to a hiring manager at the agency.
    
    Requirements:
    - Maximum 300 characters (LinkedIn limit)
    - Mention the specific role by title
    - One genuine reason why this role is a fit
    - No generic phrases like 'I came across your profile'
    - End with a low-pressure question or statement
    """,
    expected_output="""A LinkedIn message under 300 characters that is specific,
    genuine, and starts a real conversation.""",
    agent=outreach_specialist,
    context=[task_analyze, task_resume]
)

# ═══════════════════════════════════════════════════════════════════════
# CREW — assemble the team and run
# ═══════════════════════════════════════════════════════════════════════

crew = Crew(
    agents=[job_analyzer, resume_customizer, cover_letter_writer, outreach_specialist],
    tasks=[task_analyze, task_resume, task_cover_letter, task_outreach],
    process=Process.sequential,
    verbose=False
)

print("Running 4-agent pipeline...\n")
result = crew.kickoff()

print("=" * 60)
print("JOB ANALYSIS")
print("=" * 60)
print(task_analyze.output.raw)

print("\n" + "=" * 60)
print("CUSTOMIZED RESUME")
print("=" * 60)
print(task_resume.output.raw)

print("\n" + "=" * 60)
print("COVER LETTER")
print("=" * 60)
print(task_cover_letter.output.raw)

print("\n" + "=" * 60)
print("LINKEDIN OUTREACH")
print("=" * 60)
print(task_outreach.output.raw)