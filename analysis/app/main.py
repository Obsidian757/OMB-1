"""
FastAPI web dashboard for Federal AI Use Case Inventory Analysis.
"""

from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from typing import Optional
import json

from .analysis import AIInventoryAnalyzer

# Initialize FastAPI app
app = FastAPI(
    title="Federal AI Use Case Inventory Analyzer",
    description="Analysis dashboard for the 2024 Federal Agency AI Use Case Inventory",
    version="1.0.0",
)

# Setup templates
templates_dir = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

# Initialize analyzer with data directory
DATA_DIR = Path("/data")
analyzer = AIInventoryAnalyzer(str(DATA_DIR))


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Main dashboard page."""
    try:
        summary = analyzer.get_summary_stats()
        agencies = analyzer.get_agency_breakdown().head(15).to_dict("records")
        topics = analyzer.get_topic_distribution().to_dict("records")
        stages = analyzer.get_dev_stage_distribution().to_dict("records")
        year_compare = analyzer.get_year_comparison()
        impact_by_agency = analyzer.get_impact_by_agency().head(10).to_dict("records")

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "summary": summary,
                "agencies": agencies,
                "topics": topics,
                "stages": stages,
                "year_compare": year_compare,
                "impact_by_agency": impact_by_agency,
            },
        )
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error loading data</h1><p>{str(e)}</p>", status_code=500)


@app.get("/api/summary")
async def api_summary():
    """API endpoint for summary statistics."""
    return JSONResponse(content=analyzer.get_summary_stats())


@app.get("/api/agencies")
async def api_agencies(limit: int = Query(default=50, ge=1, le=100)):
    """API endpoint for agency breakdown."""
    df = analyzer.get_agency_breakdown().head(limit)
    return JSONResponse(content=df.to_dict("records"))


@app.get("/api/topics")
async def api_topics():
    """API endpoint for topic distribution."""
    df = analyzer.get_topic_distribution()
    return JSONResponse(content=df.to_dict("records"))


@app.get("/api/stages")
async def api_stages():
    """API endpoint for development stage distribution."""
    df = analyzer.get_dev_stage_distribution()
    return JSONResponse(content=df.to_dict("records"))


@app.get("/api/impact")
async def api_impact():
    """API endpoint for impact analysis."""
    return JSONResponse(content=analyzer.get_risk_report())


@app.get("/api/impact-by-agency")
async def api_impact_by_agency(limit: int = Query(default=20, ge=1, le=50)):
    """API endpoint for impact by agency."""
    df = analyzer.get_impact_by_agency().head(limit)
    return JSONResponse(content=df.to_dict("records"))


@app.get("/api/compare-years")
async def api_compare_years():
    """API endpoint for year-over-year comparison."""
    return JSONResponse(content=analyzer.get_year_comparison())


@app.get("/api/pii")
async def api_pii():
    """API endpoint for PII analysis."""
    return JSONResponse(content=analyzer.get_pii_analysis())


@app.get("/api/search")
async def api_search(
    q: str = Query(default="", description="Search query"),
    agency: Optional[str] = Query(default=None, description="Filter by agency"),
    topic: Optional[str] = Query(default=None, description="Filter by topic"),
    impact: Optional[str] = Query(default=None, description="Filter by impact type"),
    limit: int = Query(default=50, ge=1, le=200),
):
    """API endpoint for searching use cases."""
    df = analyzer.search_use_cases(
        query=q,
        agency=agency,
        topic=topic,
        impact_type=impact,
        limit=limit,
    )
    # Return subset of columns for readability
    cols_to_return = []
    for col in df.columns[:10]:  # First 10 columns
        cols_to_return.append(col)

    return JSONResponse(content=df[cols_to_return].fillna("").to_dict("records"))


@app.get("/api/columns")
async def api_columns():
    """API endpoint to list available columns."""
    return JSONResponse(content={"columns": analyzer.get_column_names()})


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "data_dir": str(DATA_DIR)}
