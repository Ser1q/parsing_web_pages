from bs4 import BeautifulSoup, NavigableString
import re

with open('../bs4/three_sisters.html', 'r') as fp:
    soup = BeautifulSoup(fp, 'html.parser')

print(soup.prettify())

# Filters
soup.find_all('b') # finds tags b

# Regular expressions

for tag in soup.find_all(re.compile('^b')): # starts with b
    print(tag.name)
# body
# b

for tag in soup.find_all(re.compile('l')): # contains l
    print(tag.name)
# html
# title

for tag in soup.find_all(True): # finds all tags
    print(tag.name)
# html
# head
# title
# body
# p
# b
# p
# a
# a
# a
# p

# own functions for filtering by tag
def has_class_but_no_id(tag):
    return tag.has_attr('class') and not tag.has_attr('id')

soup.find_all(has_class_but_no_id)


def surrounded_by_strings(tag):
    return (isinstance(tag.next_element, NavigableString) and isinstance(tag.previous_element, NavigableString))

for tag in soup.find_all(surrounded_by_strings):
    print(tag.name)
    
# list 
soup.find_all(['a','b'])
# [<b>The Dormouse's story</b>,
#  <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]


# find_all(name, attrs, recursive, string, limit, **kwargs)
soup.find_all(href = re.compile('elsie')) 
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]

soup.find_all(id = True) # all tags with id
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

# functions to filter by attribute

def no_lacie(href):
    return href and not re.compile('lacie').search(href)

soup.find_all(href = no_lacie)

soup.find_all(id = ['link1', re.compile('3$')])
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

soup.find_all(href = re.compile('elsie'), id = 'link1')
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]

# some keywords cannot be used in find_all
# we enter them as dict then

data_soup = BeautifulSoup('<div data-foo="value">foo!</div>', 'html.parser')
# data_soup.find_all(data-foo = 'value') error

data_soup.find_all(attrs={'data-foo': 'value'}) # [<div data-foo="value">foo!</div>]

# CSS classes
soup
soup.find_all('a', class_ = 'sister') # cannot use class, but we have class_
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

soup.find_all(class_ = re.compile('itl'))
#[<p class="title"><b>The Dormouse's story</b></p>]

def six_figures_class(css_class):
    return css_class is not None and len(css_class) == 6

soup.find_all(class_ = six_figures_class)
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

# single tag can have multiple values for class
# filter searches for any value of its class that matches
css_soup = BeautifulSoup('<p class="body strikeout"></p>', 'html.parser')

css_soup.find_all(class_ = 'body')
css_soup.find_all(class_ = 'strikeout')
# [<p class="body strikeout"></p>] for both

# can search for exact string value
css_soup.find_all(class_ = 'body strikeout')
# [<p class="body strikeout"></p>]

# switching will not work
css_soup.find_all("p", class_="strikeout body")
# []

# to search for tags that match two or more classes at once use tag.select
css_soup.select('p.strikeout.body')
# [<p class="body strikeout"></p>]

# string - looks for texts 
soup.find_all(string = re.compile('Dormouse'))
# ["The Dormouse's story", "The Dormouse's story"]

soup.find_all(string = 'Elsie') # ['Elsie']
soup.find_all(string = ['Elsie', 'Lacie', 'Tillie']) # ['Elsie', 'Lacie', 'Tillie']

def only_child_string(s):
    return (s == s.parent.string)

soup.find_all(string = only_child_string)
# ["The Dormouse's story",
#  "The Dormouse's story",
#  'Elsie',
#  'Lacie',
#  'Tillie',
#  '...']

soup.find_all('a', string = 'Elsie')
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]

# limit
soup.find_all('a', limit = 2)
# [<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
#  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>]

soup.html.find_all('title')
# [<title>The Dormouse's story</title>]

# we can look only for the direct childs with recursice = False
soup.html.find_all('title', recursive = False)
# [] since:
# <html>
#  <head>
#   <title>
#    The Dormouse's story
#   </title>
#  </head>
# ...

# find gives only the first tag

# find_all returns empty list for not found tag
# find returns None in that case

# find_parent and find_parents works like find and find_all, just backwards
a_string = soup.find(string = 'Lacie')
a_string

a_string.find_parent()
# <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>

a_string.find_parents('a')
# [<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>]

a_string.find_parent('p')
# <p class="story">Once upon a time there were three little sisters; and their names were
# <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
# <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and
# <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>;
# and they lived at the bottom of a well.</p>

# finding siblings
soup.a.find_next_siblings()
# [<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]

first_para = soup.find('p', 'story')
print(first_para)

first_para.find_next_sibling('p')
# <p class="story">...</p>

last_link = soup.find('a', id = 'link3')
last_link

last_link.find_previous_siblings('a')
# [<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]

first_story_para = soup.find('p', 'story')
first_story_para

first_story_para.find_previous_sibling('p')
# <p class="title"><b>The Dormouse's story</b></p>

# find_next and find_all_next
first_link = soup.a
first_link.find_all_next(string = True)
# ['Elsie',
#  ',\n',
#  'Lacie',
#  ' and\n',
#  'Tillie',
#  ';\nand they lived at the bottom of a well.',
#  '\n',
#  '...']

first_link.find_next('p')
# <p class="story">...</p>

# find_all_previous and find_previous
first_link

first_link.find_all_previous('p')
first_link.find_previous('title')
