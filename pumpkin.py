import globals
import craft
import utils

# 素材からカボチャエリアサイズを計算（外周はヒマワリ）
def size():
	world_size = get_world_size()
	# 外周はヒマワリなので、カボチャは (size-1) x (size-1)
	max_size = world_size - 1

	# 最大サイズ分のカボチャが作れるかチェック（枯れ修復のため2倍で見積もる）
	need = max_size * max_size * 2

	# 最大サイズが作れなければカボチャエリアなし
	if craft.calc_can_make(Entities.Pumpkin) < need:
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
	# statesでPumpkinかDead_Pumpkinが記録されているセルの数
	count = 0
	pumpkin_size = get_size()
	for px in range(pumpkin_size):
		for py in range(pumpkin_size):
			actual = globals.get(px, py)["actual"]
			if actual == Entities.Pumpkin or actual == Entities.Dead_Pumpkin:
				count += 1
	return count

def exec_cell(x, y):
	# カボチャモード同期収穫処理
	etype = get_entity_type()

	# カボチャ以外が植えられていたら収穫
	if etype != None and etype != Entities.Pumpkin and etype != Entities.Dead_Pumpkin:
		if can_harvest():
			harvest()
		# 収穫後は空セル → elseでカボチャを植える
		etype = None

	# 枯れたカボチャ（1周後にまとめて修復）
	if etype == Entities.Dead_Pumpkin:
		globals.pumpkin_dead.append((x, y))
		globals.set(x, y, etype, False, None)
	# 収穫可能なカボチャ
	elif etype == Entities.Pumpkin and can_harvest():
		globals.set(x, y, etype, True, None)
	# 育成中のカボチャ
	elif etype == Entities.Pumpkin:
		globals.set(x, y, etype, False, None)
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

def clear_area_states():
	globals.pumpkin_scan_complete = False
	globals.pumpkin_dead = []
	globals.pumpkin_last_dead = None
	# プラン更新フラグを立てる（次サイクルで再計算）
	globals.need_update_plan = True
	# 原点に移動して次の周回を開始
	utils.goto(0, 0)

def fix_dead():
	# 記録された枯れたカボチャを修復
	if len(globals.pumpkin_dead) == 0:
		check_and_harvest()
		return

	# 最後の要素を記録（2以上から一気に0になる場合に備える）
	globals.pumpkin_last_dead = globals.pumpkin_dead[-1]

	still_dead = []
	for px, py in globals.pumpkin_dead:
		utils.goto(px, py)
		etype = get_entity_type()

		# パンプキンになったら除外
		if etype == Entities.Pumpkin:
			continue

		# 枯れたカボチャなら修復を試みる
		if etype == Entities.Dead_Pumpkin:
			harvest()
			plant(Entities.Pumpkin)

		# まだパンプキンじゃないならstill_deadに残す
		still_dead.append((px, py))

	globals.pumpkin_dead = still_dead
	if len(globals.pumpkin_dead) > 0:
		fix_dead()
		return
	
	check_and_harvest()

def check_and_harvest():
	# 最後に修復したカボチャが収穫可能になるまで待機
	if globals.pumpkin_last_dead != None:
		px, py = globals.pumpkin_last_dead
		utils.goto(px, py)
		while not can_harvest():
			utils.wait()
	harvest()
	clear_area_states()
