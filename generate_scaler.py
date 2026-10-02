import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from sklearn.preprocessing import MinMaxScaler
import joblib

print("Fetching data to recreate scaler...")
cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

params = {
    "latitude": 30.0626, "longitude": 31.2497,
    "start_date": "1974-01-01", "end_date": "2024-01-01",
    "hourly": ["temperature_2m", "relative_humidity_2m", "surface_pressure",
               "wind_speed_10m", "cloudcover", "precipitation"],
    "timezone": "Africa/Cairo"
}
responses = openmeteo.weather_api("https://archive-api.open-meteo.com/v1/archive", params=params)
hourly = responses[0].Hourly()

df = pd.DataFrame({
    "temp": hourly.Variables(0).ValuesAsNumpy(),
    "humidity": hourly.Variables(1).ValuesAsNumpy(),
    "pressure": hourly.Variables(2).ValuesAsNumpy(),
    "wind": hourly.Variables(3).ValuesAsNumpy(),
    "cloud": hourly.Variables(4).ValuesAsNumpy(),
    "rain": hourly.Variables(5).ValuesAsNumpy()
})
df.ffill(inplace=True)

scaler = MinMaxScaler()
scaler.fit(df.values)
joblib.dump(scaler, "weather_scaler.pkl")
print("Saved weather_scaler.pkl successfully!")
