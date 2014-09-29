#Execute with: 'setup.py build'

import os,sys,zipfile,shutil
from cx_Freeze import setup, Executable
from datetime import datetime

now = datetime.now()
fileName = '_'.join(["build","-".join([str(now.month),str(now.day),str(now.year)[2:]])])

def zipdir(path,zip):
	for root,dirs,files in os.walk(path):
		for file in files:
			zip.write(os.path.join(root,file))
			print os.path.join(root,file)

includes = ['bin\\','thcut.dat','license.txt','README.md','config.cfg','controls.txt']
packages = ["os","pygame","pygame.locals","random","sys","urllib2","traceback","ctypes"]
excludes = ["tkinter"]

build_exe_options = {"packages":packages,"excludes":excludes,"include_files":includes}

base = None
if sys.platform == "win32":
	base = "Win32GUI"

setup(	name="BossFight",
		version='0.1',
		description='Dot Boss Fight!',
		options={'build_exe':build_exe_options},
		executables=[Executable("launcher.py",base=base)])

print "Saving source to folder..."

if not os.path.exists(fileName):
	zipf = zipfile.ZipFile('build\\src.zip','w')
else:
	zipf = zipfile.ZipFile(fileName + '\\src.zip','w')

for i in includes:
	zipdir(i,zipf)

	if not i.endswith("\\"):
		zipf.write(i)

zipf.close()

pack_name = fileName

if not os.path.exists(fileName):
	os.rename("build\\",fileName)
else:
	num = 1
	for f in os.listdir(os.getcwd()):
		if f.startswith(fileName):
			num += 1

	pack_name = fileName + " (" + str(num) + ")"
	os.rename("build\\",pack_name)

nuclear = u'\u2622'
