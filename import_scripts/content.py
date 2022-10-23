from dateutil.parser import parse
# from pprint import pprint
import re
import urllib.request

from grab import Grab

# Run-specific config
# FETCH_IMAGES = True
FETCH_IMAGES = False
LIMIT = 300


# SQL templates
SQL_MAIN = """INSERT INTO 3cbposts VALUES(
    NULL,
    1,
    '{post_date}',
    '{post_date}',
    '{post_content}',
    '{post_title}',
    '',
    'publish',
    'open',
    'open',
    '',
    '{post_name}',
    '',
    '',
    '{post_date}',
    '{post_date}',
    '',
    0,
    '{post_name}',
    0,
    'post',
    '',
    0
);\n"""

# SQL_SETVAR = 'SET @liid=last_insert_id()\n'

SQL_ADD_TAG = """INSERT INTO 3cbterm_relationships VALUES (
    last_insert_id(),
    (SELECT term_taxonomy_id FROM 3cbterm_taxonomy WHERE term_id =
         (SELECT term_id FROM 3cbterms WHERE name='{tag_name}')
     ),
    0
); \n"""

SQL_ADD_CAT = """INSERT INTO 3cbterm_relationships VALUES (
    last_insert_id(),
    7,
    0
); \n"""


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

    #print('Fetching: ', beer_page)

    g.go(beer_page)

    post = {}

    # slug
    post['post_name'] = beer_page.split('/').pop()

    # title
    post['title'] = g.doc.select('//title')[0].text()

    # reformat publishing date
    pub_date = g.doc.select('//div[@class="date"]')[0].text()
    post['post_date'] = parse(pub_date).strftime('%Y-%m-%d')

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

        ### POSSIBLY A BUG HERE
        regexp = re.compile(r'https://(.*)' + filename, re.DOTALL)
        body = regexp.sub(HOST_FOLDER + filename, body)

    # body should be built by now
    post['body'] = body
    # post['body'] = 'hello again, world'


    # pprint(post)

    sql = SQL_MAIN.format(
            post_date = post['post_date'],
            post_content = post['body'].replace('"','\\"').replace("'","\\'")   ,
            post_title = post['title'].replace("'","\\'"),
            post_name = post['post_name']
        )

    # sql = sql + SQL_SETVAR

    # add tags
    for tag in post['tags']:
        sql = sql+ SQL_ADD_TAG.format(tag_name=tag)

    sql = sql + SQL_ADD_CAT

    print(sql)


    # break if necessary
    ctr += 1

    if ctr >= LIMIT:
        break
