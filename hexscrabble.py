import argparse, pygame, copy, math
from random import shuffle
from sys import exit

#parsowanie argumentów z wiersza poleceń
parser = argparse.ArgumentParser()

parser.add_argument('-s', '--liczba_graczy_sztucznych', type = int, nargs = '?', help = 'Liczba graczy sztucznych')
parser.add_argument('-S', '--plik_słownika', type = str, nargs = '?', help = 'Plik słownika słów')
parser.add_argument('-c', '--plik_konfiguracyjny', type = str, nargs = '?', help = 'Plik konfiguracyjny')
parser.add_argument('nazwy_graczy_realnych', type = str, nargs = '*', help = 'Nazwy graczy realnych oddzielone spacją')

#ustalamy domyślne plik ze słownikiem i plik konfiguracyjny
parser.set_defaults(plik_słownika = 'slownik.txt', plik_konfiguracyjny = 'hexscrabble.cnf')
args = parser.parse_args()

#tworzymy listę mozliwych do utworzenia słów na podstawie podanego pliku słownika
lista_ze_słownika = [słowo for słowo in open(args.plik_słownika).read().split() if len(słowo) > 1]

#inicjalizacja biblioteki pygame, czcionek i outline'u planszy
pygame.init()
screen = pygame.display.set_mode((1500, 800), pygame.RESIZABLE)
pygame.display.set_caption('Hex Scrabble')
zegar = pygame.time.Clock()

czcionka = pygame.font.Font('czcionki/Bitter-Regular.otf', 32)
czcionka_b_mała = pygame.font.Font('czcionki/Bitter-Regular.otf', 22)
czcionka_mała = pygame.font.Font('czcionki/Bitter-Regular.otf', 30)
czcionka_idealna = pygame.font.Font('czcionki/Bitter-Bold.otf', 25)
czcionka_najmn = pygame.font.Font('czcionki/Bitter-Regular.otf', 20)
czcionka_średnia = pygame.font.Font('czcionki/Bitter-Bold.otf', 30)
czcionka_duża = pygame.font.Font('czcionki/Bitter-Bold.otf', 38)

tło = pygame.image.load('grafiki/wallpaper.jpeg')
tło = pygame.transform.rotozoom(tło, 0, 1.2)

nazwa = czcionka_duża.render('Hex Scrabble', True, (116, 82, 74))
runda = czcionka_średnia.render('Runda ', True, (102, 70, 62))
wyświetl_gracza = czcionka_mała.render('Tura gracza ', True, (102, 70, 62))
litery = czcionka_mała.render('Twoje litery:', True, (116, 82, 74))
wynik_gracza = czcionka_idealna.render('Twój aktualny wynik to ', True, (102, 70, 62))
litery_woreczek = czcionka_b_mała.render('Liczba liter pozostałych w woreczku:', True, (102, 70, 62))

#przyciski
przycisk = pygame.image.load('grafiki/button.png')
przycisk.set_colorkey((255, 255, 255))
przycisk.convert_alpha()

przycisk2 = pygame.image.load('grafiki/button2.png')
przycisk2.set_colorkey((255, 255, 255))
przycisk2.convert_alpha()

#przycisk wymiany liter
przycisk_w_rect = przycisk.get_rect(center = (960, 500))
przycisk_w2_rect = przycisk.get_rect(center = (960, 500))
czy_wymiana = czcionka_najmn.render('WYMIANA', True, (241, 205, 191))
czy_wymiana_rect = czy_wymiana.get_rect(center = przycisk_w_rect.center)

#przycisk końca tury
przycisk_k_rect = przycisk.get_rect(center = (1160, 500))
przycisk_k2_rect = przycisk2.get_rect(center = (1160, 500))
koniec = czcionka_najmn.render('KONIEC TURY', True, (241, 205, 191))
koniec_rect = koniec.get_rect(center = przycisk_k_rect.center)

heksagon = pygame.image.load('grafiki/hexagon1.png')
heksagon.set_colorkey((255, 255, 255))
heksagon.convert_alpha() #ogólnie zawsze convert przy uploadowaniu obrazu
heksagon_1_rect = heksagon.get_rect(topleft = (0,0))
	
heksagon_2 = pygame.image.load('grafiki/hexagon2.png') 
heksagon_2.set_colorkey((255, 255, 255))
heksagon_2.convert_alpha()
heksagon_2_rect = heksagon_2.get_rect(topleft = (0,0))

heksagon_3 = pygame.image.load('grafiki/hexagon3.png') 
heksagon_3.set_colorkey((255, 255, 255))
heksagon_3.convert_alpha()
heksagon_3_rect = heksagon_3.get_rect(topleft = (0,0))

