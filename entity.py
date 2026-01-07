import pumpkin
import globals
import craft
import const

# サイクル進行中かどうか（進行中ならプラン更新をスキップ）
def is_cycle_in_progress():
	if globals.actual_target == Entities.Pumpkin:
		# カボチャモード中はフラグで制御
		return not globals.need_update_plan
	# カボチャモード以外は毎周更新（サイクルなし）
	return False

# 実際のターゲットを計算
def calc_actual_target():
	# ひまわりが少ない & 全マス分のコストがある → 全部ひまわり（最優先）
	size = get_world_size()
	total_cells = size * size
	
	# ひまわりモード中は5倍のしきい値を使用（ヒステリシス）
	threshold = const.SUNFLOWER_POWER_THRESHOLD
	if globals.actual_target == Entities.Sunflower:
		threshold = threshold * const.SUNFLOWER_HYSTERESIS

	if num_items(Items.Power) < threshold:
		if craft.calc_can_make(Entities.Sunflower) >= total_cells:
			return Entities.Sunflower

	# カボチャモード
	pumpkin_size = pumpkin.get_size()
	if pumpkin_size > 0:
		return Entities.Pumpkin

	# カボチャが目標だがモードに入れない → 人参の素材を作る
	if globals.target_item == Entities.Pumpkin:
		return craft.get_required_entity(Entities.Carrot)

	# 目標から再帰的に必要なものを計算
	required = craft.get_required_entity(globals.target_item)
	if required != None:
		return required

	# フォールバック: 基礎素材
	return Entities.Tree

# 一周開始時に栽培計画を更新
def update_plan():
	# 実際のターゲットを計算
	globals.actual_target = calc_actual_target()

	# コンパニオンモード判定
	target = globals.actual_target
	globals.companion_enabled = (target == Entities.Grass or target == Entities.Tree or target == Entities.Carrot)

	globals.need_update_plan = False

# メイン処理
def exec_cell(x, y):
	target = globals.actual_target

	# カボチャは専用処理
	if target == Entities.Pumpkin:
		result = pumpkin.exec_cell(x, y)
		do_water()
		return result

	do_plant(x, y, target)
	do_water()
	return True

# 統合植え付け処理
def do_plant(x, y, entity_type):
	# 収穫
	if can_harvest():
		harvest()
		# 収穫したら記録をクリア
		if (x, y) in globals.planted:
			globals.planted.pop((x, y))
		if (x, y) in globals.companion_requests:
			globals.companion_requests.pop((x, y))

	# コンパニオンモード
	if globals.companion_enabled:
		# 植え済みスキップ
		if (x, y) in globals.planted:
			return
		# 素材チェック
		if entity_type == Entities.Carrot and num_items(Items.Carrot) <= 0:
			return
		# 隣接からの要望があれば優先
		if (x, y) in globals.companion_requests:
			entity_type = globals.companion_requests[(x, y)]

	# 地面準備
	if entity_type == Entities.Grass or entity_type == Entities.Tree or entity_type == Entities.Bush:
		if get_ground_type() != Grounds.Grassland:
			till()
	else:
		if get_ground_type() != Grounds.Soil:
			till()

	# 植え付け
	plant(entity_type)

	# コンパニオン要望を記録（即座には行かない）
	if globals.companion_enabled:
		globals.planted[(x, y)] = entity_type
		result = get_companion()
		if result != None:
			companion, (cx, cy) = result
			globals.companion_requests[(cx, cy)] = companion

def do_water():
	if get_water() < 0.75 and num_items(Items.Water) > 0:
		use_item(Items.Water)
