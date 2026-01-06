# 素材/コスト計算関連

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
def calc_can_make(entity):
	cost = get_cost(entity)
	if cost == None:
		return 999999
	result = 999999
	for item in cost:
		result = min(result, num_items(item) // cost[item])
	return result

# 目標エンティティを作るために必要なエンティティを再帰的に取得
# 例: Pumpkin → Carrot不足 → Carrot → Wood不足 → Tree
def get_required_entity(target):
	if target == None:
		return None
	cost = get_cost(target)
	if cost == None:
		return target  # コストなし、そのまま作れる

	# カボチャは枯れ修復のため倍で見積もる
	multiplier = 1
	if target == Entities.Pumpkin:
		multiplier = 2

	# 素材チェック
	for item in cost:
		if num_items(item) < cost[item] * multiplier:
			# 素材が足りない → その素材を作るエンティティを再帰的に取得
			entity = item_to_entity(item)
			return get_required_entity(entity)
	# 全素材あり
	return target
