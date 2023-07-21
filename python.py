import requests
from bs4 import BeautifulSoup
import telegram
import os
import asyncio

# Set up Telegram bot
bot = telegram.Bot(token="6399721967:AAHeDS5LuDOw8ahjs-ixmhnuBFZXwcAu47I")
chat_id = "@CryptoMarketAlpha"

# Scraping coinmarketcap data
url = "https://coinmarketcap.com/"
result = requests.get(url).text
doc = BeautifulSoup(result, "html.parser")

tbody = doc.tbody
trs = tbody.contents

prices = {}

for tr in trs[:10]:
    name, price = tr.contents[2:4]
    fixed_name = name.p.string
    fixed_price = price.a.string

    prices[fixed_name] = fixed_price

# Function to get the price of a specific cryptocurrency
def get_price(crypto):
    if crypto in prices:
        return prices[crypto]
    else:
        return "Cryptocurrency not found"

# Function to get the top N cryptocurrencies by market cap
def get_top_n(n):
    top_n = {}
    for tr in trs[:n]:
        name, _, _, _, market_cap = tr.contents[1:6:2]
        fixed_name = name.p.string
        fixed_market_cap = market_cap.string.strip().replace("$", "").replace(",", "")
        top_n[fixed_name] = fixed_market_cap
    return top_n

# Send message to Telegram channel
async def send_telegram_message():
    message = "Top 10 cryptocurrencies by market cap:\n\n"
    for name, price in prices.items():
        message += f"{name}: {price}\n"

    await bot.send_message(chat_id=chat_id, text=message)

# Main program
async def main():
    while True:
        await send_telegram_message()
        await asyncio.sleep(600)  # 1 minute delay

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())