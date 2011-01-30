import urllib
from BeautifulSoup import BeautifulSoup

google = 'http://www.google.com/search?q=allintitle:+site:epguides.com+'

#search epguides link on google.com -> <h1>Forbidden</h1>Your client does not have permission to get URL <code>
def get_epguides_url(series):
	query = google+series
	site = urllib.urlopen(query).read()#googlesuche
	soup = BeautifulSoup(site)
	div = soup.find("div", id="ires")
	a = div.find('a')
	return a['href']

#get airdate table from epguides as string
def get_airtable(epguides_url):
	site = urllib.urlopen(epguides_url).read()
	soup = BeautifulSoup(site)
	navbar = soup.find("div", id="topnavbar")
	eplink = navbar.findAll("a")[4]['href']
	site = urllib.urlopen(eplink).read()
	soup = BeautifulSoup(site)
	eptable = soup.find("textarea").string
	return eptable.strip()

