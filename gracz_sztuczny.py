
import argparse, re, copy
from random import shuffle

'''
schemat ruchu gracza:
1. szukamy miejsc na planszy, w których da się utworzyć słowa - osobno dla każdego kierunku 
   przechowujemy je, np. w słowniku (współrzędne): [litera, najdłuższe słowo, które można utworzyć]
2. dla każdej literki tworzymy listę słów, które można utworzyć, nie przekraczających danej długości
   - kompilujemy te listy, tak aby nie utracić informacji o danym polu i literze
3. sprawdzamy, które słowo jest najwyżej punktowane i ustawiamy je
4. jeśli nie da się utworzyć żadnego słowa, wymieniamy wszystkie litery oprócz samogłosek, jeśli ich liczba nie przekracza 3

'''
'''
def da_się_utworzyć(słowo, zbiór_gracza):
	płytki = litery_gracza(zbiór_gracza)
	for litera in słowo:
		#jeśli mamy literę w zbiorze płytek, usuwa ją i kontynuuje   
		if litera.upper() in płytki:
			płytki.remove(litera.upper())
		else:
			return False
	return True
	#trzeba będzie zmienić
'''
def da_się_utworzyć(słowo, płytki: list):
	#płytki = litery_gracza(zbiór_gracza)
	litery = copy.deepcopy(płytki)
	for litera in słowo:
		#jeśli mamy literę w zbiorze płytek, usuwa ją i kontynuuje   
		if litera.upper() in litery:
			litery.remove(litera.upper())
		else:
			return False
	return True

def można_utworzyć(potrzebne_litery, zbiór_gracza):
	płytki = litery_gracza(zbiór_gracza)
	for litera in potrzebne_litery:
		#jeśli mamy literę w zbiorze płytek, usuwa ją i kontynuuje   
		if litera.upper() in płytki:
			płytki.remove(litera.upper())
		else:
			return False
	return True

def słowo_ma_litery(słowo, wymagane_litery):
	if not wymagane_litery:
		return True
	else:
		return all(litera.lower() in słowo for litera in wymagane_litery)

def utwórz_słowa(zbiór_gracza, litera_z_planszy, długość, słownik = args.plik_słownika, wymagane_litery = ''):
	#zwraca listę słów, które da się utworzyć ze zbioru gracza, zaczynających się na podaną literę w kolejności od najwyżej punktowanych
	płytki = litery_gracza(zbiór_gracza)
	płytki.append(litera_z_planszy)
	słowa = [(słowo, wynik(słowo)) for słowo in lista_ze_słownika(słownik)
		if słowo.startswith(litera_z_planszy.lower()) and da_się_utworzyć(słowo, płytki) and
		słowo_ma_litery(słowo, wymagane_litery) and len(słowo) <= długość]
	
	return sorted(słowa, key = lambda x: x[1], reverse = True)

def najlepsze(lista_słów):
	return lista_słów[0]

def stwórz_dostawkę(słowo: str, pierwsza_współrzędna: tuple, kierunek: str):
	#zwraca listę krotek w postaci (litera, współrzędne) w zależności od kierunku wpisywanego słowa
	słowo = słowo.upper()
	współrzędne = []
	x,y = pierwsza_współrzędna

	if kierunek.lower() == 'p':
		i = 0
		while i <= len(słowo):
			współrzędne.append((x,y))
			x += 1
			i += 1
	elif kierunek.lower() == 'g':
		i = 0
		while i <= len(słowo):
			współrzędne.append((x,y))
			y += 1
			i += 1
	elif kierunek.lower() == 'd':
		i = 0
		while i <= len(słowo):
			współrzędne.append((x,y))
			x -= 1
			y -= 1
			i += 1	
	else: 
		return False
	return list(zip(słowo, współrzędne))

print(stwórz_dostawkę('kot', (0,0), 'p'))

