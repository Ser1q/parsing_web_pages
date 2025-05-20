from bs4 import BeautifulSoup
import requests
import csv

# getting raw html
URL = 'https://codewithsadee.github.io/realvine/'
r = requests.get(URL)
print(r.content)

# creating soup
soup = BeautifulSoup(r.content, 'html5lib')
print(soup.prettify())

property_list = soup.find('ul', 'property-list')
print(property_list.prettify())

houses_list = []

for property in property_list.find_all('li', class_=False):
    house = {}
    house_main_info = property.find_all('li', 'card-item') # converting into list with main info
    
    house['img'] = URL + property.img['src'][2:] # concat with main url
    house['address'] = property.find('a', 'card-title').text
    
    house['area(sqf)'] = house_main_info[0].span.text.split('s')[0] # getting size without sqf
    # house['area(sqf)'] = house_main_info[0].span.text[:-3] # getting size without sqf
    house['num_of_beds'] = house_main_info[1].span.text[:-5] # getting number without word "beds"
    house['num_of_baths'] = house_main_info[2].span.text[:-6] # getting number without word "baths"
    
    price_and_rating_data = property.find('span', 'meta-text') # getting span with both price and rating within
    
    house['price($)'] = price_and_rating_data.text[1:] # retrieving price without "$" sign
    house['rating'] = price_and_rating_data.find_next('span', 'meta-text').span.text.split('(')[0] # rating only
    house['rating_number'] = price_and_rating_data.find_next('span', 'meta-text').span.text[-3:-1] # number of rating responses
    houses_list.append(house)
    
# saving in csv
file_name = './houses.csv'

with open(file_name, 'w', newline='') as f:
    w = csv.DictWriter(f, ['img', 'address', 'area(sqf)', 'num_of_beds', 'num_of_baths', 'price($)', 'rating', 'rating_number'])
    w.writeheader()
    for house in houses_list:
        w.writerow(house)
