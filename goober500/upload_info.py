import os
import sys
import json
import math
import MySQLdb as mdb
con = mdb.connect("localhost","spotco_sql","dododo","spotco_jumpdiecreatelevels")
cur = con.cursor()
cur.execute("DELETE FROM level")
cur.execute("DELETE FROM level_playcount")
cur.execute("DELETE FROM level_review")

levels_dir = sys.argv[1]
ratinginfo_file = open(sys.argv[2],"r")
ratinginfo = json.loads(ratinginfo_file.read())

def generate_ratings(file_ratingcount,file_ratingavg):
	val_min = int(math.floor(file_ratingavg))
	val_max = int(math.ceil(file_ratingavg))
	rtv = {val_min:0,val_max:0}
	cur = 0
	for i in range(0,file_ratingcount):
		
		if cur < file_ratingavg:
			cur -= cur / (i+1.0)
			cur += val_max / (i+1.0)
			rtv[val_max] = rtv[val_max] + 1
		else:
			cur -= cur / (i+1.0)
			cur += val_min / (i+1.0)
			rtv[val_min] = rtv[val_min] + 1
	return rtv

for xml_filename in os.listdir(levels_dir):
	fileid = int(xml_filename.split(".")[0])
	file_handle = open(os.path.join(levels_dir,xml_filename),"r")
	
	file_xml_contents = file_handle.read()
	
	file_handle.close()
	file_ratinginfo = ratinginfo[str(fileid)]

	file_ratingavg = file_ratinginfo["ratingavg"]
	file_date_created = file_ratinginfo["date_created"]
	file_playcount = file_ratinginfo["playcount"]
	file_ratingcount = file_ratinginfo["ratingcount"]
	file_ratings = generate_ratings(file_ratingcount,file_ratingavg)
	file_creator_name = file_ratinginfo["creator_name"]
	file_level_name = file_ratinginfo["level_name"]

	print "adding level id %d"%(fileid)

	cur.execute("INSERT INTO level(id,xml,date_created,creator_name,level_name) VALUES(%s,%s,%s,%s,%s)",(fileid,file_xml_contents,file_date_created,file_creator_name,file_level_name))
	cur.execute("INSERT INTO level_playcount(level_id,playcount) VALUES(%s,%s)",(fileid,file_playcount))
	for rating_key in file_ratings:
		for i in range(0,file_ratings[rating_key]):
			cur.execute("INSERT INTO level_review(rating,level_id) VALUES(%s,%s)",(rating_key,fileid))
