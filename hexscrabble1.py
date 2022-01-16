
from random import shuffle

#lista krotek określająca punktację i częstość występowania liter
letterfreq = [('A', 1, 9), ('E', 1, 7), ('I', 1, 8), ('N', 1, 5), ('O', 1, 6),
('R', 1, 4), ('S', 1, 4), ('W', 1, 4), ('Z', 1, 5), ('C', 2, 3), ('D', 2, 3),
('K', 2, 3), ('L', 2, 3), ('M', 2, 3), ('P', 2, 3), ('T', 2, 3), ('Y', 2, 4),
('B', 3, 2), ('G', 3, 2), ('H', 3, 2), ('J', 3, 2), ('Ł', 3, 2), ('U', 3, 2),
('Ą', 5, 1), ('Ę', 5, 1), ('F', 5, 1), ('Ó', 5, 1), ('Ś', 5, 1), ('Ż', 5, 1),
('Ć', 6, 1), ('Ń', 7, 1), ('Ź', 9, 1)]


plansza = {}
def stwórz_planszę(r):
	#tworzy planszę w postaci słownika, w postaci współrzędne:litera
	#jej przedstawieniem graficznym będzie duży sześciokąt o promieniu r
	global plansza
	
	y = r
	start = -r
	end = 0

	while y >= -r:
		for x in range(start, end + 1, 1):
			plansza[x,y] = ' '

		#tworzymy kolejny rząd o jeden dłuższy od poprzedniego, aż dojdziemy do połowy sześciokąta
		y -= 1
		if y >= 0:
			end += 1

		#po dojściu do połowy, rzędy zaczynają skracać się o 1
		if y < 0:
			start += 1

	#return plansza
stwórz_planszę(3)
print(plansza)


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

def pozostałe_litery(woreczek):
	#zwraca liczbę płytek pozostałych w woreczku
	return len(woreczek)


# Zbiór gracza
def dodaj_do_zbioru(zbiór_gracza):
	#bierze płytkę z woreczka i dodaje do zbioru liter gracza
	zbiór_gracza.append(woreczek.pop())

def początkowy_zbiór_gracza():
	#inicjuje zbiór liter gracza i daje do niego początkowe 7 liter
	zbiór = []
	for i in range(7):
		dodaj_do_zbioru(zbiór)
	return zbiór

def zbiór_gracza_str(zbiór_gracza: list) -> str: 
	#wyświetla zbiór liter gracza w formie litera(liczba_punktów)
	nowa_lista = []
	for litera, punkty in zbiór_gracza:
		płytka = f'{litera}({punkty})' 
		nowa_lista.append(płytka)
	return ', '.join(nowa_lista)

def usuń_ze_zbioru(zbiór_gracza, litera):
	#usuwa płytkę ze zbioru gracza, w momencie kiedy gracz ją zużywa lub wymienia
	zbiór_gracza.remove(litera)

def uzupełnij_zbiór(zbiór_gracza):
	#dodaje płytki do zbioru gracza, aby miał ich 7 (jeśli jest odpowiednia liczba płytek w woreczku)
	while len(zbiór_gracza) < 7 and pozostałe_litery(woreczek) > 0:
		dodaj_do_zbioru(zbiór_gracza)

# Gracze (realni)
gracze = {}
#słownik w postaci: nr gracza: [imię, zbiór liter, wynik]
for i in range(2):
	gracze[i] = []
	gracze[i].append('imię')
	gracze[i].append(początkowy_zbiór_gracza())
	gracze[i].append(0)
print(gracze)

def zwiększ_wynik(gracz, punkty: int):
	#zwiększa wynik gracza o konketną liczbę
	wynik += punkty


# Plansza
plansza = []
#tworzymy dwuwymiarową planszę w postaci listy wierszy
for y in range(3,-4,-1):
	wiersz = []
	for x in range(-3,4,1):
		wiersz.append((x,y))
	plansza.append(wiersz)
print('\n', plansza, '\n')

plansza = {}
#tworzymy początkową planszę w postaci słownika, gdzie kluczem są współrzędne, a wartością ' ' lub litera
for y in range(3,-4,-1):
	for x in range(-3,4,1):
		plansza[x,y] = ' '
print('\n', plansza, '\n')



"""

				   -3  -2  -1  0   1   2   3 
				/ \ / \ / \ / \ / \ / \ / \
             3 |-33|-23|-13| 03| 13| 23| 33|
			  / \ / \ / \ / \ / \ / \ / \ /
           2 |-32|-22|-12| 02| 12| 22| 32| 
		    / \ / \ / \ / \ / \ / \ / \ / 
         1 |-31|-21|-11| 01| 11| 21| 31|
		  / \ / \ / \ / \ / \ / \ / \ / 
       0 |-30|-20|-10|0,0| 10| 20| 30|
		/ \ / \ / \ / \ / \ / \ / \ /
    -1 |-31|-21|-11|0-1|1-1|2-1|3-1|
	  / \ / \ / \ / \ / \ / \ / \ /
  -2 |-32|-22|-12|0-2|1-2|2-2|3-2|
	/ \ / \ / \ / \ / \ / \ / \ / 
-3 |-33|-23|-13|0-3|1-3|2-3|3-3|
	\ / \ / \ / \ / \ / \ / \ / 

"""
#plansza jako słownik, gdzie klucz to współrzedne
#dodajemy do słownika, kiedy gracz umieści jakieś słowo - wtedy może być nieskończona

