import requests
from datetime import datetime
import logging
import os

logging.basicConfig(
    filename="log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logging.info("Program Started")
ProgramWorked = True

try:
    Key = os.environ.get("NEWS_API_KEY")
    URL = "https://newsapi.org/v2/top-headlines"

    categories = [
        "business", "entertainment", "general", 
        "health", "science", "sports", "technology"
    ]
    categoryDict = {}

    logging.info("About To Call API")
    for category in categories:
        params = {"country": "us", "apiKey": Key, "pageSize": 100, "category": category}

        response = requests.get(URL, params)
        if response.status_code != 200:
            logging.error(f"{category}: Request failed (status {response.status_code})")
            ProgramWorked = False
            continue

        try:
            data = response.json()
            articles = data.get("articles", [])
            categoryDict[category] = articles
        except ValueError:
            logging.error(f"{category}: response is not a valid JSON")
            ProgramWorked = False

    logging.info("API Handling Finished. Writing to news.txt")

    with open("news.txt", "w", encoding="utf-8") as file:
        file.write(f"Latest Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        if not ProgramWorked:
            file.write("\n!!! ATTENTION: This update may be incomplete due to errors !!!\n")

        for categ, articles in categoryDict.items():
            file.write(f"\n{'='*20}\n{categ.upper()}\n{'='*20}\n")
            for article in articles:
                file.write(f"- {article.get('title','No Title')}\n")

    if ProgramWorked:
        logging.info("Program Finished Without problems")
    else:
        logging.info("Program Finished With Errors")

except Exception as e:
    logging.error(f"Critical error: {e}")
