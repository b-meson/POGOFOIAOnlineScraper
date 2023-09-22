import time
import requests
import pandas as pd
import json
from bs4 import BeautifulSoup
import datetime
import calendar
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

cookies = {

        }

headers = {

        }

opt = webdriver.ChromeOptions()

opt.add_argument("-headless")
opt.add_argument("--no-referrers")
download_dir = "/home/admin/POGOFOIAOnlineScraper"
opt.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True
})

driver = webdriver.Chrome(options=opt)

sesh = requests.session()

for file in sorted(os.listdir(download_dir)):
     #filename = os.fsdecode(file)
     if file.startswith("csv_part_"):
         with open(file, encoding='utf-8') as f:
            df = pd.read_csv(f, engine='python', encoding='utf-8', on_bad_lines='skip')
   # print(df.columns.values.tolist())
            tracking_list=df.trackingNumber.unique()
            print("--------------------------------------")
            print("-----OPENING FILE --------------------")
            print("---- " + "FILENAME : " + f.name.upper())
            print("--------------------------------------")
            print("--------------------------------------")
            print("--------------------------------------")
            for entry in tracking_list:
#                print(entry)
                if entry is not None:
                    try:
                        print("Attempting to get file from FOIA number:  " + str(entry))
                # THIS IS A REAL RESPONSE WITH MULTIPLE FILES TO DOWNLOAD
                # https://foiaonline.gov/foiaonline/action/public/submissionDetails?trackingNumber=EPA-R10-2023-006231&type=Request
                        #driver.get("https://foiaonline.gov/foiaonline/action/public/submissionDetails?trackingNumber=EPA-R10-2023-006231&type=Request")
                        driver.get("https://foiaonline.gov/foiaonline/action/public/submissionDetails?trackingNumber="+str(entry)+"&type=Request")
                        cookies = driver.get_cookies()
                        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH,".//*[@id=\"recordsTable\"]/tbody/tr/td[2]/a")))
                        elements=driver.find_elements(By.XPATH, ".//*[@id=\"recordsTable\"]/tbody/tr/td[2]/a")
                        for element in elements:
                            print('Attempted to grab filename  : ' + str(element.text))
                            e = element.click()
                            time.sleep(5)
                            filename = max([os.path.join(download_dir,f) for f in os.listdir(download_dir)], key=os.path.getctime)
                            j = "FOIA_Request_Number_"+str(entry)+str("_")+ str(element.text)
                            print("file downloaded:  " + j+"_"+ str(element.text) +'.pdf')
                            os.rename(filename,j+'.pdf')
                    except Exception as e:
                        print("Error:" + " on request  " + str(entry))
                        continue
