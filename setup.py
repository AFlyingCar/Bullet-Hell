#Execute with: 'setup.py build'

import sys
from cx_Freeze import setup, Executable

includes = ['Boss-1.png','img-75.png','img-76.png','img-77.png','img-78.png','img-s_bkg.png','player.png','THSpatial.ttf']
packages = ["os","pygame","pygame.locals","random","sys"]
excludes = ["tkinter"]

build_exe_options = {"packages":packages,"excludes":excludes,"include_files":includes}

base = None

setup(	name="BossFight",
		version='0.1',
		description='Dot Boss Fight!',
		options={'build_exe':build_exe_options},
		executables=[Executable("boss-1-1-v2.py",base=base)])