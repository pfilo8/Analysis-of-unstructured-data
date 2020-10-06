#!/usr/bin/env python
# coding: utf-8

import itertools
import pickle
import requests

from bs4 import BeautifulSoup


def extract_authors(data):
    return [el.strip() for el in "".join(itertools.takewhile(lambda x: x!="(", data)).replace(' ', '').split(',')]


r = requests.get('http://prac.im.pwr.wroc.pl/~hugo/HSC/Publications.html')
r.encoding = 'utf-16'

html = BeautifulSoup(r.text)

data = []

for el in html.find_all('li'):
    text = el.text.replace('\n', '')
    authors = extract_authors(text)
    authors = [el for el in authors if el != '']
    data.append(authors)

with open('authors.pickle', 'wb') as f:
    pickle.dump(data, f)
