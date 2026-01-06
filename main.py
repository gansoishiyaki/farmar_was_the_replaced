import utils
import entity
import globals

def main():
	# 目標エンティティを設定
	globals.target_entity = Entities.Pumpkin
	
	while True:
		# 原点に戻ったら栽培計画を更新（サイクル進行中はスキップ）
		if utils.is_origin() and not entity.is_cycle_in_progress():
			entity.update_plan()
			
		farm()
		utils.next()

# 各Cellに対する処理
def farm():
	x = get_pos_x()
	y = get_pos_y()
	entity.exec_cell(x, y)
	
if __name__ == "__main__":
	clear()
	change_hat(Hats.Tree_Hat)
	main()
	
	
	