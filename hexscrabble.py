import argparse, re, pygame, copy
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

lista_ze_słownika = [słowo for słowo in open(args.plik_słownika).read().split() if len(słowo) > 1]

#wyświetlamy planszę
sp.stwórz_planszę(8)
plansza = sp.rysuj_planszę()

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
	screen.blit(instrukcja1, (880, 338))
	screen.blit(instrukcja2, (880, 365))

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
					screen.blit(komunikat, (880, 323))
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

#print(stwórz_dostawkę('kot', (0,0), 'p'))


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

def sprawdź_słowo(słowo: str):
	if słowo.lower() in lista_ze_słownika: return True
	return False

# Sprawdzanie dostawki

# Funkcje pomocnicze
def sprawdź_wstecz_p(x,y, słowo):
	global plansza
	kopia_planszy = copy.deepcopy(plansza)

	if not (x-1, y) in kopia_planszy:
		#musimy jeszcze odwrócić słowo
		return słowo[::-1] #mamy na razie sam początek słowa

	if kopia_planszy[(x-1, y)][0] == ' ':
		return słowo[::-1]
			
	
	słowo += kopia_planszy[(x-1, y)][0]
	return sprawdź_wstecz_p(x-1, y, słowo)
		
def sprawdź_wstecz_g(x,y, słowo):
	global plansza
	kopia_planszy = copy.deepcopy(plansza)

	if not (x, y-1) in kopia_planszy:
		return słowo[::-1] 
	if kopia_planszy[(x, y-1)][0] == ' ':
		return słowo[::-1] 
	
	słowo += kopia_planszy[(x, y-1)][0]
	return sprawdź_wstecz_g(x, y-1, słowo)

def sprawdź_wstecz_d(x,y, słowo):
	global plansza
	kopia_planszy = copy.deepcopy(plansza)

	if not (x-1, y+1) in kopia_planszy:
		return słowo[::-1]
	if kopia_planszy[(x-1, y+1)][0] == ' ':
		return słowo[::-1]
	
	słowo += kopia_planszy[(x-1, y+1)][0]
	return sprawdź_wstecz_d(x-1,y+1, słowo)

def sprawdź_dalej_p(x,y, słowo):
	global plansza
	kopia_planszy = copy.deepcopy(plansza)

	if not (x+1, y) in kopia_planszy:
		return słowo

	if kopia_planszy[(x+1, y)][0] == ' ':
		return słowo 
	
	słowo += kopia_planszy[(x+1, y)][0]
	return sprawdź_dalej_p(x+1, y, słowo)

def sprawdź_dalej_g(x,y, słowo):
	global plansza
	kopia_planszy = copy.deepcopy(plansza)

	if not (x, y+1) in kopia_planszy:
		return słowo
	if kopia_planszy[(x, y+1)][0] == ' ':
		return słowo 

	słowo += kopia_planszy[(x, y+1)][0]
	return sprawdź_dalej_g(x, y+1, słowo)

def sprawdź_dalej_d(x,y, słowo):
	global plansza
	kopia_planszy = copy.deepcopy(plansza)

	if not (x+1, y-1) in kopia_planszy:
		return słowo
	if kopia_planszy[(x+1, y-1)][0] == ' ':
		return słowo 

	słowo += kopia_planszy[(x+1, y-1)][0]
	return sprawdź_dalej_d(x+1,y-1, słowo)

