import random
import time
import pygame
import math
from connect4 import connect4

class connect4Player(object):
	def __init__(self, position, seed=0, CVDMode=False):
		self.position = position
		self.opponent = None
		self.seed = seed
		random.seed(seed)
		if CVDMode:
			global P1COLOR
			global P2COLOR
			P1COLOR = (227, 60, 239)
			P2COLOR = (0, 255, 0)

	def play(self, env: connect4, move: list) -> None:
		move = [-1]

class human(connect4Player):

	def play(self, env: connect4, move: list) -> None:
		move[:] = [int(input('Select next move: '))]
		while True:
			if int(move[0]) >= 0 and int(move[0]) <= 6 and env.topPosition[int(move[0])] >= 0:
				break
			move[:] = [int(input('Index invalid. Select next move: '))]

class human2(connect4Player):

	def play(self, env: connect4, move: list) -> None:
		done = False
		while(not done):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

				if event.type == pygame.MOUSEMOTION:
					pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
					posx = event.pos[0]
					if self.position == 1:
						pygame.draw.circle(screen, P1COLOR, (posx, int(SQUARESIZE/2)), RADIUS)
					else: 
						pygame.draw.circle(screen, P2COLOR, (posx, int(SQUARESIZE/2)), RADIUS)
				pygame.display.update()

				if event.type == pygame.MOUSEBUTTONDOWN:
					posx = event.pos[0]
					col = int(math.floor(posx/SQUARESIZE))
					move[:] = [col]
					done = True

class randomAI(connect4Player):

	def play(self, env: connect4, move: list) -> None:
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		move[:] = [random.choice(indices)]

class stupidAI(connect4Player):

	def play(self, env: connect4, move: list) -> None:
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		if 3 in indices:
			move[:] = [3]
		elif 2 in indices:
			move[:] = [2]
		elif 1 in indices:
			move[:] = [1]
		elif 5 in indices:
			move[:] = [5]
		elif 6 in indices:
			move[:] = [6]
		else:
			move[:] = [0]

class minimaxAI(connect4Player):

	def gameCheck(self, env, j, player, case):
		i = env.topPosition[j] 
		print (i)
		offset = case - 1
		minRowIndex = max((j - offset), 0)
		maxRowIndex = min(j + offset, env.shape[1]-1)
		maxColumnIndex = max(i - offset, 0)
		minColumnIndex = min(i + offset, env.shape[0]-1)
		minLeftDiag = [max(j - offset, j), min(i + offset, env.shape[0]-1)]
		maxLeftDiag = [min(j + offset, env.shape[1]-1), max(i - offset, 0)]
		minRightDiag = [min(j + offset, j), min(i + offset, env.shape[0]-1)]
		maxRightDiag = [max(j - offset, 0), max(i - offset, 0)]
		# Iterate over extrema to find patterns
		# Horizontal solutions
		count = 0
		for s in range(minRowIndex, maxRowIndex+1):
			if env.board[i, s] == player:
				count += 1
			else:
				count = 0
			if count == case:
				if env.visualize:
					pygame.draw.line(screen, BLACK, (int(s*SQUARESIZE+SQUARESIZE/2), int((i+1.5)*SQUARESIZE)), (int((s-4)*SQUARESIZE+SQUARESIZE+SQUARESIZE/2), int((i+1.5)*SQUARESIZE)), 5)
					pygame.display.update()
				print ("Horizontal")
				return True
		# Verticle solutions
		count = 0
		for s in range(maxColumnIndex, minColumnIndex+1):
			if env.board[s, j] == player:
				print (s, j)
				count += 1
			else:
				count = 0
			if count == case:
				if env.visualize:
					pygame.draw.line(screen, WHITE, (int(j*SQUARESIZE+SQUARESIZE/2), int((s+2)*SQUARESIZE)), (int(j*SQUARESIZE+SQUARESIZE/2), int((s-2)*SQUARESIZE)), 5)
					pygame.display.update()
				print ("Vertical")
				return True
		# Left diagonal
		row = i
		col = j
		count = 0
		up = 0
		while row > -1 and col > -1 and env.board[row][col] == player:
			print (row, col)
			count += 1
			row -= 1
			col -= 1
		down_count = count
		row = i + 1
		col = j + 1
		while row < env.shape[0] and col < env.shape[1] and env.board[row][col] == player:
			count += 1
			row += 1
			col += 1
		if count == case:
			if env.visualize:
					# top, bottom
					pygame.draw.line(screen, BLACK, (int((j+0.5-(down_count-1))*SQUARESIZE), int((i+1.5-(down_count-1))*SQUARESIZE)), (int((j+0.5+(4-down_count))*SQUARESIZE), int((i+1.5+(4-down_count))*SQUARESIZE)), 5)
					pygame.display.update()
			print ("Left Diagonal")
			return True
		# Right diagonal
		row = i
		col = j
		count = 0
		while row < env.shape[0] and col > -1 and env.board[row][col] == player:
			count += 1
			row += 1
			col -= 1
		down_count = count
		row = i - 1
		col = j + 1
		while row > -1 and col < env.shape[1] and env.board[row][col] == player:
			count += 1
			row -= 1
			col += 1
		if count == case:
			if env.visualize:
					# top, bottom
					pygame.draw.line(screen, BLACK, (int((j+0.5-(down_count-1))*SQUARESIZE), int((i+1.5+(down_count-1))*SQUARESIZE)), (int((j+0.5+(4-down_count))*SQUARESIZE), int((i+1.5-(4-down_count))*SQUARESIZE)), 5)
					pygame.display.update()
			print ("Right Diagonal")
			return True
		#return False
		return len(env.history[0]) + len(env.history[1]) == env.shape[0]*env.shape[1]

	def play(self, env: connect4, move: list) -> None:
		#print ("mini")
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		if 3 in indices:
			move[:] = [3]
		elif 2 in indices:
			move[:] = [2]
		elif 1 in indices:
			move[:] = [1]
		elif 5 in indices:
			move[:] = [5]
		elif 6 in indices:
			move[:] = [6]
		else:
			move[:] = [0]
		if (self.gameCheck(env, move[0], 2, 3)):
			print ("Test")
			

class alphaBetaAI(connect4Player):

	def play(self, env: connect4, move: list) -> None:
		pass


SQUARESIZE = 100
BLUE = (0,0,255)
BLACK = (0,0,0)
P1COLOR = (255,0,0)
P2COLOR = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)




