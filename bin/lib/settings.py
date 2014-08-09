# Tyler Robbins
# 8/8/14
# Settings
# Load all settings from config.cfg

from config import *
from debugger import logging

def getSetting(setting):
	try:
		return ConfigSettings[setting]
	except BaseException as e:
		if isDebugInit():
			logging("Attempted to access setting: " + setting + ", but no such setting was found.","err")
		else:
			print "Attempted to access setting: " + setting + ", but no such setting was found."

		return ""

ConfigSettings,error = configReader()

if isDebugInit():
	logging("Loaded settings with " + str(error) + " errors.", "std")
else:
	print "Loaded settings with " + str(error) + " errors."

nuclear = u'\u2622'