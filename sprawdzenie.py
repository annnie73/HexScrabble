def wymiana(): 
    litery_do_wymiany = re.split(r', |; |,|;|\s', input('Które litery chcesz wymienić? '))
    if not sprawdź_wymianę(litery_do_wymiany): wymiana()

    for litera in litery_do_wymiany:
        usuń_ze_zbioru(gracze[aktualny_gracz][1], litera)
    uzupełnij_zbiór(gracze[aktualny_gracz][1])
    print('Litery zostały wymienione. \nTwój aktualny zbiór liter to: ' + zbiór_gracza_str(gracze[aktualny_gracz][1]))

"""
    elif czy_wymiana == 'nie' or czy_wymiana == 'n':
        return False
        #słowo_gracza = input('Podaj słowo, które chcesz zagrać: ')
        #if sprawdź_słowo(słowo_gracza): break
        #else: 
        #    print('Twoje słowo jest nieprawidłowe.')
        #    continue
    else:
        print('Jedyne możliwe odpowiedzi to tak/t i nie/n.')
        continue
"""





def rozgrywka(plansza, woreczek):
    global gracze, numer_rundy, aktualny_gracz

    if len(woreczek) != 0:
        #pokazuje, czyja jest tura, wyświetla aktualny stan planszy i zbiór liter gracza
        print('\nRunda ' + str(numer_rundy) + ': Tura gracza ' + gracze[aktualny_gracz][0])
        print('Liczba liter pozostałych w woreczku to ' + str(len(woreczek)) + '.')
        #rysuj_planszę(plansza)
        print('\nZbiór liter gracza ' + gracze[aktualny_gracz][0] + ': ' + zbiór_gracza_str(gracze[aktualny_gracz][1]))

        while True:
            czy_wymiana = input('\nCzy chcesz wymienić litery? ').lower()
            if czy_wymiana == 'tak' or czy_wymiana == 't':
                wymiana()
                break
            elif czy_wymiana == 'nie' or czy_wymiana == 'n':
                break
            else:
                print('Jedyne możliwe odpowiedzi to tak/t i nie/n.')
                continue



        while True: 
            wymiana = input('\nCzy chcesz wymienić litery? ').lower()
            if wymiana == 'tak' or wymiana == 't': 
                while True:
                    litery_do_wymiany = re.split(r', |; |,|;|\s', input('Które litery chcesz wymienić? '))
                    if not sprawdź_wymianę(litery_do_wymiany): continue
                    else: break

                for litera in litery_do_wymiany:
                    usuń_ze_zbioru(gracze[aktualny_gracz][1], litera)
                uzupełnij_zbiór(gracze[aktualny_gracz][1])
                print('Litery zostały wymienione. \nTwój aktualny zbiór liter to: ' + zbiór_gracza_str(gracze[aktualny_gracz][1]))
                break 

            elif wymiana == 'nie' or wymiana == 'n':
                słowo_gracza = input('Podaj słowo, które chcesz zagrać: ')
                if sprawdź_słowo(słowo_gracza): break
                else: 
                    print('Twoje słowo jest nieprawidłowe.')
                    continue
            else:
                print('Jedyne możliwe odpowiedzi to tak/t i nie/n.')
                continue

        #coś trzeba pozmieniać z tą pętlą, bo np. kiedy jest 'nie nakładają się poprawnie', wraca mnie tylko do 'podaj współrzędne'

        if wymiana != 'tak' and wymiana != 't':
            while True:
                współrzędne = input('Podaj współrzędne pierwszej litery: ')
                if sprawdź_współrzędne(współrzędne): 
                    współrzędne = sprawdź_współrzędne(współrzędne)
                else: 
                    print('Te współrzędne są nieprawidłowe.')
                    continue

                kierunek = input('Podaj kierunek, w którym chcesz ustawić słowo - poziomo (p), w górę (g) lub w dół (d): ')
                if stwórz_dostawkę(słowo_gracza, współrzędne, kierunek):
                    dostawka = stwórz_dostawkę(słowo_gracza, współrzędne, kierunek)
                    if sprawdź_czy_poprawne(dostawka): break
                    else: 
                        continue
                else:
                    print('Ten kierunek nie jest poprawny.')
                    continue


            gracze[aktualny_gracz][2] += punkty(plansza, dostawka)
            wstaw(plansza, dostawka)

            #usuń_ze_zbioru ...

            uzupełnij_zbiór(gracze[aktualny_gracz][1])

            print(plansza)

        #wyświetlamy aktualny wynik gracza
        print('\n' + gracze[aktualny_gracz][0] + ', Twój aktualny wynik to ' + str(gracze[aktualny_gracz][2]) + '.')

        #kolejny gracz
        if aktualny_gracz != len(gracze)-1:
            aktualny_gracz += 1
        else:
            aktualny_gracz = 0
            numer_rundy += 1

        #funkcja wołana rekurencyjnie
        rozgrywka(plansza, woreczek)

    else:
        koniec_gry()