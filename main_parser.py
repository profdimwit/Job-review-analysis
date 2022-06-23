# -*- coding: utf-8 -*-

import bs4 as bs  # text retreival lib
import urllib2
import time
import pandas as pd
import sys
import numpy as np
import re

headers = { 'User-Agent' : 'Mozilla/5.0' }

# making russian text visible
reload(sys)
sys.setdefaultencoding('utf8')

# reading links and putting them into a pd.Series
with open('data_norm.csv') as f:
    content = f.readlines()
content = pd.Series([x.strip() for x in content])

# initiating variables for further needs
df2 = pd.DataFrame()
i = 0
# interate over all links in "content" Series
for link in content:

    href = 'https://otrude.net' + str(link)
    try:
        request = urllib2.Request(href, None, headers)
        sause = urllib2.urlopen(request).read()
        soup = bs.BeautifulSoup(sause, 'html.parser')

        stars = pd.Series(soup.find_all('div', class_='review-recommend-row')) # данные об оценке (необходимо вручную подчистить)
        if not stars.empty:
            print(str(i), '/', len(content), href)
        else:
            print(str(i), '/', len(content), 'Ciphered')

        date = pd.Series(elem.text for elem in soup.find_all('div', class_='review-title date'))
        place = pd.Series(elem.text for elem in soup.find_all('span', class_='review-data place'))
        tenure = pd.Series(elem.text for elem in soup.find_all('span', class_=re.compile('review-data person')))
        position = pd.Series(elem.text for elem in soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['review-title']))
        body = pd.Series(elem.text.strip() for elem in soup.find_all('div', class_='review-body')) # вручную разделить на плюсы и минусы
        if not body.empty:
            body = body.replace('\r\n+|\r|\n', ' ', regex=True)
        plus = pd.Series(elem.text for elem in soup.find_all('span', class_='plus'))
        minus = pd.Series(elem.text for elem in soup.find_all('span', class_='minus'))
        hrefs = pd.Series(elem.text for elem in soup.find_all('span', class_='minus')) # duplicating previous series to assign links here later

        df = pd.concat([stars, date, place, tenure, position, body, plus, minus, hrefs], axis=1)  # type: object
        df.iloc[:, [8]] = href # assigning links here

        df2 = df2.append(df)

        time.sleep(1.1)

        # for testing
        # if i > 30:
        #     break
        i = i + 1
    except urllib2.HTTPError as e:
        print(e)

print(df2.head())
df2.to_csv('output_test.csv')
