# -*- coding: utf-8 -*-

import bs4 as bs  # text retreival lib
import urllib2
import time
import pandas as pd
import sys
import numpy as np
import xlrd

# headers = { 'User-Agent' : 'Mozilla/5.0' }

# making russian text visible
reload(sys)
sys.setdefaultencoding('utf8')

orgs = pd.read_excel('orgs_clean.xlsx', sheet_name='Sheet1')
orgs['Number of pages'] = orgs['Number of pages'].astype(int)
href = ''

links = []

for row in orgs.iterrows():
    if (row[1]['Number of pages'] == 1):
        href = '' + str(row[1]['Link'])
        links.append(href)
    elif (row[1]['Number of pages'] > 1):
        i = row[1]['Number of pages']
        while i > 1:
            href = '' + str(row[1]['Link']) + '?page=' + str(i)
            links.append(href)
            i = i - 1
        href = '' + str(row[1]['Link'])
        links.append(href)
linkss = pd.Series(links)
print(len(linkss))
print(linkss[30:60])
print(linkss.tail())

linkss.to_csv('data.csv')