DirEW = East   # 初期は右へ

def next(size, x, y):
	global DirEW

	going_up = (x % 2 == 0)

	# 縦に進めるなら最優先
	if going_up and y + 1 < size:
		move(North)
		return
	if not going_up and y - 1 >= 0:
		move(South)
		return

	# 縦の端に来た → 横へ
	if DirEW == East:
		if x + 1 < size:
			move(East)
			return
		else:
			DirEW = West
			move(West)
			return
	else:  # DirX == West
		if x - 1 >= 0:
			move(West)
			return
		else:
			DirEW = East
			move(East)
			return
	
def goto(x, y):
	while get_pos_x() != x:
		if get_pos_x() < x:
			move(East)
		else:
			move(West)
	while get_pos_y() != y:
		if get_pos_y() < y:
			move(North)
		else:
			move(South)

def wait():
	pass