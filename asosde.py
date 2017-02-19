from pyzvlab import HTMLParser
from urllib import request
from urllib.parse import urlencode, quote_plus
from time import sleep

import urllib.parse
import http.cookiejar
import gzip
import re
import json

class AsosDEReq():

    def __init__(self):
        self.__cookie = http.cookiejar.CookieJar()
        self.__urlOpener = request.build_opener(request.HTTPCookieProcessor(self.__cookie))

    def getSidebar(self):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate, sdch",
            "Accept-Language":"en-US,en;q=0.8,id;q=0.6,ms;q=0.4",
            "Connection":"keep-alive",
            "Upgrade-Insecure-Requests":1}

        req = request.Request("http://www.asos.de/herren/jacken-mantel/blazer/cat/?cid=11903", headers = headers)

        try:
            res = self.__urlOpener.open(req)
            charset = res.info().get_content_charset()
            html = gzip.decompress(res.read()).decode(charset)
            
            parser = HTMLParser()
            root = parser.feed(html)
            parser.close()

            data = {}

            panelDivs = root.findall(".//div[@class='panel']")
            for panelDiv in panelDivs:
                panel = panelDiv.find("div[@class='panel-content']")
                span = panel.find("a[@class='refinement-header']/h3/span[@class='facet-name']")
                if span != None:
                    if span.text in ("kollektion", "farbe", "grösse", "marke"):
                        data[span.text] = {}
                        panelsOpt = panel.findall("div/ul/li")
                        if len(panelsOpt) != 0:
                            for li in panelsOpt:
                                a = li.find("a")
                                dataName = li.get("data-name")
                                data[span.text][dataName] = {}
                                data[span.text][dataName]["id"] = li.get("data-id")
                                data[span.text][dataName]["href"] = a.get("href")
                                data[span.text][dataName]["count"] = re.sub('[()]', '', a.find("span[@class='count']").text)

                    if span.text == "preisrahmen":
                        data[span.text] = {}
                        data[span.text]['id'] = panelDiv.get("data-id")
                        data[span.text]['min'] = panelDiv.get("data-min")
                        data[span.text]['max'] = panelDiv.get("data-max")
            
        except Exception as e:
            print(e)

        return data

    def getSearchData(self, url, queryString):
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
            "Accept":"application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding":"gzip, deflate, sdch",
            "Accept-Language":"en-US,en;q=0.8,id;q=0.6,ms;q=0.4",
            "Connection":"keep-alive"}

        req = request.Request(url.format(queryString))

        data = {}

        try:
            res = self.__urlOpener.open(req)
            charset = res.info().get_content_charset()
            data = json.loads(res.read().decode(charset))
                
        except Exception as e:
            print(e)

        return data

# test request to asos de
asosReq = AsosDEReq()

# get sidebar data
print("Get sidebar data...")
data = asosReq.getSidebar()
data = json.dumps(data, sort_keys=False, indent=4, separators=(',', ': '))

# write data to file in json format
print("Write sidebar data to json file...")
with open('sidebar.json', 'w') as f:
    f.write(data)
    f.close()
print("Generate sidebar data finished.")

print("===============================")

print("Test request search resutl data...")
# get search data request result
queryString = {
    "currency":"EUR",
    "store":4,
    "lang":"de",
    "rowlength":3,
    "channel":"desktop-web",
    "offset":0,
    "limit":36,
    "refine":"currentprice:145<405",
    "currentpricerange":"35-495"}
data = asosReq.getSearchData("http://searchapi.asos.com/product/search/v1/categories/11903?{}", urllib.parse.urlencode(queryString))
data = json.dumps(data, sort_keys=False, indent=4, separators=(',', ': '))

# write data to file in json format
print("Write search result data to json file...")
with open('searchResultExample.json', 'w') as f:
    f.write(data)
    f.close()
print("Generate search result data finished.")
print("Done!")
