from pprint import pprint
import re
import urllib.request

from grab import Grab


# FETCH_IMAGES = True
FETCH_IMAGES = False

LIMIT = 3 # 00
DL_DIR = './_dl/'

BASE_URL = 'https://threehundredbeers.com'
START_PAGE = BASE_URL + '/the-beers'
HOST_FOLDER = '/wp-content/uploads/2022/10/'

g = Grab()
g.go(START_PAGE)

# loop over the beer pages
ctr = 0

beer_urls = g.doc.select('//div[@class="post-content"]/*/li/a')

for url in beer_urls:

    beer_page = BASE_URL + url.attr('href')

    print('Fetching: ', beer_page)

    g.go(beer_page)

    post = {}

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

    # WTF Tumblr?
    body = body.replace('https://href.li/?', '')

    # sort out the images
    imgs = g.doc.select('//div[@class="post-content"]/*/img')
    img_urls = list(elem.attr('src') for elem in imgs)

    for url in img_urls:

        filename = url.split('/').pop()

        # download the file
        if FETCH_IMAGES:
            urllib.request.urlretrieve(url, DL_DIR + filename)

        regexp = re.compile(r'https://(.*)' + filename, re.DOTALL)
        body = regexp.sub(HOST_FOLDER + filename, body)

    post['body'] = body

    pprint(post)

    ctr += 1

    if ctr >= LIMIT:
        break
