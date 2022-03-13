import csv
import numpy as np
import time

import utils

class body:

	def __init__(self, csvLine=""):
		self.creationFlag = True

		if csvLine != "": # creates body from a .csv file

			# FORMAT: M,X0,X1,X2,S0,S1,S2(,LABEL)

			csvData = csvLine.split(",")

			try:
				self.mass = float(csvData[0])

				pos = np.array([float(csvData[1]), float(csvData[2]), float(csvData[3])])
				spd = np.array([float(csvData[4]), float(csvData[5]), float(csvData[6])])

				self.coordinates = np.array([pos, spd])
				self.trajectory = np.array([pos])

			except(IndexError):
				print(utils.colorPrint("\n\tError: csv error", utils.bcolors.RED))
				self.creationFlag = False

			except(ValueError):
				print(utils.colorPrint("\n\tError: value error, check csv file", utils.bcolors.RED))
				self.creationFlag = False

			except:
				print(utils.colorPrint("\n\tError, check code or csv file", utils.bcolors.RED))
				self.creationFlag = False

			try:
				self.label = csvData[7].replace("\n", "") # label not required

			except(IndexError):
				self.label = ""

		else:
			try: 
				self.mass = float(input("\n\tMass, M: "))

				if self.mass < 0:
					print(utils.colorPrint("\n\tPay attention with negative masses", utils.bcolors.RED))

				pos = np.array([.0, .0, .0])
				spd = np.array([.0, .0, .0])

				print() # needed space
				for p in range(3):
					pos[p] = float(input("\tPosition, X_" + str(p + 1) + ": "))

				print() # needed space
				for s in range(3):
					spd[s] = float(input("\tSpeed, S_" + str(s + 1) + ": "))

				self.coordinates = np.array([pos, spd])
				self.trajectory = np.array([pos])

				self.label = str(input("\n\tLabel (can be empty): "))

				print(utils.colorPrint("\n\tNew body created", utils.bcolors.GREEN))

			except(ValueError):
				print(utils.colorPrint("\n\tError: value error", utils.bcolors.RED))
				self.creationFlag = False

			except(KeyboardInterrupt):
				print() # needed space
				print(utils.colorPrint("\n\tCancelled", utils.bcolors.RED))
				self.creationFlag = False

			except(EOFError):
				print(utils.colorPrint("\n\tCancelled", utils.bcolors.RED))
				self.creationFlag = False

			except:
				print(utils.colorPrint("\n\tError: unknown error", utils.bcolors.RED))
				self.creationFlag = False
	
	def __str__(self, others=[]) -> str:
		selfString = "\n\t\tMass, M: " + str(self.mass)

		selfString += "\n\t\tPosition, X: "

		for x in self.coordinates[0]:
			selfString += str(round(x, 4)) + " "

		selfString += "\n\t\tSpeed, S: "

		for s in self.coordinates[1]:
			selfString += str(round(s, 4)) + " "
		
		selfString += "-> " + str(round(np.linalg.norm(self.coordinates[1]), 4))

		if len(others) > 1:
			selfString += "\n"

			for ob in others:
				if self != ob:
					selfString += "\n\t\tDistance from body " + str(others.index(ob)) + ": " + str(round(self.distance(ob), 4))

		return selfString

	def distance(self, other) -> float:
		return np.linalg.norm(self.coordinates[0] - other.coordinates[0])

	def update(self, force: np.array, dt: float):
		self.coordinates[1] += force / self.mass * dt
		self.coordinates[0] += self.coordinates[1] * dt

		self.trajectory = np.vstack([self.trajectory, self.coordinates[0]])

def newton(fb: body, sb: body) -> np.array:
	return fb.mass * sb.mass / (fb.distance(sb) ** 3) * (sb.coordinates[0] - fb.coordinates[0])

def computeOrbits(bodies: list, sdOptions=[], ddOptions=[]):
	rOptions = ["-t", "-st"] # requires time and steps

	if not utils.checkOptions(rOptions, sdOpts=sdOptions, ddOpts=ddOptions):
		return bodies

	# OPTIONS LOADING

	for opts in sdOptions:
		try:
			if opts[0] == "-st": # number of steps
				stepsNumber = abs(int(opts[1]))

			if opts[0] == "-t": # computation time
				computeTime = float(opts[1])
		
		except(ValueError):
			print(utils.colorPrint("\n\tError: no computed orbits", utils.bcolors.RED))
			return bodies

	if stepsNumber == 0:
		print(utils.colorPrint("\n\tError: steps error", utils.bcolors.RED))
		return bodies

	stepsSize = computeTime / stepsNumber
	forceArray = np.zeros_like(np.arange(3 * len(bodies)).reshape(len(bodies), 3), dtype=float)

	if stepsSize < 0:
		print(utils.colorPrint("\n\tComputing (backwards) " + str(stepsNumber) + " steps with size " + str(abs(stepsSize)) + " for " + str(len(bodies)) + " bodies...", utils.bcolors.GREEN))
	else:
		print(utils.colorPrint("\n\tComputing " + str(stepsNumber) + " steps with size " + str(stepsSize) + " for " + str(len(bodies)) + " bodies...", utils.bcolors.GREEN))

	computeStart = time.time()

	try:

		for steps in range(stepsNumber):
			for i in range(len(bodies)):
				for j in range(len(bodies)):
					if j != i:
						forceArray[i] += newton(bodies[i], bodies[j]) # calculate newton's force for bodies i, j while i != j
				
			for k in range(len(bodies)):
				bodies[k].update(forceArray[k], stepsSize)
				forceArray[k] *= .0 # forceArray "reset"

		computeEnd = time.time()
		
		print(utils.colorPrint("\tDone, elapsed time: " + str(round(computeEnd - computeStart, 4)) + " seconds", utils.bcolors.GREEN))

	except(KeyboardInterrupt):
		computeEnd = time.time()
		print() # needed space
		print(utils.colorPrint("\tStopped, elapsed time: " + str(round(computeEnd - computeStart, 4)) + " seconds", utils.bcolors.RED))
		print(utils.colorPrint("\t" + str(steps) + " steps evaluated", utils.bcolors.RED))

	except(EOFError):
		computeEnd = time.time()
		print(utils.colorPrint("\tStopped, elapsed time: " + str(round(computeEnd - computeStart, 4)) + " seconds", utils.bcolors.RED))
		print(utils.colorPrint("\t" + str(steps) + " steps evaluated", utils.bcolors.RED))

	except(ZeroDivisionError):
		computeEnd = time.time()
		print(utils.colorPrint("\tOverlapped bodies, elapsed time: " + str(round(computeEnd - computeStart, 4)) + " seconds", utils.bcolors.RED))
		print(utils.colorPrint("\t" + str(steps) + " steps evaluated", utils.bcolors.RED))

	return bodies
