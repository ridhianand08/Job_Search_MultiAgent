from pydantic import BaseModel
from typing import Optional

# ── Requests (what the frontend sends) ───────────────────────────────

class JobSearchRequest(BaseModel):
    keyword: str
    location: Optional[str] = ""
    results_per_page: Optional[int] = 5


class ApplyRequest(BaseModel):
    job_description: str
    base_resume: str


# ── Responses (what the backend returns) ─────────────────────────────

class JobListing(BaseModel):
    title: str
    agency: str
    location: str
    salary_min: str
    salary_max: str
    salary_interval: str
    closing_date: str
    url: str


class JobSearchResponse(BaseModel):
    count: int
    jobs: list[JobListing]


class ApplicationResponse(BaseModel):
    job_analysis: str
    customized_resume: str
    cover_letter: str
    linkedin_outreach: str
    output_folder: str


class ApplicationRecord(BaseModel):
    folder: str
    timestamp: str
    files: list[str]


class ApplicationHistoryResponse(BaseModel):
    count: int
    applications: list[ApplicationRecord]