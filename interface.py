#!/usr/bin/env python3
import os
import numpy as np
import colorama

# PHYSICS

import physics

# GRAPHICS

import graphics

# UTILS

import utils
colorama.init()


bodies = []
computedFlag = False

if not os.path.exists(str(os.getcwd()) + "/data"):
    os.makedirs(str(os.getcwd()) + "/data")

print(utils.colorPrint("N-BODY", utils.bcolors.BLUE))
print(utils.colorPrint("N-body orbits visualization program with CLI", utils.bcolors.BLUE))
print(utils.colorPrint("Developed by Andrea Di Antonio", utils.bcolors.BLUE))
print(utils.colorPrint("\nType \'help\' if needed", utils.bcolors.BLUE))

try:
	user = os.getlogin()

except:
	user = "user"

while True: # interface
	try:
		command = " ".join(input("\n" + user + "@N-BODY: ").split()).lower()
		instructions = command.split(" ")

		# OPTIONS, SINGLE DASH [[-key1, value1], ...] AND DOUBLE DASH [--key1, ...]

		try: 
			sdOpts = []
			ddOpts = []

			for inst in instructions:
				if "--" in inst:
					ddOpts.append(inst)
				
				elif "-" in inst:
					sdOpts.append([inst, instructions[instructions.index(inst) + 1]])

		except(IndexError):
			print(utils.colorPrint("\n\tError: syntax error", utils.bcolors.RED))
			continue

		if len(instructions) > 0:

			# EXIT PROGRAM

			if instructions[0] in ["exit", "quit"]:
				break

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
					print(b)

					if len(bodies) > 1:
						print() # needed space
						for db in bodies:
							if b != db:
								print("\tDistance from body " + str(bodies.index(db)) + ": " + str(round(b.distance(db), 4)))
				
				continue

			# PLOT COMPUTED ORBITS

			elif instructions[0] == "show":
				if not computedFlag:
					print(utils.colorPrint("\n\tError: no computed orbits", utils.bcolors.RED))
					continue

				graphics.plot(bodies, sdOptions=sdOpts, ddOptions=ddOpts)
				continue

			# CLEAR BODIES LIST

			elif instructions[0] == "clear":
				bodies = []
				computedFlag = False
				print(utils.colorPrint("\n\tCleared bodies list", utils.bcolors.GREEN))
				continue

			# CREATE A NEW BODY
		
			elif instructions[0] == "newbody":
				newBody = physics.body()

				if newBody.creationFlag:
					bodies.append(newBody)
				continue

			# DUMP BODIES LIST TO A FILE
			
			elif instructions[0] == "dump":
				utils.dump(bodies, sdOptions=sdOpts)
				continue

			# LOAD BODIES LIST FROM A FILE
				
			elif instructions[0] == "load":
				bodies = utils.load(sdOptions=sdOpts)
				computedFlag = False
				continue

			# COMPUTE ORBITS

			elif instructions[0] == "compute":
				if len(bodies) < 2:
					print(utils.colorPrint("\n\tError: not enough bodies", utils.bcolors.RED))
					continue
				
				bodies = physics.computeOrbits(bodies, sdOptions=sdOpts, ddOptions=ddOpts)
				computedFlag = True
				continue
		
		print(utils.colorPrint("\n\tError: syntax error", utils.bcolors.RED))

	except(KeyboardInterrupt):
		print() # needed space
		continue

	except(EOFError):
		continue