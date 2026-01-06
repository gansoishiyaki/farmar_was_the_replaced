# 全マスの状態を記録
# type: 予測/計画（entity.calc_type()の結果）
# actual: 実際のエンティティタイプ（get_entity_type()の結果）
states = {}

def _default():
	return {"type": None, "actual": None, "ready": False, "petals": None}

def get(x, y):
	key = str(x) + "," + str(y)
	if key not in states:
		states[key] = _default()
	return states[key]

def set(x, y, actual, ready, petals):
	key = str(x) + "," + str(y)
	if key not in states:
		states[key] = _default()
	states[key]["actual"] = actual
	states[key]["ready"] = ready
	states[key]["petals"] = petals

def clear():
	global states
	states = {}

# 予測/計画タイプ
def set_type(x, y, etype):
	key = str(x) + "," + str(y)
	if key not in states:
		states[key] = _default()
	states[key]["type"] = etype

def get_type(x, y):
	key = str(x) + "," + str(y)
	if key in states:
		return states[key]["type"]
	return None

# 実際のエンティティタイプ
def set_actual(x, y, actual):
	key = str(x) + "," + str(y)
	if key not in states:
		states[key] = _default()
	states[key]["actual"] = actual

def get_actual(x, y):
	key = str(x) + "," + str(y)
	if key in states:
		return states[key]["actual"]
	return None
