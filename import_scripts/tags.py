import urllib.request
from lxml import etree


SITE_URL = 'https://threehundredbeers.com/'

with urllib.request.urlopen(SITE_URL) as response:
    html = response.read()

    tree = etree.HTML(html)

    tagtree = tree.xpath("//li/a[contains(@href, 'tagged')]/@href")

    taglist = [elem.replace('/tagged/', '') for elem in tagtree]

    with open('./tags.sql', 'w') as fp:
        for item in taglist:

            slug = item.lower()
            tagtext = item.replace('-', ' ')

            sql = "INSERT INTO 3cbtags VALUES (NULL,'{a}','{b}',NULL)".format(a = tagtext, b = slug)

            #print(entry)

            fp.write("%s\n" % sql)

        print('Done')