def inicjalizacja_gry():
	global screen, czcionka, czcionka_b_mała, czcionka_duża, czcionka_mała, czcionka_średnia, tło
	global nazwa, runda, wyświetl_gracza, litery, przycisk, przycisk_w_rect, przycisk2, przycisk_w2_rect
	global czy_wymiana, czy_wymiana_rect, heksagon, heksagon_1_rect, heksagon_2, heksagon_2_rect
	global heksagon_3, heksagon_3_rect, litery_woreczek, wynik_gracza

	screen.blit(tło, (0,0))
	screen.blit(nazwa, (1030, 40))
	screen.blit(runda, (880, 110))
	screen.blit(wyświetl_gracza, (880, 150))
	screen.blit(przycisk, przycisk_w_rect)
	screen.blit(czy_wymiana, czy_wymiana_rect)
	screen.blit(przycisk, przycisk_k_rect)
	screen.blit(koniec, koniec_rect)
	screen.blit(wynik_gracza, (880, 600))
	screen.blit(litery_woreczek, (880, 650))


def stwórz_planszę(r):
	#tworzy planszę w postaci słownika, w postaci współrzędne:litera
	#jej przedstawieniem graficznym będzie duży sześciokąt o promieniu r

	global plansza
	plansza = {}
	
	y = r
	start = -r
	end = 0

	while y >= -r:
		for x in range(start,end + 1,1):
			plansza[x,y] = ' '

		#tworzymy kolejny rząd o jeden dłuższy od poprzedniego, aż dojdziemy do połowy sześciokąta
		y -= 1
		if y >= 0:
			end += 1

		#po dojściu do połowy, rzędy zaczynają skracać się o 1
		if y < 0:
			start += 1
	
	return plansza

stwórz_planszę(8)

def rysuj_planszę():
	#rysuje planszę i zmienia strukturę słownika planszy na współrzędne pola:[litera, rect(pole)], 
	#przechowując dodatkowo informację o położeniu pola w pikselach

	global plansza

	pos_x = 260
	pos_x0 = pos_x
	pos_y = 75

	rząd = list(plansza.keys())[0][1]
	start = list(plansza.keys())[0][0]
	end = 0

	for x,y in plansza:
		heksagon_rect = heksagon.get_rect(center = (pos_x, pos_y))
		plansza[x,y] = list(plansza[x,y])
		if len(plansza[x,y]) < 2:
			#chcemy zeby słownik powiększył się tylko przy pierwszym wołaniu funkcji
			plansza[x,y].append(heksagon_rect)
		screen.blit(heksagon, heksagon_rect) 

		litera = (czcionka.render(plansza[x,y][0], True, (116, 82, 74)))
		litera_rect = litera.get_rect(center = (pos_x, pos_y))
		screen.blit(litera, litera_rect)
		

		if y == rząd and not x == end:
			pos_x += heksagon.get_width() + 2

		else:
			rząd -= 1
			pos_y += heksagon.get_height()/2 + heksagon.get_width()/(2 * math.sqrt(3)) + 2

			if rząd >= 0:
				pos_x = pos_x0 - heksagon.get_width()/2 - 1
				pos_x0 = pos_x0 - heksagon.get_width()/2 - 1
				end += 1
				
			else:
				pos_x = pos_x0 + heksagon.get_width()/2 + 1
				pos_x0 = pos_x0 + heksagon.get_width()/2 + 1
	return plansza
			
rysuj_planszę()

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
	return woreczek

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

def wyświetl_litery(aktualny_gracz):
	#tworzy listkę płytek z ich współrzędnymi w pikselach i wyświetla litery gracza
	lista_płytek = []
	x = 882
	y = 253
	for i in range(len(gracze[aktualny_gracz][1])):
		płytka = gracze[aktualny_gracz][1][i][0] +'(' + str(gracze[aktualny_gracz][1][i][1]) + ')'
		if i != len(gracze[aktualny_gracz][1]) - 1:
			płytka_graf = czcionka_mała.render((płytka + ', '), True, (102, 70, 62))
		else: płytka_graf = czcionka_mała.render(płytka, True, (102, 70, 62))
		płytka_rect = płytka_graf.get_rect(topleft = (x,y))
		lista_płytek.append((płytka, płytka_graf, płytka_rect))
		screen.blit(płytka_graf, płytka_rect)
		x += płytka_rect.width
	return lista_płytek

def wymiana(aktualny_gracz):
	lista_płytek = wyświetl_litery(aktualny_gracz)
	instrukcja1 = czcionka_b_mała.render('Kliknij myszką na litery, które chcesz wymienić,', True, (102, 70, 62))
	instrukcja2 = czcionka_b_mała.render('a następnie naciśnij ENTER', True, (102, 70, 62))
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
							ciemna_płytka = czcionka_mała.render((płytka + ', '), True, (69, 39, 30))
						else:
							ciemna_płytka = czcionka_mała.render(płytka, True, (69, 39, 30))
						ciemna_płytka_rect = płytka_rect
						screen.blit(ciemna_płytka, ciemna_płytka_rect)

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					for litera in litery_do_wymiany:
						usuń_ze_zbioru(gracze[aktualny_gracz][1], litera)
					uzupełnij_zbiór(gracze[aktualny_gracz][1])
					inicjalizacja_gry()
					rysuj_planszę()
					napis2 = czcionka_mała.render('Twój aktualny zbiór liter:', True, (116, 82, 74))
					screen.blit(napis2, (880, 210))
					komunikat = czcionka_b_mała.render('Litery zostały wymienione.', True, (102, 70, 62))
					screen.blit(komunikat, (880, 323))
					return True
		pygame.display.update()
		zegar.tick(60)
		
