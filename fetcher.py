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

    categories = ["business", "entertainment", "general", "health", "science", "sports", "technology"]
    categoryDict = {}

    logging.info("About To Call API")
    for category in categories:
        params = {"country": "us", "apiKey": Key, "pageSize": 100, "category": category}
        try:
            response = requests.get(URL, params)
            if response.status_code == 200:
                data = response.json()
                categoryDict[category] = data.get("articles", [])
            else:
                logging.error(f"{category}: Request failed (status {response.status_code})")
                ProgramWorked = False
        except Exception as e:
            logging.error(f"{category}: Error occurred: {e}")
            ProgramWorked = False

    logging.info("Writing to index.html")

    with open("index.html", "w", encoding="utf-8") as file:
        file.write("<!DOCTYPE html><html><head><meta charset='utf-8'><title>News Feed</title>")
        file.write("<style>body{font-family:sans-serif; line-height:1.6; max-width:800px; margin:auto; padding:20px; background:#f9f9f9;}")
        file.write("h1{color:#333; border-bottom:2px solid #333;} h2{background:#333; color:#fff; padding:10px; margin-top:30px;}")
        file.write("ul{list-style:none; padding:0;} li{background:#fff; margin-bottom:10px; padding:15px; border-radius:5px; box-shadow:0 2px 5px rgba(0,0,0,0.1);}</style></head><body>")
        
        file.write(f"<h1>Daily News Digest</h1>")
        file.write(f"<p><strong>Last Updated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>")
        
        if not ProgramWorked:
            file.write("<p style='color:red; font-weight:bold;'>Note: Some categories failed to load.</p>")

        for categ, articles in categoryDict.items():
            file.write(f"<h2>{categ.upper()}</h2><ul>")
            for article in articles:
                file.write(f"<li>{article.get('title','No Title')}</li>")
            file.write("</ul>")
        
        file.write("</body></html>")

    logging.info("Program Finished")

except Exception as e:
    logging.error(f"Critical error: {e}")
