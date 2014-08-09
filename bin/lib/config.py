# Tyler Robbins
# 8/7/14
# Config
# Hold configuration functions in a separate file

import urllib2,os
from debugger import *

def configReader():
	config_path = os.path.join(os.path.abspath(os.getcwd()),"config.cfg")
	
	if not os.path.exists(config_path):
		if isDebugInit():
			logging("Could not find config file, attempting to downloading default file", "err")
		else:
			print "Could not find config file, attempting to downloading default file"
		try:
			link = urllib2.urlopen("tylerclay.com/config.cfg")
			open(config_path,"w").write(link.read())
		except Exception as e:
			if isDebugInit():
				logging("Unable to download default config file. Shutting down...","err",e)
			else:
				print "Unable to download default config file. Shutting down..."
				print type(e).__name__,str(e)

			shutdown()

	text = open(config_path,"r").read()

	return configParser(text)

def configParser(text):
	returns = {}
	parsed = text.split("\n")
	error = 0

	for i in parsed:
		if i.startswith("@") or i == "": continue

		else:
			try:
				var_val = i.split("=",1)

				if var_val[0].endswith(" "):
					var_val[0] = var_val[0].strip()

				if var_val[1].startswith(" "):
					var_val[1] = var_val[1].strip()
				
				if var_val[1].startswith("\t"):
					var_val[1] = var_val[1].lstrip()

				if var_val[1].startswith('"') or var_val[1].startswith("'"):
					r = var_val[1][1:-1]

					if r.startswith("cwd\\") or r.startswith("cwd//"):
						r = os.path.join(os.path.abspath(os.getcwd()),r[5:])

					returns[var_val[0]] = r
				
				elif var_val[1].isdigit(): 										returns[var_val[0]] = int(var_val[1])
				elif var_val[1].startswith('('):								returns[var_val[0]] = STRtoTUP(var_val[1],tuple)
				elif var_val[1].startswith('['):								returns[var_val[0]] = STRtoTUP(var_val[1],list)
				elif var_val[1] == "false": 									returns[var_val[0]] = False
				elif var_val[1] == "true": 										returns[var_val[0]] = True
				else: 															returns[var_val[0]] = var_val[1]

			except Exception as e:
				if isDebugInit():
					logging("An error occurred while parsing config.cfg.","err",e)
				else:
					print "An error occurred while parsing config.cfg."
					print type(e).__name__, str(e)

				error += 1

	return [returns,error]

def STRtoTUP(string,ltype):
	tup = string[1:-1]
	if "," in tup:
		tup = tup.split(",")
		for i in tup:
			if i.isdigit(): 							 tup[tup.index(i)] = int(i)
			elif i.startswith('"') or i.startswith("'"): tup[tup.index(i)] = i[1:-1]
			elif i.startswith('('): 					 tup[tup.index(i)] = STRtoTUP(i,tuple)
			elif i.startswith('['): 					 tup[tup.index(i)] = STRtoTUP(i,list)
			elif i == "false": 							 tup[tup.index(i)] = False
			elif i == "true": 							 tup[tup.index(i)] = True
			else: 										 tup[tup.index(i)] = i

	return ltype(tup)

nuclear = u'\u2622'