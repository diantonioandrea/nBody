import os, sys

# PHYSICS

import physics

# GRAPHICS

import graphics

# UTILS

import utils


print(utils.colorPrint("N-BODY", utils.bcolors.BLUE))
print(utils.colorPrint("N-body orbits computation visualization program with CLI written in Python", utils.bcolors.BLUE))
print(utils.colorPrint("Developed by Andrea Di Antonio", utils.bcolors.BLUE))
print(utils.colorPrint("\nType \'help\' if needed", utils.bcolors.BLUE))

try:

	if not os.path.exists(str(os.getcwd()) + "/data"):
		os.makedirs(str(os.getcwd()) + "/data")
	
except:
	print(utils.colorPrint("\n\tError: couldn't create \'data\' folder\n\tExited\n", utils.bcolors.RED))
	sys.exit(-1)

try:
	user = os.getlogin()

	if user == "":
		user = "user"

except:
	user = "user"

bodies = []
orbits = []
computedFlag = False

while True: # interface
	try:
		hostName = "N-BODY"
		computedFlag = len(orbits) > 0

		try:
			if len(bodies) > 0:
				hostName = hostName.replace("N", str(len(bodies)))
		
		except:
			pass

		instructions, sdOpts, ddOpts = utils.getCommand("\n" + user + "@" + hostName + ": ")

		if len(instructions) > 0:

			if instructions[0] == "skip": # Ctrl+C or EOF handler
				continue

			# EXIT PROGRAM

			elif instructions[0] in ["exit", "quit"]:
				sys.exit(0)

			# HELP

			elif instructions[0] == "help":
				utils.help()
				continue

			# LIST BODIES
			
			elif instructions[0] == "list":
				if len(bodies) == 0:
					print(utils.colorPrint("\n\tError: not enough bodies", utils.bcolors.RED))
					continue

				for b in bodies:
					bodyLabel = ""

					if b.label != "":
						bodyLabel = ", " + b.label

					print(utils.colorPrint("\n\tBody " + str(bodies.index(b)) + bodyLabel + ": ", utils.bcolors.BLUE))
					print(b.__str__(bodies))
				
				continue
		
			# CLEAR BODIES LIST

			elif instructions[0] == "clear":
				if "--all" in ddOpts:
					bodies = []
					orbits = []
					print(utils.colorPrint("\n\tCleared bodies and orbits list", utils.bcolors.GREEN))
					continue
				
				elif "--orbits" in ddOpts or "--bodies" in ddOpts:
					if "--orbits" in ddOpts:
						orbits = []
						print(utils.colorPrint("\n\tCleared orbits list", utils.bcolors.GREEN))

					if "--bodies" in ddOpts:
						orbits = []
						print(utils.colorPrint("\n\tCleared bodies list", utils.bcolors.GREEN))
				
					continue

			# CREATE A NEW BODY
		
			elif instructions[0] == "new":
				newBody = physics.body()

				if newBody.creationFlag:
					bodies.append(newBody)
				continue

			# COMPUTE ORBITS

			elif instructions[0] == "compute":
				if len(bodies) < 2:
					print(utils.colorPrint("\n\tError: not enough bodies", utils.bcolors.RED))
					continue
				
				orbits = physics.computeOrbits(bodies, sdOptions=sdOpts, ddOptions=ddOpts, errorReturn=orbits)
				continue

			# PLOT COMPUTED ORBITS

			elif instructions[0] == "show":
				if not computedFlag:
					print(utils.colorPrint("\n\tError: no computed orbits", utils.bcolors.RED))
					continue

				graphics.plot(orbits, sdOptions=sdOpts, ddOptions=ddOpts)
				continue

			# DUMP BODIES AND ORBITS LIST TO A .pck FILE
			
			elif instructions[0] == "dump":
				utils.dump([bodies, orbits], sdOptions=sdOpts) # dumps to a .pck file
				continue

			# LOAD BODIES AND ORBITS LIST FROM A .pck OR BODIES LIST FROM A .csv FILE
				
			elif instructions[0] == "load":
				loadContent, loadExt = utils.load(sdOptions=sdOpts, ddOptions=ddOpts, noneObject=[[], []])

				if loadExt == ".pck":
					bodies = loadContent[0]
					orbits = loadContent[1]
					
					loadColor = utils.bcolors.GREEN

				elif loadExt == ".csv":
					bodies = []
					orbits = []

					loadColor = utils.bcolors.GREEN

					for csvLines in loadContent:
						newBody = physics.body(csvLines)

						if newBody.creationFlag:
							bodies.append(newBody)
						
						else:
							loadColor = utils.bcolors.RED
							break
				
				if len(bodies) > 0:
					print(utils.colorPrint("\tLoaded " + str(len(bodies)) + " bodies", loadColor))
				continue
		
		print(utils.colorPrint("\n\tError: syntax error", utils.bcolors.RED))

	except(KeyboardInterrupt):
		print() # needed space
		continue

	except(EOFError):
		continue