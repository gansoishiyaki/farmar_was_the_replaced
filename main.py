import utils
import entity

def main():
	while True:
		# 原点に戻ったら栽培計画を更新
		if utils.is_origin():
			entity.update_plan()
			
		farm()
		utils.next()

# 各Cellに対する処理
def farm():
	entity.exec_cell()

	x = get_pos_x()
	y = get_pos_y()
	expected = entity.get_type(x, y)

	utils.harvest_if_mismatch(expected)
	entity.get_func(expected)()
	
if __name__ == "__main__":
	clear()
	change_hat(Hats.Tree_Hat)
	main()
	
	
	