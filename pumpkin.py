import state

def get_size():
	size = get_world_size()
	pumpkin_size = size // 4
	if pumpkin_size < 1:
		pumpkin_size = 1
	return pumpkin_size

def is_area(x, y):
	pumpkin_size = get_size()
	return x < pumpkin_size and y < pumpkin_size

def exec_cell(x, y):
	# カボチャエリア外ならFalse
	if not is_area(x, y):
		return False

	etype = get_entity_type()

	# 枯れたカボチャは植え直す
	if etype == Entities.Dead_Pumpkin:
		harvest()
		plant(Entities.Pumpkin)
		state.set(x, y, Entities.Pumpkin, False, None)
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

	return True

def all_ready():
	pumpkin_size = get_size()
	for px in range(pumpkin_size):
		for py in range(pumpkin_size):
			s = state.get(px, py)
			if not s["ready"]:
				return False
	return True

def clear_area_states():
	pumpkin_size = get_size()
	for px in range(pumpkin_size):
		for py in range(pumpkin_size):
			state.set(px, py, None, False, None)
