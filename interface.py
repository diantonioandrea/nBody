#!/usr/bin/env python3
import pickle
import os
import numpy as np
import colorama

# PHYSICS

import physics

# GRAPHICS

import graphics
colorama.init()


bodies = []
computedFlag = False

if not os.path.exists(str(os.getcwd()) + "/data"):
    os.makedirs(str(os.getcwd()) + "/data")

print(graphics.colorPrint("N-BODY", graphics.bcolors.BLUE))
print(graphics.colorPrint("N-body orbits visualization program with CLI", graphics.bcolors.BLUE))
print(graphics.colorPrint("Developed by Andrea Di Antonio", graphics.bcolors.BLUE))
print(graphics.colorPrint("\nExit with Ctrl+c", graphics.bcolors.BLUE))

while True: # interface
	try:
		command = " ".join(input("\nN-BODY command: ").split()).lower()
		instructions = command.split(" ")

		if len(instructions) in [1, 2]:
			if instructions[0] == "list":
				if len(bodies) == 0:
					print(graphics.colorPrint("\n\tError: not enough bodies", graphics.bcolors.RED))
					continue

				for b in bodies:
					print("\n\tBody " + str(bodies.index(b)) + ": ")
					print(b)

					if len(bodies) > 1:
						print()
						for db in bodies:
							if b != db:
								print("\tDistance from body " + str(bodies.index(db)) + ": " + str(round(b.distance(db), 4)))
				
				continue

			elif instructions[0] == "show":
				if not computedFlag:
					print(graphics.colorPrint("\n\tError: no computed orbits", graphics.bcolors.RED))
					continue

				fastFlag = False

				if len(instructions) == 2:
					if instructions[1] == "now":
						fastFlag = True

				graphics.plot(bodies, fastFlag)
				continue

			elif instructions[0] == "clear":
				bodies = []
				computedFlag = False

				print(graphics.colorPrint("\n\tCleared bodies list", graphics.bcolors.GREEN))
				continue
		
		if len(instructions) == 2:
			if instructions[0] == "new" and instructions[1] == "body":
				try: 
					mass = float(input("\nM: "))

					if mass < 0:
						print(graphics.colorPrint("\n\tNegative mass will repulse positive mass", graphics.bcolors.GREEN))

					pos = np.array([.0, .0, .0])
					print()
					for p in range(3):
						pos[p] = float(input("X_" + str(p + 1) + ": "))

					spd = np.array([.0, .0, .0])
					print()
					for s in range(3):
						spd[s] = float(input("V_" + str(s + 1) + ": "))
					
					bodies.append(physics.body(mass, pos, spd))
					print(graphics.colorPrint("\n\tNew body added", graphics.bcolors.GREEN))
					continue
				
				except(ValueError):
					print(graphics.colorPrint("\n\tError: value error", graphics.bcolors.RED))
					continue
			
			elif instructions[0] == "dump":
				dumpFile = open("data/" + instructions[1] + ".pck", "wb")
				pickle.dump(bodies, dumpFile)
				dumpFile.close()

				print(graphics.colorPrint("\n\tDumped data to file: " + instructions[1] + ".pck", graphics.bcolors.GREEN))
				continue
				
			elif instructions[0] == "load":
				try:
					loadFile = open("data/" + instructions[1] + ".pck", "rb")
					bodies = pickle.load(loadFile)
					loadFile.close()
					computedFlag = False
					
					print(graphics.colorPrint("\n\tLoaded data from file: " + instructions[1] + ".pck", graphics.bcolors.GREEN))
					continue

				except(FileNotFoundError):
					print(graphics.colorPrint("\n\tError: file not found", graphics.bcolors.RED))
					continue

		elif len(instructions) == 3:
			if instructions[0] == "compute":
				if len(bodies) < 2:
					print(graphics.colorPrint("\n\tError: not enough bodies", graphics.bcolors.RED))
					continue

				try:
					computeTime = float(instructions[1])
					stepsNumber = int(instructions[2])
				
				except(ValueError):
					print(graphics.colorPrint("\n\tError: value error", graphics.bcolors.RED))
					continue
				
				bodies = physics.computeOrbits(bodies, computeTime, stepsNumber)
				computedFlag = True
				continue
		
		print(graphics.colorPrint("\n\tError: syntax error", graphics.bcolors.RED))

	except(KeyboardInterrupt):
		print()
		break

	except(EOFError):
		continue