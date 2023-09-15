import requests
import json
import time
import pprint as pp
from requests_html import AsyncHTMLSession
import asyncio


#session = requests.Session()
#csrf=session.get("https://foiaonline.gov/foiaonline/action/public/search/quickSearch")

#r=session.get('https://foiaonline.gov/foiaonline/api/search/advancedSearch')
#print(session.cookies)
#print(session.headers)

cookies = {
    'foiaonline_session_cookie': 'e992f0d76d004d769432e3a156a15330|85fca2fcb504287ead389d608d097bb1',
    'JSESSIONID': '18659215515E9B06D1D519E5D0A10E68',
}

headers = {
    'authority': 'foiaonline.gov',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'en-US,en;q=0.9',
    # Already added when you pass json=
    # 'content-type': 'application/json',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'foiaonline_session_cookie=e992f0d76d004d769432e3a156a15330|85fca2fcb504287ead389d608d097bb1; JSESSIONID=18659215515E9B06D1D519E5D0A10E68',
    'origin': 'https://foiaonline.gov',
    'referer': 'https://foiaonline.gov/foiaonline/action/public/search/advancedSearch',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    'x-csrf-token': 'de702477-c60c-4b32-baf2-37eb61aef28b',
    'x-foia-page-url': 'https://foiaonline.gov/foiaonline/action/public/search/advancedSearch',
    'x-requested-with': 'XMLHttpRequest',
}

json_data = {
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
        'EPA',
    ],
    'toIndividual': [],
    'track': [],
    'type': [],
    'draw': 2,
    'lastItemDisplayed': 0,
    '_': 200,
    'toOrganizationIncludeSubAgencies': True,
}

asession = AsyncHTMLSession()
#r = session.get('https://foiaonline.gov/foiaonline/api/search/advancedSearch')

async def get_files():
    r = await asession.get('https://foiaonline.gov/foiaonline/action/public/submissionDetails?trackingNumber=EPA-2023-006415&type=Request', cookies=cookies, headers=headers)
    await r.html.arender()
    print(r.html.absolute_links)
    return r

results = asession.run(get_files)
exit()

async def get_urls_and_more():
    try:
        response = await asession.post('https://foiaonline.gov/foiaonline/api/search/advancedSearch', cookies=cookies, 
                             headers=headers, json=json_data)
        response_dict = response.json()
        print(response_dict)
        time.sleep(3)
#        await files_to_grab = session.get('https://foiaonline.gov/foiaonline/action/public/submissionDetails?trackingNumber=EPA-2023-006415&type=Request', cookies=cookies, headers=headers)
        time.sleep(10)
        await files_to_grab.html.render()
        time.sleep(10)
        print(files_to_grab.html.absolute_links)
        time.sleep(10)
        return files_to_grab
    except Exception as e:
        print('ERROR:')
        print(e)
    exit()
    

def filter_by_releases(data_dict):
    key, value = data_dict
    dispositions = ["Affirmed on Appeal", "Completely Reversed/Remanded", "Fee-Related Reason", "Full Grant",  "Other", "Partial Grant/Partial Denial", "Partially Affirmed & Partially Reversed/Remanded"]
    if value in dispositions:
        return True
    else:  
        return False
    

async def main():
    get_urls_and_more()#this will do nothing because coroutine object is created but not awaited
    await get_urls_and_more()

asyncio.run(main())


#for x in response_dict['data']: 
#    data_dict=x
#    filtered_released_docs=dict(filter(filter_by_releases, x.items()))
#    if filtered_released_docs:
#        print('Disposition: ')
#        print(x['finalDisposition'])
#        print('Tracking Number')
#        print(x['trackingNumber'])      


    
#from requests import get  # to make GET request


# def download(url, file_name):
    # open in binary mode
#    with open(file_name, "wb") as file:
        # get request
#        response = get(url)
#        # write to file
#        file.write(response.content)