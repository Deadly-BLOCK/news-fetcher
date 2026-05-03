import requests
from datetime import datetime
import logging
import os
import json

# logging configure
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
                # Store titles in a list for the dict
                categoryDict[category] = [a.get('title', 'No Title') for a in data.get("articles", [])]
            else:
                logging.error(f"{category}: Request failed (status {response.status_code})")
                ProgramWorked = False
        except Exception as e:
            logging.error(f"{category}: Error occurred: {e}")
            ProgramWorked = False

    logging.info("Writing to index.html")

    # Generating Clean HTML Output
    with open("index.html", "w", encoding="utf-8") as file:
        file.write("<!DOCTYPE html>\n<html>\n<head>\n<meta charset='utf-8'>\n")
        file.write("<title>News API Feed</title>\n")
        
        # This section is for automated tools - they can grab the JSON inside this script tag
        file.write("<!-- RAW DATA FOR TOOLS -->\n")
        file.write("<script id='news-data' type='application/json'>\n")
        file.write(json.dumps(categoryDict))
        file.write("\n</script>\n</head>\n<body>\n")
        
        file.write(f"<h1>News Feed</h1>\n")
        file.write(f"<p>Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>\n")
        
        if not ProgramWorked:
            file.write("<p>Warning: Some sources failed to load.</p>\n")

        # Simple semantic structure
        for categ, titles in categoryDict.items():
            file.write(f"<h2>{categ}</h2>\n<ul>\n")
            for title in titles:
                file.write(f"  <li>{title}</li>\n")
            file.write("</ul>\n")
        
        file.write("</body>\n</html>")

    logging.info("Program Finished")

except Exception as e:
    logging.error(f"Critical error: {e}")
