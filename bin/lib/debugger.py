# Tyler Robbins
# 7/28/14
# Debugger
# Holds simple debugging and logging functions

import os
from datetime import datetime
# from constants import *

# now = datetime.now()

#NOTE
# This will be moved eventually to be pulled from a config file
debug_path = os.path.join(os.path.abspath(os.getcwd()),".logs")
# debug_path = log_path

unlogged = [] #This is for files that have yet to be logged

messageQueue = {} #messagetype:message1|[message2]

def genLogName(logEveryRun=False,newName=""):
	'''	Generate a log file name that has been timestamped with the date.
		logEveryRun <- Whether to make a new log file everytime genLogName is run, or simply return the last log file used on this date
	'''
	now = datetime.now()
	runs = 1

	date_stamp = "-".join([str(now.year)[2:],str(now.month),str(now.day)])

	#Here we get how many logs have been created on this date
	if logEveryRun:
		for i in os.listdir(debug_path):
			if i.endswith(str(date_stamp) + ".log"): runs += 1

		filename = "_".join([newName + "Log",date_stamp, "r" + str(runs)]) + ".log"
                
	else: filename = "_".join([newName + "Log",date_stamp]) + ".log"

	return filename

def debugInit(logEveryRun=False,setPath=None,fileName=""):
	'''Only call this once at the start of your program'''

	# if setPath:
	# 	debug_path = setPath

	filename = genLogName(logEveryRun,fileName)

	if not setPath:
		if not os.path.exists(debug_path):
			os.mkdir(debug_path)

	else:
		if not os.path.exists(setPath):
			os.mkdir(setPath)

	full_path = os.path.join(debug_path,filename)
	
	if filename not in os.listdir(debug_path):
		log_file = open(full_path,"w")
	else:
		log_file = open(full_path,"a")
		log_file.write("\n" + ("="*25) + "RESTART" + ("="*25) + "\n\n")

	log_file.close()

	open("config.tmpcfg",'w').write("logDir=" + log_file.name)

	return full_path # This gets sent to a tmpcfg file, which gets deleted once the program terminates

def debugUnInit():
	logging("Uninitializing the debug engine...","std")
	try:
		tmpcfg_path = os.path.join(os.path.abspath(os.getcwd()),"config.tmpcfg")

		if os.path.exists(tmpcfg_path): os.remove(tmpcfg_path)

	except Exception as e:
		logging("Could not delete config.tmpcfg!", "err", message2=e)

def logging(message1, msg_type, message2=None,dflag=False,queue=False):
	'''Write messages to a .log file stored in a .logs/ folder.'''
	now = datetime.now()
	
	tmpcfg_path = os.path.join(os.path.abspath(os.getcwd()),"config.tmpcfg")

	if os.path.exists(tmpcfg_path):
		filename = open(tmpcfg_path,'r').read().split("\n")[0].split("=")[1]
	else:
		print "ERROR! Unable to find config.tmpcfg!"
		print "Setting filename to current folder."

		filename = genLogName()
	try:
		msg_time = "[" + ":".join([str(now.hour), str(now.minute), str(now.second)])
		msg = str(message1)

		if msg_type == "err": 		msg_type = " - ERROR]: "
		elif msg_type == "warn": 	msg_type = " - WARNING]: "
		elif msg_type == "test":	msg_type = " - TEST]: "
		else: 						msg_type = " - STDOUT]: "

		if message2:
			full_msg = str(message2).split("\n")
		
			for line in full_msg:
				msg += "\n"
				msg += ("\t>>> " + line)

		output = msg_time + msg_type + msg

		if dflag:
			print output
			print "More information can be found in:"
			print full_path

		if not queue:
			parseQueue()

		open(filename,'a').write(output + "\n")

	except Exception as e:
		print "A FATAL ERROR OCCURRED!"
		print "UNABLE TO WRITE OUTPUT TO", filename, "!"
		print "FULL ERROR MESSAGE:\n", type(e).__name__, e

def isDebugInit():
	tmpcfg_path = os.path.join(os.path.abspath(os.getcwd()),"config.tmpcfg")

	return os.path.exists(tmpcfg_path)

def parseQueue():
	'''Currently broken.
	Meant to allow logging to store a queue of messages until the program ends in the case of the debugging engine
	not being initialized.'''
	for msg in messageQueue:
		message2 = messageQueue[msg]
		if message2 is "None": message2 = None

		logging(msg,messageQueue[msg],message2=message2,queue=True)

def getLogName():
	if isDebugInit():
		tmpcfg_path = os.path.join(os.path.abspath(os.getcwd()),"config.tmpcfg")
		filename = open(tmpcfg_path,'r').read().split("\n")[0].split("=")[1]
	else:
		filename = genLogName()

	return filename

if __name__ == "__main__":
	#For testing purposes only
	filename = debugInit()

	# open("config.tmpcfg",'w').write("logDir=" + filename)

	logging("Some weird error","err")

	logging(raw_input("Error: "),"err")
	logging(raw_input("warning: "),"warn")
	logging(raw_input("stdout: "),"std")

	# logging(raw_input("ErrorNew: "),"err","Oh noes!\nSOme stupid error happened, and now I don't know how to fix\nit!")

	debugDeInit()

nuclear = u'\u2622'