def sprawdź_czy_poprawne(dostawka): 
	#sprawdza czy słowa poprawnie się nakładają i czy gracz ma litery potrzebne do utworzenia słowa

	global plansza, gracze, aktualny_gracz
	kopia_planszy = copy.deepcopy(plansza)
	słowo = ''

	if not dostawka: return False
	x0, y0 = dostawka[0][1]

	if 'Gracz sztuczny nr' in gracze[aktualny_gracz][0]:
		#gracz realny nie ma mozliwości nadpisywania liter, ale dla gracza sztucznego musimy sprawdzić, czy tego nie robi
		for litera, współrzędne in dostawka:
			if plansza[współrzędne][0] != ' ' and plansza[współrzędne] != litera.upper():
				return False

	#osobno rozwazamy przypadek jednoliterowej dostawki
	if len(dostawka) == 1:
		if (x0-1, y0) in plansza and (plansza[(x0-1, y0)][0] != ' ' or plansza[(x0+1, y0)][0] != ' '):
			kierunek = 'p'
		elif (x0, y0-1) in plansza and (plansza[(x0, y0-1)][0] != ' ' or plansza[(x0, y0+1)][0] != ' '):
			kierunek = 'g'
		elif (x0-1,y0+1) in plansza and (plansza[(x0-1,y0+1)][0] != ' ' or plansza[(x0+1,y0-1)][0] != ' '):
			kierunek = 'd'
		else:
			komunikat = sp.czcionka_b_mała.render('Twoje słowo musi łączyć się z innymi', True, (102, 70, 62))
			komunikat2 = sp.czcionka_b_mała.render('słowami na planszy.', True, (102, 70, 62))
			screen.blit(komunikat, (880, 338))
			screen.blit(komunikat2, (880, 365))
			sp.rysuj_planszę()
			return False

	#jeśli dla wszystkich liter y-współrzędna jest taka sama: kierunek słowa to poziomo - sortujemy dostawkę od po x
	elif all(dostawka[i][1][1] == y0 for i in range(len(dostawka))):
		dostawka = sorted(dostawka, key = lambda x: x[1][0])
		kierunek = 'p'

	#analogicznie z x-współrzędną - wtedy kierunek to do góry i sortujemy po y
	elif all(dostawka[i][1][0] == x0 for i in range(len(dostawka))):
		dostawka = sorted(dostawka, key = lambda x: x[1][1])
		kierunek = 'g'

	#jeśli nie, kierunek powinien być do dołu - sortujemy po x i sprawdzamy czy y się zmniejszają
	else:
		dostawka = sorted(dostawka, key = lambda x: x[1][0])
		if all(dostawka[j][1][1] < dostawka[i][1][1] for i in range(len(dostawka)-1) for j in range(i+1, len(dostawka))):
			kierunek = 'd'
		else: 
			print('1')
			print(dostawka)
			komunikat = sp.czcionka_b_mała.render('Twoje litery muszą leżeć w jednej linii.', True, (102, 70, 62))
			screen.blit(komunikat, (880, 338))
			sp.rysuj_planszę()
			return False

	#mając zidentyfikowany kierunek, sprawdzamy czy gracz przedłuzał słowo z planszy, cofając się po odpowiednich współrzędnych
	
	if kierunek == 'p':
		słowo = sprawdź_wstecz_p(x0, y0, '')

	elif kierunek == 'g':
		słowo = sprawdź_wstecz_g(x0, y0, '')

	elif kierunek == 'd':
		słowo = sprawdź_wstecz_d(x0, y0, '')

	else:
		raise Exception

	#teraz sprawdzamy czy litery dostawione przez uzytkownika sa w jednej linii i nie ma przerw w środku, równolegle dodając litery które wstawił na planszę do listy liter, których potrzebuje, aby utworzyć dane słowo i przedłuzając słowo o odpowiednie litery
	potrzebne_litery = []
	x, y = x0, y0

	if kierunek == 'p':
		while x <= dostawka[-1][1][0]:
			if kopia_planszy[(x, y)][0] == ' ':
				for i in range(len(dostawka)):
					if (x, y) == dostawka[i][1]:
						słowo += dostawka[i][0]
						potrzebne_litery.append(dostawka[i][0])
						x += 1
						break
				else:
					#jeśli plansza jest pusta, a w utworzonej przez gracza dostawce nie ma takich współrzędnych, oznacza to, ze w słowie jest przerwa

					komunikat = sp.czcionka_b_mała.render('W Twoim słowie nie może być przerw.', True, (102, 70, 62))
					screen.blit(komunikat, (880, 338))
					sp.rysuj_planszę()
					return False
			else:
				słowo += kopia_planszy[(x, y)][0]
				x += 1

	#analogicznie z dwoma pozostałymi kierunkami
	elif kierunek == 'g':
		while y <= dostawka[-1][1][1]:
			if kopia_planszy[(x, y)][0] == ' ':
				for i in range(len(dostawka)):
					print(dostawka)
					if (x, y) == dostawka[i][1]:
						słowo += dostawka[i][0]
						potrzebne_litery.append(dostawka[i][0])
						y += 1
						break
				else:
					komunikat = sp.czcionka_b_mała.render('W Twoim słowie nie może być przerw.', True, (102, 70, 62))
					screen.blit(komunikat, (880, 338))
					sp.rysuj_planszę()
					return False
			else:
				słowo += kopia_planszy[(x, y)][0]
				y += 1

	elif kierunek == 'd':
		while x <= dostawka[-1][1][0] and y >= dostawka[-1][1][1]:
			if kopia_planszy[(x, y)][0] == ' ':
				for i in range(len(dostawka)):
					if (x, y) == dostawka[i][1]:
						słowo += dostawka[i][0]
						potrzebne_litery.append(dostawka[i][0])
						x += 1
						y -= 1
						break
				else:
					komunikat = sp.czcionka_b_mała.render('W Twoim słowie nie może być przerw.', True, (102, 70, 62))
					screen.blit(komunikat, (880, 338))
					sp.rysuj_planszę()
					return False
			else:
				słowo += kopia_planszy[(x, y)][0]
				x += 1
				y -= 1

	#teraz sprawdzamy jeszcze czy za ostatnią dodaną literą nie ma kontynuacji słowa
	(xo, yo) = dostawka[-1][1]
	if kierunek == 'p':
		słowo = sprawdź_dalej_p(xo, yo, słowo)

	elif kierunek == 'g':
		słowo = sprawdź_dalej_g(xo, yo, słowo)
	
	elif kierunek == 'd':
		słowo = sprawdź_dalej_d(xo, yo, słowo)

	#teraz dla kazdej litery sprawdzamy jej sąsiadów poza tymi w kierunku, w którym ustawione jest słowo - jeśli pole nie jest puste, idziemy w tę stronę tak długo, az nie dojdziemy do pustego pola

	lista_słów = [słowo]

	for i in range(len(dostawka)):
		litera = dostawka[i][0]
		x, y = dostawka[i][1]
		if kierunek == 'p':
			#jeśli główne słowo układane jest w prawo, to dla kazdej dostawionej litery sprawdzamy litery w obu kierunkach po skosie

			słowo1 = ''
			if (x, y-1) in kopia_planszy and kopia_planszy[(x, y-1)] != ' ':
				słowo1 = sprawdź_wstecz_g(x,y, litera)
			if (x, y+1) in kopia_planszy and kopia_planszy[(x, y+1)] != ' ':
				if len(słowo1) > 1:
					słowo1 += sprawdź_dalej_g(x,y, słowo1)
				else: słowo1 = sprawdź_dalej_g(x,y, litera)
			if len(słowo1) > 1:
				lista_słów.append(słowo1)
				print(lista_słów)

			słowo2 = ''
			if (x+1, y-1) in kopia_planszy and kopia_planszy[(x+1, y-1)] != ' ':
				słowo2 = sprawdź_wstecz_d(x,y, litera)

			if (x-1, y+1) in kopia_planszy and kopia_planszy[(x-1, y+1)] != ' ':
				if len(słowo2) > 1:
					słowo2 += sprawdź_dalej_d(x,y, słowo2)
				else: słowo2 = sprawdź_dalej_d(x,y, litera)
			if len(słowo2) > 1:
				lista_słów.append(słowo2)
				print(lista_słów)

		
		elif kierunek == 'g':
			#analogicznie w przypadku pozostałych kierunków
			słowo1 = ''
			if (x-1, y) in kopia_planszy and kopia_planszy[(x-1, y)] != ' ':
				słowo1 = sprawdź_wstecz_p(x,y, litera)
			if (x+1, y) in kopia_planszy and kopia_planszy[(x+1, y)] != ' ':
				if len(słowo1) > 1:
					słowo1 += sprawdź_dalej_p(x,y, słowo1)
				else: słowo1 = sprawdź_dalej_p(x,y, litera)
			if len(słowo1) > 1:
				lista_słów.append(słowo1)
				print(lista_słów)

			słowo2 = ''
			if (x+1, y-1) in kopia_planszy and kopia_planszy[(x+1, y-1)] != ' ':
				słowo2 = sprawdź_wstecz_d(x,y, litera)
			if (x-1, y+1) in kopia_planszy and kopia_planszy[(x-1, y+1)] != ' ':
				if len(słowo2) > 1:
					słowo2 += sprawdź_dalej_d(x,y, słowo2)
				else: słowo2 = sprawdź_dalej_d(x,y, litera)
			if len(słowo2) > 1:
				lista_słów.append(słowo2)
				print(lista_słów)
		
		elif kierunek == 'd':
			słowo1 = ''
			if (x-1, y) in kopia_planszy and kopia_planszy[(x-1, y)] != ' ':
				słowo1 = sprawdź_wstecz_p(x,y,litera)
			if (x+1, y) in kopia_planszy and kopia_planszy[(x+1, y)] != ' ':
				if len(słowo1) > 1:
					słowo1 += sprawdź_dalej_p(x,y, słowo1)
				else: słowo1 = sprawdź_dalej_p(x,y, litera)
			if len(słowo1) > 1:
				lista_słów.append(słowo1)
				print(lista_słów)

			słowo2 = ''
			if (x, y-1) in kopia_planszy and kopia_planszy[(x, y-1)] != ' ':
				słowo2 = sprawdź_wstecz_g(x,y,litera)
			if (x, y+1) in kopia_planszy and kopia_planszy[(x, y+1)] != ' ':
				if len(słowo2) > 1:
					słowo2 += sprawdź_dalej_g(x,y, słowo1)
				else: słowo2 = sprawdź_dalej_g(x,y, litera)
			if len(słowo2) > 1:
				lista_słów.append(słowo2)
				print(lista_słów)
			
	#na końcu sprawdzamy czy słowo łączy się z jakimś słowem na planszy i dla kazdego z utworzonych słów sprawdzamy czy jest ono w liście ze słownika
	print(lista_słów)
	for słowo in lista_słów:
		if słowo.isalpha():
			if len(potrzebne_litery) == len(słowo) and (not all(plansza[klucz][0] == ' ' for klucz in plansza)):
				komunikat = sp.czcionka_b_mała.render('Twoje słowo musi łączyć się z innymi', True, (102, 70, 62))
				komunikat2 = sp.czcionka_b_mała.render('słowami na planszy.', True, (102, 70, 62))
				screen.blit(komunikat, (880, 338))
				screen.blit(komunikat2, (880, 365))
				sp.rysuj_planszę()
				return False

			if not słowo.lower() in lista_ze_słownika: 
				print(słowo.lower())
				komunikat = sp.czcionka_b_mała.render('Tego słowa nie ma w słowniku.', True, (102, 70, 62))
				screen.blit(komunikat, (880, 338))
				sp.rysuj_planszę()
				return False

	#sprawdzamy, czy gracz ma w swoim zbiorze potrzebne płytki
	if not można_utworzyć(potrzebne_litery, gracze[aktualny_gracz][1]):
		komunikat = sp.czcionka_b_mała.render('Nie masz liter potrzebnych do utworzenia', True, (102, 70, 62))
		komunikat2 = sp.czcionka_b_mała.render('tego słowa.', True, (102, 70, 62))
		screen.blit(komunikat, (880, 338))
		screen.blit(komunikat2, (880, 365))
		sp.rysuj_planszę()
		return False

	#upewniamy się, że pierwsze słowo postawione na planszy przechodzi przez punkt 0,0
	if all(kopia_planszy[klucz][0] == ' ' for klucz in kopia_planszy) and (not sprawdź_pierwszą_współrzędną(dostawka)):
		komunikat = sp.czcionka_b_mała.render('Pierwsze słowo na planszy musi', True, (102, 70, 62))
		komunikat2 = sp.czcionka_b_mała.render('przechodzić przez jej środek.', True, (102, 70, 62))
		screen.blit(komunikat, (880, 338))
		screen.blit(komunikat2, (880, 365))
		sp.rysuj_planszę()
		return False
	
	return lista_słów, potrzebne_litery

