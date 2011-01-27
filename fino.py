#!/usr/bin/env python
import filestube
import urllib
import time
import MySQLdb 
from BeautifulSoup import BeautifulSoup
import csv

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

#TODO:erste zeile wegschmeißen, kommas aus den titeln entfernen!
def get_episodes_from_txt(filepath):
  cursor = connect_to_database()
  f = open(filepath, 'r')
  for line in f:
    s = line.strip().split(",")  
    #data array contains: season, episode, airdate, title
    t = time.strptime(s[4],"%d/%b/%y")
    date = s[4].split("/")
    airdate = time.strftime("%Y-%m-%d",t)
    data = [s[1],s[2],`airdate`,s[5]]
    #write into database
    write_episodes_to_database(data,cursor)
    print airdate
  f.close()
  
def connect_to_database():
  mysql_opts = { 
    'host': "localhost", 
    'user': "root", 
    'pass': "pw", 
    'db':   "tvdb" 
    } 
  mysql = MySQLdb.connect(mysql_opts['host'], mysql_opts['user'], mysql_opts['pass'], mysql_opts['db'])
  mysql.apilevel = "2.0" 
  mysql.paramstyle = "format" 
  return mysql.cursor()  
    
def write_episodes_to_database(data,cursor):
  cursor.execute("INSERT INTO episodes (season, episode, airdate, title) VALUES ("+data[0]+","+data[1]+","+data[2]+","+data[3]+")") 

def get_month(string):
  months = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
  return months[string]
