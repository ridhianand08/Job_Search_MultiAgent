from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import jobs, applications

app = FastAPI(
    title="Job Search Agent API",
    description="Multi-agent job application automation powered by CrewAI and Gemini",
    version="1.0.0"
)

# CORS lets your Streamlit frontend talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Register routes
app.include_router(jobs.router)
app.include_router(applications.router)


@app.get("/")
async def root():
    return {"status": "running", "docs": "/docs"}