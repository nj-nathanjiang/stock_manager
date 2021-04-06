import requests
from twilio.rest import Client


API_KEY = "Stock API Key"
NEWS_API_KEY = "News API Key"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
COMPANY_NAME = "TSLA"
account_sid = "Twilio Account Sid"
auth_token = "Twilio Auth Token"

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": COMPANY_NAME,
    "apikey": API_KEY,
}

response = requests.get("https://www.alphavantage.co/query", params=parameters)
response.raise_for_status()
response = response.json()
response = response["Time Series (Daily)"]

data_list = [value for (key, value) in response.items()]
yesterday = data_list[0]
yesterday_closing_price = yesterday["4. close"]
yesterday_closing_price = float(yesterday_closing_price)

day_before_yesterday = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday["4. close"]
day_before_yesterday_closing_price = float(day_before_yesterday_closing_price)

diff = abs(round(float(yesterday_closing_price) - float(day_before_yesterday_closing_price), 2))
if float(yesterday_closing_price) > float(day_before_yesterday_closing_price):
    diff_percentage = abs(round(diff / day_before_yesterday_closing_price, 2))
else:
    diff_percentage = abs(round(diff / yesterday_closing_price, 2))

if diff_percentage > 5:
    news_parameters = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": "Tesla",
    }

    response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    articles = response.json()["articles"]

    three_articles = articles[:3]

    counter = 0
    formatted_articles = [f"Headline: {article['title']}, \nBrief: {article['description']}" for article in three_articles]
    client = Client(account_sid, auth_token)
    for article in formatted_articles:
        counter += 1
        if counter <= 3:
            message = client.messages.create(body=f"{COMPANY_NAME}'s stocks have changed by %{diff_percentage}.\n" + article,
                                             from_='Twilio Phone Number',
                                             to="My Phone Number")