def rysuj_planszę(plansza):
	n = len(plansza)
	m = int((n-1)/2)
	l = 6*m
"""
	pierwszy_rząd = ' ' + l *' '
	for i in range(-m, 0, 1):
		pierwszy_rząd += f'{i}  '

	for i in range(0, m+1):
		pierwszy_rząd += f'{i}   '

	tablica = pierwszy_rząd + '\n'
	l = l - 3
	tablica += ' ' + l *' ' + (n) * ' / \\' + '\n'

	for i in range(-m, 0, 1):
		l = l - 2
		tablica += l *' ' + f'{i}' + ' | ' + ' |'.join(plansza[i] if type(plansza[i]) == str else ' ') + '\n'
		tablica += (l+1) *' ' + (n) * ' / \\' + ' /' + '\n' 
		#l = l - 2
		#tablica += l *' ' +

	#parzysty_rząd = (l-2)*' ' + (n-1) * r' \ /' + r' \ '
	#rząd_z_wartościami = (l-4)*' ' + f'{i}' + ' | ' + ' |'.join(plansza[i])
	
	drugi_rząd = '  ' + n * '| . ' + '|'
	trzeci_rząd = n * ' / \\' + r' / '
	czwarty_rząd = n * '| . ' + '|' + '  '

	
	#tablica += parzysty_rząd + '\n'
	#tablica += rząd_z_wartościami + '\n'

	for i in range(n):
		tablica += parzysty_rząd + '\n'
		tablica += drugi_rząd + '\n'
		tablica += trzeci_rząd + '\n'
		tablica += czwarty_rząd + '\n'
	tablica += pierwszy_rząd

	print(tablica)
"""

#Dostawka
def dostawka(słowo: str, pierwsza_współrzędna: tuple, kierunek: str):
	#zwraca listę krotek w postaci (litera, współrzędne) w zależności od kierunku wpisywanego słowa
	słowo = słowo.upper()
	współrzędne = []
	x,y = pierwsza_współrzędna

	if kierunek.lower() == 'poziomo':
		i = 0
		while i <= len(słowo):
			współrzędne.append((x,y))
			x += 1
			i += 1
	if kierunek.lower() == 'w górę':
		i = 0
		while i <= len(słowo):
			współrzędne.append((x,y))
			y += 1
			i += 1
	if kierunek.lower() == 'w dół':
		i = 0
		while i <= len(słowo):
			współrzędne.append((x,y))
			x -= 1
			y -= 1
			i += 1	
	return list(zip(słowo, współrzędne))

print(dostawka('kot', (0,0), 'poziomo'))

def sprawdź_współrzędne(współrzędne: tuple):
	if len(współrzędne) != 2: return False
	for lista in plansza:
		if współrzędne in lista: return True
	return False

def sprawdź_słowo(słowo: str):
	if słowo.lower() in open('slownik.txt').read(): return True
	return False

def sprawdź_czy_poprawne(dostawka):
	słowo = ''
	for lista in dostawka:
		współrzędne = lista[1]
		if not sprawdź_współrzędne(współrzędne): return False
		słowo += lista[0]
	if not sprawdź_słowo(słowo): return False
	return True

print(sprawdź_czy_poprawne([['k', (0,0)], ['o', (0,1)], ['t', (0,2)]]))

def punkty(plansza, dostawka) -> int: 
#zwraca ile punktów zdobywają litery wstawione na planszę zgodnie z dostawką
#jeśli dostawka jest nieprawidłowa zwraca −1 lub rzuca wyjątkiem. Plansza nie zmienia się.
	count = 0
	if sprawdź_czy_poprawne(dostawka):
		for i in range(len(dostawka)):
			count += letterfreq[i][1]
	else:
		return -1

def wstaw(plansza, dostawka) -> bool:
	#wstawia dostawkę na planszę. Zwraca True gdy udało się, False gdy dostawka nie jest prawidłowa.

	#w którym momencie zwrócić False ?
	for krotka in dostawka:
		litera = krotka[0]
		współrzędne = krotka[1]

		for wiersz in plansza:
			for i in range(len(wiersz)):
				if wiersz[i] == współrzędne:
					wiersz[i] = litera
					continue
	else: return True


print(wstaw(plansza, dostawka('kot', (0,0), 'poziomo')))
print(wstaw(plansza, dostawka('kot', (0,0), 'poziomo')))
print(plansza)


