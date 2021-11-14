from bs4 import BeautifulSoup
import urllib.request,sys,time
import requests
import pandas as pd
import re  

import urllib.request,sys,time
from bs4 import BeautifulSoup
import requests
import pandas as pd

# pagesToGet= 5

def scrapTrain(numberOfpages):
    frame=[]
    for page in range(1,numberOfpages+1):
        print('processing page :', page)
        url = 'https://www.politifact.com/factchecks/list/?page='+str(page)
        print(url)
        
        #an exception might be thrown, so the code should be in a try-except block
        try:
            #use the browser to get the url. This is suspicious command that might blow up.
            page=requests.get(url)                             # this might throw an exception if something goes wrong.
        
        except Exception as e:                                   # this describes what to do if an exception is thrown
            error_type, error_obj, error_info = sys.exc_info()      # get the exception information
            print ('ERROR FOR LINK:',url)                          #print the link that cause the problem
            print (error_type, 'Line:', error_info.tb_lineno)     #print error info and line that threw the exception
            continue                                              #ignore this page. Abandon this and go back.
        time.sleep(2)   
        soup=BeautifulSoup(page.text,'html.parser')
        
        links=soup.find_all('li',attrs={'class':'o-listicle__item'})
        print(len(links))

        for j in links:
            Link = "https://www.politifact.com"
            Link += j.find("div",attrs={'class':'m-statement__quote'}).find('a')['href'].strip()
            Statement = j.find("div",attrs={'class':'m-statement__quote'}).text.strip()
            Label = j.find('div', attrs ={'class':'m-statement__content'}).find('img',attrs={'class':'c-image__original'}).get('alt').strip()
            Source = j.find('div', attrs={'class':'m-statement__meta'}).find('a').text.strip()
            if (Label =='true'):
                Label = 'REAL'
            elif (Label =='false'):
                Label ='FAKE'
            if(Label == 'REAL') or (Label == 'FAKE'):
                row= {"text": Statement, "link":Link, "source":Source, "label": Label}
                frame.append(row)
    #data scraped into csv to train it
    data= pd.DataFrame.from_dict(frame)
    data.to_csv("./data.csv",index=False)
    return frame