import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import json
import csv
didchange = "n"
optionChose = "0"
pageRange = 500
minPrice = 0
maxPrice = 999999999
starzItem = "anything"


# input search name
print("what you whant to search: ")
searchInput = input()
filename = 'amazon-'+searchInput
filecsv = open(filename+'.csv', 'w', encoding='utf8')
# Set the URL you want to webscrape from
url = 'https://www.amazon.sa/s?k='+searchInput + \
    '&i=toys&rh=n%3A12463618031&dc&crid=2J8D038E4V5IH&qid=1608914391&rnid=17120842031&sprefix=gund%2Caps%2C236&ref=sr_pg_3&page='
print("we will search in ***\n " + url+"\n *** URL")
file = open(filename+'.json', 'w', encoding='utf8')
file.write('[\n')
data = {}
csv_columns = ['name', 'price', 'img']

print("\ndid you whant to change options")
didchange = input()
# change options
while didchange == "y" or didchange == "Y":

    print("chose option(0 to see all options): ")
    optionChose = input()
    print(optionChose)
    print(optionChose == "1")
    if optionChose == "0":  # print all options

        print("1: values of options")
        print("2: change range pages for search")
        print("2: change max and minimum price for items")
    elif optionChose == "1":
        print("options".center(50, "-"))
        # range page
        print("range of pages: "+str(pageRange))
        # default price, min - max
        print("minimum price "+str(minPrice))
        print("maximum price "+str(maxPrice))

        # satrz
        print("satrz " + starzItem)

    elif optionChose == "2":
        print("the new range for pages to search")
        pageRange = int(input())
    elif optionChose == "3":
        print("the new maximum and minimum price")
        print("max parice")
        maxPrice = int(input())
        print("minimum parice")
        minPrice = int(input())

    else:
        print("you chose wrong number chose \"0\" to see all methonds")
    print("did you whant to continue change[y/n]")
    didchange = input()

for page in range(pageRange):
    print('---', page, '---')
    r = requests.get(url + str(page))
    print(url + str(page))
    soup = BeautifulSoup(r.content, "html.parser")
    ancher = soup.find_all('div', {
                           'class': 'sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col sg-col-4-of-20'})
    writer = csv.DictWriter(filecsv, fieldnames=csv_columns)
    i = 0
    writer.writeheader()

    for pt in ancher:

        name = pt.find(
            'span', {'class': 'a-size-base-plus a-color-base a-text-normal'})
        itemPrice = pt.find('span', {'class': 'a-price-whole'})
        img = pt.find('img', {'class': 's-image'})
        print('name => ', name.text)
        # print('price => ', itemPrice.text)
        # print('img => ', img.get('src'))

        if img and itemPrice:
            writer.writerow({'name': name.text.replace('                    ', '').strip(
                '\r\n'), 'price': itemPrice.text, 'img': img.get('src')})
            data['name'] = name.text.replace(
                '                    ', '').strip('\r\n')
            data['price'] = itemPrice.text
            data['img'] = img.get('src')
            json_data = json.dumps(data, ensure_ascii=False)
            file.write(json_data)
            file.write(",\n")
file.write("\n]")
filecsv.close()
file.close()
