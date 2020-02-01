import re
from robobrowser import RoboBrowser
import pdb #debugger
import pandas as spreadsheet
import requests
from bs4 import BeautifulSoup

##### -- GLOBALS --
page = requests.get('https://pathofexile.gamepedia.com/Prophecy#Upgrading_uniques')
soup = BeautifulSoup(page.content, "lxml")
browser = RoboBrowser()
browser.open("https://poe.trade/")
form = browser.get_form(id="search")
fated_uniques = [[],[],[]]
prices = [[0 for x in range(57)],[0 for x in range(57)],[0 for x in range(57)]]
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
    acts = row.td.next_sibling.em.find_all(class_="c-item-hoverbox__activator")
    fated_uniques[1].append( acts[0].get_text() )
    fated_uniques[2].append( acts[1].get_text() )
    count += 1
##### --

def print_row(prof="n/a",p1="n/a",base="n/a",p2="n/a",fated="n/a",p3="n/a"):
    print("\t{:<27}\t{:<17}\t{:<20}\t{:<10}\t{:<21}\t{:<7}".format(prof, p1, base, p2, fated, p3)     )

##### -- GET PRICES (BATCHED)
def get_prices_batched():
    max = 56
    batch = 7 #(56/8) #7 batches if 8 searches each
    batch_count = 0
    start = 0

    for col in range(0,3):
        batch_count = 0
        start = 0 #re-start for each of 3 collumns

        for i in range(0, (int((max-batch)/7)+1) ):
            print('Start: ' + str(start) + '  s+batch: ' + str(start+batch) +'  col: ' + str(col))

            #was getting remainder of 1, so it was going out of index in the next batch. just monkey patching this
            if start!=56:
                get_prices(start, (start+batch), col  )     #0-7 // 8-15  // 16-23  24-31  32-39  40-47  48-55  (remainder of 1) actually 55 would equal 56 elements with [0]
            else:
                get_prices(start, start, col  )     # put an 'end' counter. and just if start is 48, increase the end by 1

            start += (batch+1)
            i += (batch+1)
            batch_count += 1

            print('Batch ' + str(batch_count) + ' complete -- ' +
                  'Column ' + str(col+1) + '/3 - ' + str(round(((8/max)*batch_count)*100)) + '% complete')
            print(' ## ' * batch_count )

# Personal debugging
#def print_vars(i, start, end, col):
#    print("I={:<7}\tStart={:<7}\tEnd={:<7}\tCOL={:<7}".format(i, start , end, col)     )

def get_prices(start,end,col):
    for i in range(start,end+1):
        form['name'] = fated_uniques[col][i]
        browser.submit_form(form)
        parsed = BeautifulSoup(str(browser.parsed()), "lxml")
        results = parsed.find(class_="search-results")
        t = results.tbody.find(attrs={"data-name":"price_in_chaos_new"})
        y = t.find(class_="currency")
        price = y['title']

        prices[col][i] = price
        print_row(fated_uniques[0][i], prices[0][i],
                  fated_uniques[1][i], prices[1][i],
                  fated_uniques[2][i], prices[2][i])
##### --
##### --
get_prices_batched()

##### -- CSV/EXCEL
fated_market = spreadsheet.DataFrame({
    'Prophecy': fated_uniques[0],
    'Price1': prices[0],
    'Base': fated_uniques[1],
    'Price2': prices[1],
    'Fated': fated_uniques[2],
    'Price3': prices[2],
})
fated_market.to_excel("fated_uniques.xlsx", sheet_name='Prophecies Profit') 
