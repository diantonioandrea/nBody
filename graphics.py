import matplotlib.pyplot as plt
import matplotlib.animation as animation

import utils

# PLOTS

def updateLines(num: int, trajectories: list, lines: list, speed: int) -> list:

	# UPDATE LINES BY "SPEED" AT A TIME

	for line, trajectory in zip(lines, trajectories):
		line.set_data(trajectory[:num * speed, :2].T)
		line.set_3d_properties(trajectory[:num * speed, 2])

	return lines

def findLimits(orbits: list, axis: int) -> tuple:

	# FIND PLOT LIMITS FOR X, Y, Z BEFORE PLOTTING

	minValue = 0
	maxValue = 0

	for b in orbits:
		for h in b.trajectory:
			if h[axis] < minValue:
				minValue = h[axis]

			if h[axis] > maxValue:
				maxValue = h[axis]

	if minValue == maxValue:
		minValue -= 1
		maxValue += 1
	
	return (minValue, maxValue)

def plot(plotOrbits: list, sdOptions=[], ddOptions=[]) -> None:
	# DEFAULTS

	speed = 1
	instantPlot = False
	rangeFlag = False
	rangeString = ""
	rStart = 0
	rEnd = len(plotOrbits)

	# OPTIONS LOADING

	for opts in sdOptions:
		try:
			if opts[0] == "-sp": # speed
				speed = abs(int(opts[1]))
				print(utils.colorPrint("\n\tSpeed set with value: " + str(speed), utils.bcolors.GREEN))

		except(ValueError):
			print(utils.colorPrint("\n\tError: syntax error", utils.bcolors.RED))

		if opts[0] == "-rn":
			try:
				rStart = int(opts[1].split(":")[0])
				rEnd = int(opts[1].split(":")[1])

				rangeString = opts[1]
				rangeFlag = True
			
			except(IndexError, ValueError):
				print(utils.colorPrint("\n\tError: syntax error, plotting all orbits", utils.bcolors.RED))

	for opts in ddOptions:
		if opts == "--now": # FAST PLOTTING
			instantPlot = True

	if rangeFlag:
		if 0 <= rStart < len(plotOrbits) and 0 < rEnd <= len(plotOrbits) and rStart < rEnd:
			orbits = plotOrbits[rStart:rEnd]
		
		else:
			orbits = plotOrbits
			print(utils.colorPrint("\n\tError: invalid range, plotting all orbits", utils.bcolors.RED))
	
	else:
		orbits = plotOrbits

	fig = plt.figure()
	ax = fig.add_subplot(projection='3d')
	ax.set_title('N-body problem with ' + str(len(orbits)) + ' orbits')

	ax.set(xlim3d=findLimits(orbits, 0), xlabel='X')
	ax.set(ylim3d=findLimits(orbits, 1), ylabel='Y')
	ax.set(zlim3d=findLimits(orbits, 2), zlabel='Z')

	if not instantPlot:
		trajectories = [b.trajectory for b in orbits]
		lines = [ax.plot([], [], [])[0] for _ in trajectories]

		framesNumber = int(len(orbits[0].trajectory) / speed)

	else:
		for b in orbits:
			ax.plot3D(b.trajectory[:, 0], b.trajectory[:, 1], b.trajectory[:, 2])

	for l in ax.lines:
		if orbits[ax.lines.index(l)].label == "":
			l.set_label('Body ' + str(ax.lines.index(l)))
	
		else:
			l.set_label(orbits[ax.lines.index(l)].label)

	ax.legend()

	if not rangeFlag:
		print(utils.colorPrint("\n\tShowing orbits for " + str(len(orbits)) + " orbits", utils.bcolors.GREEN))
	
	else:
		print(utils.colorPrint("\n\tShowing orbits for " + str(len(orbits)) + " orbits in range " + rangeString, utils.bcolors.GREEN))

	if not instantPlot:
		ani = animation.FuncAnimation(fig, updateLines, frames=framesNumber, fargs=(trajectories, lines, speed), interval=1, repeat=False)

	plt.show()