import time
import requests
from config import logger, headers, url


def connect_to_api():
    """
    Connects to Alpha Vantage API and retrieves intraday stock data
    """
    stocks = ["TSLA", "MSFT", "GOOGL"]
    responses = []

    for stock in stocks:
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": stock,
            "interval": "5min",
            "outputsize": "compact",
            "datatype": "json"
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            # Validate API response
            if "Meta Data" not in data:
                logger.error(f"{stock} API returned invalid payload: {data}")
                continue

            responses.append(data)
            logger.info(f"{stock} has been successfully loaded")

            # Rate-limit protection (Alpha Vantage free tier)
            time.sleep(12)

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed for {stock}: {e}")

    return responses


def extract_json(response_list):
    """
    Transforms API JSON responses into structured stock records
    """
    records = []

    for data in response_list:
        if "Meta Data" not in data:
            continue

        symbol = data["Meta Data"]["2. Symbol"]
        time_series = data.get("Time Series (5min)", {})

        for timestamp, metrics in time_series.items():
            record = {
                "symbol": symbol,
                "date": timestamp,
                "open": metrics["1. open"],
                "high": metrics["2. high"],
                "low": metrics["3. low"],
                "close": metrics["4. close"]
            }
            records.append(record)

    return records


