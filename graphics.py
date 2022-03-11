import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math

class bcolors:
	GREEN = '\033[92m'
	BLUE = '\033[94m'
	CYAN = '\033[96m'
	RED = '\033[91m'
	ENDC = '\033[0m'

def updateLines(num, trajectories, lines, skips):
	for line, trajectory in zip(lines, trajectories):
		line.set_data(trajectory[:num * skips, :2].T)
		line.set_3d_properties(trajectory[:num * skips, 2])		
	return lines

def findLimits(bodies: list, axis: int):
	minValue = 0
	maxValue = 0

	for b in bodies:
		for h in b.history:
			if h[axis] < minValue:
				minValue = h[axis]

			if h[axis] > maxValue:
				maxValue = h[axis]

	if minValue == maxValue:
		minValue -= 1
		maxValue += 1
	
	return (minValue, maxValue)

def colorPrint(string: str, color: str):
	return color + string + '\033[0m'

def plot(bodies: list, fastFlag: bool):
	fig = plt.figure()
	ax = fig.add_subplot(projection='3d')
	ax.set_title('N-body problem with ' + str(len(bodies)) + ' bodies')

	ax.set(xlim3d=findLimits(bodies, 0), xlabel='X')
	ax.set(ylim3d=findLimits(bodies, 1), ylabel='Y')
	ax.set(zlim3d=findLimits(bodies, 2), zlabel='Z')

	if not fastFlag:

		trajectories = [b.history for b in bodies]
		lines = [ax.plot([], [], [])[0] for _ in trajectories]

		stepsNumber = len(bodies[0].history)
		skips = 2 * int(math.log(stepsNumber, 10)) + 1

		framesNumber = int(stepsNumber / skips)
	
	else:

		for b in bodies:
			ax.plot3D(b.history[:, 0], b.history[:, 1], b.history[:, 2])

	for l in ax.lines:
		l.set_label('Body ' + str(ax.lines.index(l)))

	ax.legend()

	print(colorPrint("\n\tShowing orbits for " + str(len(bodies)) + " bodies", bcolors.GREEN))

	if not fastFlag:
		ani = animation.FuncAnimation(fig, updateLines, frames=framesNumber, fargs=(trajectories, lines, skips), interval=1, repeat=False)

	plt.show()