def wynik(słowo):
	count = 0
	if sprawdź_słowo(słowo):
		for litera in słowo:
			for i in range(len(letterfreq)):
				if letterfreq[i][0] == litera.upper():
					count += letterfreq[i][1]
					continue
		return count
	return -1

def punkty(plansza, dostawka) -> int: 
#zwraca ile punktów zdobywają litery wstawione na planszę zgodnie z dostawką
#jeśli dostawka jest nieprawidłowa zwraca −1 lub rzuca wyjątkiem. Plansza nie zmienia się.
	count = 0
	lista_słów, potrzebne_litery = sprawdź_czy_poprawne(dostawka)
	if not lista_słów or not potrzebne_litery: return False
	for słowo in lista_słów:
		if słowo.isalpha():
			for litera in słowo:
				for i in range(len(letterfreq)):
					if letterfreq[i][0] == litera:
						count += letterfreq[i][1]
			return count
	raise Exception('Niepoprawna dostawka.')

def wstaw(dostawka) -> bool:
	#wstawia dostawkę na planszę. Zwraca True gdy udało się, False gdy dostawka nie jest prawidłowa.
	global plansza

	#jeśli dostawka była prawidłowa, funkcja sprawdź_czy_poprawne zwraca listę liter do usunięcia ze zbioru gracza
	dostawka_spr = sprawdź_czy_poprawne(dostawka)
	if not dostawka_spr: return False
	lista_słów, potrzebne_litery = dostawka_spr

	gracze[aktualny_gracz][2] += punkty(plansza, dostawka)
	for lit in potrzebne_litery:
		usuń_ze_zbioru(gracze[aktualny_gracz][1], lit)
	uzupełnij_zbiór(gracze[aktualny_gracz][1])

	#dodajemy dostawkę na planszę
	for krotka in dostawka:
		litera = krotka[0]
		współrzędne = krotka[1]

		for (x,y) in plansza:
			if (x,y) == współrzędne:
					plansza[(x,y)][0] = litera
					continue
	return True


