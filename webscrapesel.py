#import Libraries
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
import pandas as pd
import time

path={'ENTER PATH TO CHROMEDRIVER ON YOUR COMPUTER'}

#Use Incognito mode when scraping

chrome_options = Options()
chrome_options.add_argument(" — incognito")
browser = webdriver.Chrome(path, options=chrome_options)
# pages=int(input('How Many Pages Do You Want to Scrape? '))

#define number of pages to scrape and starting URL (usually page 1)
pages=3
url='http://books.toscrape.com/catalogue/page-1.html'

#Create Function to scrape webpage

def getdata(start_url,pgs):
    current=0
    urls=browser.get(start_url)
    data={}
    df=pd.DataFrame(columns=['Title','Price','Stock','Star'])
    dictionary = {'One':1, 'Two':2, 'Three':3, 'Four':4, 'Five':5}
    while current<pages:
        books = browser.find_elements_by_css_selector('ol.row')
        for book in books:
            for b in book.find_elements_by_css_selector('article.product_pod'):
                data['Title'] = b.find_elements_by_css_selector('img')[0].get_attribute('alt')
                data['Price'] = b.find_elements_by_css_selector('div.product_price p.price_color')[0].text
                data['Stock'] = b.find_elements_by_css_selector('div.product_price p.instock.availability')[0].text
                data['Star'] = b.find_elements_by_css_selector('p')[0].get_attribute('class').split()[-1]
                data['Star'] = [v for k,v in dictionary.items() if k in data['Star']][0]
                df=df.append(data, ignore_index=True)
        next = browser.find_elements_by_css_selector('li.next a')[0].click()
        current+=1
        df.index += 1 #Increments the index from 0 to 1
    return df
output=getdata(url,pages) 
output.to_excel('test.xlsx')
print(output)
