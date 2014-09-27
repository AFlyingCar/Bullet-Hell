# Tyler Robbins
# 8/4/14
# Launcher
# A launcher program which will initialize all modules, files, and settings

from bin.lib.basic import shutdown
from bin.lib.settings import *
from bin.lib.debugger import *
from urllib2 import *
import os,pygame,traceback,ctypes

def fontInit():
	# fontPath = configReader()['path_font']
	fontPath = ConfigSettings['path_font']
	fonts = {}
	for i in os.listdir(fontPath):
		if i.endswith(".ttf"):
			fonts[i] = pygame.font.Font(os.path.join(fontPath,i),29)
			logging("Successfully loaded " + str(i),"std")

	return fonts

def initAll():
	variables = {}

	try:
		basicLink = "tylerclay.com/"
		link = 		urlopen(basicLink + "changedFiles.txt")
		newFiles = 	link.read().split("\n")

		for i in newFiles:
			link = urlopen(basicLink + i)
			path = os.path.join(os.getcwd(),i)
			open(path,"wb").write(link.read())

	except Exception as e:
		# print "Unable to check for downloaded files"
		# print e

		if isDebugInit():
			logging("Unable to check for downloaded files","err",e)
		else:
			print "Unable to check for downloaded files."
			print e

	for times in range(10):
		'''Attempt to initialize 10 times before giving up.'''
		try:
			debugInit(setPath=getSetting("path_log"))
			success = True

			fonts = fontInit()
			success = True

			if getSetting("enable_sound"):
				pygame.mixer.pre_init(frequency=22050, size=-16, buffer=500)
				success = True

			pygame.init()

			#End if no errors are found
			break

		except Exception as e:
			if isDebugInit():
				logging("A fatal error occurred.","err",e)
			else:
				print "A fatal error occurred."
				print type(e).__name__," ",e
			success = False

	return success

if __name__ == "__main__":
	success = initAll()

	if not success:
		print "Unable to initialize properly. Shutting down."
		shutdown()
	else:
		try:
			pygame.mouse.set_visible(False)
			import main
		except BaseException as e:
			if type(e) != SystemExit:
				prgname = getSetting('prg_name') + " " + getSetting('game_version')

				error = traceback.format_exc()
				logging("Sorry.\n" + '-'*30 + "\nA fatal runtime error has occurred in " + prgname + ", and it must be shut down.","err",error)

				if sys.platform == "win32":
					ctypes.windll.user32.MessageBoxW(0,u'A fatal runtime error has occurred in ' + prgname + ', and it must be shut down.'
						+ ' See\n'+ str(getLogName()) + "\nfor more details.",u'Error', 0)
				
				shutdown()

nuclear = u'\u2622'