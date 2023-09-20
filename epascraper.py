import time
import pprint as pp
from requests_html import AsyncHTMLSession
import asyncio
import requests_html
import requests
import pandas as pd

cookies = {
    'foiaonline_session_cookie': '876ae20da569645f54253c56be7f8f0c|85fca2fcb504287ead389d608d097bb1',
    'JSESSIONID': 'C542DADAA51EAA362739A50DC86D7499',
}

headers = {
    'authority': 'foiaonline.gov',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    # Already added when you pass json=
    # 'content-type': 'application/json',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'foiaonline_session_cookie=876ae20da569645f54253c56be7f8f0c|85fca2fcb504287ead389d608d097bb1; JSESSIONID=C542DADAA51EAA362739A50DC86D7499',
    'origin': 'https://foiaonline.gov',
    'pragma': 'no-cache',
    'referer': 'https://foiaonline.gov/foiaonline/action/public/search/advancedSearch',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    'x-csrf-token': '22d4b738-04be-4a83-9c2d-fec62282327b',
    'x-foia-page-url': 'https://foiaonline.gov/foiaonline/action/public/search/advancedSearch',
    'x-requested-with': 'XMLHttpRequest',
}


asession = AsyncHTMLSession()
sesh = requests.session()

for x in range(0, 10000, 100):
    json_flra_data = {
        'appealDisposition': [],
        'customField': [],
        'exemptions': [],
        'phase': [],
        'processTime': [],
        'requestDisposition': [],
        'requestTypes': [],
        'status': [],
        'statutes': [],
        'subtypes': [],
        'taskType': [],
        'toOrganization': [
            'FLRA',
        ],
        'toIndividual': [],
        'track': [],
        'type': [],
        'draw': 2,
        'lastItemDisplayed': x,
        'numberOfRecords': 100,
        'toOrganizationIncludeSubAgencies': True,
    }
    try:
        r = requests.post('https://foiaonline.gov/foiaonline/api/search/advancedSearch', cookies=cookies, headers=headers, json=json_flra_data)
        a = r.json()
        b = a['data']
        print('FLRA data')
        df = pd.DataFrame(b)
        df.to_csv("flra_data.csv", mode='a')
        time.sleep(5)
        print(x)
    except Exception as e:
        print("ERROR:  " + str(e))


async def get_files():
    r = await asession.get('https://foiaonline.gov/foiaonline/action/public/submissionDetails?trackingNumber=EPA-2023-006415&type=Request',
        cookies=cookies, headers=headers)
#    await r.html.arender()
#    print(r.html.absolute_links)
    return r


results = asession.run(get_files)
exit()


async def get_urls_and_more():
    try:
        response = await asession.post('https://foiaonline.gov/foiaonline/api/search/advancedSearch', cookies=cookies,headers=headers, json=json_data)
        response_dict = response.json()
        print(response_dict)
        time.sleep(3)
        #        await files_to_grab = session.get('https://foiaonline.gov/foiaonline/action/public/submissionDetails?trackingNumber=EPA-2023-006415&type=Request', cookies=cookies, headers=headers)
        time.sleep(10)
#        await files_to_grab.html.render()
        time.sleep(10)
#        print(files_to_grab.html.absolute_links)
        time.sleep(10)
#        return files_to_grab
    except Exception as e:
        print('ERROR:')
        print(e)
    exit()


def filter_by_releases(data_dict):
    key, value = data_dict
    dispositions = ["Affirmed on Appeal", "Completely Reversed/Remanded", "Fee-Related Reason", "Full Grant", "Other",
                    "Partial Grant/Partial Denial", "Partially Affirmed & Partially Reversed/Remanded"]
    if value in dispositions:
        return True
    else:
        return False


async def main():
    get_urls_and_more()  # this will do nothing because coroutine object is created but not awaited
    await get_urls_and_more()


#asyncio.run(main())


# def download(url, file_name):
    # open in binary mode
#    with open(file_name, "wb") as file:
        # get request
#        response = get(url)
#        # write to file
#        file.write(response.content)