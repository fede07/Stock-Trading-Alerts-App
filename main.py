import requests
from dotenv import load_dotenv
from os import getenv

load_dotenv(".env")

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = getenv("STOCK_API_KEY")
NEWS_API_KEY = getenv("NEWS_API_KEY")

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

news_params = {
    "apikey": NEWS_API_KEY,
    "qInTitle": COMPANY_NAME
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(f"Yesterday's closing price: {yesterday_closing_price}")

day_before_data = data_list[1]
day_before_closing = day_before_data["4. close"]
print(f"Day before yesterday closing price: {day_before_closing}")

difference = abs(float(yesterday_closing_price) - float(day_before_closing))
print("Difference: %.2f" %difference)

diff_percent = (difference / float(yesterday_closing_price)) * 100
print("Difference percent: %.2f" %diff_percent)

if(diff_percent >= 0.1):
    ## STEP 2: https://newsapi.org/ 
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 
    print("*** NEWS ***")
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    news_data = news_response.json()["articles"]
    articles = news_data[:3]
    formated_articles = [f"Headline: {article['title']}.\nBrief: {article['description']}" for article in articles]

    print(formated_articles)


#TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.

#TODO 9. - Send each article as a separate message via Twilio. 



#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

