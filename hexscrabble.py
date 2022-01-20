import argparse, re, pygame
from random import shuffle
import silnik_planszy as sp

#parsowanie argumentów z wiersza poleceń
parser = argparse.ArgumentParser()

parser.add_argument('-s', '--liczba_graczy_sztucznych', type = int, nargs = '?', help = 'Liczba graczy sztucznych')
parser.add_argument('-S', '--plik_słownika', type = str, nargs = '?', help = 'Plik słownika słów')
parser.add_argument('-c', '--plik_konfiguracyjny', type = str, nargs = '?', help = 'Plik konfiguracyjny')
parser.add_argument('nazwy_graczy_realnych', type = str, nargs = '*', help = 'Nazwy graczy realnych oddzielone spacją')

#ustalamy domyślne plik ze słownikiem i plik konfiguracyjny
parser.set_defaults(plik_słownika = 'slownik.txt', plik_konfiguracyjny = 'hexscrabble.cnf')
args = parser.parse_args()

#wyświetlamy planszę
plansza = sp.stwórz_planszę(8)
sp.rysuj_planszę()
screen = sp.screen
czcionka = sp.czcionka
czcionka_mała = sp.czcionka_mała
czcionka_średnia = sp.czcionka_średnia
czcionka_duża = sp.czcionka_duża

#wczytujemy zmienne lettercnt i letterfreq z pliku konfiguracyjnego
konfiguracja = compile(open(args.plik_konfiguracyjny).read(), 'string', 'exec')
eval(konfiguracja)

# Woreczek
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


# Zbiór gracza

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
	#zwraca listę jedynie litery, bez punktów
	return [płytka[0].upper() for płytka in zbiór_gracza]

def płytka(litera):
	#zwraca krotkę w postaci (litera, liczba punktów)
	for krotka in letterfreq:
		if krotka[0] == litera.upper():
			return (litera.upper(), krotka[1])
	raise Exception('Niepoprawnie podana litera.')

def usuń_ze_zbioru(zbiór_gracza, litera):
	#usuwa płytkę ze zbioru gracza, w momencie kiedy gracz ją zużywa lub wymienia
	if płytka(litera) in zbiór_gracza:
		zbiór_gracza.remove(płytka(litera))
	else: raise Exception('W zbiorze gracza nie ma podanej litery: ' + str(litera) + '.')

def uzupełnij_zbiór(zbiór_gracza):
	#dodaje płytki do zbioru gracza, aby miał ich 7 (jeśli jest odpowiednia liczba płytek w woreczku)
	while len(zbiór_gracza) < lettercnt and len(woreczek) > 0:
		dodaj_do_zbioru(zbiór_gracza)


#Rozgrywka

def sprawdź_wymianę(litery_do_wymiany):
	for litera in litery_do_wymiany:
		if not litera.isalpha():
			print('\nPodaj tylko litery.')
			return False
		if len(litera) > 1:
			print('\nOddziel litery, które chcesz wymienić.')
			return False
		if not litera.upper() in litery_gracza(gracze[aktualny_gracz][1]):
			print('\nPodaj tylko litery, które posiadasz.')
			return False
	return True

def wyświetl_litery(aktualny_gracz):
	#tworzy listkę płytek z ich współrzędnymi w pikselach i wyświetla litery gracza
	lista_płytek = []
	x = 882
	y = 253
	for i in range(len(gracze[aktualny_gracz][1])):
		płytka = gracze[aktualny_gracz][1][i][0] +'(' + str(gracze[aktualny_gracz][1][i][1]) + ')'
		if i != len(gracze[aktualny_gracz][1]) - 1:
			płytka_graf = sp.czcionka_mała.render((płytka + ', '), True, (102, 70, 62))
		else: płytka_graf = sp.czcionka_mała.render(płytka, True, (102, 70, 62))
		płytka_rect = płytka_graf.get_rect(topleft = (x,y))
		lista_płytek.append((płytka, płytka_graf, płytka_rect))
		screen.blit(płytka_graf, płytka_rect)
		x += płytka_rect.width
	return lista_płytek

