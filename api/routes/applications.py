from fastapi import APIRouter, HTTPException
from models.schemas import (
    ApplyRequest, ApplicationResponse,
    ApplicationHistoryResponse, ApplicationRecord
)
from tasks.job_tasks import (
    create_analysis_task, create_resume_task,
    create_cover_letter_task, create_outreach_task
)
from crewai import Crew, Process
from datetime import datetime
import os

router = APIRouter(prefix="/applications", tags=["Applications"])


@router.post("/apply", response_model=ApplicationResponse)
async def apply_to_job(request: ApplyRequest):
    """Run the full 4-agent pipeline for a job application."""
    try:
        task_analyze = create_analysis_task(request.job_description)
        task_resume = create_resume_task(request.base_resume, task_analyze)
        task_cover_letter = create_cover_letter_task(task_analyze, task_resume)
        task_outreach = create_outreach_task(task_analyze, task_resume)

        crew = Crew(
            agents=[],
            tasks=[task_analyze, task_resume, task_cover_letter, task_outreach],
            process=Process.sequential,
            verbose=False
        )

        # Use async kickoff since FastAPI runs in an event loop
        await crew.kickoff_async()

        # Save outputs
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
            with open(f"{output_dir}/{filename}", "w") as f:
                f.write(content)

        return ApplicationResponse(
            job_analysis=task_analyze.output.raw,
            customized_resume=task_resume.output.raw,
            cover_letter=task_cover_letter.output.raw,
            linkedin_outreach=task_outreach.output.raw,
            output_folder=output_dir
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline error: {str(e)}")


@router.get("/history", response_model=ApplicationHistoryResponse)
async def get_application_history():
    """Return all saved application runs."""
    if not os.path.exists("outputs"):
        return ApplicationHistoryResponse(count=0, applications=[])

    applications = []
    for folder in sorted(os.listdir("outputs"), reverse=True):
        folder_path = f"outputs/{folder}"
        if os.path.isdir(folder_path):
            files = os.listdir(folder_path)
            applications.append(ApplicationRecord(
                folder=folder,
                timestamp=folder,
                files=files
            ))

    return ApplicationHistoryResponse(
        count=len(applications),
        applications=applications
    )