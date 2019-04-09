

# Import dependencies
from splinter import Browser
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import re


# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'C:/Anaconda/webscrapes/chromedriver'}
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('log-level=3')
browser = Browser('chrome', **executable_path, wait_time=2,headless=True,options=chrome_options)


# scrape links to each dealer and place in a list
url = 'https://www.lennox.com/locate/dealer-list/'
browser.visit(url)
html = browser.html
lennox_soup = BeautifulSoup(html, 'html.parser')

dealer_links = []

for i in lennox_soup.find_all(href=re.compile('/locate/dealer')):
    dealer_links.append('https://www.lennox.com'+i.get('href'))


# import time
# start_time = time.time()

df = pd.DataFrame()
for dealer in dealer_links[1:100]:
    try:
        browser.visit(dealer)
        html = browser.html
        dealer_soup = BeautifulSoup(html, 'html.parser')
        
        name = dealer_soup.find(itemprop='name').get_text(strip=True)
        street = dealer_soup.find(itemprop='streetAddress').get_text(strip=True)
        city = dealer_soup.find(itemprop='addressLocality').get_text(strip=True)
        state = dealer_soup.find(itemprop='addressRegion').get_text(strip=True)
        zipcode = dealer_soup.find(itemprop='PostalCode').get_text(strip=True)
        country = dealer_soup.find(itemprop="addressCountry")['content']
        phone = dealer_soup.find(itemprop='telephone').get_text('[0-9]',strip=True)[-12:]
        lat = dealer_soup.find(itemprop="latitude")['content']
        long = dealer_soup.find(itemprop="longitude")['content']
        try:
            website = dealer_soup.find(attrs={'class':'website ng-binding ng-scope'}).get('href')
        except:
            website = ''
        
    except:
        pass
    dealer_df = pd.DataFrame({'name':name,
                             'street':street,
                             'city':city,
                             'state':state,
                             'zipcode':zipcode,
                             'country':country,
                             'phone':phone,
                             'lat':lat,
                             'long':long,
                             'website':website,
                             'brand':'Lennox'},index=[0]
                             
                            )

    df = df.append(dealer_df,ignore_index=True)
browser.quit()    
# print("--- %s seconds ---" % (time.time() - start_time))



from sqlalchemy import create_engine
import urllib


params = urllib.parse.quote_plus('DRIVER={SQL Server Native Client 10.0};Server=gmlsql2hou; DATABASE=invplannersapp;Trusted_Connection=yes;')

engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
df.to_sql('GBU_Webscrape',engine,if_exists='append',index=False)



print('Lennox Scrape completed')

