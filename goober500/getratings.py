from urllib2 import urlopen
from urllib import urlencode
import xml
from xml.dom.minidom import parseString
import threading
from time import sleep
import sys
import re
import os.path
import json

vals = {}
vals_lock = threading.Lock()

class Request(threading.Thread):
	def __init__(self,offset):
		threading.Thread.__init__(self)
		self.offset = offset
		
	def run(self):
		resc = urlopen('http://flashegames.net/spotco/getrecent.php',urlencode({"offset":self.offset})).read()
		xmlobj = parseString(resc)
		for levellist in xmlobj.getElementsByTagName("levellist"):
			for level in levellist.getElementsByTagName("level"):
				level_id = int(level.attributes["id"].value)
				date_created = level.attributes["date_created"].value.encode('ascii','replace')
				playcount = int(level.attributes["playcount"].value)
				ratingavg = float(level.attributes["ratingavg"].value)
				ratingcount = int(level.attributes["ratingcount"].value)
				creator_name = level.attributes["creator_name"].value.encode('ascii','replace')
				level_name = level.attributes["level_name"].value.encode('ascii','replace')
				vals_lock.acquire()
				vals[level_id] = {
					"date_created":date_created,
					"playcount":playcount,
					"ratingavg":ratingavg,
					"ratingcount":ratingcount,
					"creator_name":creator_name,
					"level_name":level_name
				}
				vals_lock.release()
		print "%d/900"%(self.offset)



threads = []
for offset in range(0,900,5):
	thread = Request(offset)
	thread.start()
	threads.append(thread)
	sleep(1)
	
for thread in threads:
	thread.join()

print ">>>BEGIN JSON"
print json.dumps(vals)
print ">>>END JSON"
	
#sys.exit("early end")
