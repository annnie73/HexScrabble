def sprawdź_czy_poprawne(dostawka): 
	#sprawdza czy słowa poprawnie się nakładają i czy gracz ma litery potrzebne do utworzenia słowa
	#global kopia_planszy
    #kierunek = None

    x0, y0 = dostawka[0][1]
    #jeśli dla wszystkich liter y-współrzędna jest taka sama: kierunek słowa to poziomo - sortujemy dostawkę od po x
    if all(dostawka[i][1][1] == y0 for i in range(len(dostawka))):
        dostawka = sorted(dostawka, key = lambda x: x[1][0])
        kierunek = 'p'


	#analogicznie z x-współrzędną - wtedy kierunek to do góry
    elif all(dostawka[i][1][0] == x0 for i in range(len(dostawka))):
        dostawka = sorted(dostawka, key = lambda x: x[1][1])
        kierunek = 'g'

	#jeśli nie, kierunek powinien być do dołu - sortujemy po x i sprawdzamy czy y się zmniejszają
    else:
        dostawka = sorted(dostawka, key = lambda x: x[1][0])
        if all(dostawka[j][1][1] < dostawka[i][1][1] for i in range(len(dostawka)) for j in range(i+1, len(dostawka))):
            kierunek = 'd'
        else: 
            #coś jeszcze blitujemy
            return False
    return kierunek

print(sprawdź_czy_poprawne([('K', (-1, 1)), ('O', (0, 0)), ('T', (1, -1))]))