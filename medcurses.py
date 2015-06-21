#! /usr/bin/python3

import curses
import os
from subprocess import call
from re import sub

_home = os.path.expanduser("~")
_path = "{}/roms".format(_home)
_files = []
_numFiles = 0
_cursorPos = 0
_noExit = True
_windows = []

def main(stdscr):
	global _files
	global _numFiles
	global _noExit

	screenLayout()
	
	_files = getFiles(_path)
	_numFiles = len(_files)

	while _noExit:
		printFiles(_files, _windows[1])
		inputCheck(_windows[1])

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
	global _home
	xinitrc = "{}/.xinitrc".format(_home)
	newXinitrc = xinitrcString()

	if os.path.isfile(xinitrc):
		os.rename(xinitrc, "{}.bak".format(xinitrc))
	file = open(xinitrc, "w")
	file.write(newXinitrc)
	file.close()
	call("startx")

def cleanup():
	global _home
	xinitrc = "{}/.xinitrc".format(_home)
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

def printFiles(files, window):
	global _cursorPos

	line = 0
	window.clear()
	for file in files:
		if line == _cursorPos:
			window.addstr(line, 0, file, curses.color_pair(1))
			length = len(file)
		else:
			window.addstr(line, 0, file)
		line += 1
	# Refresh only the print window
	refreshOne(window)

def screenLayout():
	global _windows
	curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
	heightRemaining = curses.LINES

	# Title bar
	title_x = 0
	title_y = 0
	title_h = 1
	title = "MedCurses"

	titlebar = curses.newwin(title_h, curses.COLS, title_y, title_x)

	titlebar.bkgd(' ', curses.color_pair(1))
	titlebar.addstr(0, center(title), title)

	_windows.append(titlebar)
	refreshOne(titlebar)

	# File list
	filelist = curses.newwin(curses.LINES - title_h, curses.COLS, 2, 0)
	filelist.keypad(True)
	
	_windows.append(filelist)

	# Instructions
	

	# Directory Input
	# TODO

def center(string):
	return (curses.COLS // 2) - (len(string) // 2)

def refreshAll():
	global _windows
	for window in _windows:
		window.refresh()

def refreshOne(window):
	window.noutrefresh()
	curses.doupdate()

curses.wrapper(main)
