import pumpkin
import state

def get_unlocks_entity_types():
	res = [Entities.Bush]
	
	if num_unlocked(Unlocks.Grass):
		res.append(Entities.Grass)
	if num_unlocked(Unlocks.Trees):
		res.append(Entities.Tree)
	if num_unlocked(Unlocks.Carrots):
		res.append(Entities.Carrot)
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
	if type == Entities.Grass:
		return exec_grass
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

def item_to_entity(item):
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

# エンティティを作れる数を計算
def calc_can_make(entity, max_count):
	cost = get_cost(entity)
	if cost == None:
		return max_count
	can_make = max_count
	for item in cost:
		available = num_items(item) // cost[item]
		if available < can_make:
			can_make = available
	return can_make

# ヒマワリエリアサイズを計算（11本以上確保）
def calc_sunflower_width(pumpkin_size):
	if pumpkin_size == 0:
		return 0
	# カボチャの高さに合わせて幅を計算
	# 11本以上: width * pumpkin_size >= 11
	width = 11 // pumpkin_size
	if width * pumpkin_size < 11:
		width = width + 1
	return width

# 優先度リストを取得（unlock順の逆、ヒマワリ/基礎素材除外）
def get_priorities():
	unlocked = get_unlocks_entity_types()
	exclude = [Entities.Sunflower, Entities.Tree, Entities.Grass, Entities.Bush]
	result = []
	for i in range(len(unlocked) - 1, -1, -1):
		entity = unlocked[i]
		if entity not in exclude:
			result.append(entity)
	return result

# 優先度順にエンティティを取得
def get_priority_entity():
	priorities = get_priorities()
	for entity in priorities:
		cost = get_cost(entity)
		if cost == None:
			return entity
		can_make = True
		for item in cost:
			if num_items(item) < cost[item]:
				can_make = False
		if can_make:
			return entity
	return None  # 基礎素材へ

# stateから取得（update_plan()で事前計算済み）
def get_type(x, y):
	etype = state.get_type(x, y)
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
			state.set_type(x, y, etype)

# 実際の計算ロジック
def calc_type(x, y):
	# エリアサイズを決定（pumpkinモジュールのキャッシュを使用）
	pumpkin_size = pumpkin.get_size()
	sunflower_width = calc_sunflower_width(pumpkin_size)

	# 左上: カボチャ（正方形）
	if x < pumpkin_size and y < pumpkin_size:
		return Entities.Pumpkin

	# カボチャの右: ヒマワリ（11本以上、高さはカボチャと同じ）
	if x >= pumpkin_size and x < pumpkin_size + sunflower_width and y < pumpkin_size:
		return Entities.Sunflower

	# 残りエリア: 優先度順に判定
	priorities = get_priorities()
	for ent in priorities:
		if calc_can_make(ent, 1) >= 1:
			if ent == Entities.Pumpkin:
				# カボチャエリア確保できてれば基礎素材へ
				if pumpkin_size > 0:
					break
				continue
			return ent

	# 基礎素材（フォールバック or カボチャ補充）
	if (x + y) % 2 == 0:
		return Entities.Tree
	else:
		return Entities.Grass

def exec_grass():
	if get_ground_type() != Grounds.Grassland:
		till()

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
	x = get_pos_x()
	y = get_pos_y()

	# カボチャモードの場合のみ特別処理
	if pumpkin.is_area(x, y):
		pumpkin.exec_cell(x, y)

	# 通常エリアは普通に収穫
	elif can_harvest():
		harvest()

	if get_water() < 0.75 and num_items(Items.Water) > 0:
		use_item(Items.Water)

