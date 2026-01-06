import globals
import craft
import utils

# 素材からカボチャエリアサイズを計算（外周はヒマワリ）
def size():
	max_size = get_world_size() - 1
	# 最大サイズが作れなければカボチャエリアなし（枯れ修復のため2倍で見積もる）
	if craft.calc_can_make(Entities.Pumpkin) < max_size * max_size * 2:
		return 0
	return max_size

def get_size():
	# サイクル中はキャッシュを返す
	if not globals.need_update_plan and globals.pumpkin_size != None:
		return globals.pumpkin_size
	# サイクル開始前/収穫後は再計算
	globals.pumpkin_size = size()
	return globals.pumpkin_size

def is_active():
	# カボチャモードかどうか（サイズ > 0）
	return get_size() > 0

def is_area(x, y):
	pumpkin_size = get_size()
	return x < pumpkin_size and y < pumpkin_size

def is_corner(x, y):
	pumpkin_size = get_size()
	return (x == 0 or x == pumpkin_size - 1) and (y == 0 or y == pumpkin_size - 1)

def get_confirmed_count():
	# pumpkin_confirmedのサイズを返すだけ（O(1)）
	return len(globals.pumpkin_confirmed)

def exec_cell(x, y):
	# カボチャモード同期収穫処理
	etype = get_entity_type()

	# カボチャ以外が植えられていたら収穫
	if etype != None and etype != Entities.Pumpkin and etype != Entities.Dead_Pumpkin:
		if can_harvest():
			harvest()
		# 収穫後は空セル → elseでカボチャを植える
		etype = None

	# 枯れたカボチャ（収穫して即座に再植え）
	if etype == Entities.Dead_Pumpkin:
		harvest()
		plant(Entities.Pumpkin)
		globals.pumpkin_dead.append((x, y))
		globals.pumpkin_confirmed[(x, y)] = True

	# 収穫可能なカボチャ
	elif etype == Entities.Pumpkin and can_harvest():
		globals.pumpkin_confirmed[(x, y)] = True

	# 育成中のカボチャ
	elif etype == Entities.Pumpkin:
		globals.pumpkin_confirmed[(x, y)] = True

	# 空セル → カボチャを植える（状態未確認なのでsetしない）
	else:
		if get_ground_type() != Grounds.Soil:
			till()
		plant(Entities.Pumpkin)

	# エリア1周したら枯れたカボチャを修復
	if globals.pumpkin_scan_complete:
		fix_dead()
	elif is_corner(x, y) and get_confirmed_count() >= get_size() * get_size():
		# 四隅でのみ1周完了をチェック（毎回は無駄）
		globals.pumpkin_scan_complete = True
		fix_dead()

	# 収穫サイクル完了後は原点で待機
	return not globals.need_update_plan

def clear_area_states():
	globals.pumpkin_scan_complete = False
	globals.pumpkin_dead = []
	globals.pumpkin_confirmed = {}
	globals.clear()
	# プラン更新フラグを立てる（次サイクルで再計算）
	globals.need_update_plan = True
	# 原点に移動して次の周回を開始
	utils.goto(0, 0)

def fix_dead():
	# 記録された枯れたカボチャを修復
	if len(globals.pumpkin_dead) == 0:
		check_and_harvest()
		return

	for px, py in list(globals.pumpkin_dead):
		utils.goto(px, py)
		etype = get_entity_type()

		# パンプキンになったら除外
		if etype == Entities.Pumpkin:
			globals.pumpkin_dead.remove((px, py))
			continue

		# また枯れてたら収穫してから植え直し
		if etype == Entities.Dead_Pumpkin:
			harvest()
		plant(Entities.Pumpkin)

	if len(globals.pumpkin_dead) > 0:
		fix_dead()
		return

	check_and_harvest()

def check_and_harvest():
	# (0,0)と(0, last_y)のmeasure()が同じになるまで待機
	pumpkin_size = get_size()
	last_y = pumpkin_size - 1

	while True:
		utils.goto(0, 0)
		first_id = measure()
		utils.goto(0, last_y)
		last_id = measure()
		if first_id == last_id:
			break

	harvest()
	clear_area_states()
