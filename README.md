# API Status Monitor

A lightweight API uptime monitor built with **FastAPI**. It checks configured endpoints, stores the latest status in memory, and exposes a clean dashboard plus JSON API.

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-ready-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)
![CI](https://img.shields.io/badge/CI-GitHub%20Actions-black)

## Features

- Monitor multiple HTTP endpoints
- Track status code, response time, and availability
- Simple web dashboard
- JSON API for integrations
- Config-driven endpoint list
- Docker support
- GitHub Actions CI
- Beginner-friendly codebase

## Demo

After running the app, open:

```txt
http://localhost:8000
```

You will see a status dashboard for the APIs listed in `config.yaml`.

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/api-status-monitor.git
cd api-status-monitor
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
uvicorn app.main:app --reload
```

Open:

```txt
http://localhost:8000
```

## Configuration

Edit `config.yaml`:

```yaml
check_interval_seconds: 60
endpoints:
  - name: GitHub API
    url: https://api.github.com
  - name: Example API
    url: https://jsonplaceholder.typicode.com/posts/1
```

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/` | Web dashboard |
| GET | `/api/status` | Current status of all endpoints |
| POST | `/api/check-now` | Manually trigger a status check |
| GET | `/health` | App health check |

Example response:

```json
{
  "GitHub API": {
    "url": "https://api.github.com",
    "is_up": true,
    "status_code": 200,
    "response_time_ms": 124.5,
    "checked_at": "2026-05-28T12:30:00Z",
    "error": null
  }
}
```

## Run with Docker

```bash
docker build -t api-status-monitor .
docker run -p 8000:8000 api-status-monitor
```

## Project Structure

```txt
api-status-monitor/
├── app/
│   ├── main.py
│   ├── monitor.py
│   ├── models.py
│   └── templates.py
├── tests/
│   └── test_app.py
├── .github/
│   ├── workflows/ci.yml
│   └── ISSUE_TEMPLATE/
├── config.yaml
├── Dockerfile
├── requirements.txt
├── LICENSE
└── README.md
```

## Roadmap

- [ ] Store history in SQLite/PostgreSQL
- [ ] Add email/Telegram/Slack alerts
- [ ] Add authentication for private dashboards
- [ ] Add charts for uptime history
- [ ] Add latency percentile metrics
- [ ] Add public status page mode

## Good First Issues

- Improve dashboard styling
- Add more tests
- Add endpoint tags
- Add dark mode
- Add uptime percentage calculation

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

## License

This project is licensed under the MIT License.
