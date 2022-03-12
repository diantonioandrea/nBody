import matplotlib.pyplot as plt
import matplotlib.animation as animation

from utils import colorPrint, bcolors

# PLOTS

def updateLines(num, trajectories, lines, speed):

	# UPDATE LINES BY "SPEED" AT A TIME

	for line, trajectory in zip(lines, trajectories):
		line.set_data(trajectory[:num * speed, :2].T)
		line.set_3d_properties(trajectory[:num * speed, 2])		
	return lines

def findLimits(bodies: list, axis: int):

	# FIND PLOT LIMITS FOR X, Y, Z BEFORE PLOTTING

	minValue = 0
	maxValue = 0

	for b in bodies:
		for h in b.trajectory:
			if h[axis] < minValue:
				minValue = h[axis]

			if h[axis] > maxValue:
				maxValue = h[axis]

	if minValue == maxValue:
		minValue -= 1
		maxValue += 1
	
	return (minValue, maxValue)

def plot(bodies: list, sdOptions=[], ddOptions=[]):

	# DEFAULTS

	speed = 1
	instantPlot = False

	# OPTIONS LOADING

	for opts in sdOptions:
		if opts[0] == "-sp": # SPEED
			speed = abs(int(opts[1]))
	
	for opts in ddOptions:
		if opts == "--now": # FAST PLOTTING
			instantPlot = True

	fig = plt.figure()
	ax = fig.add_subplot(projection='3d')
	ax.set_title('N-body problem with ' + str(len(bodies)) + ' bodies')

	ax.set(xlim3d=findLimits(bodies, 0), xlabel='X')
	ax.set(ylim3d=findLimits(bodies, 1), ylabel='Y')
	ax.set(zlim3d=findLimits(bodies, 2), zlabel='Z')

	if not instantPlot:
		trajectories = [b.trajectory for b in bodies]
		lines = [ax.plot([], [], [])[0] for _ in trajectories]

		framesNumber = int(len(bodies[0].trajectory) / speed)
	
	else:
		for b in bodies:
			ax.plot3D(b.trajectory[:, 0], b.trajectory[:, 1], b.trajectory[:, 2])

	for l in ax.lines:
		l.set_label('Body ' + str(ax.lines.index(l)))

	ax.legend()

	print(colorPrint("\n\tShowing orbits for " + str(len(bodies)) + " bodies", bcolors.GREEN))

	if not instantPlot:
		ani = animation.FuncAnimation(fig, updateLines, frames=framesNumber, fargs=(trajectories, lines, speed), interval=1, repeat=False)

	plt.show()