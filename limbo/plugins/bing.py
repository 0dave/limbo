"""!search <query> will return the top bing result for that query (!bing is an alias)"""
from bs4 import BeautifulSoup
import re
try:
    from urllib import quote, unquote
except ImportError:
    from urllib.request import quote, unquote
import requests


def bing(q):
    query = quote(q)
    url = "https://www.bing.com/search?q={0}".format(query)
    soup = BeautifulSoup(requests.get(url).text, "html5lib")

    answer = soup.findAll("a", attrs={"class": "image"})
    if not answer:
        return ":crying_cat_face: Sorry, bing doesn't have an answer for you :crying_cat_face:"

    try:
        return unquote(re.findall(r"q=(.*?)&", str(answer[0]))[0])
    except IndexError:
        # in this case there is a first answer without a link, which is a
        # bing response! Let's grab it and display it to the user.
        return ' '.join(answer[0].stripped_strings)

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!(?:bing|search) (.*)", text)
    if not match:
        return

    return bing(match[0])
