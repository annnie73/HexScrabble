from operator import truediv
from termios import OFDEL
import pygame, math, copy
from sys import exit

#inicjalizacja biblioteki pygame, czcionek i outline'u planszy
pygame.init()
screen = pygame.display.set_mode((1500, 800), pygame.RESIZABLE)
#screen.fill((245, 222, 179))
pygame.display.set_caption('Hex Scrabble')
zegar = pygame.time.Clock()

czcionka = pygame.font.Font('czcionki/Bitter-Regular.otf', 32)
czcionka_b_mała = pygame.font.Font('czcionki/Bitter-Regular.otf', 22)
czcionka_mała = pygame.font.Font('czcionki/Bitter-Regular.otf', 30)
czcionka_najmn = pygame.font.Font('czcionki/Bitter-Regular.otf', 20)
czcionka_średnia = pygame.font.Font('czcionki/Bitter-Bold.otf', 30)
czcionka_duża = pygame.font.Font('czcionki/Bitter-Bold.otf', 38)

tło = pygame.image.load('grafiki/wallpaper.jpeg')
tło = pygame.transform.rotozoom(tło, 0, 1.2)

nazwa = czcionka_duża.render('Hex Scrabble', True, (116, 82, 74))
runda = czcionka_średnia.render('Runda ', True, (102, 70, 62))
wyświetl_gracza = czcionka_mała.render('Tura gracza ', True, (102, 70, 62))
litery = czcionka_mała.render('Twoje litery:', True, (116, 82, 74))

#przycisk wymiany liter
przycisk = pygame.image.load('grafiki/button.png')
przycisk.set_colorkey((255, 255, 255))
przycisk.convert_alpha()

przycisk2 = pygame.image.load('grafiki/button2.png')
przycisk2.set_colorkey((255, 255, 255))
przycisk2.convert_alpha()

przycisk_w_rect = przycisk.get_rect(center = (960, 460))
przycisk_w2_rect = przycisk.get_rect(center = (960, 460))
wymiana = czcionka_najmn.render('WYMIANA', True, (241, 205, 191))
wymiana_rect = wymiana.get_rect(center = przycisk_w_rect.center)

przycisk_k_rect = przycisk.get_rect(center = (1160, 460))
przycisk_k2_rect = przycisk2.get_rect(center = (1160, 460))
koniec = czcionka_najmn.render('KONIEC TURY', True, (241, 205, 191))
koniec_rect = koniec.get_rect(center = przycisk_k_rect.center)

"""
wynik_gracza
"""
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

tekst = czcionka.render('A', True, (116, 82, 74))

def inicjalizacja_gry():
	global screen, czcionka, czcionka_b_mała, czcionka_duża, czcionka_mała, czcionka_średnia, tło
	global nazwa, runda, wyświetl_gracza, litery, przycisk, przycisk_w_rect, przycisk2, przycisk_w2_rect
	global wymiana, wymiana_rect, heksagon, heksagon_1_rect, heksagon_2, heksagon_2_rect
	global heksagon_3, heksagon_3_rect, tekst

	screen.blit(tło, (0,0))
	screen.blit(nazwa, (1050, 50))
	screen.blit(runda, (880, 110))
	screen.blit(wyświetl_gracza, (880, 150))
	screen.blit(przycisk, przycisk_w_rect)
	screen.blit(wymiana, wymiana_rect)
	screen.blit(przycisk, przycisk_k_rect)
	screen.blit(koniec, koniec_rect)

plansza = {}
def stwórz_planszę(r):
	#tworzy planszę w postaci słownika, w postaci współrzędne:litera
	#jej przedstawieniem graficznym będzie duży sześciokąt o promieniu r
	global plansza
    #plansza = {}
	
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
					screen.blit(wymiana, wymiana_rect)
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
						kopia_planszy = copy.deepcopy(plansza)
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

#rysuj_planszę()
#print(plansza)

if __name__ == '__main__':
	inicjalizacja_gry()
	ruch_gracza_realnego(1)

