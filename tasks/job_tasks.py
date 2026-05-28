from crewai import Task
from agents.job_analyzer import job_analyzer
from agents.resume_customizer import resume_customizer
from agents.cover_letter_writer import cover_letter_writer
from agents.outreach_specialist import outreach_specialist


def create_analysis_task(job_description: str) -> Task:
    return Task(
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
        expected_output="""A structured job analysis covering skills, experience 
        level, key responsibilities, top keywords, and agency priorities.""",
        agent=job_analyzer
    )


def create_resume_task(base_resume: str, analysis_task: Task) -> Task:
    return Task(
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
        context=[analysis_task]
    )


def create_cover_letter_task(analysis_task: Task, resume_task: Task) -> Task:
    return Task(
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
        context=[analysis_task, resume_task]
    )


def create_outreach_task(analysis_task: Task, resume_task: Task) -> Task:
    return Task(
        description="""
        Write a LinkedIn connection request message to a hiring manager at the agency.

        Requirements:
        - Maximum 300 characters (LinkedIn limit)
        - Mention the specific role by title
        - One genuine reason why this role is a fit
        - No generic phrases like 'I came across your profile'
        - End with a low-pressure question or statement
        """,
        expected_output="""A LinkedIn message under 300 characters that is 
        specific, genuine, and starts a real conversation.""",
        agent=outreach_specialist,
        context=[analysis_task, resume_task]
    )