def wymiana(aktualny_gracz):
	lista_płytek = wyświetl_litery(aktualny_gracz)
	instrukcja1 = sp.czcionka_b_mała.render('Kliknij myszką na litery, które chcesz wymienić,', True, (102, 70, 62))
	instrukcja2 = sp.czcionka_b_mała.render('a następnie naciśnij ENTER', True, (102, 70, 62))
	screen.blit(instrukcja1, (880, 303))
	screen.blit(instrukcja2, (880, 330))

	litery_do_wymiany = []
	
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				pozycja_myszki = pygame.mouse.get_pos()

				for i in range(len(lista_płytek)):
					#identyfikujemy sześciokąt, na który kliknął użytkownik, żeby wpisać literę
					płytka = lista_płytek[i][0]
					płytka_rect = lista_płytek[i][2]

					if płytka_rect.collidepoint(pozycja_myszki):
						#kiedy użytkownik klika w literę, podświetlamy ją i dodajemy do liter do wymiany
						litery_do_wymiany.append(płytka[0])
						if i != len(lista_płytek) - 1:
							ciemna_płytka = sp.czcionka_mała.render((płytka + ', '), True, (69, 39, 30))
						else:
							ciemna_płytka = sp.czcionka_mała.render(płytka, True, (69, 39, 30))
						ciemna_płytka_rect = płytka_rect
						screen.blit(ciemna_płytka, ciemna_płytka_rect)

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					for litera in litery_do_wymiany:
						usuń_ze_zbioru(gracze[aktualny_gracz][1], litera)
					uzupełnij_zbiór(gracze[aktualny_gracz][1])
					sp.inicjalizacja_gry()
					sp.rysuj_planszę()
					napis2 = czcionka_mała.render('Twój aktualny zbiór liter:', True, (116, 82, 74))
					screen.blit(napis2, (880, 210))
					komunikat = sp.czcionka_b_mała.render('Litery zostały wymienione.', True, (102, 70, 62))
					screen.blit(komunikat, (880, 303))
					return True
		pygame.display.update()
		sp.zegar.tick(60)
		
def koniec_tury(aktualny_gracz):
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				pozycja_myszki = pygame.mouse.get_pos()

				if sp.przycisk_k_rect.collidepoint(pozycja_myszki):
					screen.blit(sp.przycisk2, sp.przycisk_k2_rect)
					screen.blit(sp.koniec, sp.koniec_rect)
					return True

		pygame.display.update()
		sp.zegar.tick(60)

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
			#trza dodać blita wszędzie
			return False

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


# Gracze 

gracze = {}
#słownik w postaci: nr gracza: [imię, zbiór liter, wynik]
for i in range(len(args.nazwy_graczy_realnych)):
	gracze[i] = []
	gracze[i].append(args.nazwy_graczy_realnych[i])
	gracze[i].append(początkowy_zbiór_gracza())#[('K', 2), ('T', 2), ('R', 1), ('O', 1), ('Z', 1), ('O', 1), ('M', 2)])
	gracze[i].append(0)
"""
x = 1
for j in range(len(args.nazwy_graczy_realnych), args.liczba_graczy_sztucznych + len(args.nazwy_graczy_realnych)):
	gracze[j] = []
	gracze[j].append('Gracz sztuczny nr ' + str(x))
	gracze[j].append(początkowy_zbiór_gracza())
	gracze[j].append(0)
	x += 1
"""

# Gracze sztuczni

def da_się_utworzyć(słowo, zbiór_gracza):
	płytki = litery_gracza(zbiór_gracza)
	for litera in słowo:
		#jeśli mamy literę w zbiorze płytek, usuwa ją i kontynuuje   
		if litera.upper() in płytki:
			płytki.remove(litera.upper())
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
		return all(litera in słowo for litera in wymagane_litery)

def utwórz_słowa(zbiór_gracza, litera_z_planszy, słownik, wymagane_litery = ''):
	#zwraca listę słów, które da się utworzyć ze zbioru gracza, zaczynających się na podaną literę w kolejności od najwyżej punktowanych
	płytki = litery_gracza(zbiór_gracza)
	płytki.append(litera_z_planszy)
	słowa = [(słowo, wynik(słowo)) for słowo in lista_ze_słownika(słownik)
		if słowo.startswith(litera_z_planszy) and da_się_utworzyć(słowo, płytki) and
		słowo_ma_litery(słowo, wymagane_litery)]
	
	return sorted(słowa, key = lambda x: x[1], reverse = True)

print(utwórz_słowa([('N', 1), ('A', 1), ('Ł', 3), ('E', 1), ('Y', 2), ('G', 3), ('L', 2)], 'b', 'slownik.txt'))

#print(wstaw(plansza, stwórz_dostawkę('kot', (0,0), 'p')))
#print(plansza)


