from os.path import join
from os import listdir, rmdir
import os
from shutil import move

rootdir = 'D:\CSCI-5502-Datamining\SportsVU-Movement-Mining-Project\SportVU-Data\data\SportVU_JSON_Data'

for subdir, dirs, files in os.walk(rootdir):
	#print subdir
	#print dirs
	#for file in files:
		#print file
    	#move(join())
        #print os.path.join(subdir, file)
    for filename in listdir((subdir)):
		print filename
		move(join(rootdir, subdir, filename), join(rootdir, filename))
#rmdir(root)



