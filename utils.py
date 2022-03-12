import pickle
import numpy as np

# COLORS

class bcolors:
	GREEN = '\033[92m'
	BLUE = '\033[94m'
	CYAN = '\033[96m'
	RED = '\033[91m'
	ENDC = '\033[0m'

def colorPrint(string: str, color: str):
	return color + string + '\033[0m'

def checkOptions(rOpts: list, sdOpts=[], ddOpts=[]):
	for opts in rOpts:
		if opts not in ddOpts and "--" in opts:
			print(colorPrint("\n\tError: not enough options", bcolors.RED))
			return False
	
	for opts in rOpts:
		if opts not in [col[0] for col in sdOpts] and "-" in opts and "--" not in opts:
			print(colorPrint("\n\tError: not enough options", bcolors.RED))
			return False
	
	return True

def dump(tbDumped, sdOptions=[]):
	rOptions = ["-o"]

	if not checkOptions(rOptions, sdOpts=sdOptions):
		return None

	path = "data/"

	for opts in sdOptions:
		if opts[0] == "-o": # output file
			filename = opts[1] + ".pck"

		elif opts[0] == "-p": # path (until folder before)
			path = opts[1]

	try:
		dumpFile = open("data/" + filename, "wb")
	
	except(FileNotFoundError):
		print(colorPrint("\n\tError: file or directory not found", bcolors.RED))
		return None

	pickle.dump(tbDumped, dumpFile)
	dumpFile.close()

	print(colorPrint("\n\tDumped data to file: " + filename, bcolors.GREEN))

def load(sdOptions=[]):
	rOptions = ["-i"]

	if not checkOptions(rOptions, sdOpts=sdOptions):
		return None

	path = "data/"

	for opts in sdOptions:
		if opts[0] == "-i": # input file
			filename = opts[1] + ".pck"

		elif opts[0] == "-p": # path (until folder before)
			path = opts[1]

	try:
		loadFile = open("data/" + filename, "rb")
	
	except(FileNotFoundError):
		print(colorPrint("\n\tError: file or directory not found", bcolors.RED))
		return None

	loadContent = pickle.load(loadFile)
	loadFile.close()

	print(colorPrint("\n\tLoaded data from file: " + filename, bcolors.GREEN))

	return loadContent