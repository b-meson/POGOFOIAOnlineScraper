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

To grab the files, you can easily make a request to find the released records (i.e. open https://foiaonline.gov/foiaonline/action/public/submissionDetails?trackingNumber=EPA-2023-006415&type=Request_) but that doesn't get you everything. Instead, the website loads the file links in a jquery table with download links (i.e. https://foiaonline.gov/foiaonline/api/request/downloadFile/Interim%20Policy%20on%20Annual%20Leave%20Accrual%20for%20Non-Federal%20or%20Uniformed%20Service%20Work%20Experience.pdf/ca743032-e7f7-4cbc-9e8b-9d4f47971903?x-csrf-token=ee74b464-8f38-4648-b89c-f36a14765bde_). The csrf token we have already from the setup task so in theory we can just wget -c " " the file. 

But I don't know how to deal with the jquery table and how to grab the URL to pull the files from without the file names. 

Alternatively, can we mess with _https://foiaonline.gov/foiaonline/api/request/downloadFile_ endpoint to have it tell us the filename? 