def koniec_tury(aktualny_gracz):
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				pozycja_myszki = pygame.mouse.get_pos()

				if przycisk_k_rect.collidepoint(pozycja_myszki):
					screen.blit(przycisk2, przycisk_k2_rect)
					screen.blit(koniec, koniec_rect)
					return True

		pygame.display.update()
		zegar.tick(60)


# Sprawdzanie dostawki

# Funkcje pomocnicze

def sprawdź_pierwszą_współrzędną(dostawka):
	#sprawdza, czy pierwsze słowo na planszy przechodzi przez punkt 0,0
	for lista in dostawka:
		if lista[1] == (0,0): return True
	return False

def sprawdź_słowo(słowo: str):
	#sprawdza, czy ułozone słowo jest w słowniku
	if słowo.lower() in lista_ze_słownika: return True
	return False

def da_się_utworzyć(słowo, zbiór_gracza):
	#sprawdza, czy z gracz ma w swoim zbiorze litery wymagane litery
	płytki = copy.deepcopy(litery_gracza(zbiór_gracza))
	for litera in słowo:
		#jeśli mamy literę w zbiorze płytek, usuwa ją i kontynuuje - w ten sposób sprawdzamy, czy ma odpowiednią liczbę powtarzających się liter  
		if not litera.upper() in płytki:
			return False
		else:
			płytki.remove(litera.upper())
	return True

