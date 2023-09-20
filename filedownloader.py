import time
import requests
import pandas as pd
import json
from bs4 import BeautifulSoup
import datetime
import calendar
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

cookies = {
    'foiaonline_session_cookie': '75c891ca741094a1531f89fa1a1d6d2b|85fca2fcb504287ead389d608d097bb1',
    'JSESSIONID': '9D5B2106473E3FE516D32C225161B2CD',
    'cebs': '1',
    '_ce.s': 'v~a7e3e2a52236d856b4109e154dfcd9f4f84f9d4e~lcw~1694453787905~vpv~0~lcw~1694453787906',
    '_gid': 'GA1.2.1758653570.1695057245',
    '_gat_EPA': '1',
    '_gat_GSA_ENOR0': '1',
    '_ga': 'GA1.1.1176546414.1694453787',
    '_ga_2SEC4V3SK9': 'GS1.1.1695150722.6.1.1695150744.0.0.0',
    '_ga_CSLL4ZEK4L': 'GS1.1.1695150722.6.1.1695150744.0.0.0',
}

headers = {
    'authority': 'foiaonline.gov',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'foiaonline_session_cookie=ae44877653411adbdccca3e4ca784a50|85fca2fcb504287ead389d608d097bb1; JSESSIONID=6FD188510D96C7E64DE4F772322CA911; cebs=1; _ce.s=v~a7e3e2a52236d856b4109e154dfcd9f4f84f9d4e~lcw~1694453787905~vpv~0~lcw~1694453787906; _gid=GA1.2.1758653570.1695057245; _ga_2SEC4V3SK9=GS1.1.1695141697.5.1.1695141779.0.0.0; _ga=GA1.1.1176546414.1694453787; _ga_CSLL4ZEK4L=GS1.1.1695141697.5.1.1695141779.0.0.0',
    'dnt': '1',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
}

opt = webdriver.ChromeOptions()
#opt.add_argument('--headless')
opt.add_argument("--no-referrers")
download_dir = "D:\scraperfiles"
opt.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True
})
driver = webdriver.Chrome(options=opt)

sesh = requests.session()

# submission details https://foiaonline.gov/foiaonline/action/public/submissionDetails?trackingNumber=EPA-R5-2023-006692&type=Request

with open('epa_data.csv', encoding='utf-8') as file:
    df = pd.read_csv(file)
   # print(df.columns.values.tolist())
    tracking_list=df.trackingNumber.unique()
    for entry in tracking_list:
        if entry is not None:
            try:
                driver.get("https://foiaonline.gov/foiaonline/action/public/submissionDetails?trackingNumber="+ str(entry) +"&type=Request")
                cookies = driver.get_cookies()
                # Text you want to search
                WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH,".//*[@id=\"savedSupportingFiles\"]/tbody/tr/td[2]/a")))
                #elements = driver.find_elements(By.ID, "savedSupportingFiles")
                #WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, ".//*[@id=\"savedSupportingFiles\"]/tbody/tr/td[2]/a")))
                elements=driver.find_elements(By.XPATH, "//*[@id=\"savedSupportingFiles\"]/tbody/tr/td[2]/a")
                for element in elements:
                    e = element.click()
                    time.sleep(5)
                print('Attempted to grab file from request  : ' + str(entry))
            except Exception as e:
                print("Error:  " + str(e) + " on request  " + str(entry))
                continue
                #/html/body/div[2]/div/div[2]/div/div/div[2]/div[2]/form/fieldset[2]/div/div/table/tbody/tr/td[2]/a
                #.//*[@id=\"savedSupportingFiles\"]/tbody/tr/td[2]/a

                #
                # response = requests.get(url)
                # soup = BeautifulSoup(response.text, 'lxml')
                # csrfToken = soup.find('input', attrs={'name': 'x-csrf-token'})['value']
                # print(csrfToken)
                # if csrfToken:
                #     xhr_headers = {
                #        'authority': 'foiaonline.gov',
                #         'accept': 'application/json, text/javascript, */*; q=0.01',
                #         'accept-language': 'en-US,en;q=0.9',
                #         # Already added when you pass json=
                #         # 'content-type': 'application/json',
                #         # Requests sorts cookies= alphabetically
                #         # 'cookie': 'foiaonline_session_cookie=75c891ca741094a1531f89fa1a1d6d2b|85fca2fcb504287ead389d608d097bb1; JSESSIONID=9D5B2106473E3FE516D32C225161B2CD; cebs=1; _ce.s=v~a7e3e2a52236d856b4109e154dfcd9f4f84f9d4e~lcw~1694453787905~vpv~0~lcw~1694453787906; _gid=GA1.2.1758653570.1695057245; _gat_EPA=1; _gat_GSA_ENOR0=1; _ga=GA1.1.1176546414.1694453787; _ga_2SEC4V3SK9=GS1.1.1695150722.6.1.1695150744.0.0.0; _ga_CSLL4ZEK4L=GS1.1.1695150722.6.1.1695150744.0.0.0',
                #         'dnt': '1',
                #         'origin': 'https://foiaonline.gov',
                #         'referer': url,
                #         'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
                #         'sec-ch-ua-mobile': '?0',
                #         'sec-ch-ua-platform': '"Windows"',
                #         'sec-fetch-dest': 'empty',
                #         'sec-fetch-mode': 'cors',
                #         'sec-fetch-site': 'same-origin',
                #         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
                #         'x-csrf-token': 'e2d715cb-6aba-4a86-8846-00d2ba6d097b',
                #         'x-foia-page-url': url,
                #         'x-requested-with': 'XMLHttpRequest',
                #     }
                #     date = datetime.datetime.utcnow()
                #     utc_time = calendar.timegm(date.utctimetuple())
                #     xhr_post = requests.post('https://foiaonline.gov/foiaonline/api/request/publicRecords/EPA-R5-2023-006692/Request?_', cookies=cookies, headers=xhr_headers, json=xhr_json_data, timeout=2.5)
                #     print(xhr_post)
                #     print(xhr_post.text)
                #     get_new_request=requests.get(url,cookies=cookies, headers=xhr_headers)
                #     print(get_new_request)
                #     response_dict = response.json()
                #     print(response_dict)
                # exit()


#input-type=hidden name='x-csrf-token'