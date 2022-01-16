
import argparse
from random import shuffle
import re
import copy

parser = argparse.ArgumentParser()

parser.add_argument('-s', '--liczba_graczy_sztucznych', type = int, nargs = '?', help = 'Liczba graczy sztucznych')
parser.add_argument('-S', '--plik_słownika', type = str, nargs = '?', help = 'Plik słownika słów')
parser.add_argument('-c', '--plik_konfiguracyjny', type = str, nargs = '?', help = 'Plik konfiguracyjny')
parser.add_argument('nazwy_graczy_realnych', type = str, nargs = '*', help = 'Nazwy graczy realnych oddzielone spacją')

#ustalamy domyślne plik ze słownikiem i plik konfiguracyjny
parser.set_defaults(plik_słownika = 'slownik.txt', plik_konfiguracyjny = 'hexscrabble.cnf')
args = parser.parse_args()

#wczytujemy zmienne lettercnt i letterfreq z pliku konfiguracyjnego
konfiguracja = compile(open(args.plik_konfiguracyjny).read(), 'string', 'exec')
eval(konfiguracja)

aktualny_gracz = 0

woreczek = []

def dodaj_do_woreczka(litera, ilość):
	#dodaje do woreczka podaną ilość danej płytki
	for i in range(ilość):
		woreczek.append(litera)

def początkowy_woreczek():
	#dodaje początkowy zbiór płytek do woreczka
	for i in range(len(letterfreq)):
		dodaj_do_woreczka((letterfreq[i][0],letterfreq[i][1]), letterfreq[i][2])
	shuffle(woreczek)
początkowy_woreczek()

def dodaj_do_zbioru(zbiór_gracza):
	#bierze płytkę z woreczka i dodaje do zbioru liter gracza
	zbiór_gracza.append(woreczek.pop())

def początkowy_zbiór_gracza():
	#inicjuje zbiór liter gracza i daje do niego początkowe 7 liter
	zbiór = []
	for i in range(lettercnt):
		dodaj_do_zbioru(zbiór)
	return zbiór

def zbiór_gracza_str(zbiór_gracza: list) -> str: 
	#wyświetla zbiór liter gracza w formie litera(liczba_punktów)
	lista = []
	for litera, punkty in zbiór_gracza:
		płytka = f'{litera}({punkty})' 
		lista.append(płytka)
	return ', '.join(lista)

def litery_gracza(zbiór_gracza) -> list:
	return [płytka[0].upper() for płytka in zbiór_gracza]

def płytka(litera):
	for krotka in letterfreq:
		if krotka[0] == litera.upper():
			return (litera.upper(), krotka[1])
	raise Exception('Niepoprawnie podana litera.')

def usuń_ze_zbioru(zbiór_gracza, litera):
	#usuwa płytkę ze zbioru gracza, w momencie kiedy gracz ją zużywa lub wymienia
	if płytka(litera) in zbiór_gracza:
		zbiór_gracza.remove(płytka(litera))
	else: raise Exception('W zbiorze gracza nie ma podanej litery. ')

def uzupełnij_zbiór(zbiór_gracza):
	#dodaje płytki do zbioru gracza, aby miał ich 7 (jeśli jest odpowiednia liczba płytek w woreczku)
	while len(zbiór_gracza) < lettercnt and len(woreczek) > 0:
		dodaj_do_zbioru(zbiór_gracza)

gracze = {}
#słownik w postaci: nr gracza: [imię, zbiór liter, wynik]
for i in range(3):
	gracze[i] = []
	gracze[i].append('imię')
	gracze[i].append([('K', 2), ('O', 1), ('T', 2), ('E', 1), ('K', 2), ('C', 2), ('Z', 1)])
	gracze[i].append(0)

plansza = {}
#tworzymy początkową planszę w postaci słownika, gdzie kluczem są współrzędne, a wartością ' ' lub litera
#dodajemy do słownika, kiedy gracz umieści jakieś słowo - dzięki temu plansza może być nieskończona
for y in range(3,-4,-1):
	for x in range(-3,4,1):
		plansza[x,y] = ' '

def sprawdź_słowo(słowo: str):
	if słowo.lower() in lista_ze_słownika(args.plik_słownika): return True
	return False

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

def lista_ze_słownika(słownik):
	return [słowo for słowo in open(słownik).read().split() if len(słowo) > 1]

def litery_gracza(zbiór_gracza) -> list:
	return [płytka[0].upper() for płytka in zbiór_gracza]


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

def utwórz_słowa(zbiór_gracza, litera_z_planszy, długość, słownik = 'slownik.txt', wymagane_litery = ''):
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

def punkty(plansza, dostawka) -> int: 
#zwraca ile punktów zdobywają litery wstawione na planszę zgodnie z dostawką
#jeśli dostawka jest nieprawidłowa zwraca −1 lub rzuca wyjątkiem. Plansza nie zmienia się.
	count = 0
	if sprawdź_czy_poprawne(dostawka):
		for lista in dostawka:
			litera = lista[0].upper()
			for i in range(len(letterfreq)):
				if letterfreq[i][0] == litera:
					count += letterfreq[i][1]
					continue
		return count
	raise Exception('Niepoprawna dostawka.')

def wstaw(plansza, dostawka) -> bool:
	#wstawia dostawkę na planszę. Zwraca True gdy udało się, False gdy dostawka nie jest prawidłowa.

	#jeśli dostawka była prawidłowa, funkcja sprawdź_czy_poprawne zwraca listę liter do usunięcia ze zbioru gracza
	potrzebne_litery = sprawdź_czy_poprawne(dostawka)
	if not potrzebne_litery: return False

	gracze[aktualny_gracz][2] += punkty(plansza, dostawka)
	for lit in potrzebne_litery:
		usuń_ze_zbioru(gracze[aktualny_gracz][1], lit)
	uzupełnij_zbiór(gracze[aktualny_gracz][1])

	#dodajemy dostawkę na planszę
	for krotka in dostawka:
		litera = krotka[0]
		współrzędne = krotka[1]

		for klucz in plansza:
			if klucz == współrzędne:
					plansza[klucz] = litera
					continue #można spróbować z break
	return True

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

opcje = []
for pole in plansza:
	if plansza[pole] != ' ':
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

print(lista_słów_ze_współrzędnymi)

print(sorted(lista_słów_ze_współrzędnymi, key = lambda x: x[0][1], reverse = True))
