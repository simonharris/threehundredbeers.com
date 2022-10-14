import urllib.request
from lxml import etree
# from pprint import pprint


SITE_URL = 'https://threehundredbeers.com/'

with urllib.request.urlopen(SITE_URL) as response:
    html = response.read()

    tree = etree.HTML(html)

    tagtree = tree.xpath("//li/a[contains(@href, 'tagged')]/@href")

    taglist = [elem.replace('/tagged/', '') for elem in tagtree]
    # pprint(taglist)

    with open(r'./tags.txt', 'w') as fp:
        for item in taglist:

            fp.write("%s\n" % item)

        print('Done')
