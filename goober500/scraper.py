from urllib2 import urlopen
from urllib import urlencode
import xml
from xml.dom.minidom import parseString
import threading
from time import sleep
import sys
import re
import os.path


class Request(threading.Thread):
	def __init__(self,offset):
		threading.Thread.__init__(self)
		self.offset = offset
		
	def run(self):
		resc = urlopen('http://flashegames.net/spotco/getmostplayed.php',urlencode({"offset":offset})).read()
		xmlobj = parseString(resc)
		for i in xmlobj.getElementsByTagName("level"):
			tar_id = i.attributes["id"].value
			# if os.path.isfile("levels/%i.xml"%(int(tar_id))):
				# continue
			level_xml = urlopen('http://flashegames.net/spotco/getbyid.php',urlencode({"id":tar_id})).read()
			f = open("levels/%i.xml"%(int(tar_id)),"w")
			level = parseString(level_xml)
			level.getElementsByTagName("level")[0].setAttribute("author",i.attributes["creator_name"].value)
			f.write(level.toprettyxml().encode('utf-8'))
			sleep(1)
			

numlevels = int(parseString(urlopen('http://flashegames.net/spotco/getnumlevels.php').read()).getElementsByTagName("numlevels")[0].attributes["val"].value)
numlevels = numlevels+5

threads = []
for offset in range(0,numlevels,5):
	thread = Request(offset)
	thread.start()
	threads.append(thread)
	sleep(1)
	
for thread in threads:
	thread.join()
	
#sys.exit("early end")
