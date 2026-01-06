def get_unlocks_entity_types():
	res = [Entities.Bush]
	
	if num_unlocked(Unlocks.Grass):
		res.append(Entities.Grass)
	if num_unlocked(Unlocks.Carrots):
		res.append(Entities.Carrot)
	if num_unlocked(Unlocks.Trees):
		res.append(Entities.Tree)
	if num_unlocked(Unlocks.Pumpkins):
		res.append(Entities.Pumpkin)
	if num_unlocked(Unlocks.Sunflowers):
		res.append(Entities.Sunflower)
	return res

def get_unlocks_item_types():
	res = [Items.Hay]

	if num_unlocked(Unlocks.Carrots):
		res.append(Items.Carrot)
	if num_unlocked(Unlocks.Trees):
		res.append(Items.Wood)
	if num_unlocked(Unlocks.Pumpkins):
		res.append(Items.Pumpkin)
	if num_unlocked(Unlocks.Sunflowers):
		res.append(Items.Power)
	return res

def get_func(type):
	if type == Entities.Bush:
		return exec_bush
	if type == Entities.Carrot:
		return exec_carrot
	if type == Entities.Tree:
		return exec_tree
	if type == Entities.Pumpkin:
		return exec_pumpkin
	if type == Entities.Sunflower:
		return exec_sunflower
	return exec_grass

def item_to_type(item):
	if item == Items.Hay:
		return Entities.Grass
	if item == Items.Wood:
		return Entities.Tree
	if item == Items.Carrot:
		return Entities.Carrot
	if item == Items.Pumpkin:
		return Entities.Pumpkin
	if item == Items.Power:
		return Entities.Sunflower
	return None

def get_type(x, y):
	size = get_world_size()

	# コスト: 人参1つ = wood4 + hay4, カボチャ/ヒマワリ = 人参1
	# Sunflower: 10本以上 + 花びら最大で5倍ボーナス

	# 配分: 人参1つに tree4 + grass4 = 8マス必要
	# tree:grass:carrot = 4:4:1 の比率が理想

	pumpkin_size = size // 4
	if pumpkin_size < 1:
		pumpkin_size = 1

	# Sunflowerは10本以上必要（5倍ボーナス）
	sunflower_size = pumpkin_size
	if sunflower_size < 4:
		sunflower_size = 4  # 最低4x4=16本

	# 左上: カボチャ（正方形）
	if x < pumpkin_size and y < pumpkin_size:
		return Entities.Pumpkin

	# カボチャの右: ヒマワリ（10本以上）
	if x >= pumpkin_size and x < pumpkin_size + sunflower_size and y < sunflower_size:
		return Entities.Sunflower

	# 残りエリア: tree:grass:carrot = 4:4:1 の市松模様
	# カボチャの下
	if x < pumpkin_size:
		if (x + y) % 2 == 0:
			return Entities.Tree
		else:
			return Entities.Grass

	# 右側と下側のエリア
	cell = x + y * size
	cycle = cell % 9  # 9マスサイクル

	if cycle == 8:
		return Entities.Carrot

	# 市松模様でtreeとgrassを交互配置
	if (x + y) % 2 == 0:
		return Entities.Tree
	else:
		return Entities.Grass

def get_tree_or_bush(x, y):
	if x % 2 * y % 2 == 0:
		return Entities.Tree
	return Entities.Bush

def exec_grass():
	pass

def exec_carrot():
	if get_ground_type() != Grounds.Soil:
		till()
	plant(Entities.Carrot)

def exec_bush():
	if get_ground_type() != Grounds.Grassland:
		till()
	plant(Entities.Bush)
	
def exec_tree():
	if get_ground_type() != Grounds.Grassland:
		till()
	plant(Entities.Tree)

def exec_pumpkin():
	if get_ground_type() != Grounds.Soil:
		till()
	plant(Entities.Pumpkin)

def exec_sunflower():
	if get_ground_type() != Grounds.Soil:
		till()
	plant(Entities.Sunflower)

def exec_cell():
	import pumpkin
	x = get_pos_x()
	y = get_pos_y()

	# カボチャエリアは特別処理
	if not pumpkin.exec_cell(x, y):
		# 通常エリアは普通に収穫
		if can_harvest():
			harvest()

	if get_water() < 0.75 and num_items(Items.Water) > 0:
		use_item(Items.Water)

