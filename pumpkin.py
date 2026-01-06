import state
import entity

# 素材からカボチャエリアサイズを計算（最大サイズのみ）
def size():
	size = get_world_size()
	# ヒマワリ幅は最小2（6x2=12本）と仮定
	sunflower_width = 2

	# 最大サイズ: ヒマワリを確保した残り
	max_size = size - sunflower_width
	if max_size < 6:
		max_size = 6

	# 最大サイズ分のカボチャが作れるかチェック
	need = max_size * max_size
	can_make = entity.calc_can_make(Entities.Pumpkin, need)

	# 最大サイズが作れなければカボチャエリアなし
	if can_make < need:
		return 0

	return max_size

# 現在のカボチャエリアサイズを記憶
current_size = None
# 巡回中のカウンタ
visited_count = 0
dead_positions = []
# 1周完了フラグ（状態が全セル確定するまで収穫しない）
scan_complete = False

def get_size():
	global current_size
	if current_size == None:
		current_size = size()
	return current_size

def check_size_change():
	global current_size
	if current_size == None:
		return False
	new_size = size()
	if new_size != current_size:
		return True
	return False

def reset_size():
	global current_size
	current_size = None

def reset_all():
	global current_size
	global visited_count
	global dead_positions
	global scan_complete
	current_size = None
	visited_count = 0
	dead_positions = []
	scan_complete = False
	# 状態もクリア
	size = get_world_size()
	for px in range(size):
		for py in range(size):
			state.set(px, py, None, False, None)

def is_active():
	# カボチャモードかどうか（サイズ > 0）
	return get_size() > 0

def rescan_area():
	# カボチャエリアを再スキャンして状態を保存
	import utils
	pumpkin_size = get_size()
	if pumpkin_size == 0:
		return
	for px in range(pumpkin_size):
		for py in range(pumpkin_size):
			utils.goto(px, py)
			etype = get_entity_type()
			ready = (etype == Entities.Pumpkin and can_harvest())
			state.set(px, py, etype, ready, None)

def is_area(x, y):
	pumpkin_size = get_size()
	return x < pumpkin_size and y < pumpkin_size

def exec_cell(x, y):
	global visited_count
	global dead_positions
	global scan_complete

	# カボチャエリア外ならFalse
	if not is_area(x, y):
		return False

	etype = get_entity_type()
	visited_count += 1

	# 枯れたカボチャ（1周後にまとめて修復）
	if etype == Entities.Dead_Pumpkin:
		dead_positions.append((x, y))
		state.set(x, y, etype, False, None)
	# 収穫可能なカボチャ
	elif etype == Entities.Pumpkin and can_harvest():
		state.set(x, y, etype, True, None)
		# 全部揃ったら収穫
		if all_ready():
			harvest()
			clear_area_states()
	# まだ育ってない or 空
	else:
		state.set(x, y, etype, False, None)

	# エリア1周したら枯れたカボチャを修復
	pumpkin_size = get_size()
	if visited_count >= pumpkin_size * pumpkin_size:
		scan_complete = True
		fix_dead()
		visited_count = 0
		dead_positions = []

	return True

def all_ready():
	# 1周完了してなければFalse
	if not scan_complete:
		return False
	# 保存された状態をチェック（actual で実際のタイプを確認）
	pumpkin_size = get_size()
	for px in range(pumpkin_size):
		for py in range(pumpkin_size):
			s = state.get(px, py)
			if s["actual"] != Entities.Pumpkin or not s["ready"]:
				return False
	return True

def clear_area_states():
	global scan_complete
	pumpkin_size = get_size()
	for px in range(pumpkin_size):
		for py in range(pumpkin_size):
			state.set(px, py, None, False, None)
	scan_complete = False
	reset_size()
	# 原点に移動して次の周回を開始
	import utils
	utils.goto(0, 0)

def fix_dead():
	# 記録された枯れたカボチャを修復
	global dead_positions

	count = len(dead_positions)
	if count == 0:
		check_and_harvest()
		return

	import utils
	for px, py in dead_positions:
		utils.goto(px, py)
		if get_entity_type() == Entities.Dead_Pumpkin:
			harvest()
			plant(Entities.Pumpkin)
			state.set(px, py, Entities.Pumpkin, False, None)

	# 再スキャンして状態を更新
	dead_positions = []
	pumpkin_size = get_size()
	for px in range(pumpkin_size):
		for py in range(pumpkin_size):
			utils.goto(px, py)
			etype = get_entity_type()
			if etype == Entities.Dead_Pumpkin:
				dead_positions.append((px, py))
			# 状態も更新
			ready = (etype == Entities.Pumpkin and can_harvest())
			state.set(px, py, etype, ready, None)

	if len(dead_positions) > 0:
		fix_dead()
	else:
		harvest()
		clear_area_states()

def check_and_harvest():
	# 全部揃ってたら即収穫（今いる場所でOK）
	if not all_ready():
		return
	harvest()
	clear_area_states()
