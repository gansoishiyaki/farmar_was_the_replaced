import utils
import entity
import globals

def main():
	# 目標エンティティを設定
	globals.target_entity = Entities.Pumpkin
	size = get_world_size()

	while True:
		x = get_pos_x()
		y = get_pos_y()

		# 原点に戻ったら栽培計画を更新（サイクル進行中はスキップ）
		if x == 0 and y == 0 and not entity.is_cycle_in_progress():
			entity.update_plan()

		if farm(x, y):
			utils.next(size, x, y)

# 各Cellに対する処理（Trueで次に進む、Falseで原点待機）
def farm(x, y):
	return entity.exec_cell(x, y)
	
if __name__ == "__main__":
	clear()
	change_hat(Hats.Tree_Hat)
	main()
	
	
	