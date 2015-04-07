import os
import sys

path = sys.argv[1]
nums = [int(x.split(".xml")[0]) for x in os.listdir(path)]
for i in range(0,max(nums)+1):
	if not i in nums:
		print "MISSING %d"%(i)