import requests
import smtplib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as soup
import re
import pandas as pd
import time
import lxml
import io
import os
from selenium.webdriver.chrome.options import Options
from urllib.request import urlopen

options = Options()

options.add_argument('--user-data-dir=C:/Users/e1mhd37/AppData/Local/Google/Chrome/User Data/Profile 1')
headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}

url = 'https://www.amazon.com/?tag=amazusnavi-20&hvadid=381823327672&hvpos=1t1&hvnetw=g&hvrand=5076690707764625637&hvpone=&hvptwo=&hvqmt=e&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9008471&hvtargid=aud-840076997981:kwd-10573980&ref=pd_sl_7j18redljs_e&hydadcr=28883_11845445&gclid=Cj0KCQiAiZPvBRDZARIsAORkq7fF_iZWBen-r1q4fQmiga6cHELLC1ly_b76SPet9xf4BOVCU_2rvckaAjwCEALw_wcB'
print("What are you searching for today?")
search_terms = "32in tv"

driver = webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe', options=options)


driver.get(url)

time.sleep(6)
search_bar = driver.find_element_by_xpath("/html/body/div[1]/header/div/div[1]/div[3]/div/form/div[3]/div[1]/input")


driver.implicitly_wait(30)
search_bar.send_keys(search_terms)
search_bar.send_keys(u'\ue007')

curr_url = driver.current_url
client = urlopen(curr_url)
page_html = client.read()
client.close()


page_soup = soup(page_html, "html.parser")

# container contains Price, Item Description and Reviews and Rating
containers = page_soup.findAll("div", {"class":"sg-col-4-of-12 sg-col-8-of-16 sg-col-16-of-24 sg-col-12-of-20 sg-col-24-of-32 sg-col sg-col-28-of-36 sg-col-20-of-28"})
container = containers[0]


filename = "best_items.csv"

f = open(filename, "w", encoding="utf-8")
headers = "Item_Description\n"
f.write(headers)


for container in containers:
    itm_desc_cont = container.findAll("span", {"class":"a-size-medium a-color-base a-text-normal"})
    itm_desc = itm_desc_cont[0].text

    prc_whl_container = container.findAll("span", {"class":"a-price-whole"})
    itm_price_whole = prc_whl_container[0]

    prc_dec_container = container.findAll("span", {"class":"a-price-fraction"})
    itm_price_decimal = prc_dec_container[0]
    itm_price = str(itm_price_whole) + str(itm_price_decimal)

    #Get Item Star Review
    #Get count of Ratings
    #Get Discounted Price
    #Take difference and represent it as a discount percent 
    #sort results by largest discount percent
    #Flip through 5 pages of results
    f.write(itm_desc.replace(",","|") + "\n" + itm_price + "\n")

f.close()



driver.close()
