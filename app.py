import streamlit as st
import requests

API_BASE = "http://localhost:8000"

# ── Page config ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="Job Search Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("Job Search Agent by Manan Bhutiani")
st.caption("Finds jobs and writes your application materials automatically ")

# ── Sidebar — resume input + history ─────────────────────────────────
with st.sidebar:
    st.header("Your Resume")
    base_resume = st.text_area(
        "Paste your resume here",
        height=300,
        placeholder="Jane Smith\n\nEXPERIENCE\n...\n\nSKILLS\n..."
    )

    st.divider()

    st.header("Application History")
    if st.button("Refresh History"):
        st.session_state.history_refresh = True

    try:
        history = requests.get(f"{API_BASE}/applications/history").json()
        if history["count"] == 0:
            st.caption("No applications yet")
        else:
            for app in history["applications"]:
                st.markdown(f"📁 `{app['timestamp']}`")
                for f in app["files"]:
                    st.caption(f"  • {f}")
    except:
        st.error("API not reachable")

# ── Main area — job search ────────────────────────────────────────────
st.header("Search Jobs")

col1, col2, col3 = st.columns([3, 2, 1])
with col1:
    keyword = st.text_input("Job title or keyword", placeholder="data analyst")
with col2:
    location = st.text_input("Location", placeholder="Washington DC")
with col3:
    results = st.selectbox("Results", [3, 5, 10], index=0)

if st.button("🔍 Search", type="primary"):
    if not keyword:
        st.warning("Enter a keyword to search")
    else:
        with st.spinner("Searching USAJobs..."):
            try:
                response = requests.post(
                    f"{API_BASE}/jobs/search",
                    json={
                        "keyword": keyword,
                        "location": location,
                        "results_per_page": results
                    }
                )
                data = response.json()
                # Store results in session state so they persist after button clicks
                st.session_state.jobs = data["jobs"]
                st.session_state.job_count = data["count"]
            except Exception as e:
                st.error(f"Search failed: {e}")

# ── Display job results ───────────────────────────────────────────────
if "jobs" in st.session_state and st.session_state.jobs:
    st.subheader(f"Found {st.session_state.job_count} jobs")

    for i, job in enumerate(st.session_state.jobs):
        with st.expander(f"**{job['title']}** — {job['agency']}"):
            col_a, col_b = st.columns(2)

            with col_a:
                st.markdown(f"📍 **Location:** {job['location']}")
                st.markdown(f"📅 **Closes:** {job['closing_date']}")

            with col_b:
                # Format salary nicely
                if job['salary_min'] == "0":
                    st.markdown("💰 **Salary:** Unpaid / Volunteer")
                else:
                    st.markdown(
                        f"💰 **Salary:** ${int(float(job['salary_min'])):,} "
                        f"— ${int(float(job['salary_max'])):,} "
                        f"({job['salary_interval']})"
                    )
                st.markdown(f"🔗 [View on USAJobs]({job['url']})")

            st.divider()

            # Apply button — unique key per job using index
            if st.button(f"🤖 Apply with AI", key=f"apply_{i}"):
                if not base_resume.strip():
                    st.warning("Paste your resume in the sidebar first")
                else:
                    with st.spinner("Running 4-agent pipeline... this takes ~60 seconds"):
                        try:
                            job_description = f"""
                            Position: {job['title']}
                                Agency: {job['agency']}
                                Location: {job['location']}
                                Closing: {job['closing_date']}
                                URL: {job['url']}
                            """
                            result = requests.post(
                                f"{API_BASE}/applications/apply",
                                json={
                                    "job_description": job_description,
                                    "base_resume": base_resume
                                },
                                timeout=300  # 5 min timeout for agent pipeline
                            )
                            data = result.json()

                            if result.status_code == 200:
                                st.success(f"✅ Saved to `{data['output_folder']}`")

                                # Store result in session state keyed by job index
                                st.session_state[f"result_{i}"] = data
                            else:
                                st.error(f"Error: {data.get('detail', 'Unknown error')}")

                        except Exception as e:
                            st.error(f"Pipeline failed: {e}")

            # Show results if this job has been applied to
            if f"result_{i}" in st.session_state:
                data = st.session_state[f"result_{i}"]

                tab1, tab2, tab3, tab4 = st.tabs([
                    "📋 Job Analysis",
                    "📄 Resume",
                    "✉️ Cover Letter",
                    "💼 LinkedIn"
                ])
                with tab1:
                    st.markdown(data["job_analysis"])
                with tab2:
                    st.markdown(data["customized_resume"])
                with tab3:
                    st.markdown(data["cover_letter"])
                with tab4:
                    st.markdown(data["linkedin_outreach"])