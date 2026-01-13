# Federal AI Use Case Inventory Analysis Tool

A Dockerized analysis toolkit for exploring the 2024 Federal Agency AI Use Case Inventory.

## Quick Start

```bash
# Start all services
docker-compose up -d

# Access the dashboard
open http://localhost:8000

# Access Jupyter notebook
open http://localhost:8888
```

## Services

| Service | Port | Description |
|---------|------|-------------|
| Dashboard | 8000 | FastAPI web dashboard with summary stats and search |
| Jupyter | 8888 | Interactive notebook for custom analysis |

## Dashboard Features

- **Summary Statistics**: Total use cases, agencies, high-impact counts
- **Year Comparison**: 2023 vs 2024 growth analysis
- **Agency Breakdown**: Top agencies by use case count
- **Topic Distribution**: Interactive charts by topic area
- **Impact Analysis**: Rights-impacting and safety-impacting breakdown
- **Search**: Filter use cases by keyword, agency, topic

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/summary` | High-level summary statistics |
| `GET /api/agencies` | Use case counts by agency |
| `GET /api/topics` | Distribution by topic area |
| `GET /api/stages` | Development stage distribution |
| `GET /api/impact` | Risk report (rights/safety impacting) |
| `GET /api/compare-years` | 2023 vs 2024 comparison |
| `GET /api/search?q=keyword` | Search use cases |
| `GET /health` | Health check |

## Usage Examples

### API Queries

```bash
# Get summary stats
curl http://localhost:8000/api/summary

# Search for AI use cases
curl "http://localhost:8000/api/search?q=machine+learning&limit=10"

# Filter by agency
curl "http://localhost:8000/api/search?agency=Veterans"

# Get high-impact analysis
curl http://localhost:8000/api/impact
```

### Jupyter Notebook

The exploration notebook (`notebooks/exploration.ipynb`) provides:
- Data loading and preview
- Agency analysis with visualizations
- Topic area distribution
- Development stage breakdown
- Impact classification analysis
- Year-over-year comparison
- Custom analysis cells

## Development

```bash
# Build images
docker-compose build

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Run dashboard only
docker-compose up dashboard

# Run jupyter only
docker-compose up jupyter
```

## Data

The tool expects CSV data files in the `../data/` directory:
- `2024_consolidated_ai_inventory_raw_v2.csv` (required)
- `2023_consolidated_ai_inventory_raw.csv` (optional, for comparison)

## Tech Stack

- **FastAPI** - Web framework
- **Pandas** - Data analysis
- **Chart.js** - Dashboard visualizations
- **Plotly** - Notebook visualizations
- **Tailwind CSS** - Dashboard styling
- **Jupyter Lab** - Interactive exploration