# Funkcje rekurencyjne szukające we wszystkich kierunkach ułozonych juz wyrazów, az do momentu napotkania pustego pola

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
	return sprawdź_wstecz_d(x-1, y+1, słowo)

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
	return sprawdź_dalej_d(x+1, y-1, słowo)

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
		if ((x0-1, y0) in plansza and plansza[(x0-1, y0)][0] != ' ') or ((x0+1, y0) in plansza and plansza[(x0+1, y0)][0] != ' '):
			kierunek = 'p'
		elif ((x0, y0-1) in plansza and plansza[(x0, y0-1)][0] != ' ') or ((x0, y0+1) in plansza and plansza[(x0, y0+1)][0] != ' '):
			kierunek = 'g'
		elif ((x0-1, y0+1) in plansza and plansza[(x0-1,y0+1)][0] != ' ') or ((x0+1, y0-1) in plansza and plansza[(x0+1, y0-1)][0] != ' '):
			kierunek = 'd'
		else:
			if not 'Gracz sztuczny nr' in gracze[aktualny_gracz][0]:
				komunikat = czcionka_b_mała.render('Twoje słowo musi łączyć się z innymi', True, (102, 70, 62))
				komunikat2 = czcionka_b_mała.render('słowami na planszy.', True, (102, 70, 62))
				screen.blit(komunikat, (880, 338))
				screen.blit(komunikat2, (880, 365))
				rysuj_planszę()
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
			if not 'Gracz sztuczny nr' in gracze[aktualny_gracz][0]:
				komunikat = czcionka_b_mała.render('Twoje litery muszą leżeć w jednej linii.', True, (102, 70, 62))
				screen.blit(komunikat, (880, 338))
				rysuj_planszę()
			return False

	#mając zidentyfikowany kierunek, sprawdzamy czy gracz przedłuzał słowo z planszy, cofając się po odpowiednich współrzędnych
	
	if kierunek == 'p':
		słowo = sprawdź_wstecz_p(x0, y0, '')

	elif kierunek == 'g':
		słowo = sprawdź_wstecz_g(x0, y0, '')

	elif kierunek == 'd':
		słowo = sprawdź_wstecz_d(x0, y0, '')

	else:
		return False

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
					if not 'Gracz sztuczny nr' in gracze[aktualny_gracz][0]:
						komunikat = czcionka_b_mała.render('W Twoim słowie nie może być przerw.', True, (102, 70, 62))
						screen.blit(komunikat, (880, 338))
						rysuj_planszę()
					return False
			else:
				słowo += kopia_planszy[(x, y)][0]
				x += 1

	#analogicznie z dwoma pozostałymi kierunkami
	elif kierunek == 'g':
		while y <= dostawka[-1][1][1]:
			if kopia_planszy[(x, y)][0] == ' ':
				for i in range(len(dostawka)):
					if (x, y) == dostawka[i][1]:
						słowo += dostawka[i][0]
						potrzebne_litery.append(dostawka[i][0])
						y += 1
						break
				else:
					if not 'Gracz sztuczny nr' in gracze[aktualny_gracz][0]:
						komunikat = czcionka_b_mała.render('W Twoim słowie nie może być przerw.', True, (102, 70, 62))
						screen.blit(komunikat, (880, 338))
						rysuj_planszę()
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
					if not 'Gracz sztuczny nr' in gracze[aktualny_gracz][0]:
						komunikat = czcionka_b_mała.render('W Twoim słowie nie może być przerw.', True, (102, 70, 62))
						screen.blit(komunikat, (880, 338))
						rysuj_planszę()
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
					słowo1 = sprawdź_dalej_g(x,y, słowo1)
				else: słowo1 = sprawdź_dalej_g(x,y, litera)
			if len(słowo1) > 1:
				lista_słów.append(słowo1)

			słowo2 = ''
			if (x+1, y-1) in kopia_planszy and kopia_planszy[(x+1, y-1)] != ' ':
				słowo2 = sprawdź_wstecz_d(x,y, litera)
			if (x-1, y+1) in kopia_planszy and kopia_planszy[(x-1, y+1)] != ' ':
				if len(słowo2) > 1:
					słowo2 = sprawdź_dalej_d(x,y, słowo2)
				else: słowo2 = sprawdź_dalej_d(x,y, litera)
			if len(słowo2) > 1:
				lista_słów.append(słowo2)

		elif kierunek == 'g':
			#analogicznie w przypadku pozostałych kierunków
			słowo1 = ''
			if (x-1, y) in kopia_planszy and kopia_planszy[(x-1, y)] != ' ':
				słowo1 = sprawdź_wstecz_p(x,y, litera)
			if (x+1, y) in kopia_planszy and kopia_planszy[(x+1, y)] != ' ':
				if len(słowo1) > 1:
					słowo1 = sprawdź_dalej_p(x,y, słowo1)
				else: słowo1 = sprawdź_dalej_p(x,y, litera)
			if len(słowo1) > 1:
				lista_słów.append(słowo1)

			słowo2 = ''
			if (x+1, y-1) in kopia_planszy and kopia_planszy[(x+1, y-1)] != ' ':
				słowo2 = sprawdź_wstecz_d(x,y,litera)
			if (x-1, y+1) in kopia_planszy and kopia_planszy[(x-1, y+1)] != ' ':
				if len(słowo2) > 1:
					słowo2 = sprawdź_dalej_d(x,y, słowo2)
				else: słowo2 = sprawdź_dalej_d(x,y, litera)
			if len(słowo2) > 1:
				lista_słów.append(słowo2)

		
		elif kierunek == 'd':
			słowo1 = ''
			if (x-1, y) in kopia_planszy and kopia_planszy[(x-1, y)] != ' ':
				słowo1 = sprawdź_wstecz_p(x,y,litera)
			if (x+1, y) in kopia_planszy and kopia_planszy[(x+1, y)] != ' ':
				if len(słowo1) > 1:
					słowo1 = sprawdź_dalej_p(x,y, słowo1)
				else: słowo1 = sprawdź_dalej_p(x,y, litera)
			if len(słowo1) > 1:
				lista_słów.append(słowo1)

			słowo2 = ''
			if (x, y-1) in kopia_planszy and kopia_planszy[(x, y-1)] != ' ':
				słowo2 = sprawdź_wstecz_g(x,y,litera)
			if (x, y+1) in kopia_planszy and kopia_planszy[(x, y+1)] != ' ':
				if len(słowo2) > 1:
					słowo2 = sprawdź_dalej_g(x,y, słowo2)
				else: słowo2 = sprawdź_dalej_g(x,y, litera)
			if len(słowo2) > 1:
				lista_słów.append(słowo2)
			
	#na końcu sprawdzamy czy słowo łączy się z jakimś słowem na planszy i dla kazdego z utworzonych słów sprawdzamy czy jest ono w liście ze słownika
	for słowo in lista_słów:
		if słowo.isalpha():
			if len(potrzebne_litery) == len(słowo) and (not all(plansza[klucz][0] == ' ' for klucz in plansza)):
				if not 'Gracz sztuczny nr' in gracze[aktualny_gracz][0]:
					komunikat = czcionka_b_mała.render('Twoje słowo musi łączyć się z innymi', True, (102, 70, 62))
					komunikat2 = czcionka_b_mała.render('słowami na planszy.', True, (102, 70, 62))
					screen.blit(komunikat, (880, 338))
					screen.blit(komunikat2, (880, 365))
					rysuj_planszę()
				return False

			if not słowo.lower() in lista_ze_słownika: 
				if not 'Gracz sztuczny nr' in gracze[aktualny_gracz][0]:
					komunikat = czcionka_b_mała.render('Tego słowa nie ma w słowniku.', True, (102, 70, 62))
					screen.blit(komunikat, (880, 338))
					rysuj_planszę()
				return False

	#sprawdzamy, czy gracz ma w swoim zbiorze potrzebne płytki
	litery_str = ''.join(potrzebne_litery).lower()
	if not da_się_utworzyć(potrzebne_litery, gracze[aktualny_gracz][1]):
		if not 'Gracz sztuczny nr' in gracze[aktualny_gracz][0]:
			komunikat = czcionka_b_mała.render('Nie masz liter potrzebnych do utworzenia', True, (102, 70, 62))
			komunikat2 = czcionka_b_mała.render('tego słowa.', True, (102, 70, 62))
			screen.blit(komunikat, (880, 338))
			screen.blit(komunikat2, (880, 365))
			rysuj_planszę()
		return False

	#upewniamy się, że pierwsze słowo postawione na planszy przechodzi przez punkt 0,0
	if all(kopia_planszy[klucz][0] == ' ' for klucz in kopia_planszy) and (not sprawdź_pierwszą_współrzędną(dostawka)):
		if not 'Gracz sztuczny nr' in gracze[aktualny_gracz][0]:
			komunikat = czcionka_b_mała.render('Pierwsze słowo na planszy musi', True, (102, 70, 62))
			komunikat2 = czcionka_b_mała.render('przechodzić przez jej środek.', True, (102, 70, 62))
			screen.blit(komunikat, (880, 338))
			screen.blit(komunikat2, (880, 365))
			rysuj_planszę()
		return False
	
	return lista_słów, potrzebne_litery

