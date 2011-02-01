import MySQLdb

def connect_to_database(mysql_opts = { 
    'host': "localhost", 
    'user': "root", 
    'pass': "pw", 
    'db':   "tvdb" 
    #read_default_file
    } ):
  mysql = MySQLdb.connect(mysql_opts['host'], mysql_opts['user'], mysql_opts['pass'], mysql_opts['db'])
  mysql.apilevel = "2.0" 
  mysql.paramstyle = "format" 
  return mysql
    
def write_episodes_to_database(data_list, series_id, status = 'pending'):
  db = connect_to_database()
  cursor = db.cursor()
  for data in data_list:
    try: 
      cursor.execute("INSERT INTO episodes (nr, season, episode, airdate, title, series_id, status) VALUES ("+data['number']+","+data['season']+","+data['episode']+","+`data['airdate']`+","+`data['title']`+","+`series_id`+","+`status`+")") 
      print "added episode s"+data['season']+"e"+data['episode']+" from series_id "+`series_id`+" to database"
    except MySQLdb.IntegrityError:
      print "series_id "+`series_id`+" s"+data['season']+"e"+data['episode']+" has already been added to the database"
  
  cursor.close()
  db.close()
  
def get_series_id(title):
  db = connect_to_database()
  cursor = db.cursor()
  cursor.execute("SELECT id FROM series where title = "+`title`)
  result=cursor.fetchone()
  
  if not result:
    return -1
  else:
    series_id = int(result[0])
  cursor.close()
  db.close()
  return series_id
  
def write_series_to_database(title,epg_url):
  db = connect_to_database()
  cursor = db.cursor()
  try:
      cursor.execute("INSERT INTO series (title, url) VALUES("+`title`+","+`epg_url`+")")
  except MySQLdb.IntegrityError:
      print "the series has already been added to the database"
  cursor.execute("SELECT id FROM series WHERE title = "+`title`)
  result=cursor.fetchone()
  if not result:
    return -1
  else:
    series_id = int(result[0])
  cursor.close()
  db.close()
  print 'added series '+title+' to database'
  return series_id
  
  
#returns a list of pending episodes, e.g. ["californication s04e03", ...]
def get_download_list():
  db = connect_to_database()
  cursor = db.cursor()
  s="SELECT s.title, e.season, e.episode, e.title FROM series AS s, episodes AS e WHERE (e.airdate <=  CURDATE() AND e.status = 'pending' AND s.id = e.series_id)"
  cursor.execute(s)
  results = cursor.fetchall()
  episode_list = []
  for row in results:
    s = `int(row[1])`.rjust(2,`0`)
    e = `int(row[2])`.rjust(2,`0`)
    episode = row[0]+" "+"s"+s+"e"+e+" "+row[3]
    episode_list.append(episode)
  if episode_list == []:
    print "no episodes found"
  cursor.close()
  db.close()
  return episode_list

def count_pending():
	db = connect_to_database()
  cursor = db.cursor()
  s="SELECT count FROM series AS s, episodes AS e WHERE (e.airdate <=  CURDATE() AND e.status = 'pending' AND s.id = e.series_id)"
  cursor.execute(s)
  results = cursor.fetchone()
  count_pending = 0
  for row in results:
    number_pendig = row[0]
  cursor.close()
  db.close()
  return count_pending
#TODO: mark series downloading or existent
#delete series from database, set series inactive/active
#check for new episodes on epguide.com
  