def rozgrywka(gracz, plansza, woreczek):
	global numer_rundy, gracze

	if len(woreczek) != 0:
		#pokazuje, czyja jest tura, wyświetla aktualny stan planszy i zbiór liter gracza
		print('\nRunda ' + str(numer_rundy) + ': Tura gracza ' + gracze[0][0])
		rysuj_planszę(plansza)
		print('\nZbiór liter gracza ' + gracze[0][0] + ': ' + zbiór_gracza_str(gracze[0][1]))

		while True:	
			wymiana = input('\nCzy chcesz wymienić litery? ').lower()
			if wymiana == 'tak': break #dodać funkcję wymiany liter
			else: słowo_gracza = input('Podaj słowo, które chcesz zagrać: ')

			if sprawdź_słowo(słowo_gracza): break
			else: 
				print('Twoje słowo jest nieprawidłowe.')
				continue

		if wymiana != 'tak':
			while True:
				współrzędne = tuple(input('Podaj współrzędne pierwszej litery: '))
				if sprawdź_współrzędne(współrzędne): break
				else: 
					print('Te współrzędne są nieprawidłowe.')
					continue
		
		kierunek = input('Podaj kierunek, w którym chcesz ustawić słowo (poziomo, w górę lub w dół): ')
		# ...

		dostawka(słowo_gracza, współrzędne, kierunek)
		wstaw(plansza, dostawka)
		gracze[aktualny_gracz][2] += punkty(plansza, dostawka)

		#wyświetlamy aktualny wynik gracza
		print('\n' + gracze[aktualny_gracz][0] + ', Twój wynik to: ' + gracze[aktualny_gracz][2])

		#kolejny gracz
		if gracze[aktualny_gracz] != gracze[-1]:
			aktualny_gracz += 1
		else:
			aktualny_gracz = 0
			numer_rundy += 1

		#funkcja wołana rekurencyjnie
		turn(player, board, bag)

	else:
		koniec_gry()

def początek_gry():
	global numer_rundy, gracze
	print('\nWitaj w grze Hex Scrabble!')

	numer_rundy = 1
	aktualny_gracz = gracze[0]
	#początkowy_woreczek()

	rozgrywka(aktualny_gracz, plansza, woreczek)

def koniec_gry():
	#gra kończy się, kiedy w woreczku skończą się litery
	global gracze
	najwyższy_wynik = 0
	zwycięzca = ''
	for i in range(len(gracze)):
		if gracze[i][2] > najwyższy_wynik:
			najwyższy_wynik = gracze[i][2]
			zwycięzca = gracze[i][0]
	print('Koniec gry. Zwycięzcą jest ' + zwycięzca + '.')


początek_gry()


"""

 \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ 
  | . | . | 40| 31| 22| 13| 04| . | . | . |
 / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / 
| . | . | . | 30| 21| 12| 03| . | . | . |  
 \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ 
  | . | . | . | 20| 11| 02| . | . | . | . |
 / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / 
| . | . | . | . | 10| 01|-12| . | . | . |  
 \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ 
  | . | . | . | . |0,0|-11|-22| . | . | . |
 / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / 
| . | . | . | . |0-1|-10|-21| . | . | . |  
 \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ 
  | . | . | . |0-2| . |-20|-31| . | . | . |
 / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / 
| . | . | . |0-3| . | . |-30| . | . | . |  
 \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ 
  | . | . |0-4| . | . | . |-40| . | . | . |
 / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / 
| . | . |0-5| . | . | . | . |-50| . | . |  
 \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ 



		 -6  -5  -4  -3  -2  -1   0   1   2   3   4   5
	 \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ 
4	  |-64|-54|-44|-34|-24|-14| 04| 14| 24| 34| 44| 54|
	 / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / 
3	|-63|-53|-43|-33|-23|-13| 03| 13| 23| . | . | . | 6 
	 \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ 
2	  |-52| . | . |-22|-12| 02| 12| 22| . | . | . | . |
	 / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / 
1	|-51| . | . |-21|-11| 01| 11| 21| . | . | . | . | 7 
	 \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ 
0	  |-40|-30|-20|-10|0,0| 10| 20| 30| 40| 50| 60| . |
	 / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / 
-1	|-4.| . | . | . |0-1|1-1|-21| . | . | . | . | . | 8
	 \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ 
-2	  |-3.| . | . |0-2| . |2-2|-31| . | . | . | . | . |
	 / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / 
-3	|-3.| . | . |0-3| . | . |3-3| . | . | . | . | . | 9  
	 \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ 
-4	  |-2.| . |0-4| . | . | . |4-4| . | . | . | . | . |
	 / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / 
-5	|-2.| . |0-5| . | . | . | . |5-5| . | . | . | . | 10  
	 \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ 



		     -3  -2  -1   0 
	       / \ / \ / \ / \
3	      |-33|-23|-13| 03| 1
	     / \ / \ / \ / \ / \
2	    |-32|-22|-12| 02| 12| 2
	   / \ / \ / \ / \ / \ / \
1	  |-31|-21|-11| 01| 11| 21| 3
	 / \ / \ / \ / \ / \ / \ / \
0	|-30|-20|-10|0,0| 10| 20| 30|
	 \ / \ / \ / \ / \ / \ / \ /
-1	  |-21|-11|0-1|1-1|2-1|3-1|
	   \ / \ / \ / \ / \ / \ / 
-2	    |-12|0-2|1-2|2-2|3-2|
	     \ / \ / \ / \ / \ /
-3	      |0-3|1-3|2-3|3-3|
	       \ / \ / \ / \ /

"""
