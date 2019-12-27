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
    print( str(count) + ' : ' + row.td.get_text())
    acts = row.td.next_sibling.em.find_all(class_="c-item-hoverbox__activator")
    fated_uniques[1].append( acts[0].get_text() )
    fated_uniques[2].append( acts[1].get_text() )
    count += 1
#del fated_uniques[0][-42:]
#del fated_uniques[1][-42:]
#del fated_uniques[2][-42:]
##### --

##### -- GET PRICES (ALL)

def print_row(prof="n/a",p1="n/a",base="n/a",p2="n/a",fated="n/a",p3="n/a"):
    print("\t{:<30}\t{:<10}\t{:<20}\t{:<10}\t{:<27}\t{:<7}".format(prof, p1, base, p2, fated, p3)     )

"""
def get_batches(start,col):
    max = 56
    batch = 7 #(56/8) #7
    batch_count = 0
    #start = 0
    for i in range(0, (max-1)-batch ): #0-55  == 56 elements
        #get_prices(i, (r)*(i/) )
        #pdb.set_trace() # why start and end im get prices is alays 0-7

        #if (start>= max - batch):
        #    pdb.set_trace()

        #start = 0

        get_prices(start, (start+batch), col  )     #0-7 // 8-15  // 16-23  24-31  32-39  40-47  48-55  (remainder of 1) actually 55 would equal 56 elements with [0]
        start += (batch+1)
        i += (batch+1)
        batch_count += 1
        print('Batch ' + str(batch_count) + ' complete.')
        print(' ## ' * batch_count)
"""

def get_prices_batched():
    max = 56
    batch = 7 #(56/8) #7 batches if 8 searches each
    batch_count = 0
    start = 0

    print('in batched')
    get_prices(0,7,0)
    print('BATCH COMPLETE')
    get_prices(8,15,0)
    print('BATCH COMPLETE')
    get_prices(16,23,0)
    print('BATCH COMPLETE')
    get_prices(24,31,0)
    print('BATCH COMPLETE')
    get_prices(32,39,0)
    print('BATCH COMPLETE')
    get_prices(40,47,0)
    print('BATCH COMPLETE')
    get_prices(48,56,0)
    print('BATCH COMPLETE')


    print('in batched')
    get_prices(0,7,1)
    print('BATCH COMPLETE')
    get_prices(8,15,1)
    print('BATCH COMPLETE')
    get_prices(16,23,1)
    print('BATCH COMPLETE')
    get_prices(24,31,1)
    print('BATCH COMPLETE')
    get_prices(32,39,1)
    print('BATCH COMPLETE')
    get_prices(40,47,1)
    print('BATCH COMPLETE')
    get_prices(48,56,1)
    print('BATCH COMPLETE')

    print('in batched')
    get_prices(0,7,2)
    print('BATCH COMPLETE')
    get_prices(8,15,2)
    print('BATCH COMPLETE')
    get_prices(16,23,2)
    print('BATCH COMPLETE')
    get_prices(24,31,2)
    print('BATCH COMPLETE')
    get_prices(32,39,2)
    print('BATCH COMPLETE')
    get_prices(40,47,2)
    print('BATCH COMPLETE')
    get_prices(48,56,2)     ## 1 less for last one. out of range. 5
    print('BATCH COMPLETE')

    """
    for col in range(0,2):
        print('COLUMN Done! ' + str(col) + '/3')
        print('COL: ' + str(col))
        batch_count = 0
        start = 0 #re-start for each of 3 collumns
        print('restarting start: start = ' + str(start))
        #get_batches(col)

        for i in range(0, (max-1)-batch ): #0-55  == 56 elements
            #get_prices(i, (r)*(i/) )
            #pdb.set_trace() # why start and end im get prices is alays 0-7

            #if (start>= max - batch):
            #    pdb.set_trace()

            get_prices(start, (start+batch), col  )     #0-7 // 8-15  // 16-23  24-31  32-39  40-47  48-55  (remainder of 1) actually 55 would equal 56 elements with [0]
            start += (batch+1)
            i += (batch+1)
            batch_count += 1
            print('Batch ' + str(batch_count) + ' complete.')
            print(' ## ' * batch_count)
        """
# 0-8  9-16  17-25 26-34 35-43 44-5#2 4 remainder
def tst(i, start, end, col):
    print("I={:<7}\tStart={:<7}\tEnd={:<7}\tCOL={:<7}".format(i, start , end, col)     )

def get_prices(start,end,col):
    for i in range(start,end+1):
        #i gets reset to zero for each column change -good
        #! i skips a number in between batches, thowing everything off
        form['name'] = fated_uniques[col][i]
        browser.submit_form(form)
        parsed = BeautifulSoup(str(browser.parsed()), 'html.parser')
        results = parsed.find(class_="search-results")
        t = results.tbody.find(attrs={"data-name":"price_in_chaos_new"})
        y = t.find(class_="currency")
        price = y['title']

        #print(price) # the price as string

        #prices[col].append(price)
        #if (i>= 53):
        #    pdb.set_trace()

        prices[col][i] = price
        tst(i,start,end,col)
        print_row(fated_uniques[0][i], prices[0][i],
                  fated_uniques[1][i], prices[1][i],
                  fated_uniques[2][i], prices[2][i])
##### --
##### --
get_prices_batched()

pdb.set_trace()

##### -- CSV/EXCEL
fated_market = spreadsheet.DataFrame({
    'Prophecy': fated_uniques[0],
    'Price1': prices[0],
    'Base': fated_uniques[1],
    'Price2': prices[1],
    'Fated': fated_uniques[2],
    'Price3': prices[2],
})
fated_market.to_excel("fated_uniques.xlsx", sheet_name='Prophecies Profit') #, sheet_name='Prophecies Profit'
