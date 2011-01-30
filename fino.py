#!/usr/bin/env python
# coding=UTF-8
import urllib
import time
import csv
import StringIO
from BeautifulSoup import BeautifulSoup
from subprocess import call
import filestube
import epguides
import db

"""read the series names from file and try to find in database
  case 1: new series:
          get the epguides link from google
          insert the new series into database. 
          write the eptable from epguides to a txt file and fill database.
  case 2: existent series:
          check airdate in database - 
          if airdate was yesterday: search links
"""

#get list of series to download
def read_series(filepath):
  download_candidates = open(filepath, 'r')
  series_list = []
  for line in download_candidates:
    line = line.strip()
    series_list.append(line)
  download_candidates.close()
  return series_list

#saves download links to file
def build_plowfile(links,filepath='/tmp/plowfile.txt'):
  f = open(filepath, 'a')
  for downloadlink in links:
    f.write(downloadlink+'\n')
  f.close()
  
#search download links for every series in database and download them
#plowfile='/tmp/plowfile.txt'
#output_directory='/home/michelle/Videos/fino'
def download_series():
  ep_list = db.get_download_list()
  for episode in ep_list:
    links = filestube.search_links(episode)
    build_plowfile(links)
    #start plowshare  
    #call(["plowdown","-o", filepath, "-m", plowfile])
  
#add a new series and episodes to database
def add_new_series(title,epg_url=''):
  if epg_url=='':
    epg_url = epguides.get_epguides_url(title)
  s = epguides.get_airtable(epg_url)
  eptable = list(csv.DictReader(StringIO.StringIO(s), delimiter=',', quotechar='"'))
  for line in eptable:
    date = line['airdate']
    t = time.strptime(date,"%d/%b/%y")
    line['airdate'] = time.strftime("%Y-%m-%d",t)
  series_id = db.get_series_id(title)
  if series_id == -1:
    series_id = db.write_series_to_database(title,epg_url)
  db.write_episodes_to_database(eptable,series_id)  
  

