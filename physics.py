import numpy as np
import time
import sys

import graphics

class body:

	def __init__(self, mass: float, position: np.array, speed: np.array):
		self.mass = mass
		self.coordinates = np.array([position, speed])
		self.history = np.array([position])
	
	def __str__(self) -> str:
		selfString = "\n\tMass: " + str(self.mass)
		selfString += "\n\tX: " + str(self.coordinates[0])
		selfString += "\n\tV: " + str(self.coordinates[1])

		return selfString

	def distance(self, other) -> float:
		return np.linalg.norm(self.coordinates[0] - other.coordinates[0])

	def update(self, force: np.array, dt: float):
		self.coordinates[1] += force / self.mass * dt
		self.coordinates[0] += self.coordinates[1] * dt

		self.history = np.vstack([self.history, self.coordinates[0]])

def newton(fb: body, sb: body) -> np.array:
	return fb.mass * sb.mass / (fb.distance(sb) ** 3) * (sb.coordinates[0] - fb.coordinates[0])

def computeOrbits(bodies: list, computeTime: float, stepsNumber: int):
	stepsSize = computeTime / stepsNumber

	computeStart = time.time()

	forceVector = np.zeros_like(np.arange(3 * len(bodies)).reshape(len(bodies), 3), dtype=float)

	for _ in range(stepsNumber):
		for i in range(len(bodies)):
			for j in range(len(bodies)):
				if j != i:
					forceVector[i] += newton(bodies[i], bodies[j])
			
		for k in range(len(bodies)):
			bodies[k].update(forceVector[k], stepsSize)
			forceVector[k] *= .0

	computeEnd = time.time()
	
	print(graphics.colorPrint("\n\tComputed " + str(stepsNumber) + " steps with size " + str(stepsSize) + " for " + str(len(bodies)) + " bodies", graphics.bcolors.GREEN))
	print(graphics.colorPrint("\tElapsed time: " + str(round(computeEnd - computeStart, 4)) + " secoonds", graphics.bcolors.GREEN))

	return bodies
