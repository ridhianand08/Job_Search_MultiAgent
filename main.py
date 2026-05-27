from crewai import Crew, Process
from tasks.job_tasks import (
    create_analysis_task,
    create_resume_task,
    create_cover_letter_task,
    create_outreach_task
)
import os
from datetime import datetime

# ── Inputs ────────────────────────────────────────────────────────────
job_description = """
Position: Data Analyst
Agency: Department of Health and Human Services
Duties: Analyze health data using Python and SQL. Build dashboards in Tableau.
Write reports for senior stakeholders. Collaborate with engineering teams.
Required: 2 years experience, proficiency in Python, SQL, data visualization.
"""

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

# ── Build tasks ───────────────────────────────────────────────────────
task_analyze = create_analysis_task(job_description)
task_resume = create_resume_task(base_resume, task_analyze)
task_cover_letter = create_cover_letter_task(task_analyze, task_resume)
task_outreach = create_outreach_task(task_analyze, task_resume)

# ── Assemble and run crew ─────────────────────────────────────────────
crew = Crew(
    agents=[],   # CrewAI infers agents from tasks automatically
    tasks=[task_analyze, task_resume, task_cover_letter, task_outreach],
    process=Process.sequential,
    verbose=False
)

print("Running job application pipeline...\n")
crew.kickoff()

# ── Save outputs ──────────────────────────────────────────────────────
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_dir = f"outputs/{timestamp}"
os.makedirs(output_dir, exist_ok=True)

outputs = {
    "job_analysis.txt": task_analyze.output.raw,
    "resume.txt": task_resume.output.raw,
    "cover_letter.txt": task_cover_letter.output.raw,
    "linkedin_outreach.txt": task_outreach.output.raw,
}

for filename, content in outputs.items():
    filepath = f"{output_dir}/{filename}"
    with open(filepath, "w") as f:
        f.write(content)
    print(f"Saved: {filepath}")

print(f"\nAll outputs saved to: {output_dir}/")