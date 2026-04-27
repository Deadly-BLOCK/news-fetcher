import requests
from datetime import datetime
import logging
import os

# logging configure
logging.basicConfig(
    filename="log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logging.info("Program Started")
ProgramWorked = True


try:

    # Pulling from GitHub Secrets / Environment Variables
    Key = os.environ.get("NEWS_API_KEY")
    URL = "https://newsapi.org/v2/top-headlines"

    categories = [
        "business",
        "entertainment",
        "general",
        "health",
        "science",
        "sports",
        "technology",
    ]
    categoryDict = {}

    logging.info("About To Call API")
    for category in categories:
        params = {"country": "us", "apiKey": Key, "pageSize": 100, "category": category}

        response = requests.get(URL, params)
        if response.status_code != 200:
            logging.error(f"{category}: Request Not Recieved (status_code is not 200)")
            ProgramWorked = False
        try:
            data = response.json()
        except ValueError:
            logging.error(f"{category}: response is not a valid JSON")
            data = {}
            ProgramWorked = False

        if "articles" not in data:
            logging.error(
                "'Articles' Not in data (the response file after .json()), The API Likely Raised An Error "
            )
            ProgramWorked = False

        try:
            tempArticles = data["articles"]
        except KeyError:
            logging.error(
                f'{category}: Raised An Error On (probably invalid json): tempArticles = response.json()["articles"]'
            )
            ProgramWorked = False
            continue

        categoryDict[category] = tempArticles
    TextBeforeFileName = ""
    if ProgramWorked == False:
        TextBeforeFileName = "CORRUPTED - "

    logging.info(
        "API Call And Handling Finished (May or may not have problems), Starting File Writing Now"
    )
    with open(
        f"{TextBeforeFileName}{datetime.now().date()}.txt", "a", encoding="utf-8"
    ) as file:
        file.write(f"\n\n==={datetime.now().date()}===\n")

        if ProgramWorked == False:
            file.write(
                "\n\n\n================== Program Had An Error ==================\n\n\n"
            )

        for categ, articles in categoryDict.items():
            file.write(f"\n------\n[{categ}]\n------\n")
            for article in articles:
                file.write(f"{article.get('title','No Title')} \n \n \n")

    if ProgramWorked:
        logging.info("Program Finished Without problems")
    else:
        logging.info("Program Finished With Errors")


except ValueError as e:
    logging.error(f"JSON parsing failed: {e}")

except requests.exceptions.RequestException as e:
    logging.error(f"Network/API call failed: {e}")

except KeyError as e:
    logging.error(f"Expected key missing: {e}")

except OSError as e:
    logging.error(f"File writing failed: {e}")

except Exception as e:
    logging.error(f"Unexpected error occurred: {e}")
