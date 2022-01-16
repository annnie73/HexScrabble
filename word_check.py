

def sprawdź_współrzędne(współrzędne: tuple):
	#sprawdza czy współrzędne są podane poprawnie i czy na planszy nic nie ma na tym miejscu

	if len(współrzędne) != 2: return False

	#sprawdzamy czy są to liczby naturalne
	for liczba in współrzędne:
		if not liczba.isdigit(): return False

	#musimy dodać literę, która jest już na planszy !

	for krotka in plansza:
		x,y = krotka
		if współrzędne == krotka: 
			if plansza[krotka] == ' ': return True
			else: return False

	#jeśli takich współrzędnych jeszcze nie ma, dodajemy rekurencyjnie puste rzędy
	#...
	plansza[współrzędne] = ' '
	return True

def sprawdź_słowo(słowo: str):
	if słowo.lower() in open(args.plik_słownika).read(): return True
	return False

def sprawdź_czy_poprawne(dostawka):
	#trzeba jeszcze sprawdzić, czy jedna z liter jest już na planszy
	#i czy pozostałe litery są w zbiorze liter gracza
	#osobno potem trzeba zrobić dla pierwszego ustawianego słowa

	słowo = ''
	for lista in dostawka:
		współrzędne = lista[1]
		if not sprawdź_współrzędne(współrzędne): 
			#wtedy musi to być litera, która już jest na planszy
			if plansza[współrzędne].lower() not in słowo
			#tylko jedna, inaczej:
			return False
		słowo += lista[0]
	if not sprawdź_słowo(słowo): return False
	#...


	return True 





	def check_word(self):
		#Checks the word to make sure that it is in the dictionary, and that the location falls within bounds.
		#Also controls the overlapping of words.
		global round_number, players
		word_score = 0
		global dictionary 
		#if "dictionary" not in globals():
			#dictionary = open("slownik.txt").read()#.splitlines()


		current_board_ltr = ""
		needed_tiles = ""
		blank_tile_val = ""

		#Assuming that the player is not skipping the turn:
		if self.word != "":

			#Allows for players to declare the value of a blank tile.
			if "#" in self.word:
				while len(blank_tile_val) != 1:
					blank_tile_val = input("Please enter the letter value of the blank tile: ")
				self.word = self.word[:word.index("#")] + blank_tile_val.upper() + self.word[(word.index("#")+1):]

			#Reads in the board's current values under where the word that is being played will go. Raises an error if the direction is not valid.
			if self.direction == "right":
				for i in range(len(self.word)):
					if self.board[self.location[0]][self.location[1]+i][1] == " " or self.board[self.location[0]][self.location[1]+i] == "TLS" or self.board[self.location[0]][self.location[1]+i] == "TWS" or self.board[self.location[0]][self.location[1]+i] == "DLS" or self.board[self.location[0]][self.location[1]+i] == "DWS" or self.board[self.location[0]][self.location[1]+i][1] == "*":
						current_board_ltr += " "
					else:
						current_board_ltr += self.board[self.location[0]][self.location[1]+i][1]
			elif self.direction == "down":
				for i in range(len(self.word)):
					if self.board[self.location[0]+i][self.location[1]] == "   " or self.board[self.location[0]+i][self.location[1]] == "TLS" or self.board[self.location[0]+i][self.location[1]] == "TWS" or self.board[self.location[0]+i][self.location[1]] == "DLS" or self.board[self.location[0]+i][self.location[1]] == "DWS" or self.board[self.location[0]+i][self.location[1]] == " * ":
						current_board_ltr += " "
					else:
						current_board_ltr += self.board[self.location[0]+i][self.location[1]][1]
			else:
				return "Error: please enter a valid direction."

			#Raises an error if the word being played is not in the official scrabble dictionary (dic.txt).
			if self.word not in dictionary:
				return "Please enter a valid dictionary word.\n"

			#Ensures that the words overlap correctly. If there are conflicting letters between the current board and the word being played, raises an error.
			for i in range(len(self.word)):
				if current_board_ltr[i] == " ":
					needed_tiles += self.word[i]
				elif current_board_ltr[i] != self.word[i]:
					print("Current_board_ltr: " + str(current_board_ltr) + ", Word: " + self.word + ", Needed_Tiles: " + needed_tiles)
					return "The letters do not overlap correctly, please choose another word."

			#If there is a blank tile, remove it's given value from the tiles needed to play the word.
			if blank_tile_val != "":
				needed_tiles = needed_tiles[needed_tiles.index(blank_tile_val):] + needed_tiles[:needed_tiles.index(blank_tile_val)]

			#Ensures that the word will be connected to other words on the playing board.
			if (round_number != 1 or (round_number == 1 and players[0] != self.player)) and current_board_ltr == " " * len(self.word):
				print("Current_board_ltr: " + str(current_board_ltr) + ", Word: " + self.word + ", Needed_Tiles: " + needed_tiles)
				return "Please connect the word to a previously played letter."

			#Raises an error if the player does not have the correct tiles to play the word.
			for letter in needed_tiles:
				if letter not in self.player.get_rack_str() or self.player.get_rack_str().count(letter) < needed_tiles.count(letter):
					return "You do not have the tiles for this word\n"

			#Raises an error if the location of the word will be out of bounds.
			if self.location[0] > 14 or self.location[1] > 14 or self.location[0] < 0 or self.location[1] < 0 or (self.direction == "down" and (self.location[0]+len(self.word)-1) > 14) or (self.direction == "right" and (self.location[1]+len(self.word)-1) > 14):
				return "Location out of bounds.\n"

			#Ensures that first turn of the game will have the word placed at (7,7).
			if round_number == 1 and players[0] == self.player and self.location != [7,7]:
				return "The first turn must begin at location (7, 7).\n"
			return True

		#If the user IS skipping the turn, confirm. If the user replies with "Y", skip the player's turn. Otherwise, allow the user to enter another word.
		else:
			if input("Are you sure you would like to skip your turn? (y/n)").upper() == "Y":
				if round_number == 1 and players[0] == self.player:
					return "Please do not skip the first turn. Please enter a word."
				return True
			else:
				return "Please enter a word."