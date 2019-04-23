def trane_scrape(start,end):
    

    # Import dependencies
    from splinter import Browser
    from selenium import webdriver
    from bs4 import BeautifulSoup
    import pandas as pd
    import re
    from sqlalchemy import create_engine
    import urllib

    # Set the executable path and initialize the chrome browser in splinter
    executable_path = {'executable_path': 'C:/Anaconda/webscrapes/chromedriver'}
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('log-level=3')
    browser = Browser('chrome', **executable_path, wait_time=2,headless=True,options=chrome_options)

    trane_links = pd.read_csv('data/Trane_Dealer_List.csv')
    
    df = pd.DataFrame()
    for site in trane_links['0'][start:end]:
        dealer = 0
        street = 0
        city = 0
        state = 0
        zipcode = 0
        country = 0
        phone = 0
        lat = 0
        long = 0
        website = ''
        try:
            browser.visit(site)
            html = browser.html
            dealer_soup = BeautifulSoup(html, 'html.parser')
            
            dealer = dealer_soup.find(class_="headline headline--uppercase headline--dark").get_text(strip=True)
            try:
                street = dealer_soup.find(class_="address_st").get_text(strip=True)
            except:
                pass
            city_state_zip = dealer_soup.find(class_="address_city-state").get_text(strip=True)
            city = city_state_zip.split(',')[0]
            state = re.findall('(?<!\').+(?=\s)', city_state_zip.split(',')[1] )[0].strip()
            zipcode = city_state_zip.split(',')[1][-6:].strip()
            if any(c.isalpha() for c in zipcode) == True:
                country='Canada'
            else:
                country='United States'
            phone =  dealer_soup.find(class_="ss-phone").next_element.get_text(strip=True)
            lat = ''
            long = ''
            website = ''
            brand = 'Trane'
            dealer_df = {'DealerName':dealer,
                         'PostalAddress':street,
                         'City':city,
                         'State':state,
                         'ZipCode':zipcode,
                         'Country':country,
                         'Phone':phone,
                         'LocatorLatitude':lat,
                         'LocatorLongitude':long, 
                         'Website':website,
                         'Brand':brand}

            df = df.append(dealer_df,ignore_index=True)
            df.drop_duplicates(inplace=True)

        except:
            pass
  
    try:
        df2 = pd.DataFrame([df.DealerName,df.PostalAddress,df.City,df.State,df.ZipCode,df.Country,df.Phone,df.LocatorLatitude,df.LocatorLongitude,df.Website,df.Brand]).T
        
    
 

        params = urllib.parse.quote_plus('DRIVER={SQL Server Native Client 10.0};Server=gmlsql2hou; DATABASE=invplannersapp;Trusted_Connection=yes;')

        engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
        df2.to_sql('GBU_Webscrape',engine,if_exists='append',index=False)
    except:
        pass
    

    browser.quit()
    
    
    print(f'{len(df.DealerName)} dealers uploaded to DB')