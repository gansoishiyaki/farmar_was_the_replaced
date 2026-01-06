# グローバル状態管理

# 全マスの状態を記録
# type: 予測/計画（entity.calc_type()の結果）
# actual: 実際のエンティティタイプ（get_entity_type()の結果）
states = {}

# 目標エンティティ（最終的に作りたいもの）
target_entity = None

# プラン更新フラグ（Trueなら次の原点でupdate_plan()実行）
need_update_plan = True

# カボチャエリア状態
pumpkin_size = None
pumpkin_dead = []
pumpkin_scan_complete = False
pumpkin_last_dead = None

# マス状態関連
def _default():
	return {"type": None, "actual": None, "ready": False, "petals": None}

def get(x, y):
	key = (x, y)
	if key not in states:
		states[key] = _default()
	return states[key]

def set(x, y, actual, ready, petals):
	key = (x, y)
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
	key = (x, y)
	if key not in states:
		states[key] = _default()
	states[key]["type"] = etype

def get_type(x, y):
	key = (x, y)
	if key in states:
		return states[key]["type"]
	return None

# 実際のエンティティタイプ
def set_actual(x, y, actual):
	key = (x, y)
	if key not in states:
		states[key] = _default()
	states[key]["actual"] = actual

def get_actual(x, y):
	key = (x, y)
	if key in states:
		return states[key]["actual"]
	return None
