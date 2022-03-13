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
computedFlag = False

while True: # interface
	try:
		hostName = "N-BODY"
		computedFlag = utils.checkOrbits(bodies)

		try:
			if len(bodies) > 0:
				hostName = hostName.replace("N", str(len(bodies)))
		
		except:
			pass

		command = " ".join(input("\n" + user + "@" + hostName + ": ").split()).lower()
		instructions = command.split(" ")

		# OPTIONS, SINGLE DASH [[-key1, value1], ...] AND DOUBLE DASH [--key1, ...]

		try: 
			sdOpts = []
			ddOpts = []

			for inst in instructions:
				if "--" in inst:
					ddOpts.append(inst)
				
				elif "-" in inst:
					try:
						if type(float(inst)) == float: # avoids picking negative numbers
							pass

					except(ValueError):
						sdOpts.append([inst, instructions[instructions.index(inst) + 1]])

		except(IndexError):
			print(utils.colorPrint("\n\tError: syntax error", utils.bcolors.RED))
			continue

		if len(instructions) > 0:

			# EXIT PROGRAM

			if instructions[0] in ["exit", "quit"]:
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
					print(utils.colorPrint("\n\tBody " + str(bodies.index(b)) + ": ", utils.bcolors.BLUE))
					print(b.__str__(bodies))
				
				continue
		
			# CLEAR BODIES LIST

			elif instructions[0] == "clear":
				bodies = []
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
				
				bodies = physics.computeOrbits(bodies, sdOptions=sdOpts, ddOptions=ddOpts)
				continue

			# PLOT COMPUTED ORBITS

			elif instructions[0] == "show":
				if not computedFlag:
					print(utils.colorPrint("\n\tError: no computed orbits", utils.bcolors.RED))
					continue

				graphics.plot(bodies, sdOptions=sdOpts, ddOptions=ddOpts)
				continue

			# DUMP BODIES LIST TO A .pck FILE
			
			elif instructions[0] == "dump":
				utils.dump(bodies, sdOptions=sdOpts) # dumps to a .pck file
				continue

			# LOAD BODIES LIST FROM A .pck OR .csv FILE
				
			elif instructions[0] == "load":
				loadBodies, loadExt = utils.load(sdOptions=sdOpts, ddOptions=ddOpts, noneObject=[])

				if loadExt == ".pck":
					bodies = loadBodies

				elif loadExt == ".csv":
					bodies = []

					for csvLines in loadBodies:
						newBody = physics.body(csvLines)

						if newBody.creationFlag:
							bodies.append(newBody)
				
				if len(loadBodies) > 0:
					print(utils.colorPrint("\tLoaded " + str(len(loadBodies)) + " bodies", utils.bcolors.GREEN))
				continue
		
		print(utils.colorPrint("\n\tError: syntax error", utils.bcolors.RED))

	except(KeyboardInterrupt):
		print() # needed space
		continue

	except(EOFError):
		continue