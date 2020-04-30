#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 11:17:11 2018

@author: kerry
"""
global soup
global url
# import libraries
import urllib.request
from bs4 import BeautifulSoup
import csv

# specify the url 内容爬虫
urlpage =  'https://com.tansent.com/'
print(urlpage)
headers = {'User-Agent':'Chrome/81.0.4044.129 Safari/537.36'}
url1 = urllib.request.Request(urlpage,headers=headers)
# query the website and return the html to the variable 'page'
page = urllib.request.urlopen(url1)
# parse the html using beautiful soup and store in variable 'soup'
soup = BeautifulSoup(page, 'html.parser')
# find results within table
table = soup.find_all('div', attrs={'class': 'regionright'})
results = table[1].find_all('ul')
print('Number of results', len(results))

# create and write headers to a list 
rows = []
rows.append(['city', 'cname', 'lx'])

# loop over results
for result in results:
    # find all columns per result
    data = result.find_all('li')
    print('Number of result', len(result))
    print('Number of data', len(data))
    i=1
    while i<len(data):
        atmp=data[i].find_all('a')
        j=0
        url = 'https://com.tansent.com' + atmp[j].get('href')
        print(atmp[j])
        url1 = urllib.request.Request(url, headers=headers)
        page = urllib.request.urlopen(url1, timeout=15)
        soup = BeautifulSoup(page, 'html.parser')

        while j<len(atmp):
            url = 'https://com.tansent.com' + atmp[j].get('href')
            url1 = urllib.request.Request(url, headers=headers)
            page = urllib.request.urlopen(url1, timeout=15)
            soup = BeautifulSoup(page, 'html.parser')

            city = atmp[j].text

            # print(nextPage)
            while 1==1:
                url1 = urllib.request.Request(url, headers=headers)
                page = urllib.request.urlopen(url1, timeout=15)
                soup = BeautifulSoup(page, 'html.parser')

                divbody = soup.find('div', attrs={'id': 's_list'})
                divall = divbody.find_all('div', attrs={'class': 'list_bd'})

                for divm in divall:
                    cname = (divm.find('a', attrs={'class': 'com_lk'})).text
                    lx = (divm).find('div', attrs={'class': 'lx'}).text
                    rows.append([city, cname, lx])
                    print(city + ':' + cname + ':' + lx)


                # 获取下一页
                table = soup.find('table')

                nonextPage = (table.find('span', attrs={'class': 'next_nopage'}))
                nextPage = (table.find('a', attrs={'class': 'next_page'}))

                print(nonextPage)

                if nonextPage is not None or nextPage is None:
                    if nextPage is None:
                        print('nextPage is None'+url)
                        break
                    url = 'https://com.tansent.com' + atmp[j].get('href')
                    print(url)

                    break
                else:
                    url = 'https://com.tansent.com' + nextPage.get('href')
                    print('获取下一页' + url)


            j=j+1
            # break

        i=i+2
        # break



print(rows)

    
## Create csv and write rows to output file
with open('techtrack100.csv','w',encoding='utf-8', newline='') as f_output:
    csv_output = csv.writer(f_output)
    csv_output.writerows(rows)