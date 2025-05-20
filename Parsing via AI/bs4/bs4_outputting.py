from bs4 import BeautifulSoup

# pretty printing
with open('./three_sisters.html', 'r') as fp:
    soup = BeautifulSoup(fp, 'html.parser')
    
print(soup.prettify()) # used only to get the idead of html 
print(soup.a.prettify()) # can be called into separate tags

# non-pretty printing
str(soup) # to output just a string
# returns a string encoded in UTF-8

# output formatters 
soup = BeautifulSoup("&ldquo;Dammit!&rdquo; he said.", 'html.parser')
str(soup) # html entities are converted 
