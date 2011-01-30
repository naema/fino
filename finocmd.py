#!/usr/bin/env python
# ./finocmd.py funktion p1 p2 ...

import sys
import fino

def add_series(series,url=''):
  fino.add_new_series(series,url)

def download():
  fino.download_series()  

def help():
  print "help"

commands = {
  "add_series":add_series,
  "download":download(),
  "--help":help,
  "-h":help
  }

#discard program name
sys.argv.pop(0)
cmd=sys.argv.pop(0)
params=sys.argv
#call function
commands[cmd](*params)



