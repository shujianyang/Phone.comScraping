import requests
from bs4 import BeautifulSoup
import re
import json

crefile = open('credential.json', 'r')
credential = json.load(crefile)
crefile.close()

s = requests.Session()
r = s.post("https://control.phone.com/login",
    data=credential)
#print(r.text)

soup = BeautifulSoup(r.text, 'html.parser')
#print(soup.title)
add_num = soup.find(href=re.compile('add_number'))

add_num_link = 'https://control.phone.com' + add_num['href']
#print(add_num_link)

r = s.post(add_num_link, data={'action:intl_simple':'intl_simple', 'country':'CA', '_prior_action:0':'intl'})
page = r.text

soup = BeautifulSoup(page, 'html.parser')
city_list = soup.find_all(href=re.compile('did_city'))

phone_list = []
num_count = 0
for loc in city_list:
    location = loc.string
    loc_link = loc['href']
    print("Scraping phone numbers in: " + location)

    check_loc_link = 'https://control.phone.com/voip/add_number' + loc_link
    r = s.get(check_loc_link)

    num_list = []
    soup = BeautifulSoup(r.text, 'html.parser')
    result = soup.find_all('label', {'for':re.compile('inventory_id')})
    for num in result:
        num_list.append(num.string)
    
    entry = location, num_list
    phone_list.append(entry)
    print("Finish scraping numbers in: " + location)
    print("Number count:", len(num_list))
    num_count = num_count + len(num_list)

print()
print("Total cities count: ", len(phone_list))
print("Total numbers count: ", num_count)
print()

print("Exporting to file...")
output = open('PhoneNumList.txt', 'w')
for loc, nums in phone_list:
    output.write(loc)
    output.write('\n')
    for n in nums:
        output.write(n)
        output.write('\n')
    output.write('\n')
print("Finish exporting.")
output.close()

outjson = open('PhoneNumsCan.json', 'w')
outjson.write(json.dumps(phone_list, indent=4))
outjson.close()

print('All numbers scraped.')
