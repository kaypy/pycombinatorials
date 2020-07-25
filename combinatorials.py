#! /usr/bin/python

###############################################

# Copyright 2020 Kris Parker

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

###############################################

# configuration

#how many lines before we force a new file
filelimit=1000000
#file to read input data from
inputfilename="inputitems.txt"
#base output filename
outputfilename="combinationdata"
#how often to give progress feedback
dotfrequency=100000

################################################

# initialize config
itemlist=[]
outputcount=3

inputFile=open(inputfilename,"r")
# first line in inputfile is number it items to combine
outputcount=int(inputFile.readline())
# the rest is input items
while True:
	line = inputFile.readline()
	if (line == "") :
		break
	line=line.strip()
	if (line != "") :
		itemlist.append(line)
inputFile.close()

#cache input list length
ilistlen = len(itemlist)-1

# set up initial combination
outlist=[None]*outputcount
for i in range(0,outputcount) :
	outlist[i]=i

# find the next combination
# increment the last item
# if we overflow, increment one item earlier and
# then make this one the next after that
def nextcombination(node) :
	outlist[node] = outlist[node]+1
	# maximum value decreases from last to first
	if (outlist[node]>(ilistlen+node+1-outputcount)) :
		if (node == 0) :
			outlist[node] = -1
			return
		# recurse into earlier nodes
		nextcombination(node-1)
		outlist[node]=outlist[node-1]+1

# feedback initialization
dotcount=dotfrequency
totalcount=0

# file initialization
filecount=filelimit
outputfileno=1
outputfile=open(outputfilename+str(outputfileno)+".csv","w")

# print each combination until we reach an invalid combination
while outlist[0] >= 0 :
	# generate output line
	line = ""
	for i in range(0,outputcount) :
		line=line+"\""+itemlist[outlist[i]]+"\","
	outputfile.write(line+"\n")
	# increment counters
	totalcount=totalcount+1
	dotcount = dotcount-1
	filecount = filecount-1
	# check for new file
	if (filecount < 1) :
		filecount=filelimit
		outputfile.close()
		outputfileno=outputfileno+1
		outputfile=None
		outputfile=open(outputfilename+str(outputfileno)+".csv","w")
		print (outputfilename+str(outputfileno)+".csv")
	# check for printing progress report
	if (dotcount < 1) :
		dotcount = dotfrequency
		print totalcount
	# generate next combination
	nextcombination(outputcount-1)

outputfile.close()
