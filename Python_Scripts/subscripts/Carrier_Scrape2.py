from splinter import Browser
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import re



zipcodes = pd.read_csv('C:/Anaconda/US_zipcodes.csv')



# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'C:/Anaconda/webscrapes/chromedriver'}
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('log-level=3')
browser = Browser('chrome', **executable_path, wait_time=1,headless=True,options=chrome_options)

# Visit Carrier Dealer Locator site
url = 'https://www.carrier.com/residential/en/us/find-a-dealer/'
browser.visit(url)



df=pd.DataFrame()
for z in zipcodes.zip_code[5000:10000:5]:
    browser.cookies.delete()
    browser.find_by_name(name="ctl00$pageContent$FindADealer$dealerLocator").fill(z)
    browser.find_by_id("pageContent_FindADealer_btnSubmit").click()
    html = browser.html
    carrier_soup = BeautifulSoup(html, 'html.parser')
    dict_list=[]
    for i in range(29)[19:]:
        try:  #finds and extracts only portion of javascript embedded in html that contains array of objects(python dictionary) as a string
            dict_list.append(re.findall("(?<=\\')[^\\[),';].*?(?=\\')",carrier_soup.find_all('script')[i].get_text(strip=True)))  
        
        except:
            pass
#this block cleans up list of objects to be converted in list of dictionaries then to a dataframe
    clean_list=[]   
    for d in dict_list:
        try:
            clean_list.append(eval(d[0]))
        except:
            pass
    for d in clean_list:  #this dealer no is the list number on each page not the actual dealer account number
        del d['DealerNo']
        
    df=df.append(pd.DataFrame(clean_list),ignore_index=True)
    df.drop_duplicates(inplace=True)

browser.quit()


df['Country']='United States'
df['Brand'] = 'Carrier'
df['DealerName']= df['DealerName'].apply(lambda x: x.replace('amp;',''))
df['DealerName']= df['DealerName'].apply(lambda x: x.replace("#39;",''))
d2 = pd.DataFrame([df.DealerName,df.PostalAddress,df.City,df.State,df.ZipCode,df.Country,df.Phone,df.LocatorLatitude,df.LocatorLongitude,df.Website,df.Brand]).T



from sqlalchemy import create_engine
import urllib


params = urllib.parse.quote_plus('DRIVER={SQL Server Native Client 10.0};Server=gmlsql2hou; DATABASE=invplannersapp;Trusted_Connection=yes;')

engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
d2.to_sql('GBU_Webscrape',engine,if_exists='append',index=False)

print('2 of 8 complete...')