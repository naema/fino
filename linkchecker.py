import urllib

#check if megaupload link is valid TODO: extend for other hosters
def check_links(links):
  for l in links:
    try:
      s = urllib.urlopen(l).read()
    except IOError:
      return False
    if s.rfind('downloadcounter') == -1:
      return False
    return True
