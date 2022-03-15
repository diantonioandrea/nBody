import matplotlib.pyplot as plt
import matplotlib.animation as animation

import utils


def updateLines(num: int, trajectories: list, lines: list, speed: int) -> list:

	num *= speed

	# UPDATE LINES

	for line, trajectory in zip(lines, trajectories):
		line.set_data(trajectory[:num, :2].T)
		line.set_3d_properties(trajectory[:num, 2])

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

	# -sp OPTION

	speed = 1

	# -sk OPTION

	skips = 1

	# --now OPTION

	instantPlot = False

	# -rn OPTION

	rangeFlag = False
	rangeString = ""
	rStart = 0
	rEnd = len(plotOrbits)

	# OPTIONS LOADING

	for opts in sdOptions:
		try:
			if opts[0] == "-sp": # speed
				speed = abs(int(opts[1]))

				if speed != 0:
					print(utils.colorPrint("\n\tSpeed set with value: " + str(speed), utils.bcolors.GREEN))

				else:
					speed = 1
			
			elif opts[0] == "-sk": # skips
				skips = abs(int(opts[1]))

				if skips != 0:
					print(utils.colorPrint("\n\tSkips set with value: " + str(skips), utils.bcolors.GREEN))

				else:
					skips = 1

		except(ValueError):
			print(utils.colorPrint("\n\tError: syntax error", utils.bcolors.RED))

		if opts[0] == "-rn":
			try:
				rStart = int(opts[1].split(":")[0])
				rEnd = int(opts[1].split(":")[1])

				rangeString = opts[1]
				rangeFlag = True
			
			except(IndexError, ValueError):
				print(utils.colorPrint("\n\tError: error within range definition, plotting all orbits", utils.bcolors.RED))

	for opts in ddOptions:
		if opts == "--now": # instant plotting
			instantPlot = True

	# CHECKING RANGES

	if rangeFlag:
		if 0 <= rStart < len(plotOrbits) and 0 < rEnd <= len(plotOrbits) and rStart < rEnd:
			orbits = plotOrbits[rStart:rEnd]
		
		else:
			orbits = plotOrbits
			rangeFlag = False
			print(utils.colorPrint("\n\tError: invalid range, plotting all orbits", utils.bcolors.RED))
	
	else:
		orbits = plotOrbits

	# DEFINING TRAJECTORIES IN A SEPARATED LIST TO AVOID MODIFICATIONS TO ORIGINAL ORBITS

	trajectories = [[]] * len(orbits)
	
	for j in range(len(orbits)):
		if skips == 1:
			trajectories[j] = orbits[j].trajectory
		
		else:
			trajectories[j] = utils.skipStack(orbits[j].trajectory, skips)

	# PLOT TITLE BASED ON NUMBER OF BODIES AND PPB (points-per-body)

	titleString = "N-body problem with " + str(len(orbits)) + " orbits"
	titleString += "\nShowing " + str(len(trajectories[0])) + " ppb"

	# FIGURE DEFINITION

	fig = plt.figure()
	ax = fig.add_subplot(projection='3d')
	ax.set_title(titleString)

	# SETTING PLOT LIMITS 

	ax.set(xlim3d=findLimits(orbits, 0), xlabel='X')
	ax.set(ylim3d=findLimits(orbits, 1), ylabel='Y')
	ax.set(zlim3d=findLimits(orbits, 2), zlabel='Z')

	if not instantPlot:
		# DEFINING LINES FOR ANIMATED PLOT

		lines = [ax.plot([], [], [])[0] for _ in trajectories]
		framesNumber = int(len(trajectories[0]) / speed)

	else:
		# DRAWING LINES FOR INSTANT PLOT

		for t in trajectories:
			ax.plot3D(t[:, 0], t[:, 1], t[:, 2])

	# ADDING LABELS TO LINES
	# "BODY N" IF THERE IS NO LABEL

	for l in ax.lines:
		if orbits[ax.lines.index(l)].label == "":
			l.set_label('Body ' + str(ax.lines.index(l)))
	
		else:
			l.set_label(orbits[ax.lines.index(l)].label)

	# GENERATING LEGEND

	ax.legend()

	# PLOT "RESULT"

	if not rangeFlag:
		print(utils.colorPrint("\n\tShowing orbits for " + str(len(orbits)) + " orbits", utils.bcolors.GREEN))
	
	else:
		print(utils.colorPrint("\n\tShowing orbits for " + str(len(orbits)) + " orbits in range " + rangeString, utils.bcolors.GREEN))

	# SHOWING ANIMATED PLOT

	if not instantPlot:
		ani = animation.FuncAnimation(fig, updateLines, frames=framesNumber, fargs=(trajectories, lines, speed), interval=1, repeat=False)

	plt.show()