def wynik(słowo):
	#punkty za pojedyncze słowo, zgodnie z plikiem konfiguracyjnym
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

	#jeśli dostawka była prawidłowa, funkcja sprawdź_czy_poprawne zwraca listę ułozonych przez gracza słów i listę liter do usunięcia ze zbioru gracza
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

def stwórz_graczy(woreczek):
	global gracze

	gracze = {}
	#słownik w postaci: nr gracza: [imię, zbiór liter, wynik]
	if args.nazwy_graczy_realnych:
		for i in range(len(args.nazwy_graczy_realnych)):
			gracze[i] = []
			gracze[i].append(args.nazwy_graczy_realnych[i])
			gracze[i].append(początkowy_zbiór_gracza())
			gracze[i].append(0)

	if args.liczba_graczy_sztucznych:
		x = 1
		if args.nazwy_graczy_realnych:
			limit1 = len(args.nazwy_graczy_realnych)
			limit2 = args.liczba_graczy_sztucznych + len(args.nazwy_graczy_realnych)
		else: 
			limit1 = 0
			limit2 = args.liczba_graczy_sztucznych
		for i in range(limit1, limit2):
			gracze[i] = []
			gracze[i].append('Gracz sztuczny nr ' + str(x))
			gracze[i].append(początkowy_zbiór_gracza())
			gracze[i].append(0)
			x += 1
	if len(gracze) < 2:
		#graczy musi być co najmniej dwóch
		raise Exception('Niepoprawna liczba graczy.')

	shuffle(gracze)
	return gracze
	
# Ruch graczy realnych	

aktualny_heksagon = None
pole = None
dopisuje_dostawkę = False
dostawka = []
lit = None

def wstaw_literę(lit):
	#wstawia literę na planszę i przechowuje informacje o tworzonej przez gracza dostawce
	global aktualny_heksagon, pole, dopisuje_dostawkę, dostawka

	litera = (czcionka.render(lit, True, (116, 82, 74)))
	litera_rect = litera.get_rect(center = aktualny_heksagon.center)
	screen.blit(litera, litera_rect)
	dostawka.append((lit, pole))


def pobierz_literkę(adres_literki: int):
	#zwraca literę odpowiadającą odpowiedniemu przyciskowi na klawiaturze
	match adres_literki:
		case pygame.K_a:
			return 'A'
		case pygame.K_b:
			return 'B'
		case pygame.K_c:
			return 'C'
		case pygame.K_d:
			return 'D'
		case pygame.K_e:
			return 'E'
		case pygame.K_f:
			return 'F'
		case pygame.K_g:
			return 'G'
		case pygame.K_h:
			return 'H'
		case pygame.K_i:
			return 'I'
		case pygame.K_j:
			return 'J'
		case pygame.K_k:
			return 'K'
		case pygame.K_l:
			return 'L'
		case pygame.K_m:
			return 'M'
		case pygame.K_n:
			return 'N'
		case pygame.K_o:
			return 'O'
		case pygame.K_p:
			return 'P'
		case pygame.K_q:
			return 'Q'
		case pygame.K_r:
			return 'R'
		case pygame.K_s:
			return 'S'
		case pygame.K_t:
			return 'T'
		case pygame.K_u:
			return 'U'
		case pygame.K_v:
			return 'V'
		case pygame.K_w:
			return 'W'
		case pygame.K_x:
			return 'X'
		case pygame.K_y:
			return 'Y'
		case pygame.K_z:
			return 'Z'
		case _:
			return None

def aktualizuj_liste_mozliwych_pol(listamozliwychpol):
	#uniemozliwia uzytkownikowi wpisanie litery dwa razy w tym samym polu
	global pole
	listamozliwychpol.remove(pole)

