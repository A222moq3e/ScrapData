import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import json
import csv
# options default value
didchange = "n"
optionChose = "0"
pageRange = 500
minPrice = 0
maxPrice = 999999999
# not in filter right now
starzItem = "anything"

# the creat class items


class Items:
    def __init__(self):
        self.type = "item"


class Methods:
    def __init__(self):
        self.type = "types"
        self.pageRange = 500
        self.minPrice = 0
        self.maxPrice = 99 ** 5
        self.starzItem = "anything"

    def method1_PrintMethonds(self):
        print("1: values of options")
        print("2: change range pages for search")
        print("2: change max and minimum price for items")

    def method2_PrintNowValues(self):
        #  print("options".center(50, "-"))
        # range page
        print("range of pages: ", str(self.pageRange))
        # default price, min - max
        print("minimum price "+str(self.minPrice))
        print("maximum price "+str(self.maxPrice))
        # satrz
        print("satrz " + self.starzItem)
        # print("hi")

    def method3_NewRangePage(self, newRange):
        self.pageRange = newRange
        print("The new range is : ", self.pageRange)

    def method4_NewMaxAndMinimum(self, newMax, newMin):
        self.maxPrice = newMax
        self.minPrice = newMin
        print("the new max price is: ", self.maxPrice)
        print("the new min price is: ", self.minPrice)


MyMethods = Methods()


# input search name
print("what you whant to search: ")
searchInput = input()
filename = 'amazon-'+searchInput

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
        MyMethods.method1_PrintMethonds()
    elif optionChose == "1":
        MyMethods.method2_PrintNowValues()

    elif optionChose == "2":
        print("the old range page: ", MyMethods.pageRange)
        print("the new range for pages to search: ")
        pageRange = int(input())
        MyMethods.method3_NewRangePage(pageRange)

    elif optionChose == "3":
        print("the new maximum and minimum price")
        print("max parice")
        maxPrice = int(input())
        print("minimum parice")
        minPrice = int(input())
        MyMethods.method4_NewMaxAndMinimum(maxPrice, minPrice)

    elif optionChose == "99" or optionChose == "exit":
        print("did you finish[y/n]? ")
        didchange = input()

    else:
        print("you chose wrong number chose \"0\" to see all methonds or 99 for exit")


for page in range(MyMethods.pageRange):
    print('---', page, '---')
    r = requests.get(url + str(page))
    print(url + str(page))
    soup = BeautifulSoup(r.content, "html.parser")
    ancher = soup.find_all('div', {
                           'class': 'sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col sg-col-4-of-20'})

    i = 0

    for pt in ancher:

        name = pt.find(
            'span', {'class': 'a-size-base-plus a-color-base a-text-normal'})
        itemPrice = pt.find('span', {'class': 'a-price-whole'})
        img = pt.find('img', {'class': 's-image'})
        print('name => ', name.text)
        # print('price => ', itemPrice.text)

        if img and itemPrice:
            ip = itemPrice.text.split('.')
            ip_2 = ip[0].split(',')
            # print("range index for ip2 => ", len(ip_2))
            if len(ip_2) > 1:
                ip_2_sum = ip_2[0] + ip_2[1]
            else:
                ip_2_sum = ip[0]

            # print(ip[0])
            # print("ip_2_sum = ", ip_2_sum)
            # print('img => ', img.get('src'))
            if int(ip_2_sum) > MyMethods.minPrice and int(ip_2_sum) < MyMethods.maxPrice:

                data['name'] = name.text.replace(
                    '                    ', '').strip('\r\n')
                data['price'] = itemPrice.text
                # print('price == ', data['price'])
                data['img'] = img.get('src')
                json_data = json.dumps(data, ensure_ascii=False)
                file.write(json_data)
                file.write(",\n")
file.write("\n]")

file.close()


# قمت بحذف filecsv
