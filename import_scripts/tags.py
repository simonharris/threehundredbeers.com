import urllib.request
from lxml import etree
from pprint import pprint


SITE_URL = 'https://threehundredbeers.com/'

with urllib.request.urlopen(SITE_URL) as response:
    html = response.read()

    tree = etree.HTML(html)


    #/*/*/event[contains(@description, ' doubles ')]
    tagtree = tree.xpath("//li/a[contains(@href, 'tagged')]")

    taglist = [elem.text for elem in tagtree]
    pprint(taglist)


