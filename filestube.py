#!/usr/bin/env python

import sys
import urllib
from BeautifulSoup import BeautifulSoup

#build query for filestube search
def build_query(search_phrase):
   min_size = 150
   max_size = 400
   return 'http://www.filestube.com/search.html?q='+search_phrase+'&hosting=3&select=avi&sizefrom='+`min_size`+'&sizeto='+`max_size`

#check if megaupload link is valid TODO: sort into tools file, extend for other hosters
def check_links(links):
  for l in links:
   s = urllib.urlopen(l).read()
   if s.rfind('downloadcounter') == -1:
    return False
   return True

#extracts downloadlinks from filestube result-page
def extract_downloadlinks(link):
  page = urllib.urlopen(link).read()
  soup = BeautifulSoup(page)
  pre = soup.find("pre",id="copy_paste_links")
  pre = `pre`
  megaupload_links = pre[pre.find('>')+1:pre.rfind('<')].strip().split('\r\n')
  return megaupload_links

#saves download links to file TODO: sort into tools file or something, not filestube related
def build_plowfile(links,filepath='/tmp/plowfile.txt'):
  f = open(filepath, 'a')
  for downloadlink in links:
    f.write(downloadlink+'\n')
  f.close()

#get download links from filestube
def search_links(phrase):
  query = build_query(phrase)
  result_page = urllib.urlopen(query).read()
  soup = BeautifulSoup(result_page)
  search_results = soup.findAll("div",id="newresult")
  for result in search_results:
    link = result.a['href']
    megaupload_links = extract_downloadlinks(link)
    if check_links(megaupload_links) == True:
      return megaupload_links
    return '#'+search_phrase + ': no links found' 


