from operator import truediv
from termios import OFDEL
import pygame
import math
import copy
from sys import exit

#inicjalizacja biblioteki pygame
pygame.init()
screen = pygame.display.set_mode((1500, 800), pygame.RESIZABLE)
#screen.fill((245, 222, 179))
pygame.display.set_caption('Hex Scrabble')
zegar = pygame.time.Clock()

czcionka = pygame.font.Font('czcionki/Bitter-Regular.otf', 32)
duża_czcionka = pygame.font.Font('czcionki/Bitter-Bold.otf', 38)

tło = pygame.image.load('grafiki/wallpaper.jpeg')
tło = pygame.transform.rotozoom(tło, 0, 1.2)
screen.blit(tło, (0,0))

nazwa = duża_czcionka.render('Hex Scrabble', True, (116, 82, 74))
screen.blit(nazwa, (1050, 50))
"""
aktualny_gracz
litery_gracza
przycisk_wymiany
nr_rundy
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
Dopisuje_dostawke = False
dostawka = []

def wstaw_literę(lit):
	global aktualny_heksagon, pole, Dopisuje_dostawke, dostawka

	litera = (czcionka.render(lit, True, (116, 82, 74)))
	litera_rect = litera.get_rect(center = aktualny_heksagon.center)
	screen.blit(litera, litera_rect)
	dostawka.append((lit, pole))


def pobierz_literkę(adres_literki: int):
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
			return False

def aktualizuj_liste_mozliwych_pol(listamozliwychpol):
	global pole
	listamozliwychpol.remove(pole)

def ruch_gracza_realnego():
	#zwraca dostawkę na podstawie liter wpisanych przez gracza

	global aktualny_heksagon, pole, Dopisuje_dostawke, dostawka
	listamozliwychpol = [(x,y) for (x,y) in plansza if plansza[(x,y)][0] == ' ']

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				pozycja_myszki = pygame.mouse.get_pos()
				for x, y in plansza:
					#identyfikujemy sześciokąt, na który kliknął użytkownik, żeby wpisać literę
					heksagon_rect = plansza[x,y][1]

					
					#można dodać opcję, że kiedy klika strzałkę w prawo, lewo, górę lub dół, następny sześciokąt się podświetla !!

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

					if not Dopisuje_dostawke:
						kopia_planszy = copy.deepcopy(plansza)
						Dopisuje_dostawke = True

					if pobierz_literkę(event.key): #na odwrót - najpierw sprawdza czy polski znak
						if pole in listamozliwychpol:
							lit = pobierz_literkę(event.key)
							wstaw_literę(lit)
							aktualizuj_liste_mozliwych_pol(listamozliwychpol)
					
					else:
						pass #dodać polskie znaki






				if event.key == pygame.K_UP:
					if aktualny_heksagon:
						heksagon_3_rect.update(aktualny_heksagon)
						screen.blit(heksagon_3, heksagon_3_rect)

						for x,y in plansza:
							if aktualny_heksagon in plansza[x,y]:
								if (x, y+1) in plansza:
									aktualny_heksagon = plansza[x,y+1][1]
									break

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

						heksagon_2_rect.update(aktualny_heksagon)
						screen.blit(heksagon_2, heksagon_2_rect)

				if event.key == pygame.K_RETURN:
					Dopisuje_dostawke = False
					if dostawka:
						return dostawka

			#kiedy klika enter, sprawdzamy czy słowo jest poprawne i heja


		


		pygame.display.update()
		zegar.tick(60)


print(ruch_gracza_realnego())