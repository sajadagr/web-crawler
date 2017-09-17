import urllib2
from bs4 import BeautifulSoup
import json
from lxml import etree
from collections import OrderedDict

import csv


MAIN_URL = 'https://hasjob.co'
x_path_map = OrderedDict()
lines = [json.loads(l) for l in open("xpath.json")]
for line in lines:
    for key, x_path in line.iteritems():
        x_path_map[key] = x_path


def get_link(ls):
    sub_links = []
    for tag in ls:
        link = tag.get('href', None)
        if link is not None:
            # print link
            if not str(link).startswith("http") and "." in link > 1:
                sub_links.append(MAIN_URL + link)
    return sub_links


conn = urllib2.urlopen(MAIN_URL)
html = conn.read()
soup = BeautifulSoup(html)
links = soup.find_all('a')
all_links = get_link(links)

result = []
header  = x_path_map.keys()
header.append("link")
with open("result.csv", 'wb') as wr:
    writer = csv.writer(wr)
    writer.writerow(header)

    for l in all_links:
        conn = urllib2.urlopen(l)
        html = conn.read()
        tree = etree.HTML(html)
        res =[]
        for key, x_path in x_path_map.iteritems():
            cells = tree.xpath(x_path)
            for td in cells[:1]:
                res.append(td.text)
        res.append(l)
        writer.writerow(res)
