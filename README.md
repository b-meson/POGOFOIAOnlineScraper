# FOIAOnlineArchive

A scraper that will go to FOIAonline, grab the last 10,000 FOIA requests per agency and then tell you if records where released. 

#### Setup 

FOIAOnline makes CSRF very annoying to work with and while the commands work in cURL, they were failing in the Python requests library. My current workflow is to go to the [FOIA online website](https://foiaonline.gov/foiaonline/action/public/search/advancedSearch), turn on developer mode, and fill in an agency (EPA). Make your search. I think go to the Network Tab, find the request and copy as cURL. I take that output from cURL and use a nice website like [ScrapingBee](https://www.scrapingbee.com/curl-converter/python/) to make the headers and cookies work in the Python library.

Headers have to be refreshed approximately every few hours. 

### The "API" that FOIAOnline Uses

It's an undocumented API but as far as I can tell, the _json_data_ that gets sent as raw bytes is how you pull data. You can reasonably pull ~1,000 replies per query (_numberOfRecords_) but I've been doing ~300. To pull the last 300-600, you increment _lastitemDisplayed_ by 300 and so on. 

Code is in _epascraper.py_.

### Filtering the Data

I use the FOIA disposition (Partial Grant/Full Grant/Appealed etc) as a proxy for if records _may_ exist. This is probably undercounting the possible queries to grab the files, but it's what I have to work with. In the filter function, I match the dictionary key _finalDisposition_ to a list of possible dispotions. If it matches, we want to store the _trackingNumber_ since we need that to download the files. 

### File Download
## TODO

To grab the files, you can easily make a request to find the released records. First, you need to get the filenames and record ID's from the API: 

```
import requests

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
    'referer': 'https://foiaonline.gov/foiaonline/action/public/submissionDetails?trackingNumber=EPA-2023-006415&type=Request',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    'x-csrf-token': 'de702477-c60c-4b32-baf2-37eb61aef28b',
    'x-foia-page-url': 'https://foiaonline.gov/foiaonline/action/public/submissionDetails?trackingNumber=EPA-2023-006415&type=Request',
    'x-requested-with': 'XMLHttpRequest',
}

json_data = {
    'numberOfRecords': 25,
    'lastItemDisplayed': 0,
    'draw': 1,
}

response = requests.post('https://foiaonline.gov/foiaonline/api/request/publicRecords/EPA-2023-006415/Request', cookies=cookies, headers=headers, json=json_data)
```

which returns that data:

```
{
  "draw" : 1,
  "recordsTotal" : 1,
  "recordsFiltered" : 1,
  "data" : [ {
    "trackingNumber" : "EPA-2023-006415",
    "title" : "Interim Policy on Annual Leave Accrual for Non-Federal or Uniformed Service Work Experience",
    "fileName" : "Interim Policy on Annual Leave Accrual for Non-Federal or Uniformed Service Work Experience.pdf",
    "releaseType" : "UR - Unredacted - Releasable to the General Public",
    "exemptions" : null,
    "ex3statutes" : [ "N/A" ],
    "ex5subtypes" : [ "N/A" ],
    "keywords" : null,
    "uploadedBy" : "Matthew Waits",
    "uploadedByEmail" : "Waits.Matthew@epa.gov",
    "createdDate" : "09/06/2023 02:14 PM",
    "lastModifiedDate" : "09/06/2023 10:33 PM",
    "fileType" : "Adobe PDF Document",
    "fileFormat" : null,
    "author" : null,
    "addedBy" : "cbf58edf-15ec-4a7f-82bf-dff23d0f78b1",
    "size" : "0.2159",
    "recordReleaseDate" : "09/06/2023 10:33 PM",
    "retentionPeriod" : "6 Year",
    "frequentlyRequested" : null,
    "type" : "Record",
    "recordId" : "ca743032-e7f7-4cbc-9e8b-9d4f47971903",
    "referredToNonparticipatingAgency" : "No",
    "referredFromOtherAgency" : "No",
    "referredType" : null,
    "recordType" : null,
    "taskId" : null,
    "isPlaceholder" : false
  } ],
  "dataMap" : null
}```

Then you can use the _fileName_ (HTML encoded) and the _recordId_ and a CSRF token to request the file. Here is the download URL:

`
https://foiaonline.gov/foiaonline/api/request/downloadFile/Interim%20Policy%20on%20Annual%20Leave%20Accrual%20for%20Non-Federal%20or%20Uniformed%20Service%20Work%20Experience.pdf/ca743032-e7f7-4cbc-9e8b-9d4f47971903?x-csrf-token=de702477-c60c-4b32-baf2-37eb61aef28b
`