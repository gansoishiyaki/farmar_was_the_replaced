# グローバル状態管理

# 目標（エンティティまたはアイテム）
target_item = None

# 実際のターゲット（update_plan時に計算）
actual_target = None

# プラン更新フラグ（Trueなら次の原点でupdate_plan()実行）
need_update_plan = True

# カボチャエリア状態
pumpkin_size = None
pumpkin_dead = []
pumpkin_scan_complete = False
pumpkin_confirmed = {}

# コンパニオン対応: モード有効フラグ（update_plan時に設定）
companion_enabled = False
# コンパニオン対応: 植えた作物を記録 {(x, y): entity_type}
planted = {}
# コンパニオン対応: その座標に植えてほしい種類 {(x, y): entity_type}
companion_requests = {}

# ドローンタスク: [{x, y, type, entity}, ...]
# type: "Plant", "Feed"
tasks = []

def add_task(x, y, task_type, entity):
	tasks.append({"x": x, "y": y, "type": task_type, "entity": entity})

def get_next_task():
	if len(tasks) > 0:
		return tasks[0]
	return None

def pop_task():
	if len(tasks) > 0:
		return tasks.pop(0)
	return None
