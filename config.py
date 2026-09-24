import os
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

BIRTHDAY = datetime.fromisoformat(os.environ["BIRTHDAY"])
API_KEY = os.environ["OPENWEATHER_API_KEY"]
CITY = os.getenv("CITY", "Moscow")
