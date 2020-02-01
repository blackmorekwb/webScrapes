import pdb #debugger
import pandas as spreadsheet
import requests
from bs4 import BeautifulSoup

page = requests.get('http://service.prerender.io/https://poe.ninja/challenge/currency')
soup = BeautifulSoup(page.content, 'html.parser')

rows = soup.find_all(class_='fvfr3wi') #each table row of currencies

item_names = [row.find(class_='flex').get_text() for row in rows]
price_pay = [row.find_all(class_='currency-amount')[0].get_text()[:-1] for row in rows]
price_get = [row.find_all(class_='currency-amount')[1].get_text()[:-1] for row in rows]

currency_market = spreadsheet.DataFrame({
    'Item Name': item_names,
    'Chaos Price': price_pay,
    'Amt Received': price_get
})

print(currency_market)

currency_market.to_csv('poe_currencies.csv')
