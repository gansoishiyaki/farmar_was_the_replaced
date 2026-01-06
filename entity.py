import pumpkin
import globals
import craft

def exec_entity(type, x, y):
	if type == Entities.Grass:
		exec_grass()
	elif type == Entities.Bush:
		exec_bush()
	elif type == Entities.Carrot:
		exec_carrot()
	elif type == Entities.Tree:
		exec_tree()
	elif type == Entities.Pumpkin:
		pumpkin.exec_cell(x, y)
	elif type == Entities.Sunflower:
		exec_sunflower()
	else:
		exec_grass()

# サイクル進行中かどうか（進行中ならプラン更新をスキップ）
def is_cycle_in_progress():
	target = globals.target_entity
	if target == Entities.Pumpkin:
		# カボチャはフラグで制御
		return not globals.need_update_plan
	# カボチャ以外は毎周更新（サイクルなし）
	return False

# stateから取得（update_plan()で事前計算済み）
def get_type(x, y):
	etype = globals.get_type(x, y)
	if etype != None:
		return etype
	# 未計算の場合はその場で計算
	return calc_type(x, y)

# 一周開始時に全マスの栽培計画を更新
def update_plan():
	size = get_world_size()
	for x in range(size):
		for y in range(size):
			etype = calc_type(x, y)
			globals.set_type(x, y, etype)
	globals.need_update_plan = False

# 実際の計算ロジック
def calc_type(x, y):
	size = get_world_size()
	pumpkin_size = pumpkin.get_size()

	# カボチャモード: 外周はヒマワリ、内側はカボチャ
	if pumpkin_size > 0:
		if x == size - 1 or y == size - 1:
			return Entities.Sunflower
		return Entities.Pumpkin

	# カボチャが目標だがモードに入れない → 人参の素材を作る
	if globals.target_entity == Entities.Pumpkin:
		required = craft.get_required_entity(Entities.Carrot)
		if required == Entities.Tree or required == Entities.Grass:
			if (x + y) % 2 == 0:
				return Entities.Tree
			else:
				return Entities.Grass
		return required

	# 外周でヒマワリの素材があればヒマワリ（外周全体分の素材が必要）
	if x == size - 1 or y == size - 1:
		sunflower_count = size * 2 - 1
		if craft.calc_can_make(Entities.Sunflower) >= sunflower_count:
			return Entities.Sunflower

	# 目標エンティティから再帰的に必要なものを計算
	required = craft.get_required_entity(globals.target_entity)
	if required != None:
		# TreeとGrassは市松模様
		if required == Entities.Tree or required == Entities.Grass:
			if (x + y) % 2 == 0:
				return Entities.Tree
			else:
				return Entities.Grass
		return required

	# フォールバック: 基礎素材
	if (x + y) % 2 == 0:
		return Entities.Tree
	else:
		return Entities.Grass

def exec_grass():
	if can_harvest():
		harvest()
	if get_ground_type() != Grounds.Grassland:
		till()

def exec_carrot():
	if can_harvest():
		harvest()
	if get_ground_type() != Grounds.Soil:
		till()
	plant(Entities.Carrot)

def exec_bush():
	if can_harvest():
		harvest()
	if get_ground_type() != Grounds.Grassland:
		till()
	plant(Entities.Bush)

def exec_tree():
	if can_harvest():
		harvest()
	if get_ground_type() != Grounds.Grassland:
		till()
	plant(Entities.Tree)

def exec_sunflower():
	if can_harvest():
		harvest()
	if get_ground_type() != Grounds.Soil:
		till()
	plant(Entities.Sunflower)

def exec_cell(x, y):
	expected = get_type(x, y)
	exec_entity(expected, x, y)
	# 水やり
	if get_water() < 0.75 and num_items(Items.Water) > 0:
		use_item(Items.Water)
