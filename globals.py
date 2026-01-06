# グローバル状態管理

# 全マスの計画タイプを記録
states = {}

# 目標（エンティティまたはアイテム）
target_item = None

# プラン更新フラグ（Trueなら次の原点でupdate_plan()実行）
need_update_plan = True

# カボチャエリア状態
pumpkin_size = None
pumpkin_dead = []
pumpkin_scan_complete = False
pumpkin_confirmed = {}

# 計画タイプ（entity.calc_type()の結果）
def set_type(x, y, etype):
	key = (x, y)
	states[key] = etype

def get_type(x, y):
	key = (x, y)
	if key in states:
		return states[key]
	return None

def clear():
	global states
	states = {}
