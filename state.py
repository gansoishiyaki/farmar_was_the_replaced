# 全マスの状態を記録
states = {}

def get(x, y):
	key = str(x) + "," + str(y)
	if key not in states:
		states[key] = {"type": None, "ready": False, "petals": None}
	return states[key]

def set(x, y, etype, ready, petals):
	key = str(x) + "," + str(y)
	states[key] = {"type": etype, "ready": ready, "petals": petals}

def clear():
	global states
	states = {}
