import sys
import urllib
from BeautifulSoup import BeautifulSoup
import linkchecker

#build query for filestube search
def build_query(search_phrase):
   min_size = 150
   max_size = 400
   return 'http://www.filestube.com/search.html?q='+search_phrase+'&hosting=3&select=avi&sizefrom='+`min_size`+'&sizeto='+`max_size`

#extracts downloadlinks from filestube result-page
def extract_downloadlinks(link):
  page = urllib.urlopen(link).read()
  soup = BeautifulSoup(page)
  pre = soup.find("pre",id="copy_paste_links")
  pre = `pre`
  megaupload_links = pre[pre.find('>')+1:pre.rfind('<')].strip().split('\r\n')
  return megaupload_links

#get download links from filestube
def search_links(phrase):
  query = build_query(phrase)
  result_page = urllib.urlopen(query).read()
  soup = BeautifulSoup(result_page)
  search_results = soup.findAll("div",id="newresult")
  if search_results ==[]:
    return ['#'+phrase + ': no links found']
  for result in search_results:
    link = result.a['href']
    megaupload_links = extract_downloadlinks(link)
    if linkchecker.check_links(megaupload_links) == True:
      return megaupload_links
    return ['#'+phrase + ': no links found'] 


