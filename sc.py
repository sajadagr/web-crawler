import argparse
import urllib2
from bs4 import BeautifulSoup
import json
from lxml import etree
from collections import OrderedDict
import csv

# Using file as cache to make script easy to run
# Else u can also use redis or some other cache
# But for that we have to install redis on system.
cache = [str(link).replace("\n", "") for link in open("file_cache.txt")]
MAIN_URL = 'https://hasjob.co'


def load_xpath_file():
    x_path_map = OrderedDict()
    lines = [json.loads(l) for l in open("xpath.json")]
    for line in lines:
        for k, Xpath in line.iteritems():
            x_path_map[k] = Xpath
    return x_path_map


def get_link(ls):
    sub_links = []
    for tag in ls:
        url = tag.get('href', None)
        if url is not None:
            if not str(url).startswith("http") and "." in url > 1:
                sub_links.append(MAIN_URL + url)
    return sub_links


# currently we are not able to crawl two overlapping job links.

def scrap(out_put_file, x_path_map):
    headers = {
        # if it will not work u may have to change cookie , which u get can by logging in to the hasjob.co from ur browser

        'cookie' : 'lastuser=eyJhbGciOiJIUzI1NiIsInYiOjF9.eyJzZXNzaW9uaWQiOiI1S1dNSTk3aFREV2NIOVVLTlJwa2NBIiwidXNlcmlkIjoiS3ZqR1BHaEFSQXU5M1NucUQ1QndIUSJ9.MoheZQ_BVud_wZW3yVFnnHfxasXcRVyqsk9-tYiIxpw; session=.eJw9jlFrgzAUhf9KyHMekhuTtEIfNtoJw1QE-6BlDDWxNbZaWsfA4n-f2WBw4cA953ycJ64f9-ZzHDrb4_CJUYVDnGSvl_02DXJ46_bRe6vd4Tt3J8iny1VPHdWwW7xUFFFxLrad_5-Tl80GzwTbxy_ma8FIWXJKTdUIaIKa0YpZu5K2EYquaqGsj5_s0JdX25qldmSgFOecMJBKUeZ1rQQlEoRggfoguL2Vxtz_h-rswGOXitjtpthp8MT2Nv5NMD4w9ARRQEk9IqBMIcZDsV4ORTrD8_wD8thIdw.DLPX4A.JumXEael_NXtNl3gU4Y2uzS-Zcc; _ga=GA1.2.989936474.1505578155; _gid=GA1.2.33425005.1506942542; _gat=1',
        #'ocp - apim - subscription - key': '4b2f445a1ca942e6b2a3361139f05ee3'
    }
    req = urllib2.Request(MAIN_URL, None, headers)
    conn = urllib2.urlopen(req)
    html = conn.read()
    soup = BeautifulSoup(html)
    links = soup.find_all('a')
    all_links = get_link(links)

    header = x_path_map.keys()
    header.append("link")
    company_name_set = set()
    cache_writer = open("file_cache.txt", "a")
    with open(out_put_file, 'wb') as wr:
        writer = csv.writer(wr)
        writer.writerow(header)

        for l in all_links:
            if l not in cache:
                conn = urllib2.urlopen(l)
                html = conn.read()
                tree = etree.HTML(html)
                res = []
                for key, x_path in x_path_map.iteritems():
                    cells = tree.xpath(x_path)
                    for td in cells[:1]:
                        value = td.text
                        if key == "-":
                            if value not in company_name_set:
                                company_name_set.add(value)
                                res.append(value)
                        else:
                            res.append(td.text)
                if len(res) > 0:
                    res.append(l)
                    cache.append(l)
                    cache_writer.write(l + "\n")
                    writer.writerow(res)


# NOTE: Here we are not extracting job views etc, compensation and
#  email of person posting job as they are not found in html


def main():
    parser = argparse.ArgumentParser(description="web scrapper")
    parser.add_argument("-o", "--output_file", help='Output csv file', required=True)
    args = parser.parse_args()
    x_path_map = load_xpath_file()
    scrap(args.output_file, x_path_map)


if __name__ == '__main__':
    main()
