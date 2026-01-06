import utils
import entity

def main():
	while True:
		farm()
		utils.next()

# 各Cellに対する処理
def farm():
	entity.exec_cell()
	
	x = get_pos_x()
	y = get_pos_y()
	type = entity.get_type(x, y)
	entity.get_func(type)()
	
if __name__ == "__main__":
	clear()
	change_hat(Hats.Tree_Hat)
	main()
	
	
	