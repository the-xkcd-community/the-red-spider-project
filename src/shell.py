#!/usr/bin/python
import os
import sys
import stat
import subprocess
def listDir(args, showHidden=False):
	contents = os.listdir(os.getcwd())
	if contents:
		sys.stdout.write('Here there is:\n')
		for item in contents:
			if item[0] != '.' or showHidden:
				if os.path.isfile(item):
					sys.stdout.write('\t' + item + '\n')
				if os.path.islink(item):
					sys.stdout.write('\tA portal entitled "' + item + '"\n')
		sys.stdout.write('Available exits are:\n')
		if os.getcwd() != '/':
			sys.stdout.write('\tBack up\n')
		for item in contents:
			if item[0] != '.' or showHidden:
				if os.path.isdir(item):
					sys.stdout.write('\t' + item + '\n')

def statFile(args):
	fileName = ''.join(args)
	sys.stdout.write('Upon examining ' + fileName + ' you discover it to be ')
	if os.path.islink(fileName):
		sys.stdout.write('a portal enscribed ' + os.readlink(fileName) + '.\n')
	elif os.path.isdir(fileName):
		sys.stdout.write('a doorway\n')
	elif os.path.isfile(fileName):
		sys.stdout.write('an object weighing around ' + str(os.path.getsize(fileName)/1000) + 'kg.\n')
		stats = os.stat(fileName)
		if stats.st_mode & stat.S_IXUSR:
			sys.stdout.write('It looks like you could probably operate ' + fileName + ' if you wanted to.\n')
	else:
		sys.stdout.write('an unknown item.\n')

def run(args):
	fileName = ''.join(args)
	sys.stdout.write('You try to operate ' + fileName + ':\n')
	subprocess.call(os.path.abspath(fileName))

def quitShell(args):
	print 'Goodbye!'
	exit()

def changeDir(args):
	pathName = ''.join(args)
	try:
		os.chdir(pathName)
		sys.stdout.write('You are now in ' + os.getcwd() + '.\n')
	except:
		sys.stdout.write('You bump into a wall when you try to get to ' + pathName + '.\n')

print 'Welcome to compsoc'
while True:
	input = raw_input('What would you like to do?\n').split(' ')
	command = input[0]
	del input[0]
	arguments = input
	commandList = {
			'exit': quitShell,
			'look': listDir,
			'search': lambda a:listDir(arguments,True),
			'move': changeDir,
			'go': changeDir,
			'examine': statFile,
			'operate': run
	}
	if command in commandList:
		commandList[command](arguments)
	else:
		print 'Um, whut?'