# Gracze 

gracze = {}
#słownik w postaci: nr gracza: [imię, zbiór liter, wynik]
for i in range(len(args.nazwy_graczy_realnych)):
	gracze[i] = []
	gracze[i].append(args.nazwy_graczy_realnych[i])
	gracze[i].append(początkowy_zbiór_gracza())#[('K', 2), ('T', 2), ('R', 1), ('O', 1), ('Z', 1), ('O', 1), ('M', 2)])
	gracze[i].append(0)

x = 1
for j in range(len(args.nazwy_graczy_realnych), args.liczba_graczy_sztucznych + len(args.nazwy_graczy_realnych)):
	gracze[j] = []
	gracze[j].append('Gracz sztuczny nr ' + str(x))
	gracze[j].append(początkowy_zbiór_gracza())
	gracze[j].append(0)
	x += 1


# Gracze sztuczni

def da_się_utworzyć(słowo, zbiór_gracza):
	płytki = copy.deepcopy(litery_gracza(zbiór_gracza))
	for litera in słowo:
		#jeśli mamy literę w zbiorze płytek, usuwa ją i kontynuuje   
		if not litera.upper() in płytki:
			return False
		else:
			płytki.remove(litera.upper())
	return True

def można_utworzyć(potrzebne_litery, zbiór_gracza):
	#sprawdza, czy z gracz ma w swoim zbiorze litery potrzebne do utworzenia słowa
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