def ruch_gracza_realnego(aktualny_gracz):
	#zwraca dostawkę na podstawie liter wpisanych przez gracza lub None, jeśli gracz wymienia litery

	global aktualny_heksagon, pole, dopisuje_dostawkę, dostawka, lit
	listamozliwychpol = [(x,y) for (x,y) in plansza if plansza[(x,y)][0] == ' ']
	dostawka = []

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				pozycja_myszki = pygame.mouse.get_pos()

				#sprawdzamy czy uzytkownik chce wymienić litery
				if przycisk_w_rect.collidepoint(pozycja_myszki):
					screen.blit(przycisk2, przycisk_w2_rect)
					screen.blit(czy_wymiana, czy_wymiana_rect)
					#screen.blit(przycisk, przycisk_w_rect)
					#screen.blit(wymiana, wymiana_rect)
					return None

				for x, y in plansza:
					#identyfikujemy sześciokąt, na który kliknął użytkownik, żeby wpisać literę
					heksagon_rect = plansza[x,y][1]

					if heksagon_rect.collidepoint(pozycja_myszki):
						#kiedy użytkownik klika w następny sześciokąt, poprzedni przestaje się podświetlać
						if aktualny_heksagon:
							heksagon_3_rect.update(aktualny_heksagon)
							screen.blit(heksagon_3, heksagon_3_rect)
						
						#podświetlamy ostatni kliknięty przez użytkownika heksagon
						aktualny_heksagon = heksagon_rect
						pole = (x,y)
						heksagon_2_rect.update(aktualny_heksagon)
						#heksagon_2_rect = heksagon_2.get_rect(left = aktualny_heksagon.left, top = aktualny_heksagon.top)
						screen.blit(heksagon_2, heksagon_2_rect)

			#gracz nie musi za każdym razem naciskać na sześciokąt, może poruszać się po planszy strzałkami

			if event.type == pygame.KEYDOWN:
				if aktualny_heksagon:

					if not dopisuje_dostawkę:
						#kopia_planszy = copy.deepcopy(plansza)
						dopisuje_dostawke = True

					klawisze = pygame.key.get_pressed()
					#sprawdzamy, czy uzytkownik chce wprowadzić polski znak
					if klawisze[pygame.K_a] and klawisze[pygame.K_RALT]:
						lit = 'Ą'
					elif klawisze[pygame.K_c] and klawisze[pygame.K_RALT]:
						lit = 'Ć'
					elif klawisze[pygame.K_e] and klawisze[pygame.K_RALT]:
						lit = 'Ę'
					elif klawisze[pygame.K_l] and klawisze[pygame.K_RALT]:
						lit = 'Ł'
					elif klawisze[pygame.K_n] and klawisze[pygame.K_RALT]:
						lit = 'Ń'
					elif klawisze[pygame.K_o] and klawisze[pygame.K_RALT]:
						lit = 'Ó'
					elif klawisze[pygame.K_s] and klawisze[pygame.K_RALT]:
						lit = 'Ś'
					elif klawisze[pygame.K_x] and klawisze[pygame.K_RALT]:
						lit = 'Ź'
					elif klawisze[pygame.K_z] and klawisze[pygame.K_RALT]:
						lit = 'Ż'

					#jeśli nie, sprawdzamy pozostałe litery
					elif pobierz_literkę(event.key): #event.key == pobierz_literkę(event.key):
						lit = pobierz_literkę(event.key)

					if lit:
						if pole in listamozliwychpol:
							wstaw_literę(lit)
							aktualizuj_liste_mozliwych_pol(listamozliwychpol)
							lit = None

				#mozna dodac opcje backspace!!

				#gracz może poruszać się po planszy używając strzałek
				if event.key == pygame.K_UP:
					if aktualny_heksagon:
						heksagon_3_rect.update(aktualny_heksagon)
						screen.blit(heksagon_3, heksagon_3_rect)

						for x,y in plansza:
							if aktualny_heksagon in plansza[x,y]:
								if (x, y+1) in plansza:
									aktualny_heksagon = plansza[x,y+1][1]
									break
						pole = (x, y+1)
						heksagon_2_rect.update(aktualny_heksagon)
						screen.blit(heksagon_2, heksagon_2_rect)

				if event.key == pygame.K_DOWN:
					if aktualny_heksagon:
						heksagon_3_rect.update(aktualny_heksagon)
						screen.blit(heksagon_3, heksagon_3_rect)

						for x,y in plansza:
							if aktualny_heksagon in plansza[x,y]:
								if (x, y-1) in plansza:
									aktualny_heksagon = plansza[x,y-1][1]
									break
						
						pole = (x, y-1)
						heksagon_2_rect.update(aktualny_heksagon)
						screen.blit(heksagon_2, heksagon_2_rect)
						
				if event.key == pygame.K_RIGHT:
					if aktualny_heksagon:
						heksagon_3_rect.update(aktualny_heksagon)
						screen.blit(heksagon_3, heksagon_3_rect)

						for x,y in plansza:
							if aktualny_heksagon in plansza[x,y]:
								if (x+1, y) in plansza:
									aktualny_heksagon = plansza[x+1,y][1]
									break
						
						pole = (x+1, y)
						heksagon_2_rect.update(aktualny_heksagon)
						screen.blit(heksagon_2, heksagon_2_rect)
						
				if event.key == pygame.K_LEFT:
					if aktualny_heksagon:
						heksagon_3_rect.update(aktualny_heksagon)
						screen.blit(heksagon_3, heksagon_3_rect)

						for x,y in plansza:
							if aktualny_heksagon in plansza[x,y]:
								if (x-1, y) in plansza:
									aktualny_heksagon = plansza[x-1,y][1]
									break
						
						pole = (x-1, y)
						heksagon_2_rect.update(aktualny_heksagon)
						screen.blit(heksagon_2, heksagon_2_rect)

				#kiedy uzytkownik naciska enter po wpisaniu słowa, kończymy działanie funkcji i zwracamy utworzoną przez niego dostawkę
				if event.key == pygame.K_RETURN:
					dopisuje_dostawkę = False
					if dostawka:
						return dostawka

		pygame.display.update()
		zegar.tick(60)



