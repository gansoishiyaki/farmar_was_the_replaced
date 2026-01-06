# アンロック関連

def get_entity_types():
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

def get_item_types():
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
