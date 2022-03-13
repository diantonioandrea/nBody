import pickle, colorama

# COLORS

colorama.init()
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

def checkOrbits(bodies: list):
	try:
		for b in bodies:
			if len(b.trajectory) > 1:
				return True
	
	except:
		pass

	return False

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
		dumpFile = open(path + filename, "wb")
	
	except(FileNotFoundError):
		print(colorPrint("\n\tError: file or directory not found", bcolors.RED))
		return None

	pickle.dump(tbDumped, dumpFile)
	dumpFile.close()

	print(colorPrint("\n\tDumped data to file: " + filename, bcolors.GREEN))

def load(sdOptions=[], ddOptions=[], noneObject=None):
	rOptions = ["-i"]

	# DEFAULTS

	path = "data/"
	ext = ".pck"
	rMode = "rb"

	if not checkOptions(rOptions, sdOpts=sdOptions):
		return noneObject, ext

	for opts in sdOptions:
		if opts[0] == "-i": # input file
			filename = opts[1]

		elif opts[0] == "-p": # path (until folder before)
			path = opts[1]

	for opts in ddOptions:
		if opts == "--csv": # csv files
			ext = ".csv"
			rMode = "r"

	filename += ext

	try:
		loadFile = open(path + filename, rMode)
	
	except(FileNotFoundError):
		print(colorPrint("\n\tError: file or directory not found", bcolors.RED))
		return noneObject, ext

	if ext == ".pck":
		loadContent = pickle.load(loadFile)
		loadFile.close()

		print(colorPrint("\n\tLoaded data from file: " + filename, bcolors.GREEN))

	elif ext == ".csv":
		loadContent = loadFile.readlines()
		loadFile.close()

		print(colorPrint("\n\tLoaded data from file: " + filename, bcolors.GREEN))

	return loadContent, ext

def help():
	print(colorPrint("\n\tN-BODY HELP", bcolors.BLUE))

	print(colorPrint("\n\texit, quit", bcolors.BLUE))
	print("\t\tExits from program")

	print(colorPrint("\n\tlist", bcolors.BLUE))
	print("\t\tLists current bodies")

	print(colorPrint("\n\tclear", bcolors.BLUE))
	print("\t\tClears current bodies")

	print(colorPrint("\n\tnew", bcolors.BLUE))
	print("\t\tCreates a new body")

	print(colorPrint("\n\tcompute", bcolors.BLUE))
	print("\t\tComputes orbits")
	print("\n\t\tAvailable options:")
	print("\n\t\t-t N, time: sets N as computation time, " + colorPrint("required", bcolors.RED))
	print("\t\t-st N, steps: sets N as steps number, " + colorPrint("required", bcolors.RED))

	print(colorPrint("\n\tshow", bcolors.BLUE))
	print("\t\tPlots computed orbits")
	print("\n\t\tAvailable options:")
	print("\t\t-sp N, speed: sets N as plotting speed")
	print("\t\t-rn RANGESTART:RANGEEND, range: plots only bodies in this range")
	print("\n\t\t--now: instantly plots computed orbits, ignores -sp")

	print(colorPrint("\n\tdump", bcolors.BLUE))
	print("\t\tDumps current bodies to a specified file")
	print("\n\t\tAvailable options:")
	print("\n\t\t-o FILENAME, output: specifies file without any extensions, " + colorPrint("required", bcolors.RED))
	print("\t\t-p PATH, path: sets PATH as PATH/FILENAME")

	print(colorPrint("\n\tload", bcolors.BLUE))
	print("\t\tLoads bodies from a specified file previously dumped")
	print("\n\t\tAvailable options:")
	print("\n\t\t-i FILENAME, input: specifies file without any extensions, " + colorPrint("required", bcolors.RED))
	print("\t\t-p PATH, path: sets PATH as PATH/FILENAME")
	print("\t\t--csv: loads a .csv file with line format M,X0,X1,X2,S0,S1,S2(,LABEL)")
	