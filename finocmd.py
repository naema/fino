#!/usr/bin/env python
# ./finocmd.py funktion p1 p2 ...

import sys
import fino

# TODO:parse commandline args with getopt

def add_series(series,url=''):
	fino.add_new_series(series,url)

def download_all():
	fino.download_all()  

def download_episode(episode):
	fino.download_episode(episode)
	
def help():
	use = usage()
	for line in use:
		print line

#TODO: define options to use
def usage():
	use = ["Usage: ./finocmd.py [-a|-d episode|--add series [URL]]\n",	
	"Search episodes on filestube.com and download with plowshare\n",
	"default output directory is the current directory;\n",
	"Global options:\n",
	"	-a, --all: Download all pending episodes",
	"	--add SERIES [EPGUIDES_URL]: Add a new series to the database",
	"	-c, --check: Check which episodes are available",
	"	-d EPISODE, --download EPISODE: Download only specified episodes",
	"	--date DATE: specify the date from which on added episodes shall be downloaded. Formatting: '2011-01-31' default date is current date"
	"	-h, --help: Show help info",
	"	-l, --list: Get a list of the pending episodes",
  "	-m, --mark-downloaded: Mark downloaded links in (regular) FILE arguments",
  "	-x, --no-overwrite: Do not overwrite existing files",
  "	-o DIRECTORY, --output-directory=DIRECTORY: Directory where files will be saved\n"]
	return use
	
commands = {
	"--add":add_series,
  	"--all":add_series,
	"--add -a":add_series(date = false)
  	"-d":download_episode,
  	"--help":help,
  	"-h":help
  	}
# example command: 	./finocmd.py -d 'californication s04e03'    <- download only the specified episode    TODO: check if this episode is already in database, if true: mark 'downloaded'
#								./finocmd.py --all   <- donwload all pending episodes
#								./finocmd.py --add 'Private Practice' --date 2011-01-01    <- add all private practice episodes to database, episodes before 1.1.2011 will not be downloaded automatically
#								./finocmd.py --add -a SERIES   <- add all episodes from SERIES to database, all episodes will be downloaded
#discard program name
sys.argv.pop(0)
cmd=sys.argv.pop(0)
params=sys.argv
#call function
commands[cmd](*params)



