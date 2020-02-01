import re
from robobrowser import RoboBrowser
import pdb #debugger
import pandas as spreadsheet
import requests
from bs4 import BeautifulSoup


#-----------------------------
# get list of items

items_array = []
items_url = "https://elderscrollsonline.wiki.fextralife.com/Provisioning+Materials"
items_page = requests.get(items_url)
items_soup = BeautifulSoup(items_page.content, "lxml")

items_table = items_soup.find(class_="table-responsive")
items_rows = items_table.find_all('tr')
del items_rows[0]   #table header row

for row in range(len(items_rows)):
    item_name = items_rows[row].find_all('td')[1].get_text()
    items_array.append(item_name)


#------------------------------
# feed items list into parser

prices_array = []

for item in range(len(items_array)):
    price_check = "https://us.tamrieltradecentre.com/pc/Trade/SearchResult?ItemID=&SearchType=PriceCheck&ItemNamePattern=%22" + items_array[item] + "%22&ItemCategory1ID=3&ItemCategory2ID=15&ItemCategory3ID=47&ItemTraitID=&ItemQualityID=&IsChampionPoint=false&LevelMin=&LevelMax=&MasterWritVoucherMin=&MasterWritVoucherMax="
    page = requests.get(price_check)
    soup = BeautifulSoup(page.content, "lxml")

    table = soup.find(class_="trade-list-table")
    rows = table.find_all('td')
    prices = rows[1].find_all(class_="gold-amount")
    average = prices[1].get_text().strip()
    prices_array.append(average)
    print("Item: " + items_array[item] + "\t Avg Price: " + average)


#-------------------------------
# export data to spreadsheet
items_market = spreadsheet.DataFrame({
    'Item Name': items_array,
    'Avg Price': prices_array
})
items_market.to_csv('eso_materials.csv')



#----
#-todo's
# add min and max to price data
# add wighting algorith to find moving lines between min. and avg.
# pull data from recipe list, compare ingredients needed to prices of each.
   # calculate estimated profit based on weighted avg