def sprawdź_współrzędne(współrzędne: str):
	#sprawdza czy współrzędne są podane poprawnie

	współrzędne_lista =re.findall(r'-?\d+', współrzędne)
  
	if len(współrzędne_lista) != 2:
		return False

	współrzędne = [int(x) for x in współrzędne_lista]
	return tuple(współrzędne)

def sprawdź_pierwszą_współrzędną(dostawka):
	for lista in dostawka:
		if lista[1] == (0,0): return True
	return False

def lista_ze_słownika(słownik):
	return [słowo for słowo in open(słownik).read().split() if len(słowo) > 1]

def sprawdź_słowo(słowo: str):
	if słowo.lower() in lista_ze_słownika(args.plik_słownika): return True
	return False

def sprawdź_czy_poprawne(dostawka): 

	#inicjujemy listę liter, których potrzebuje gracz, aby utworzyć dane słowo
	potrzebne_litery = []

	for i in range(len(dostawka)):
		litera = dostawka[i][0]
		współrzędne = dostawka[i][1]

		#sprawdzamy poprawność współrzędnych

		if współrzędne not in plansza:
			#jeśli takich współrzędnych nie ma, dodajemy je
			plansza[współrzędne] = ' '
			potrzebne_litery.append(litera.upper())
			#... później trzeba będzie w tym miejscu albo przy rysowaniu planszy dodać puste rzędy

		elif plansza[współrzędne] == ' ':
			#jeśli nic nie ma na tym miejscu, dana litera musi być w zbiorze gracza
			potrzebne_litery.append(litera.upper())

		elif plansza[współrzędne] != litera.upper():
			print('Litery nie nakładają się poprawnie. Wybierz inne słowo. ')
			return False

	#sprawdzamy, czy słowo gracza łączy się ze słowami będącymi już na planszy
	if len(potrzebne_litery) == len(dostawka) and (not all(plansza[klucz] == ' ' for klucz in plansza)):
	#if (numer_rundy != 1 or (numer_rundy == 1 and aktualny_gracz != 0)) and current_board_ltr == " " * len(self.word):
		print('Twoje słowo musi łączyć się ze słowem będącym już na planszy. ')
		return False

	#sprawdzamy, czy gracz wykorzystał chociaż jedną literę ze swojego zbioru
	if len(potrzebne_litery) < 1:
		print('Musisz wykorzystać chociaż jedną literę ze swojego zbioru. ')
		return False

	#sprawdzamy, czy gracz ma w swoim zbiorze potrzebne płytki

	#tutaj trzeba zmienić
	if not można_utworzyć(potrzebne_litery, gracze[aktualny_gracz][1]):
		print('Nie masz liter potrzebnych do utworzenia tego słowa. ')
		return False

	#upewniamy się, że pierwsze słowo postawione na planszy przechodzi przez punkt 0,0
	if all(plansza[klucz] == ' ' for klucz in plansza) and (not sprawdź_pierwszą_współrzędną(dostawka)):
		print('Pierwsze słowo na planszy musi przechodzić przez punkt 0,0. ')
		return False
	
	return potrzebne_litery

def wynik(słowo):
	count = 0
	if sprawdź_słowo(słowo):
		for litera in słowo:
			litera = litera.upper()
			for i in range(len(letterfreq)):
				if letterfreq[i][0] == litera:
					count += letterfreq[i][1]
					continue
		return count
	return -1

print(utwórz_słowa([('N', 1), ('A', 1), ('Ł', 3), ('E', 1), ('Y', 2), ('G', 3), ('L', 2)], 'b', 10, 'slownik.txt'))

'''
def pierwsza_i_ostatnia(pierwsza = '', ostatnia = ''):
	słowa = [(słowo, punkty(plansza, stwórz_dostawkę(słowo)))
		for słowo in lista_ze_słownika('slownik.txt')
		if słowo.startswith(pierwsza) and słowo.endswith(ostatnia)]
	
	return sorted(słowa, key = lambda x: x[1], reverse = True)
'''

