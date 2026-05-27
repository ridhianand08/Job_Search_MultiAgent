from fastapi import APIRouter, HTTPException
from models.schemas import JobSearchRequest, JobSearchResponse, JobListing
import requests
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/jobs", tags=["Jobs"])


def get_usajobs_headers():
    return {
        "Host": "data.usajobs.gov",
        "User-Agent": os.getenv("USAJOBS_EMAIL"),
        "Authorization-Key": os.getenv("USAJOBS_API_KEY")
    }


@router.post("/search", response_model=JobSearchResponse)
async def search_jobs(request: JobSearchRequest):
    """Search for jobs on USAJobs by keyword and location."""
    try:
        response = requests.get(
            "https://data.usajobs.gov/api/search",
            headers=get_usajobs_headers(),
            params={
                "Keyword": request.keyword,
                "LocationName": request.location,
                "ResultsPerPage": request.results_per_page,
                "WhoMayApply": "public"
            }
        )
        response.raise_for_status()
        items = response.json()["SearchResult"]["SearchResultItems"]

        jobs = []
        for item in items:
            d = item["MatchedObjectDescriptor"]
            salary = d["PositionRemuneration"][0]
            jobs.append(JobListing(
                title=d["PositionTitle"],
                agency=d["OrganizationName"],
                location=d["PositionLocationDisplay"],
                salary_min=salary["MinimumRange"],
                salary_max=salary["MaximumRange"],
                salary_interval=salary["RateIntervalCode"],
                closing_date=d["ApplicationCloseDate"][:10],
                url=d["PositionURI"]
            ))

        return JobSearchResponse(count=len(jobs), jobs=jobs)

    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"USAJobs API error: {str(e)}")