def utwórz_słowa_pocz(zbiór_gracza, x, y):
	#zwraca listę słów, które da się utworzyć ze zbioru gracza, zaczynających się na podaną literę w kolejności od najwyżej punktowanych
	global lista_ze_słownika, plansza
	litera_z_planszy = plansza[(x,y)][0].lower()

	płytki = [litera.lower() for litera in litery_gracza(zbiór_gracza)]
	płytki.append(litera_z_planszy)

	słowa = []
	for słowo in lista_ze_słownika:
		if słowo[0] == litera_z_planszy:
			if da_się_utworzyć(słowo[1:], zbiór_gracza):
				słowa.append((słowo, wynik(słowo)))

	słowa = sorted(słowa, key = lambda x: x[1], reverse = True)
	return [[x, y, litera_z_planszy, wyraz, 'p'] for wyraz in słowa]

def utwórz_słowa_kon(zbiór_gracza, x, y):
	#zwraca listę słów, które da się utworzyć ze zbioru gracza, zaczynających się na podaną literę w kolejności od najwyżej punktowanych
	global lista_ze_słownika, plansza
	litera_z_planszy = plansza[(x,y)][0].lower()

	płytki = [litera.lower() for litera in litery_gracza(zbiór_gracza)]
	płytki.append(litera_z_planszy)

	słowa = []
	for słowo in lista_ze_słownika:
		if słowo[-1] == litera_z_planszy:
			if da_się_utworzyć(słowo[:-1], zbiór_gracza):
				słowa.append((słowo, wynik(słowo)))

	słowa = sorted(słowa, key = lambda x: x[1], reverse = True)
	return [[x, y, litera_z_planszy, wyraz, 'k'] for wyraz in słowa]

