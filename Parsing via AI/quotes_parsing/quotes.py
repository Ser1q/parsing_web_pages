from bs4 import BeautifulSoup
import requests
# import html5lib 
import csv

# getting raw html
URL = 'https://www.passiton.com/inspirational-quotes'
r = requests.get(URL)
print(r.content)

# for errors like Not Accepted we need to create User Agent
# can be found here https://deviceatlas.com/blog/list-of-user-agent-strings
# headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
# Here the user agent is for Edge browser on w

# pretty html
soup = BeautifulSoup(r.content, 'html5lib')
print(soup.prettify())

# finding div that contains all quotes
all_quotes = soup.find('div', attrs={'class':'row', 'id':'all_quotes'})
quotes = []

# iterating over div and getting all the quotes on the page 
for row in all_quotes.find_all_next('div', 'col-6 col-lg-3 text-center margin-30px-bottom sm-margin-30px-top'):
    quote = {}
    quote['theme'] = row.h5.text
    quote['url'] = row.a['href']
    quote['text'] = row.img['alt'].split(' #')[0]
    quote['author'] = row.img['alt'].split(' #')[1]
    quote['img'] = row.img['src']
    quotes.append(quote)

# saving it all in csv
file_name = 'inspirational_quotes.csv'

with open(file_name, 'w', newline='') as f:
    w = csv.DictWriter(f, ['theme', 'url', 'img', 'text', 'author'])
    w.writeheader()
    for quote in quotes:
        w.writerow(quote)