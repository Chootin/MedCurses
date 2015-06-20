#! /usr/bin/python3

import curses
import os
from subprocess import call
from re import sub

_path = "/home/pi/roms"
_files = []
_numFiles = 0
_cursorPos = 0
_noExit = True

def main(stdscr):
	global _files
	global _numFiles
	global _noExit
	
	_files = getFiles(_path)
	_numFiles = len(_files)

	while _noExit:
		printScreen(_files, stdscr)
		inputCheck(stdscr)

def inputCheck(screen):
	global _cursorPos
	global _noExit
	global _numFiles
	KEY_ESC = 27
	KEY_ENTER = 10

	input = screen.getch()
	if input == curses.KEY_DOWN:
		_cursorPos = (_cursorPos + 1) % _numFiles
	elif input == curses.KEY_UP:
		_cursorPos = (_cursorPos - 1) % _numFiles
	elif input == KEY_ENTER:
		runMednafen()
		cleanup()
	elif input == KEY_ESC:
		_noExit = False

def runMednafen():
	xinitrc = "/home/pi/.xinitrc"
	newXinitrc = xinitrcString()

	if os.path.isfile(xinitrc):
		os.rename(xinitrc, "{}.bak".format(xinitrc))
	file = open(xinitrc, "w")
	file.write(newXinitrc)
	file.close()
	call("startx")

def cleanup():
	xinitrc = "/home/pi/.xinitrc"
	xinitrcBak = "{}.bak".format(xinitrc)

	os.remove(xinitrc)
	
	if os.path.isfile(xinitrcBak):
		os.rename(xinitrcBak, xinitrc)
		

def xinitrcString():
	global _cursorPos
	global _files
	game = sub(" ", "\ ", _files[_cursorPos])

	string = "exec mednafen {}".format(game)
	return string

def getFiles(path):
	files = []
	for (dirpath, dirnames, filenames) in os.walk(path):
		for name in filenames:
			filename = name
			files.append(os.path.join(dirpath, filename))
	return files

def printScreen(files, screen):
	global _cursorPos

	line = 0
	screen.clear()
	for file in files:
		screen.addstr(line, 0, file)
		if line == _cursorPos:
			length = len(file)
			screen.addstr(line, length, " <")
		line += 1
	screen.refresh()

def printStrings(strings, screen):
	line = 0
	screen.clear()
	for string in strings:
		screen.addstr(line, 0, string)
		line += 1
	screen.refresh()

curses.wrapper(main)
