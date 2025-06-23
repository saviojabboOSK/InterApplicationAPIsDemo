from fastapi import FastAPI, HTTPException, Header
import httpx
import asyncio
from typing import Optional

app = FastAPI(title="Data Aggregator Service", version="1.0.0")

# Hard-coded API key for security
VALID_API_KEY = "secret123"


def verify_api_key(x_api_key: Optional[str] = Header(None)):
    """Verify the API key from request header"""
    if x_api_key != VALID_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return True


async def fetch_iss_data():
    """Fetch ISS current location"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://api.open-notify.org/iss-now.json")
            response.raise_for_status()
            data = response.json()
            return {
                "lat": float(data["iss_position"]["latitude"]),
                "lon": float(data["iss_position"]["longitude"]),
                "timestamp": int(data["timestamp"])
            }
    except Exception as e:
        print(f"Error fetching ISS data: {e}")
        return {"lat": 0.0, "lon": 0.0, "timestamp": 0}


async def fetch_spacex_data():
    """Fetch SpaceX latest launch"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://api.spacexdata.com/v5/launches/latest")
            response.raise_for_status()
            data = response.json()
            return {
                "name": data.get("name", "Unknown"),
                "date_utc": data.get("date_utc", ""),
                "success": data.get("success", False)
            }
    except Exception as e:
        print(f"Error fetching SpaceX data: {e}")
        return {"name": "Unknown", "date_utc": "", "success": False}


async def fetch_cat_fact():
    """Fetch random cat fact"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://catfact.ninja/fact")
            response.raise_for_status()
            data = response.json()
            return data.get("fact", "No cat fact available")
    except Exception as e:
        print(f"Error fetching cat fact: {e}")
        return "No cat fact available"


async def fetch_eur_usd_rate():
    """Fetch EUR to USD exchange rate"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://api.frankfurter.app/latest?from=EUR&to=USD")
            response.raise_for_status()
            data = response.json()
            return float(data["rates"]["USD"])
    except Exception as e:
        print(f"Error fetching EUR/USD rate: {e}")
        return 0.0


@app.get("/v1/aggregate")
async def aggregate_data(x_api_key: Optional[str] = Header(None)):
    """
    Aggregate data from multiple APIs
    Requires X-API-Key header with value 'secret123'
    """
    # Verify API key
    verify_api_key(x_api_key)
    
    # Fetch data from all APIs concurrently
    iss_task = fetch_iss_data()
    spacex_task = fetch_spacex_data()
    cat_fact_task = fetch_cat_fact()
    eur_usd_task = fetch_eur_usd_rate()
    
    # Wait for all tasks to complete
    iss_data, spacex_data, cat_fact, eur_usd_rate = await asyncio.gather(
        iss_task, spacex_task, cat_fact_task, eur_usd_task
    )
    
    # Return aggregated response
    return {
        "iss": iss_data,
        "spacex": spacex_data,
        "cat_fact": cat_fact,
        "eur_usd": eur_usd_rate
    }


@app.get("/health")
async def health_check():
    """Simple health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
