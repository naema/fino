#!/usr/bin/env python
import filestube
import urllib
from BeautifulSoup import BeautifulSoup

#read the serieslist, check for new episodes and build plowfile
def read_series(filepath):
  download_candidates = open(filepath, 'r')
  for line in download_candidates:
    line = line.strip()
    print line
    links = filestube.search_links(line)
    print links
    filestube.build_plowfile(links)  
  download_candidates.close()

filepath = '/home/michelle/codes/fino/series.txt'
read_list(filepath)

#TODO: look up next airdate in database
def check_airdate(series):
  url = 'http://epguides.com/'+series
  date_page = urllib.urlopen(url).read()
  soup = BeautifulSoup(date_page)
  div = soup.find("div",id="eplist")
  