def znajdź_dostawki_prawo(pole, kopia_planszy, count = 1):
	x,y = pole
	assert type(x) == type(y) == int
	assert pole in kopia_planszy

	#print(count, x, y)
	#print(kopia_planszy)

	if count < 8:	
		if (x+1, y) not in kopia_planszy:
			kopia_planszy[x+1,y] = ' '

		if kopia_planszy[x+1,y] != ' ':
			return [(x - (count - 1), y), plansza[x - (count - 1), y], count - 1, 'p']
		
		count += 1
		x += 1
	
		znajdź_dostawki_prawo((x,y), kopia_planszy, count)

	return [(x - (count - 1), y), plansza[x - (count - 1), y], 7, 'p']

wstaw(plansza, stwórz_dostawkę('kot', (0,0), 'p'))
print(znajdź_dostawki_prawo((0,0), copy.deepcopy(plansza)))


def znajdź_dostawki_góra(pole, kopia_planszy, count = 1):
	x,y = pole
	assert type(x) == type(y) == int
	assert pole in kopia_planszy

	if count < 8:
		if (x, y+1) not in kopia_planszy:
			kopia_planszy[x,y+1] = ' '

		if kopia_planszy[x,y+1] != ' ':
			return (x, y - (count - 1)), plansza[x, y - (count - 1)], count - 1, 'g'
		
		count += 1
		y += 1
		
		print(x, y, count)
		znajdź_dostawki_góra((x,y), kopia_planszy, count)
	
	return [(x, y - (count - 1)), plansza[x, y - (count - 1)], 7, 'g'] #trzeba będzie poprawić

print((0,0), copy.deepcopy(plansza), 1)
print(znajdź_dostawki_góra((0,0), copy.deepcopy(plansza)))

def znajdź_dostawki_dół(pole, kopia_planszy, count = 1) -> list:
	x,y = pole
	assert type(x) == type(y) == int
	assert pole in kopia_planszy

	if count < 8:
		if (x-1, y-1) not in kopia_planszy:
			kopia_planszy[x-1,y-1] = ' '

		if kopia_planszy[x-1,y-1] != ' ':
			return [(x + (count - 1), y + (count - 1)), plansza[x + (count - 1), y  + (count - 1)], count - 1, 'd']

		count += 1
		x -= 1
		y -= 1
	
		znajdź_dostawki_dół((x,y), kopia_planszy, count)

	return [(x + (count - 1), y + (count - 1)), plansza[x + (count - 1), y  + (count - 1)], 7, 'd']

print(znajdź_dostawki_dół((0,0), copy.deepcopy(plansza)))

def znajdź_dostawkę(aktualny_gracz):
	global plansza, gracze

	opcje = []
	for pole in plansza: 
		if plansza[pole][0] != ' ':
			opcje.append(znajdź_dostawki_prawo(pole, copy.deepcopy(plansza)))
			opcje.append(znajdź_dostawki_góra(pole, copy.deepcopy(plansza)))
			opcje.append(znajdź_dostawki_dół(pole, copy.deepcopy(plansza)))
		print(opcje)

	lista_słów_ze_współrzędnymi =[]
	#otrzymujemy listę list w postaci [(słowo, punkty), współrzędne, kierunek]
	for lista in opcje:
		if lista[2] > 1:
			słowa = utwórz_słowa(gracze[aktualny_gracz][1], lista[1], lista[2])
			print(słowa)
			if len(słowa) > 0:
				lista_słów_ze_współrzędnymi.append([słowa[0], lista[0], lista[3]])

	lista_słów_ze_współrzędnymi = sorted(lista_słów_ze_współrzędnymi, key = lambda x: x[0][1], reverse = True)
	if lista_słów_ze_współrzędnymi:
		return lista_słów_ze_współrzędnymi[0]
	return False
