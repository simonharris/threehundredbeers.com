from pprint import pprint
import re

from grab import Grab

LIMIT = 1


ctr = 0

# TODO: spider the website
filename = 'https://threehundredbeers.com/post/153053521719/mighty-oak-oscar-wilde'


post = {}

g = Grab()
g.go(filename)

# title
post['title'] = g.doc.select('//title')[0].text()

# tags
tags = g.doc.select('//div[@class="tags"]/p/a')
post['tags'] = list(elem.text() for elem in tags)

# sort out the body
body = g.doc.select('//div[@class="post-content"]')[0].html()

regexp = re.compile(r'\<div class="tags"\>(.*?)\</div\>', re.DOTALL)
body = regexp.sub('', body, )

regexp = re.compile(r'\<h3>(.*?)\</h3>', re.DOTALL)
body = regexp.sub('', body, 1)

# TODO: figure out how to resolve the URL references


post['body'] = body

pprint(post)

# print(post['body'])


#    ctr += 1

#    if ctr >= LIMIT:
#        break

