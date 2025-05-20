from bs4 import BeautifulSoup
import lxml
### Creating a soup
with open('./three_sisters.html', 'r') as fp:
    soup = BeautifulSoup(fp, 'html.parser')

print(soup.prettify())

# Working with tags
tag = soup.p
print(tag)

tag.attrs
tag.name
tag['class'] = 'THE title'
tag['id'] = 1

del tag['id']
tag['id']

print(tag.get('id'))

# multi-valued attributes
css_soup = BeautifulSoup('<p class = "body"></p>', 'html.parser')
css_soup.p['class']

css_soup = BeautifulSoup('<p class = "body strikeout"></p>', 'html.parser')
css_soup.p['class']

# rel-soup
rel_soup = BeautifulSoup('<p> Back to the<a rel = "index first">homepage</p>', 'html.parser')
rel_soup.a['rel']
# ['index', 'first']

rel_soup.a['rel'] = ['index', 'contents']
print(rel_soup.p)

# not multi-values attribute defined in HTML
id_soup = BeautifulSoup('<p id = "my id"></p>', 'html.parser')
id_soup.p['id']
# 'my id'

id_soup.p.get_attribute_list('id') # always give a list containter
# ['my id']

no_list_soup = BeautifulSoup('<p class="body strikeout"></p>', 'html.parser', multi_valued_attributes = None)
no_list_soup.p['class']
# 'body strikeout'

# XML soup
xml_soup = BeautifulSoup('<p class="body strikeout"></p>', 'xml')
xml_soup.p['class'] # 'body strikeout'
# no multi-valued attrs

### Navigable String
soup = BeautifulSoup('<b class="boldest">Extremely bold</b>', 'html.parser')
tag = soup.b

tag.string # 'Extremely bold'
type(tag.string) # bs4.element.NavigableString

unicode_str = str(tag.string)
unicode_str # 'Extremely bold'
type(unicode_str) # str

# cannot edit but can replace 
tag.string.replace_with('No longer bold') # returns previous string
tag.string # 'No longer bold'

# to use NavigableString outside of bs use unicode()
# else it sill carry reference to the entire bs tree

### Combining parsed docs
doc = BeautifulSoup('<document><content/>INSERT FOOTER HERE</document>', 'xml')
footer = BeautifulSoup('<footer>Here\'s the footer</footer>', 'xml')

doc.find(string = 'INSERT FOOTER HERE').replace_with(footer) # find(text = ) is deprecated, use string
doc
# <?xml version="1.0" encoding="utf-8"?>
# <document><content/><footer>Here's the footer</footer></document>

doc.name # '[document]'
footer.name # '[document]'

# html comments
markup = '<b><!--Hey, buddy. Want to buy a used parser?--></b>'

soup = BeautifulSoup(markup, 'html.parser')
soup.b.string # 'Hey, buddy. Want to buy a used parser?'
type(soup.b.string) # bs4.element.Comment - just a special type of NavigableString

print(soup.b.prettify())
# <b>
#  <!--Hey, buddy. Want to buy a used parser?-->
# </b>

### Navigating the Tree
with open('./three_sisters.html', 'r') as fp:
    soup = BeautifulSoup(fp, 'html.parser')

print(soup.prettify())

soup.find('head')
soup.body.p # <p class="title"><b>The Dormouse's story</b></p>
soup.body.p.b # <b>The Dormouse's story</b>

soup.find_all('p')

## contents and children

head_tag = soup.head
head_tag.contents # [<title>The Dormouse's story</title>]

title_tag = head_tag.contents[0]
title_tag # <title>The Dormouse's story</title>
title_tag.contents # ["The Dormouse's story"]

title_tag.children # <generator object Tag.children.<locals>.<genexpr> at 0x107a2ef80>

for child in title_tag.children:
    print(child)
# The Dormouse's story

# Don't modify the the .contents list directly:
# that can lead to problems that are subtle and difficult to spot.

## descendants

head_tag
for child in head_tag.descendants:
    print(child)
# <title>The Dormouse's story</title>
# The Dormouse's story

len(list(soup.children))

len(list(soup.descendants))

head_tag.contents
head_tag.string # children's string is also parent's string if parent has only one children-tag

# for multiple children-tags of parent string will not work
print(soup.html.string) # None

# use strings generator for this case
for string in soup.strings:
    print(repr(string))

# "The Dormouse's story"
# '\n'
# '\n'
# "The Dormouse's story"
# '\n'
# 'Once upon a time there were three little sisters; and their names were\n'
# 'Elsie'
# ',\n'
# 'Lacie'
# ' and\n'
# 'Tillie'
# ';\nand they lived at the bottom of a well.'
# '\n'
# '...'

# stripped_strings generator to remove whitespaces

for string in soup.stripped_strings:
    print(repr(string))
# "The Dormouse's story"
# "The Dormouse's story"
# 'Once upon a time there were three little sisters; and their names were'
# 'Elsie'
# ','
# 'Lacie'
# 'and'
# 'Tillie'
# ';\nand they lived at the bottom of a well.'
# '...'

# strings consisting entirely of whitespace are ignored,
# and whitespace at the beginning and end of strings is removed.

## Going Up
print(soup.title.parent) # <head><title>The Dormouse's story</title></head>
type(soup.html.parent) # bs4.BeautifulSoup

link = soup.a
link

# parents generator
for parent in link.parents:
    print(parent.name)
    
# self_and_parents generator
for parent in link.self_and_parents:
    print(parent.name)
    
## Going Sideways    
sibling_soup = BeautifulSoup("<a><b>text1</b><c>text2</c></a>", 'html.parser')
print(sibling_soup.prettify()) # b and c tags are siblings(on the same level)

sibling_soup.b.next_sibling # <c>text2</c>
sibling_soup.c.previous_sibling # <b>text1</b>

sibling_soup.b.previous_sibling # None
sibling_soup.c.next_sibling # None

print(soup.prettify())
soup.find_all('a')

link = soup.a
link # <a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>
link.next_sibling # ',\n'
link.next_sibling.next_sibling # <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>

# siblings generators
for sibling in soup.a.next_siblings:
    print(repr(sibling))

for sibling in soup.find(id='link3').previous_siblings:
    print(repr(sibling))

## Going back and Forth 
last_a_tag = soup.find('a', id='link3')
last_a_tag # <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>

last_a_tag.next_sibling # ';\nand they lived at the bottom of a well.'

last_a_tag.next_element # 'Tillie'
last_a_tag.previous_element # ' and\n'

# generator
for element in last_a_tag.next_elements:
    print(repr(element))
# 'Tillie'
# ';\nand they lived at the bottom of a well.'
# '\n'
# <p class="story">...</p>
# '...'