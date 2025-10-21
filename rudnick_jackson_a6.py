# state is 3x3 matrix
# 0 is empty, 1 is X, 2 is O
# player is 1 or 2

from copy import deepcopy
import math

state = [
	[0, 0, 0],
	[0, 0, 0],
	[0, 0, 0],
]

def transition_model(state, player, action):
	row, col = action
	if state[row][col] != 0:
		raise ValueError("Invalid action: Cell is already occupied.")
	
	new_state = deepcopy(state)
	new_state[row][col] = player
	return new_state

def get_actions(state):
	actions = []
	for i in range(3):
		for j in range(3):
			if state[i][j] == 0:
				actions.append((i, j))
	return actions

def goal_test(state):
	if utility(state) != 0:
		return True
	
	for row in state:
		for cell in row:
			if cell == 0:
				return False
	return True

def utility(state):
	# Check rows and columns
	for i in range(3):
		if state[i][0] == state[i][1] == state[i][2] != 0:
			return state[i][0]
		if state[0][i] == state[1][i] == state[2][i] != 0:
			return state[0][i]
	# Check diagonals
	if state[0][0] == state[1][1] == state[2][2] != 0:
		return state[0][0]
	if state[0][2] == state[1][1] == state[2][0] != 0:
		return state[0][2]
	return 0

def minimax_search(state, player):
	actions = get_actions(state)
	best_action = None

	# check terminal state
	u = utility(state)
	if u == 1:
		return 1, None
	elif u == 2:
		return -1, None
	# draw
	if not actions:
		return 0, None

	if player == 1:
		max_val = -math.inf
		for action in actions:
			v, _ = minimax_search(transition_model(state, player, action), 2)
			if v > max_val:
				max_val = v
				best_action = action
		return max_val, best_action
	else:
		min_val = math.inf
		for action in actions:
			v, _ = minimax_search(transition_model(state, player, action), 1)
			if v < min_val:
				min_val = v
				best_action = action
		return min_val, best_action

def print_state(state):
	symbols = {0: " ", 1: "X", 2: "O"}
	for row in state:
		print("|".join(symbols[cell] for cell in row))
		print("-" * 5)

if __name__ == "__main__":
	while get_actions(state):
		print_state(state)
		actions = get_actions(state)
		row = int(input("Enter row (1-3): "))
		col = int(input("Enter column (1-3): "))
		action = (row-1, col-1)
		if action not in actions:
			print("Invalid action. Try again.")
			continue
		state = transition_model(state, 1, action)
		if utility(state) == 1: # this isnt even possible lol
			print_state(state)
			print("Player 1 wins!")
			break
		if not get_actions(state):
			print_state(state)
			print("It's a draw!")
			break
		# Min's turn
		_, action = minimax_search(state, 2)
		state = transition_model(state, 2, action)
		if utility(state) == 2:
			print_state(state)
			print("Player 2 wins!")
			break
