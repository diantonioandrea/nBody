import numpy as np
import time

from utils import checkOptions, colorPrint, bcolors

class body:

	def __init__(self):
		self.creationFlag = True

		try: 
			self.mass = float(input("\n\tMass, M: "))

			if self.mass < 0:
				print(colorPrint("\n\tNegative mass will repulse positive mass", bcolors.GREEN))

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

			print(colorPrint("\n\tNew body created", bcolors.GREEN))

		except(ValueError):
			print(colorPrint("\n\tError: value error", bcolors.RED))
			self.creationFlag = False

		except(KeyboardInterrupt):
			print() # needed space
			print(colorPrint("\n\tCancelled", bcolors.RED))
			self.creationFlag = False

		except(EOFError):
			print(colorPrint("\n\tCancelled", bcolors.RED))
			self.creationFlag = False

		except:
			print(colorPrint("\n\tError", bcolors.RED))
			self.creationFlag = False
	
	def __str__(self) -> str:
		selfString = "\n\tMass, M: " + str(self.mass)
		selfString += "\n\tPosition, X: " + str(self.coordinates[0])
		selfString += "\n\tSpeed, S: " + str(self.coordinates[1]) + " -> " + str(round(np.linalg.norm(self.coordinates[1]), 4))

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

	if not checkOptions(rOptions, sdOpts=sdOptions, ddOpts=ddOptions):
		return bodies

	# OPTIONS LOADING

	for opts in sdOptions:
		if opts[0] == "-st": # number of steps
			stepsNumber = abs(int(opts[1]))

			if stepsNumber == 0:
				print(colorPrint("\n\tError: steps error", bcolors.GREEN))
				return bodies

		if opts[0] == "-t": # computation time
			computeTime = float(opts[1])

	stepsSize = computeTime / stepsNumber
	forceArray = np.zeros_like(np.arange(3 * len(bodies)).reshape(len(bodies), 3), dtype=float)

	if stepsSize < 0:
		print(colorPrint("\n\tComputing (backwards) " + str(stepsNumber) + " steps with size " + str(abs(stepsSize)) + " for " + str(len(bodies)) + " bodies...", bcolors.GREEN))
	else:
		print(colorPrint("\n\tComputing " + str(stepsNumber) + " steps with size " + str(stepsSize) + " for " + str(len(bodies)) + " bodies...", bcolors.GREEN))

	computeStart = time.time()

	for _ in range(stepsNumber):
		for i in range(len(bodies)):
			for j in range(len(bodies)):
				if j != i:
					forceArray[i] += newton(bodies[i], bodies[j]) # calculate newton's force force bodies i, j while i != j
			
		for k in range(len(bodies)):
			bodies[k].update(forceArray[k], stepsSize)
			forceArray[k] *= .0 # forceArray "reset"

	computeEnd = time.time()
	
	print(colorPrint("\tDone, elapsed time: " + str(round(computeEnd - computeStart, 4)) + " secoonds", bcolors.GREEN))

	return bodies
