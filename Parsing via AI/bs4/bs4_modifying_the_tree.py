from bs4 import BeautifulSoup, NavigableString, Comment

markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
soup = BeautifulSoup(markup, 'html.parser')

tag = soup.a
print(tag.get_text())

# we can replace text in tag, but it completely deletes all the stuff in it
tag.string = 'Completely new string'
tag

soup = BeautifulSoup("<a>Foo</a>", 'html.parser')

new_string = soup.a.append('Boo') # returns appended element
soup.contents
new_string

# extend - adds every element in a list to the tag
soup = BeautifulSoup("<a>Soup</a>", 'html.parser')

soup.a.extend(['\'s', ' ', 'on'])

soup
soup.a.contents

# can add several strings with NavigableString constructor
soup = BeautifulSoup("<b></b>", 'html.parser')

tag = soup.b
tag.append('Hello ')
new_string = NavigableString('there')
tag.append(new_string)

tag

# to create some Comment or other subclass of NavigableString, just call constructor
new_comment = Comment('Nice to see you!!')
tag.append(new_comment)
tag

# creating new tag
soup = BeautifulSoup("<b></b>", 'html.parser')
original_tag = soup.b

new_tag = soup.new_tag('a', href = 'http://www.example.com', string = 'New tag link') 
new_tag # tag is created from scratch and does not alter the original tag

original_tag.append(new_tag)
original_tag 
# <b><a href="http://www.example.com">New tag link</a></b>

soup # original_tag references to soup

# insertiong can be done in one line

soup = BeautifulSoup('<html></html>', 'html.parser')
html = soup.html
new_tag = html.append(soup.new_tag('title', string='Hello there!'))

soup # <html><title>Hello there!</title></html>

# insert 
markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
soup = BeautifulSoup(markup, 'html.parser')

tag = soup.a
new_string = tag.insert(1, 'but did not indorse') # can enter several items within a list

tag
tag.contents
# ['I linked to ', 'but did not indorse', <i>example.com</i>]
new_string # returns list of inserted elements

# insert before and after
# insert before inserts tg or string before something that we indicated

soup = BeautifulSoup("<b>leave</b>", 'html.parser')
tag = soup.new_tag('i', string='Don\'t')
soup.b.string.insert_before(tag) # [<i>Don't</i>]
soup # <b><i>Don't</i>leave</b>

# The insert_after() method inserts tags or strings 
# immediately after something else in the parse tree:
div = soup.new_tag('div', string='ever')
soup.b.i.insert_after('you', div)

soup # <b><i>Don't</i>you<div>ever</div>leave</b>

# Both methods return the list of newly inserted elements.

# clear
markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
soup = BeautifulSoup(markup, 'html.parser')

tag = soup.a
tag
tag.clear() # removes contents of a tag 
tag # <a href="http://example.com/"></a>8

# PageElement.extract()
# removes a tag or string from the tree. It returns the tag or string that was extracted:
markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
soup = BeautifulSoup(markup, 'html.parser')

a_tag = soup.a
i_tag = soup.i.extract()

a_tag # <a href="http://example.com/">I linked to </a>
i_tag # <i>example.com</i>

print(i_tag.parent) # None

# Tag.decompose() 
# removes a tag from the tree, then completely destroys it and its contents:
markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
soup = BeautifulSoup(markup, 'html.parser')

a_tag = soup.a
i_tag = soup.i

i_tag.decompose() # dont use decomposed tag for anything
a_tag # <a href="http://example.com/">I linked to </a>

i_tag.decomposed # True
a_tag.decomposed # False

# PageElement.replace_with() 
# extracts a tag or string from the tree, 
# then replaces it with one or more tags or strings of your choice
markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
soup = BeautifulSoup(markup, 'html.parser')

a_tag = soup.a 
a_tag # <a href="http://example.com/">I linked to <i>example.com</i></a>

b_tag = soup.new_tag('b', string='example.com')
a_tag.i.replace_with(b_tag)
a_tag # <a href="http://example.com/">I linked to <b>example.com</b></a>

bold_tag = soup.new_tag('b', string='example')
i_tag = soup.new_tag('i', string='net')

a_tag.b.replace_with(bold_tag, '.', i_tag)
a_tag # <a href="http://example.com/">I linked to <b>example</b>.<i>net</i></a>

# wrap
soup = BeautifulSoup('<p>I wish I was bold.</p>', 'html.parser')
soup # <p>I wish I was bold.</p>

soup.p.string.wrap(soup.new_tag('b')) # we wrapped string in the tag
soup # <p><b>I wish I was bold.</b></p>

soup.p.wrap(soup.new_tag('div')) # we wrapped tag itself
soup # <div><p><b>I wish I was bold.</b></p></div>

# Tag.unwrap() is the opposite of wrap(). 
# It replaces a tag with whatever's inside that tag. It's good for stripping out markup

markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
soup = BeautifulSoup(markup, 'html.parser')
a_tag = soup.a

a_tag.i.unwrap()
a_tag
# <a href="http://example.com/">I linked to example.com</a>

# smooth()

soup = BeautifulSoup("<p>A one</p>", 'html.parser')
soup.p.append(", a two")

soup.p.contents
# ['A one', ', a two']

print(soup.p.encode())
# b'<p>A one, a two</p>'

print(soup.p.prettify())
# <p>
#  A one
#  , a two
# </p>

# You can call Tag.smooth()
# to clean up the parse tree by consolidating adjacent strings:

soup.smooth()

soup.p.contents
# ['A one, a two']

print(soup.p.prettify())
# <p>
#  A one, a two
# </p>