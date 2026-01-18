import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# RapidAPI / Alpha Vantage configuration
BASEURL = "alpha-vantage.p.rapidapi.com"
url = f"https://{BASEURL}/query"

# Load API key
api_key = os.getenv("RAPIDAPI_KEY")

if not api_key:
    raise EnvironmentError("RAPIDAPI_KEY not found in environment variables")

headers = {
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": BASEURL
}

logger.info(f"API Key loaded successfully: {api_key[:4]}***")

