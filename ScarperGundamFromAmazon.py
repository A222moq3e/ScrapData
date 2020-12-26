import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import json
import csv
filecsv = open('SouqDataapple.csv', 'w', encoding='utf8')
# Set the URL you want to webscrape from
url = 'https://www.amazon.sa/s?k=gundam&i=toys&rh=n%3A12463618031&dc&crid=2J8D038E4V5IH&qid=1608914391&rnid=17120842031&sprefix=gund%2Caps%2C236&ref=sr_pg_3&page='
file = open('amzonGundam.json', 'w', encoding='utf8')
file.write('[\n')
data = {}
csv_columns = ['name', 'price', 'img']
for page in range(1000):
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