# Funkcje pomocnicze dla graczy sztucznych

def można_utworzyć(potrzebne_litery, zbiór_gracza):
	#analogiczneie sprawdza, czy z gracz ma w swoim zbiorze litery wymagane litery
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
	#zwraca listę słów, które da się utworzyć ze zbioru gracza, kończących się na podaną literę w kolejności od najwyżej punktowanych
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
	#zwraca listę hipotetycznych dostawek w postaci [współrzędne, litera z planszy, (słowo, liczba punktów), koniec/początek], posortowaną od najwyzej punktowanych słów
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

def pierwszy_ruch(aktualny_gracz):
	#jeśli komputer zaczyna, układa słowo ze swoich liter i umieszcza je poziomo na planszy, począwszy od punku (-1,0)
	
	płytki = litery_gracza(gracze[aktualny_gracz][1])
	słowa = [(słowo, wynik(słowo)) for słowo in lista_ze_słownika if da_się_utworzyć(słowo, płytki)]
	
	if słowa:
		słowa = sorted(słowa, key = lambda x: x[1], reverse = True)
		dostawka = stwórz_dostawkę_pocz(słowa[0][0], -1, 0, 'p')
		if wstaw(dostawka): return True
	
	#jeśli nie da się utworzyć zadnego słowa, gracz wymienia litery
	for litera in litery_gracza(gracze[aktualny_gracz][1]):
		usuń_ze_zbioru(gracze[aktualny_gracz][1], litera)
	uzupełnij_zbiór(gracze[aktualny_gracz][1])

def ruch_gracza_sztucznego(aktualny_gracz):
	#gracz sztuczny wstawia dostawki stanowiące najwyzej punktowane słowa kończące się lub zaczynające na jakąś literę z planszy i składające się później jedynie z liter ze zbioru gracza
	global plansza
	
	if all(plansza[klucz][0] == ' ' for klucz in plansza):
		pierwszy_ruch(aktualny_gracz)
		return True

	kierunki = ['p', 'g', 'd']
	próby = próby_dostawek(aktualny_gracz)
	if not próby: 
		#jeśli nie da się utworzyć zadnej dostawki, wymieniamy wszystkie litery
		for litera in litery_gracza(gracze[aktualny_gracz][1]):
			usuń_ze_zbioru(gracze[aktualny_gracz][1], litera)
		uzupełnij_zbiór(gracze[aktualny_gracz][1])
		return False

	for próba in próby:
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