def rozgrywka(gracze: dict, konfiguracja: list):
	#dopracować co to konfiguracja
	global numer_rundy, aktualny_gracz, woreczek, plansza
	sp.inicjalizacja_gry()
	screen.blit(sp.litery, (880, 210))
	while True:
		while len(woreczek) != 0:
			#pokazuje, czyja jest tura, wyświetla aktualny stan planszy i zbiór liter gracza
			numer = czcionka_średnia.render(str(numer_rundy), True, (102, 70, 62))
			screen.blit(numer, (988, 110))
			imię = czcionka_mała.render(gracze[aktualny_gracz][0], True, (102, 70, 62))
			screen.blit(imię, (1060, 150))
			sp.rysuj_planszę()
			#print('Liczba liter pozostałych w woreczku to ' + str(len(woreczek)) + '.')
			
			#ruch gracza realnego
			if aktualny_gracz <= len(args.nazwy_graczy_realnych) - 1: #zmienimy, zeby mogl byc najpierw komputer
				sp.rysuj_planszę()
				wyświetl_litery(aktualny_gracz)
				dostawka = sp.ruch_gracza_realnego(aktualny_gracz)
				if dostawka:#sp.ruch_gracza_realnego(aktualny_gracz):
					if wstaw(plansza, dostawka):
						sp.rysuj_planszę() 
						#dokończyć - przede wszystkim punkty i nowe literki
				else:
					wymiana(aktualny_gracz)
					screen.blit(numer, (988, 110))
					screen.blit(imię, (1060, 150))
					wyświetl_litery(aktualny_gracz)
					koniec_tury(aktualny_gracz)
					
					
					

							#blitujemy literki gracza
							#blitujemy punkty gracza
							#przechodzimy do kolejnego gracza
							#print('\nSłowo zostało ustawione. \nTwój aktualny zbiór liter to: ' + #zbiór_gracza_str(gracze[aktualny_gracz][1]))

				#print('\nZbiór liter gracza ' + gracze[aktualny_gracz][0] + ': ' + zbiór_gracza_str(gracze[aktualny_gracz][1]))

				"""
					count = 1
					while count <= 6:
						słowo_gracza = input('Podaj słowo, które chcesz zagrać: ')
						if not sprawdź_słowo(słowo_gracza): 
							print('Twoje słowo jest nieprawidłowe.')
							count += 1
							continue

						współrzędne = input('Podaj współrzędne pierwszej litery: ')
						if sprawdź_współrzędne(współrzędne): 
							współrzędne = sprawdź_współrzędne(współrzędne)
						else: 
							print('Te współrzędne są nieprawidłowe.')
							count += 1
							continue

						kierunek = input('Podaj kierunek, w którym chcesz ustawić słowo - poziomo (p), w górę (g) lub w dół (d): ')
						if stwórz_dostawkę(słowo_gracza, współrzędne, kierunek):
							dostawka = stwórz_dostawkę(słowo_gracza, współrzędne, kierunek)
							if wstaw(plansza, dostawka):
								print('\n', plansza)
								print('\nSłowo zostało ustawione. \nTwój aktualny zbiór liter to: ' + zbiór_gracza_str(gracze[aktualny_gracz][1]))
								break
							else: 
								count += 1
								continue
						else:
							print('Ten kierunek nie jest poprawny.')
							count += 1
							continue
					else:
						print('Podałeś nieprawidłowe dane za dużo razy. Twoja tura przepadła. ')

				#wyświetlamy aktualny wynik gracza
				print('\n' + gracze[aktualny_gracz][0] + ', Twój aktualny wynik to ' + str(gracze[aktualny_gracz][2]) + '.')
				"""
			#else:
				#ruch gracza sztuczego

			#kolejny gracz
			if aktualny_gracz != len(gracze)-1:
				aktualny_gracz += 1
			else:
				aktualny_gracz = 0
				numer_rundy += 1

			#funkcja wołana rekurencyjnie
			sp.pygame.display.update()
			sp.zegar.tick(60)
			rozgrywka(gracze, konfiguracja)

	else:
		koniec_gry()


def koniec_gry():
	#gra kończy się, kiedy w woreczku skończą się litery
	global gracze
	najwyższy_wynik = 0
	for i in range(len(gracze)):
		if gracze[i][2] > najwyższy_wynik:
			najwyższy_wynik = gracze[i][2]
			zwycięzca = gracze[i][0]
	print('Koniec gry. Zwycięzcą jest ' + zwycięzca + '.')

print(gracze)
#print('\nWitaj w grze Hex Scrabble!')

numer_rundy = 1
aktualny_gracz = 0
if __name__ == '__main__':
	rozgrywka(gracze, konfiguracja)