def próby_dostawek(aktualny_gracz):
	global plansza
	lista_mozliwych = []
	for x,y in plansza:
		if plansza[(x,y)][0] != ' ':
			lista_prób1 = utwórz_słowa_pocz(gracze[aktualny_gracz][1], x, y)
			lista_prób2 = utwórz_słowa_kon(gracze[aktualny_gracz][1], x, y)
			if lista_prób1:
				for próba in lista_prób1:
					lista_mozliwych.append(próba)
			if lista_prób2:
				for próba in lista_prób2:
					lista_mozliwych.append(próba)
	return sorted(lista_mozliwych, key = lambda x: x[3][1], reverse = True)

def stwórz_dostawkę_pocz(słowo: str, x, y, kierunek: str):
	#zwraca listę krotek w postaci (litera, współrzędne) w zależności od kierunku wpisywanego słowa
	global plansza
	słowo = słowo.upper()
	współrzędne = []

	if kierunek.lower() == 'p':
		for i in range(len(słowo)):
			if (x+i, y) in plansza:
				współrzędne.append((x+i, y))
			else:
				return False
	
	elif kierunek.lower() == 'g':
		for i in range(len(słowo)):
			if (x, y+i) in plansza:
				współrzędne.append((x, y+i))
			else:
				return False
	
	elif kierunek.lower() == 'd':
		for i in range(len(słowo)):
			if (x+i, y-i) in plansza:
				współrzędne.append((x+i, y-i))
			else:
				return False

	else: 
		return False
	return list(zip(słowo, współrzędne))

def stwórz_dostawkę_kon(słowo: str, x, y, kierunek: str):
	#zwraca listę krotek w postaci (litera, współrzędne) w zależności od kierunku wpisywanego słowa
	global plansza
	słowo = słowo.upper()
	współrzędne = []

	if kierunek.lower() == 'p':
		for i in range(len(słowo)):
			if (x-i, y) in plansza:
				współrzędne.append((x-i, y))
			else:
				return False
	
	elif kierunek.lower() == 'g':
		for i in range(len(słowo)):
			if (x, y-i) in plansza:
				współrzędne.append((x, y-i))
			else:
				return False
	
	elif kierunek.lower() == 'd':
		for i in range(len(słowo)):
			if (x-i, y+i) in plansza:
				współrzędne.append((x-i, y+i))
			else:
				return False

	else: 
		return False

	współrzędne = współrzędne[::-1]
	return list(zip(słowo, współrzędne))

def ruch_gracza_sztucznego(aktualny_gracz):
	kierunki = ['p', 'g', 'd']
	próby = próby_dostawek(aktualny_gracz)
	if not próby: 
		print('ups')
		#wymiana
		return False

	print(próby)
	for próba in próby:
		#w tym miejscu coś idzie nie tak
		x = próba[0]
		y = próba[1]
		słowo = próba[3][0]
		
		if próba[4] == 'p':
			i = 0
			while i < len(kierunki):
				dostawka = stwórz_dostawkę_pocz(słowo, x, y, kierunki[i])
				if dostawka:
					dostawka = dostawka[1:] #pierwsza litera jest juz na planszy
				if wstaw(dostawka):
					return True
				else:
					i += 1
		elif próba[4] == 'k':
			i = 0
			while i < len(kierunki):
				dostawka = stwórz_dostawkę_kon(słowo, x, y, kierunki[i])
				if dostawka:
					dostawka = dostawka[:-1] #ostatnia litera jest juz na planszy
				if wstaw(dostawka):
					return True
				else:
					i += 1

	print('o matko')
	return False				

