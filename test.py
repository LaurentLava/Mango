

def perform_test():
	with open("logs.txt", 'r') as f:
		data = f.read()
		# print(data)
		print(data.count('\n'))
		list_of_indexes = [pos for pos, char in enumerate(data) if char == '\n']
		print(list_of_indexes)
		print(list_of_indexes[-100])


if __name__ == "__main__":

	perform_test()