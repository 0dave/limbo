"""!search <query> will return the randon bing image result for that query (!bing is an alias)"""

try:
    from urllib import quote
except ImportError:
    from urllib.request import quote
import re
import requests
from random import shuffle


def unescape(url):
    # for unclear reasons, bing replaces url escapes with \x escapes
    return url.replace(r"\x", "%")

def bing(query):
    query = quote(query)
    
    url = "https://www.bing.com/images/search?q={}&FORM=HDRSC2".format(query)
    
    # this is an old iphone user agent. Seems to make bing return good results.
    useragent = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Versio  n/4.0.5 Mobile/8A293 Safari/6531.22.7"

    result = requests.get(url, headers={"User-agent": useragent}).text

    bings = list(map(unescape, re.findall(r"var u='(.*?)'", result)))
    shuffle(bings)

    if bings:
        return bings[0]
    else:
        return ""

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!(?:bing|search) (.*)", text)
    if not match:
        return

    
    query = match[0]
    return bing(query.encode("utf8"))