def rozgrywka(gracze: dict, konfiguracja: list):
	#dopracować co to konfiguracja
	global numer_rundy, aktualny_gracz, woreczek, plansza
	inicjalizacja_gry()

	#gra kończy się, kiedy w woreczku zabraknie liter
	while len(woreczek) != 0:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()

		#pokazuje, czyja jest tura, wyświetla aktualny stan planszy i zbiór liter gracza
		numer = czcionka_średnia.render(str(numer_rundy), True, (102, 70, 62))
		screen.blit(numer, (988, 110))
		imię = czcionka_mała.render(gracze[aktualny_gracz][0], True, (102, 70, 62))
		screen.blit(imię, (1060, 150))
		woreczek_lit = czcionka_b_mała.render(str(len(woreczek)), True, (102, 70, 62))
		screen.blit(woreczek_lit, (1273, 650))
		punktacja = czcionka_idealna.render(str(gracze[aktualny_gracz][2]), True, (102, 70, 62))
		screen.blit(punktacja, (1185, 600))
		screen.blit(litery, (880, 210))
		wyświetl_litery(aktualny_gracz)
		rysuj_planszę()
	
		#ruch gracza realnego
		if not 'Gracz sztuczny nr' in gracze[aktualny_gracz][0]:

			global kopia_planszy
			kopia_planszy = copy.deepcopy(plansza)
			#wyświetl_litery(aktualny_gracz)
			count = 0

			while count < 3:
				rysuj_planszę()
				dostawka = ruch_gracza_realnego(aktualny_gracz)
				if dostawka:
					if wstaw(dostawka):
						wszystkie_dostawki.append(dostawka)
						inicjalizacja_gry()
						rysuj_planszę()
						screen.blit(numer, (988, 110))
						screen.blit(imię, (1060, 150))
						wyświetl_litery(aktualny_gracz)
						napis1 = czcionka_b_mała.render('Twoje słowo zostało ustawione.', True, (102, 70, 62))
						screen.blit(napis1, (880, 338))
						napis2 = czcionka_mała.render('Twój aktualny zbiór liter:', True, (116, 82, 74))
						screen.blit(napis2, (880, 210))
						woreczek_lit = czcionka_b_mała.render(str(len(woreczek)), True, (102, 70, 62))
						screen.blit(woreczek_lit, (1273, 650))
						punktacja = czcionka_idealna.render(str(gracze[aktualny_gracz][2]), True, (102, 70, 62))
						screen.blit(punktacja, (1185, 600))
						koniec_tury(aktualny_gracz)
						break
							
					else: 
						count += 1
						inicjalizacja_gry()
						rysuj_planszę()
						screen.blit(numer, (988, 110))
						screen.blit(imię, (1060, 150))
						screen.blit(woreczek_lit, (1273, 650))
						screen.blit(punktacja, (1185, 600))
						screen.blit(litery, (880, 210))
						wyświetl_litery(aktualny_gracz)
						continue
				else:
					inicjalizacja_gry()
					rysuj_planszę()
					wymiana(aktualny_gracz)
					screen.blit(numer, (988, 110))
					screen.blit(imię, (1060, 150))
					wyświetl_litery(aktualny_gracz)
					koniec_tury(aktualny_gracz)
					break

			else:
				inicjalizacja_gry()
				rysuj_planszę()
				screen.blit(numer, (988, 110))
				screen.blit(imię, (1060, 150))
				screen.blit(litery, (880, 210))
				wyświetl_litery(aktualny_gracz)
				wiadomość1 = czcionka_b_mała.render('Podałeś niepoprawne słowo trzy razy.', True, (102, 70, 62))
				wiadomość2 = czcionka_b_mała.render('Twoja tura przepadła.', True, (102, 70, 62))
				screen.blit(wiadomość1, (880, 338))
				screen.blit(wiadomość2, (880, 365))
				screen.blit(woreczek_lit, (1273, 650))
				screen.blit(punktacja, (1185, 600))
				koniec_tury(aktualny_gracz)
				
		else:
			#ruch gracza sztucznego
			kopia_planszy = copy.deepcopy(plansza)
			inicjalizacja_gry()
			rysuj_planszę()
			ruch_gracza_sztucznego(aktualny_gracz)
			inicjalizacja_gry()
			rysuj_planszę()
			screen.blit(numer, (988, 110))
			screen.blit(imię, (1060, 150))
			screen.blit(litery, (880, 210))
			wyświetl_litery(aktualny_gracz)
			woreczek_lit = czcionka_b_mała.render(str(len(woreczek)), True, (102, 70, 62))
			screen.blit(woreczek_lit, (1273, 650))
			punktacja = czcionka_idealna.render(str(gracze[aktualny_gracz][2]), True, (102, 70, 62))
			screen.blit(punktacja, (1185, 600))
			

		#kolejny gracz
		if aktualny_gracz != len(gracze)-1:
			aktualny_gracz += 1
		else:
			aktualny_gracz = 0
			numer_rundy += 1

		#funkcja wołana rekurencyjnie
		pygame.display.update()
		zegar.tick(60)
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

	while True:
		screen.blit(tło, (0,0))
		screen.blit(nazwa, (1030, 40))
		rysuj_planszę()
		
		koniec = czcionka_średnia.render('Koniec gry. ', True, (102, 70, 62))
		screen.blit(koniec, (880, 145))
		wyświetl_zwycięzcę = czcionka_mała.render('Zwycięzcą jest ' + zwycięzca, True, (102, 70, 62))
		screen.blit(wyświetl_zwycięzcę, (880, 190))
		wynik_zwycięzcy = czcionka_mała.render('z wynikiem równym ' + str(najwyższy_wynik), True, (102, 70, 62))
		screen.blit(wynik_zwycięzcy, (880, 227))
		brawo = czcionka_średnia.render('Brawo!', True, (116, 82, 74))
		screen.blit(brawo, (880, 275))

		for event in pygame.event.get():
			 if event.type == pygame.QUIT:
					pygame.quit()
					exit()

		pygame.display.update()
		zegar.tick(60)
		

numer_rundy = 1
aktualny_gracz = 0
wszystkie_dostawki = []
woreczek = początkowy_woreczek()

if __name__ == '__main__':
	rozgrywka(stwórz_graczy(woreczek), konfiguracja)


