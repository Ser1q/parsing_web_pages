from bs4 import BeautifulSoup

with open('./three_sisters.html', 'r') as fp:
    soup = BeautifulSoup(fp, 'html.parser')

print(soup.prettify())

# find tags by name
soup.css.select('title') # [<title>The Dormouse's story</title>]
soup.css.select('p:nth-of-type(3)') # 3rd sibling

# find tags by id
soup.css.select('#link1')
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]

soup.css.select('a#link3')
# [<a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

# tags contained anywhere inside of other tags
soup.css.select('body a')
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

soup.css.select('html head title')
# [<title>The Dormouse's story</title>]

# find tags directly within other tags(like direct childs)
soup.css.select('body > p')

soup.css.select('p > a')

soup.css.select('p > a:nth-of-type(3)')

soup.css.select('body > a')

# find matching next siblings 
soup.css.select('#link1 ~ .sister')
# [<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

# find the next sibling tag, but only if it matches
soup.css.select('#link1 + .sister')

# find by classes
soup.css.select('.sister')

# find by attributes
soup.css.select('[class ~= title] ') # here we still use class attribute

# find tags that match any selector from list of selectors
soup.css.select('#link1,#link3')
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

# tags with certain attribute
soup.css.select('a[href]')

# selects first 
soup.css.select_one('[href]')

# also can directly call to bs
soup.select('.title')

soup.select('[class]')

# Soup Sieve features
# iselect -r returns a generator instead of a list from select
[tag['id'] for tag in soup.css.iselect('.sister')]
# ['link1', 'link2', 'link3']

elsie = soup.select_one('.sister')
elsie

elsie.css.closest('p.story') # finds closest parent that matches css selector

# match returns True or False, depending on css selector
elsie.css.match('#link1') # True
elsie.css.match('#link3') # False

# filter returns a subset of a tag's direct children, that match css selector
[tag.string for tag in soup.find('p', 'story').css.filter('a')]
# ['Elsie', 'Lacie', 'Tillie']

# The escape() method escapes CSS identifiers that would otherwise be invalid:

soup.css.escape("1-strange-identifier")
# '\\31 -strange-identifier'