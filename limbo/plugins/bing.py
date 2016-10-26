"""!image <search term> return a random result from the Bing image search result for <search term>"""

try:
    from urllib import quote
except ImportError:
    from urllib.request import quote
import re
import requests
from random import shuffle

def unescape(url):
    # for unclear reasons, google replaces url escapes with \x escapes
    return url.replace(r"\x", "%")

def bimage(searchterm, unsafe=False):
    searchterm = quote(searchterm)

    safe = "&safe=" if unsafe else "&safe=active"
    searchurl = "https://www.bing.com/images/search?q={0}{1}".format(searchterm, safe)

    # this is an old iphone user agent. Seems to make google return good results.
    useragent = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Versio  n/4.0.5 Mobile/8A293 Safari/6531.22.7"

    result = requests.get(searchurl, headers={"User-agent": useragent}).text

    bimages = list(map(unescape, re.findall(r"var u='(.*?)'", result)))
    shuffle(bimages)

    if bimages:
        return bimages[0]
    else:
        return ""

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!bimage (.*)", text)
    if not match:
        return

    searchterm = match[0]
    return bimage(searchterm.encode("utf8"))
