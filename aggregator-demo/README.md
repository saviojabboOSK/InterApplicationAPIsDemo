# Data Aggregator Demo

This is a demo showing the "private App A (corporate) ↔ aggregator App B ↔ four public APIs" pattern.

## Architecture

- **App A (Consumer)**: `client.py` - Simple Python script that calls the aggregator
- **App B (Aggregator)**: `main.py` - FastAPI service that fetches from 4 public APIs and aggregates data
- **Security**: Hard-coded API key `secret123` required in `X-API-Key` header

## APIs Used

1. **ISS Now**: http://api.open-notify.org/iss-now.json
2. **SpaceX Latest Launch**: https://api.spacexdata.com/v5/launches/latest
3. **Cat Fact Ninja**: https://catfact.ninja/fact
4. **Frankfurter EUR→USD**: https://api.frankfurter.app/latest?from=EUR&to=USD

## Setup & Run Instructions (Windows)

### 1. Create and activate virtual environment
```powershell
python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies
```powershell
pip install -r requirements.txt
```

### 3. Run the aggregator service (Terminal 1)
```powershell
uvicorn main:app --reload
```

### 4. Run the consumer client (Terminal 2)
```powershell
python client.py
```

## Expected Output

The aggregator service will return JSON like:
```json
{
  "iss": {
    "lat": 45.123,
    "lon": -93.456,
    "timestamp": 1703347200
  },
  "spacex": {
    "name": "Starlink Group 6-28",
    "date_utc": "2023-12-23T10:30:00.000Z",
    "success": true
  },
  "cat_fact": "Cats have 32 muscles that control the outer ear.",
  "eur_usd": 1.1025
}
```

## Endpoints

- `GET /v1/aggregate` - Main aggregation endpoint (requires X-API-Key: secret123)
- `GET /health` - Health check endpoint
- `GET /docs` - FastAPI automatic documentation