"""
def znajdź_dostawki_prawo(x, y, count = 1):
	global kopia_planszy

	if (x+1, y) in kopia_planszy:
		if kopia_planszy[(x+1, y)][0] != ' ':
			return x, y, count
	
	#słowo += kopia_planszy[(x+1, y)][0]
	return sprawdź_dalej_p(x+1, y, count+1)
	

	if count < 8:	
		if (x+1, y) not in kopia_planszy or kopia_planszy[x+1,y][0] != ' ':
			return [(x - (count - 1), y), plansza[x - (count - 1), y][0], count - 1, 'p']
	
	return znajdź_dostawki_prawo(x+1, y, kopia_planszy, count+1)

	#return [(x - (count - 1), y), plansza[x - (count - 1), y][0], 7, 'p']


def znajdź_dostawki_góra(x,y, kopia_planszy, count = 1):
	assert type(x) == type(y) == int

	if count < 8:
		if (x, y+1) not in kopia_planszy or kopia_planszy[x,y+1][0] != ' ':
			return (x, y - (count - 1)), plansza[x, y - (count - 1)][0], count - 1, 'g'
		
		print(x, y, count)
	return znajdź_dostawki_góra(x, y+1, kopia_planszy, count+1)
	
	#return [(x, y - (count - 1)), plansza[x, y - (count - 1)][0], 7, 'g'] #trzeba będzie poprawić

def znajdź_dostawki_dół(x, y, kopia_planszy, count = 1) -> list:
	assert type(x) == type(y) == int

	if count < 8:
		if (x-1, y-1) not in kopia_planszy or kopia_planszy[x-1,y-1][0] != ' ':
			return [(x + (count - 1), y + (count - 1)), plansza[x + (count - 1), y  + (count - 1)][0], count - 1, 'd']
	
	return znajdź_dostawki_dół(x-1, y-1, kopia_planszy, count+1)

	#return [(x + (count - 1), y + (count - 1)), plansza[x + (count - 1), y  + (count - 1)][0], 7, 'd']


def znajdź_dostawkę(aktualny_gracz):
	global plansza, gracze

	opcje = []
	for x,y in plansza: 
		if plansza[(x,y)][0] != ' ':
			opcje.append(znajdź_dostawki_prawo(x,y, copy.deepcopy(plansza)))
			opcje.append(znajdź_dostawki_góra(x,y, copy.deepcopy(plansza)))
			opcje.append(znajdź_dostawki_dół(x,y, copy.deepcopy(plansza)))
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
"""

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
			worczek_lit = sp.czcionka_b_mała.render(str(len(woreczek)), True, (102, 70, 62))
			screen.blit(worczek_lit, (1273, 650))
			punktacja = sp.czcionka_idealna.render(str(gracze[aktualny_gracz][2]), True, (102, 70, 62))
			screen.blit(punktacja, (1185, 600))
			sp.rysuj_planszę()
	
			#ruch gracza realnego
			if aktualny_gracz <= len(args.nazwy_graczy_realnych) - 1: #zmienimy, zeby mogl byc najpierw komputer

				global kopia_planszy
				kopia_planszy = copy.deepcopy(plansza)

				wyświetl_litery(aktualny_gracz)
				while True:
					sp.rysuj_planszę()
					dostawka = sp.ruch_gracza_realnego(aktualny_gracz)
					if dostawka:
						if wstaw(dostawka):
							wszystkie_dostawki.append(dostawka)
							sp.inicjalizacja_gry()
							sp.rysuj_planszę()
							screen.blit(numer, (988, 110))
							screen.blit(imię, (1060, 150))
							wyświetl_litery(aktualny_gracz)
							napis1 = sp.czcionka_b_mała.render('Twoje słowo zostało ustawione.', True, (102, 70, 62))
							screen.blit(napis1, (880, 338))
							napis2 = czcionka_mała.render('Twój aktualny zbiór liter:', True, (116, 82, 74))
							screen.blit(napis2, (880, 210))
							worczek_lit = sp.czcionka_b_mała.render(str(len(woreczek)), True, (102, 70, 62))
							screen.blit(worczek_lit, (1273, 650))
							punktacja = sp.czcionka_idealna.render(str(gracze[aktualny_gracz][2]), True, (102, 70, 62))
							screen.blit(punktacja, (1185, 600))
							koniec_tury(aktualny_gracz)
							break
							
						else: 
							continue
					else:
						wymiana(aktualny_gracz)
						screen.blit(numer, (988, 110))
						screen.blit(imię, (1060, 150))
						wyświetl_litery(aktualny_gracz)
						koniec_tury(aktualny_gracz)
						break
				
			else:
				kopia_planszy = copy.deepcopy(plansza)
				ruch_gracza_sztucznego(aktualny_gracz)
				"""
				dostawka = znajdź_dostawkę(aktualny_gracz)
				if dostawka:
					wstaw(dostawka)
				else:
					print(dostawka)
				"""

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

numer_rundy = 1
aktualny_gracz = 0
wszystkie_dostawki = []
if __name__ == '__main__':
	rozgrywka(gracze, konfiguracja)


