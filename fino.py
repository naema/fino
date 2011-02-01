#!/usr/bin/env python
# coding=UTF-8
import urllib
import time
import datetime
from datetime import date
import csv
import StringIO
from BeautifulSoup import BeautifulSoup
#from subprocess import call
import filestube
import epguides
import db

"""read the series names from commandline or try to find in database
  case 1: new series:
          get the epguides link from google
          insert the new series into database. 
          write the eptable from epguides to a txt file and fill database.
  case 2: existent series:
          check airdate in database - 
          if airdate was yesterday: search links
"""

#get list of pending episodes
def get_pending_list():
  return db.get_download_list():

#saves download links to file
def build_plowfile(links,filepath='/tmp/plowfile.txt'):
  f = open(filepath, 'a')
  for downloadlink in links:
    f.write(downloadlink+'\n')
  f.close()
  
#search download links for every pending episode
#plowfile='/tmp/plowfile.txt'
#output_directory='/home/michelle/Videos/fino'
def download_all():
	ep_list = db.get_download_list()
	for episode in ep_list:
		links = filestube.search_links(episode)
		build_plowfile(links)
    #start plowshare  
    #call(["plowdown","-o", filepath, "-m", plowfile])

def download_episode(episode):
	links = filestube.search_links(episode)
	print links
	build_plowfile(links)
    
#add a new series and episodes to database
#TODO: when adding new series mark episodes < ddate as expired
def add_new_series(title,epg_url='',ddate=datetime.date.today()):
  if epg_url=='':
    epg_url = epguides.get_epguides_url(title)
  s = epguides.get_airtable(epg_url)
  eptable = list(csv.DictReader(StringIO.StringIO(s), delimiter=',', quotechar='"'))
  for line in eptable:
		airdate = line['airdate']
		t = time.strptime(airdate,"%d/%b/%y")
    # convert to date object
		airdate = datetime.date(*t[0:3])
		#line['airdate'] = `airdate`
		line['airdate'] = time.strftime("%Y-%m-%d",t)
    # The easiest way to convert this to a datetime seems to be; 
	#now = datetime.date(*t[0:3])
  series_id = db.get_series_id(title)
  if series_id == -1:
    series_id = db.write_series_to_database(title,epg_url)
  db.write_episodes_to_database(eptable,series_id)  
  

