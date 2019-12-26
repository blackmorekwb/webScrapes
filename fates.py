import re
from robobrowser import RoboBrowser
import pdb #debugger
import pandas as spreadsheet
import requests
from bs4 import BeautifulSoup

##### -- GLOBALS --
page = requests.get('https://pathofexile.gamepedia.com/Prophecy#Upgrading_uniques')
soup = BeautifulSoup(page.content, 'html.parser')
browser = RoboBrowser()
browser.open("https://poe.trade/")
form = browser.get_form(id="search")
fated_uniques = [[],[],[]]
prices = [[],[],[]]
##### -- --

##### -- FATED SEARCH / GET NAMES
fated_page = soup.find(class_='mw-parser-output')
h2 = fated_page.find(id="Fated_Uniques")
fates = h2.parent.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling
fates_rows = fates.tbody.find_all('tr')
del fates_rows[0]

fated_uniques[0] = [row.td.get_text() for row in fates_rows]

count = 0
for row in fates_rows:
    print( str(count) + ' : ' + row.td.get_text())
    acts = row.td.next_sibling.em.find_all(class_="c-item-hoverbox__activator")
    fated_uniques[1].append( acts[0].get_text() )
    fated_uniques[2].append( acts[1].get_text() )
    count += 1
del fated_uniques[0][-55:]
del fated_uniques[1][-55:]
del fated_uniques[2][-55:]
##### --

##### -- GET PRICES (ALL)
for i in range(0, len(fated_uniques[0])):
    form['name'] = fated_uniques[0][i]
    browser.submit_form(form)
    parsed = BeautifulSoup(str(browser.parsed()), 'html.parser')
    results = parsed.find(class_="search-results")
    t = results.tbody.find(attrs={"data-name":"price_in_chaos_new"})
    y = t.find(class_="currency")
    price = y['title']

    print(price) # the price as string

    prices[0].append(price)
##### --
##### --

##### -- CSV/EXCEL

fated_market = spreadsheet.DataFrame({
    'Prophecy': fated_uniques[0],
    'Price':prices[0] ,
    'Base': fated_uniques[1],
    #'Price': prices[1],
    'Fated': fated_uniques[2],
    #'Price': prices[2],
})

fated_market.to_csv("fated_uniques.csv") #, sheet_name='Prophecies Profit'



#pdb.set_trace()
