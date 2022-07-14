import tkinter
import functools
import copy
import time
import statistics


class Stare:
    decodif_poz_matrice = [(1, 1), (1, 4), (1, 7), (2, 2), (2, 4), (2, 6), (3, 3), (3, 4), (3, 5), (4, 1), (4, 2), (4, 3), (4, 5), (4, 6), (4, 7), (5, 3), (5, 4), (5, 5), (6, 2), (6, 4), (6, 6), (7, 1), (7, 4), (7, 7)]

    #matrice 8 x 3
    @staticmethod
    def generare_matrice():  # 3

       # True = piesa alba
       # False = piesa neagra
       # None = casuta goala fara piese
       #
        return [[None for _ in range(3)] for _ in range(8)] #returneaza matricea initiala goala

    def __init__(self, matrix, piese_albe_nefolosite=9, piese_albe_pe_tabla=0, piese_negre_nefolosite=9, piese_negre_pe_tabla=0, jucator_curent_alb=True, tata=None, se_scoate_o_piesa=False):

        self.tata = tata                                      #starea din care s-a generat mutarea
        self.matrix = matrix                                  #matricea actuala a tablei de bord
        self.piese_albe_nefolosite = piese_albe_nefolosite    #nr de piese ce mai trb puse pe tabla
        self.piese_albe_pe_tabla = piese_albe_pe_tabla        #cate piese se gasesc pe tabla
        self.piese_negre_nefolosite = piese_negre_nefolosite  #nr de piese ce mai trb puse pe tabla
        self.piese_negre_pe_tabla = piese_negre_pe_tabla      #cate piese se gasesc pe tabla
        self.jucator_curent_alb = jucator_curent_alb          #ce jucator urmeaza sa mute. True daca e alb, False daca e Negru
        self.se_scoate_o_piesa = se_scoate_o_piesa            #True daca la aceasta mutare se elimina o piesa a adversarului, False daca se continua jocul
        self.l_succesori = None                               #va retine lista cu mutari posibile sau None daca nu a fost inca generata
        self.estimare = None                                  #va retine scorul estimat de euristica aleasa sau None daca nu a fost inca estimat



    def __eq__(self, o):
        # o = obiectul cu care se compara
        # returneaza True daca starile sunt echivalente

        if self.__class__ == o.__class__: #doua stari sunt echivalente daca au matricele identice + nr piese jucatori sunt egale + jucatorul care urmeaza sa mute e acelasi
                                          #daca este o mutare in care se elimina sau nu piese
            return self.matrix == o.matrix and self.jucator_curent_alb == o.jucator_curent_alb and self.piese_albe_nefolosite == o.piese_albe_nefolosite and \
                   self.piese_albe_pe_tabla == o.piese_albe_pe_tabla and self.piese_negre_nefolosite == o.piese_negre_nefolosite and self.piese_negre_pe_tabla == o.piese_negre_pe_tabla \
                   and self.se_scoate_o_piesa == o.se_scoate_o_piesa
        else:
            return False

    def print_matrix(self):

        # 4.
        # afiseaza matricea in consola pentru debug

        for i in range(len(self.matrix)):
            if i != 3:
                print(self.matrix[i])
            else:
                print(self.matrix[i], end="     ")
        print("...............")

    @classmethod
    def este_in_moara(cls, matrix, poz):

        # matrix: o matrice 8x3 pe care se face verificarea
        # poz = pozitia pentru care se verifica
        #decodif_poz_matrice contine pozitile reale pe care se afla butoanele

        lin_reala, col_reala = cls.decodif_poz_matrice[poz[0] * 3 + poz[1]]
        ok_moara_col = True
        ok_moara_lin = True
        for i in range(len(cls.decodif_poz_matrice)):
            lin_in_matrice = i // 3
            col_in_matrice = i % 3
            if cls.decodif_poz_matrice[i][0] == lin_reala:
                if matrix[lin_in_matrice][col_in_matrice] != matrix[poz[0]][poz[1]] and (lin_reala != 4 or not (col_reala < 4 < cls.decodif_poz_matrice[i][1] or col_reala > 4 > cls.decodif_poz_matrice[i][1])):
                    ok_moara_col = False
            if cls.decodif_poz_matrice[i][1] == col_reala:
                if matrix[lin_in_matrice][col_in_matrice] != matrix[poz[0]][poz[1]] and (col_reala != 4 or not (lin_reala < 4 < cls.decodif_poz_matrice[i][0] or lin_reala > 4 > cls.decodif_poz_matrice[i][0])):
                    ok_moara_lin = False
        return ok_moara_lin or ok_moara_col # returneaza True daca piesa respectiva se afla in moara, False altfel

    @classmethod
    def aproape_moara(cls, matrix, poz):


        #verifica daca in configuratie sunt 2 piese de aceeasi culoare



        lin_reala, col_reala = cls.decodif_poz_matrice[poz[0] * 3 + poz[1]]
        for i in range(len(cls.decodif_poz_matrice)):
            lin_in_matrice = i // 3
            col_in_matrice = i % 3
            if matrix[lin_in_matrice][col_in_matrice] == matrix[poz[0]][poz[1]] and matrix[lin_in_matrice][col_in_matrice] is not None:
                if cls.decodif_poz_matrice[i][0] == lin_reala and cls.decodif_poz_matrice[i][1] != col_reala:
                    if lin_reala != 4 or not (col_reala < 4 < cls.decodif_poz_matrice[i][1] or col_reala > 4 > cls.decodif_poz_matrice[i][1]):
                        return True
                if cls.decodif_poz_matrice[i][1] == col_reala and cls.decodif_poz_matrice[i][0] != lin_reala:
                    if col_reala != 4 or not (lin_reala < 4 < cls.decodif_poz_matrice[i][0] or lin_reala > 4 > cls.decodif_poz_matrice[i][0]):
                        return True
        return False         #True daca piesa respectiva se afla pe aceeași linie sau coloana cu o alta piesa de aceeași culoare, False altfel

    @classmethod
    def se_poate_deplasa(cls, matrix, poz):

        #verifica daca se poate muta o piesa sau nu

        linie_reala_actuala, coloana_reala_actuala = Stare.decodif_poz_matrice[poz[0] * 3 + poz[1]]
        for lin, col in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            try:
                idx_pozitie_noua = cls.decodif_poz_matrice.index((linie_reala_actuala + lin * max(1, abs(coloana_reala_actuala - 4)), coloana_reala_actuala + col * max(1, abs(linie_reala_actuala - 4))))
                new_lin = idx_pozitie_noua // 3
                new_col = idx_pozitie_noua % 3
                if matrix[new_lin][new_col] is None:
                    return True          #daca piesa se poate deplasa
            except ValueError:
                continue
        return False    #daca nu se poate deplasa piesa

    def generare_succesori(self): #5.

        # Va parcurge toate elementele din matrix. Daca nu mai sunt piese de adaugat, pentru elementele care au aceeasi culoare cu a jucatorului curent,
        # se vor incerca din cele maxim 4 directii posibile de deplasare, care sunt libere si se va genera noul succesor
        # returneaza lista mutarilor posibile pentru jucatorul curent

        if self.l_succesori is None:
            self.l_succesori = []
            for i in range(8):
                for j in range(3):
                    if self.se_scoate_o_piesa: #daca se poate scoate o piesa a adversarului
                        try:
                            self.l_succesori.append(self.eliminare_piesa(stare=self, lin=i, col=j))
                        except ValueError:
                            continue
                    else:
                        if (self.jucator_curent_alb and self.piese_albe_nefolosite > 0) or ((not self.jucator_curent_alb) and self.piese_negre_nefolosite > 0):
                            try:
                                self.l_succesori.append(self.adaugare_piesa(stare=self, lin=i, col=j))
                            except ValueError:
                                continue
                        else:
                            if self.matrix[i][j] == self.jucator_curent_alb:    #pentru elem care au aceeasi culoare cu a jucatorului curent
                                if (self.jucator_curent_alb and self.piese_albe_pe_tabla > 3) or ((not self.jucator_curent_alb) and self.piese_negre_pe_tabla > 3):
                                    for lin, col in [(-1, 0), (0, 1), (1, 0), (0, -1)]: #va incerca cele 4 directii de deplasare libere si va genera succesorul
                                        try:

                                            #obtinem linia si coloana reala a pozitiei curente. Apoi ne uitam sus, jos, stanga, dreapta, iar pt acele pozitii care exista
                                            #obtinem linia si coloana din matrice la care se afla elementul adiacent. Daca este o pozitie libera, generam un nou succesor

                                            linie_reala_actuala, coloana_reala_actuala = Stare.decodif_poz_matrice[i * 3 + j]
                                            idx_pozitie_noua = Stare.decodif_poz_matrice.index((linie_reala_actuala + lin * max(1, abs(coloana_reala_actuala - 4)), coloana_reala_actuala + col * max(1, abs(linie_reala_actuala - 4))))
                                            self.l_succesori.append(self.muta_piesa(stare=self, old_lin=i, old_col=j, new_lin=idx_pozitie_noua // 3, new_col=idx_pozitie_noua % 3))
                                        except ValueError:
                                            continue
                                else:

                                    #au ramas 3 piese pentru jucatorul curent, deci poate sa sara cum vrea

                                    for lin in range(8):
                                        for col in range(3):
                                            if self.matrix[lin][col] is None:
                                                try:
                                                    self.l_succesori.append(self.muta_piesa(stare=self, old_lin=i, old_col=j, new_lin=lin, new_col=col))
                                                except ValueError:
                                                    continue
        return self.l_succesori

    @classmethod
    def muta_piesa(cls, stare, old_lin, old_col, new_lin, new_col):

        # Muta o piesa de pe pozitia veche pe o pozitie noua. Ridica exceptia ValueError pentru o mutare incorecta
        # old_lin: linia pozitiei de pe care se muta
        # old_col: coloana pozitiei de pe care se muta
        # new_lin: noua linie la care se doreste sa se mute
        # new_col: noua coloana la care se doreste sa se mute
        # returneaza o noua stare in care s-a realizat mutarea, sau ridica o exceptie de tip ValueError daca s-a introdus o mutare invalida

        if stare.matrix[new_lin][new_col] is None:
            new_matrix = copy.deepcopy(stare.matrix)
            new_matrix[old_lin][old_col] = None
            new_matrix[new_lin][new_col] = stare.jucator_curent_alb
            eliminare = Stare.este_in_moara(new_matrix, (new_lin, new_col)) #verifica daca noua stare este in format de moara, daca da, atunci poate sa stearga o piesa a inamicului
            if eliminare:
                jucator_nou = stare.jucator_curent_alb #jucatorul care urmeaza va fi tot jucatorul curent
            else:
                jucator_nou = not stare.jucator_curent_alb #altfel e celalalt jucator
            stare_noua = Stare(tata=stare, matrix=new_matrix, piese_albe_nefolosite=stare.piese_albe_nefolosite, piese_albe_pe_tabla=stare.piese_albe_pe_tabla,
                               piese_negre_pe_tabla=stare.piese_negre_pe_tabla, piese_negre_nefolosite=stare.piese_negre_nefolosite, se_scoate_o_piesa=eliminare, jucator_curent_alb=jucator_nou)
            return stare_noua
        else:
            raise ValueError

    @classmethod
    def eliminare_piesa(cls, stare, lin, col):

        #primind o stare, elimina o piesa aflata pe o pozitie data
        #exceptia ValueError pentru o mutare incorecta
        # lin, col -> linia si coloana la care se afla piesa pe care vrem sa o eliminam
        # stare -> starea pe care se face mutarea
        if (not stare.jucator_curent_alb) == stare.matrix[lin][col] and (not Stare.este_in_moara(stare.matrix, (lin, col))):
            new_matrix = copy.deepcopy(stare.matrix)
            new_matrix[lin][col] = None
            negre_ramase = stare.piese_negre_pe_tabla
            albe_ramase = stare.piese_albe_pe_tabla
            if stare.jucator_curent_alb:
                negre_ramase -= 1
            else:
                albe_ramase -= 1
            stare_noua = Stare(tata=stare, matrix=new_matrix, piese_albe_nefolosite=stare.piese_albe_nefolosite, piese_albe_pe_tabla=albe_ramase,
                               piese_negre_pe_tabla=negre_ramase, piese_negre_nefolosite=stare.piese_negre_nefolosite, se_scoate_o_piesa=False, jucator_curent_alb=not stare.jucator_curent_alb)
            return stare_noua #stare noua in care s-a realizat stergerea
        else:
            raise ValueError #ridica o exceptie de tip ValueError daca s-a introdus o mutare invalida

    @classmethod
    def adaugare_piesa(cls, stare, lin, col):

        # Primind o stare, adauga o noua piesa pe tabla (in ordinea in care urmeaza in functie de stare.jucator_curent_alb).
        # Ridica exceptia ValueError pentru o mutare incorecta
        # lin, col = linia si coloana pe care vrem sa mutam piesa
        # returneaza o noua stare in care s-a realizat adaugarea, sau ridica o exceptie de tip ValueError daca s-a introdus o mutare invalida

        if stare.matrix[lin][col] is None:
            negre_nefolosite = stare.piese_negre_nefolosite
            negre_ramase = stare.piese_negre_pe_tabla
            albe_nefolosite = stare.piese_albe_nefolosite
            albe_ramase = stare.piese_albe_pe_tabla
            if stare.jucator_curent_alb:
                albe_ramase += 1
                albe_nefolosite -= 1
            else:
                negre_ramase += 1
                negre_nefolosite -= 1
            new_matrix = copy.deepcopy(stare.matrix)
            new_matrix[lin][col] = stare.jucator_curent_alb
            eliminare = Stare.este_in_moara(new_matrix, (lin, col)) #verif daca e in configuratie de 3 de moara
            if eliminare:                                      #daca da, atunci se poate scoate o piesa a adversarului
                jucator_nou = stare.jucator_curent_alb
            else:
                jucator_nou = not stare.jucator_curent_alb
            stare_noua = Stare(tata=stare, matrix=new_matrix, piese_albe_nefolosite=albe_nefolosite, piese_albe_pe_tabla=albe_ramase,
                               piese_negre_pe_tabla=negre_ramase, piese_negre_nefolosite=negre_nefolosite, se_scoate_o_piesa=eliminare, jucator_curent_alb=jucator_nou)
            return stare_noua
        else:
            raise ValueError

    def is_final_state(self):  #7
        #daca se ajunge intr-o stare fara succesori iar jucatorii au mai mult de 3 piese atunci e remiza
        #un jucator castiga daca adversarul mai are doua piese
        if self.piese_albe_nefolosite == 0 and self.piese_negre_nefolosite == 0 and (self.piese_negre_pe_tabla < 3 or self.piese_albe_pe_tabla < 3):
            return True
        else:
            return len(self.generare_succesori()) == 0


class MorrisBoard(tkinter.Tk):
    buttons = []

    def __init__(self, algoritm=2, jucator_om=1, adancime_maxima=2, euristica=True):

        #initializarea jocului
        #jucator_om: primeste culoarea cu care joaca omul. True=alb, False=negru
        # adancime_maxima:adancimea arborelui folosit de algoritmii minimax si alphabeta
        # euristica: True pentru o euristica mai buna, False pentru una mai putin buna

        super().__init__()
        self.geometry("440x552") #self.geometry indica dimensiunea ferestrei care se va deschide
        self.title("Creita Andreea - Tintar")
        self.board_frame = tkinter.Frame(self, width=440, height=512) #va tine frame-ul care se va deschide in fereastra(care va tine toate celelalte componente grafice)
        bg = tkinter.PhotoImage(file="board13.png")
        self.label = tkinter.Label(self.board_frame, image=bg)
        self.label.place(x=0, y=0)       #va adauga imaginea de fundal a tablei de tintar
        self.stare_curenta = Stare(Stare.generare_matrice()) #self.stare_curenta va retine configuratia actuala a jocului la care s-a ajuns
        self.exit_button = None          #butonul din centru care e de iesire
        self.add_buttons(5)              #retine toate butoanele pe care se poate deplasa o piesa
        self.poz_piesa_care_se_muta = None #folosit cand trebuie sa mutam o piesa, astfel incat in urma selectarii sa nu se treaca la alt jucator. Are valoarea None cand se poate trece
        self.jucator_ai = not jucator_om          #culoarea pt ai
        self.algoritm = algoritm                  #Primeste algoritmul cu care se joaca. 0=om vs om, 1=minimax, 2=alpha-beta
        self.board_frame.grid(row=1, column=1)
        self.adancime_maxima = adancime_maxima
        self.utilizator_ready = False             #retine daca omul si-a terminat toate mutarile si poate sa vina randul la ai
        self.t_ai = []                            #o lista folosita pentru statisticile legate de timpul algoritmului minimax/alpha-beta
        self.nr_noduri_ai = []                    #o lista folosita pentru statisticile legate de nr de noduri generate de algoritmului minimax/alpha-beta
        self.nr_noduri_ai_curent = 0              #retine nr de noduri generate de algoritmului minimax/alpha-beta la pasul curent
        self.t = time.time()                      #timpul la care s-a efectuat ultima mutare
        self.t0 = time.time()                     #retine timpul de inceput al jocului
        self.co_apeluri_ai = 0                    #cate mutari a facut calculatorul
        self.co_apeluri_om = 0                    #numara cate mutari a facut omul
        self.finalizat = False                    #retine daca s-a finaliat jocul. Ia valoarea True dupa ce se executa functia de finalizare, blocand tabla
        self.euristica = euristica

        if jucator_om == 2:  # optiunea 2 = ai vs ai
            while not Stare.is_final_state(self.stare_curenta):

                self.ai_play()
                self.euristica = not self.euristica
                self.jucator_ai = not self.jucator_ai
        else:
            #daca jucatorul alege sa joace cu piesele negre, atunci ai -ul va muta primul
            #alb incepe mereu
            if self.algoritm > 0 and self.jucator_ai:
                self.ai_play()

        #incepe ascultarea inputului pana la finalizarea jocului
        self.mainloop()

        self.finalizare(forced_quit=True)

##### 6 ######
    def play_next_move(self, poz): #poz: primeste pozitia butonului
        #Cand se apasa un buton de pe tabla se cheama una dintre metodele de mai jos
        #pt utilizatorul uman

        if not self.finalizat:
            utilizator = "alb" if self.stare_curenta.jucator_curent_alb else "negru"
            print("Este randul jucatorului " + utilizator)
            self.utilizator_ready = False
            try:
                idx = Stare.decodif_poz_matrice.index(poz)
                lin, col = (idx // 3, idx % 3)
                if self.stare_curenta.se_scoate_o_piesa:

                    self.eliminare_piesa(idx=idx, lin=lin, col=col) #se scoate piesa adversarului care nu e in configuratie de 3(moara)

                else:
                    if (self.stare_curenta.jucator_curent_alb and self.stare_curenta.piese_albe_nefolosite > 0) or ((not self.stare_curenta.jucator_curent_alb) and self.stare_curenta.piese_negre_nefolosite > 0):


                        self.adaugare_piesa(idx=idx, lin=lin, col=col) #daca jucatorul mai are piese si e randul lui se adauga piesa pe o pozitie goala

                    else:
                        #muta piesa pe pozitia aleasa

                        self.mutare_piesa(poz=poz, idx=idx, lin=lin, col=col)

                print("Timp de gandire {}: {}s".format(utilizator, time.time() - self.t)) #timp pt  metoda utilizatorului
                self.stare_curenta.print_matrix()
                self.t = time.time()
                self.co_apeluri_om += 1 #creste nr de mutari facute de om
                if self.algoritm > 0 and self.utilizator_ready and (not self.stare_curenta.se_scoate_o_piesa) and self.algoritm > 0:
                    self.ai_play()
            except ValueError:
                return
            self.finalizare()

    def ai_play(self):

        #Executa mutarea calculatorului. Daca dupa prima mutare se ajunge intr-o stare in care trebuie sa se scoata o piesa a adversarului
        #se mai genereaza inca un arbore al algoritmului minimax/alpha-beta

        if not self.finalizat:
            utilizator = "alb" if self.jucator_ai else "negru"
            print("Este randului AI: jucator " + utilizator)
            self.nr_noduri_ai_curent = 0
            if self.algoritm == 1:
                self.stare_curenta = self.mini_max(stare=self.stare_curenta, jucator_curent=self.jucator_ai, adancime_ramasa=self.adancime_maxima)
                if self.stare_curenta.se_scoate_o_piesa:
                    self.stare_curenta = self.mini_max(stare=self.stare_curenta, jucator_curent=self.jucator_ai, adancime_ramasa=self.adancime_maxima)
                    self.co_apeluri_ai += 1
            else:
                self.stare_curenta = self.alpha_beta(stare=self.stare_curenta, alpha=float('-inf'), beta=float('inf'), jucator_curent=self.jucator_ai, adancime_ramasa=self.adancime_maxima)
                if self.stare_curenta.se_scoate_o_piesa:
                    self.stare_curenta = self.alpha_beta(stare=self.stare_curenta, alpha=float('-inf'), beta=float('inf'), jucator_curent=self.jucator_ai, adancime_ramasa=self.adancime_maxima)
                    self.co_apeluri_ai += 1

            for i in range(len(self.stare_curenta.matrix)):   #coloreaza butoanele apasate pt mutarile facute
                for j in range(len(self.stare_curenta.matrix[i])):
                    if self.stare_curenta.matrix[i][j] is True:
                        self.buttons[i * 3 + j].configure(bg='white')
                    elif self.stare_curenta.matrix[i][j] is False:
                        self.buttons[i * 3 + j].configure(bg='black')
                    else:
                        self.buttons[i * 3 + j].configure(bg='pink')

            timp_gandire = time.time() - self.t
            self.t_ai.append(timp_gandire)
            self.t = time.time()
            self.co_apeluri_ai += 1
            self.nr_noduri_ai.append(self.nr_noduri_ai_curent)
            print("Timp de gandire AI-{}: {}s".format(utilizator, timp_gandire))
            euristica = "estimeaza_scor_by_pioni" if self.euristica else "estimeaza_scor_by_moara"
            print("Estimare Scor AI: {}, folosind Euristica={}".format(self.stare_curenta.estimare, euristica))
            print("Nr noduri generate de AI: {}".format(self.nr_noduri_ai_curent))
            self.stare_curenta.print_matrix()
            self.finalizare()

    def add_buttons(self, dim=5):

        # :param dim: dimensiunea unui buton. Clasa e configurata cu butoane de dimensiune 5

        # self.buttons va retine butoanele adaugate

        for lin, col in Stare.decodif_poz_matrice:
            button = tkinter.Button(self.board_frame, height=dim, width=dim, command=functools.partial(self.play_next_move, (lin, col)), bg="pink", activebackground='green')
            button.grid(row=lin, column=col)
            self.buttons.append(button)
        self.exit_button = tkinter.Button(self.board_frame, height=3, width=3, command=self._root().destroy, activebackground='red')
        self.exit_button.grid(row=4, column=4)

    def eliminare_piesa(self, idx, lin, col):

        #Se elimina o piesa aflata la o pozitie data si se actualizeaza butonul si starea curenta daca a fost eliminata cu succes
        #sau ridica exceptia ValueError pt o mutare incorecta
        #Foloseste metoda eliminare_piesa din clasa Stare
         #idx: pozitia butonului care trebuie actualizat
         #lin: linia de stergere
         #col: coloana de stergere


        if self.stare_curenta.matrix[lin][col] == (not self.stare_curenta.jucator_curent_alb) and (not Stare.este_in_moara(self.stare_curenta.matrix, (lin, col))):
            stare = Stare.eliminare_piesa(stare=self.stare_curenta, lin=lin, col=col)
            if stare in self.stare_curenta.generare_succesori():
                self.stare_curenta = stare     #daca a fost eliminata piesa cu succes, atunci se actualizeaza starea
                self.buttons[idx].configure(bg='pink') #butonul devine gol
                self.utilizator_ready = True
            else:
                raise ValueError
        else:
            raise ValueError

    def adaugare_piesa(self, idx, lin, col):

        # daca la pozitia data nu se afla nicio piesa atunci va actualiza butonul si starea curenta
        if self.stare_curenta.matrix[lin][col] is None:
            stare = Stare.adaugare_piesa(stare=self.stare_curenta, lin=lin, col=col) #se foloseste de metoda adaugare_piesa din cls Stare
            if stare in self.stare_curenta.generare_succesori():
                if self.stare_curenta.jucator_curent_alb:
                    self.buttons[idx].configure(bg='white')
                else:
                    self.buttons[idx].configure(bg='black')
                self.stare_curenta = stare
                self.utilizator_ready = True
            else:
                raise ValueError
        else:
            raise ValueError

    def mutare_piesa(self, poz, idx, lin, col):


         # poz: pozitia de la care se muta
         # idx: indexul butonului de actualizat (in lista self,buttons)
         # lin: linia noua
         # col: coloana noua


        if self.poz_piesa_care_se_muta is None:   #daca nu e selectata nicio piesa pe care vrem sa o mutam
            if self.stare_curenta.matrix[lin][col] == self.stare_curenta.jucator_curent_alb: #daca piesa pe care o selectezi e piesa jucatorului curent atunci
                self.poz_piesa_care_se_muta = poz       #piesa care se muta va lua pozitia butonului selectat (adica pozitia de la care se muta)
                self.buttons[idx].configure(bg='cyan') #piesa pe care o selectezi va fi culoarea cyan pana cand va fi mutata
                raise ValueError
        else:
            old_idx = Stare.decodif_poz_matrice.index(self.poz_piesa_care_se_muta)
            old_lin, old_col = (old_idx // 3, old_idx % 3)
            if self.stare_curenta.jucator_curent_alb:          #coloreaza butoanele in functie de ce culoare a ales jucatorul sa fie
                self.buttons[old_idx].configure(bg='white')
            else:
                MorrisBoard.buttons[old_idx].configure(bg='black')
            if self.stare_curenta.matrix[lin][col] is None:      #se muta piesa pe un loc liber
                stare = Stare.muta_piesa(stare=self.stare_curenta, old_lin=old_lin, old_col=old_col, new_lin=lin, new_col=col)
                if stare in self.stare_curenta.generare_succesori():
                    self.buttons[old_idx].configure(bg='pink')    #se schimba culorile pt butoane
                    if self.stare_curenta.jucator_curent_alb:
                        self.buttons[idx].configure(bg='white')
                    else:
                        self.buttons[idx].configure(bg='black')
                    self.stare_curenta = stare
                    self.utilizator_ready = True
                else:
                    self.poz_piesa_care_se_muta = None
                    raise ValueError
            else:
                self.poz_piesa_care_se_muta = None
                raise ValueError
            self.poz_piesa_care_se_muta = None

    def estimeaza_scor(self, stare): #8 pt stari care nu sunt finale

        #functiile de estimare a scorului dupa euristica aleasa
        #stare = starea pt care se face estimarea
        #se returmeaza valoarea estimarii

        def estimeaza_scor_by_pioni(stare):  #euristica 1

            #Influentat de cate piese are alb vs negru si daca o piesa e blocata sau nu
            #Cu cat jucatorul 1 are mai putine piese, cu atat este in avantaj celalalt jucator

            co = 0 #valoarea estimarii
            for i in range(len(stare.matrix)): #starea pt care se face estimarea
                for j in range(len(stare.matrix[i])):
                    if stare.matrix[i][j] is True:
                        co += 1
                        if Stare.se_poate_deplasa(stare.matrix, (i, j)): #se foloseste de conditia daca o piesa se poate deplasa sau nu
                            co += 0.5
                    elif stare.matrix[i][j] is False:
                        co -= 1
                        if not Stare.se_poate_deplasa(stare.matrix, (i, j)):
                            co += 0.5
            return co

        def estimeaza_scor_by_moara(stare):        #euristica 0

            #Influentat de cate piese are alb vs negru si daca avem mori sau nu
            #Daca exista o moara langa o configuratie de 2 pioni, si din moara se scoate o piesa si se adauga la configuratia de 2 pioni, se formeaza o moara
            co = 0 #valoarea estimarii
            for i in range(len(stare.matrix)):
                for j in range(len(stare.matrix[i])):
                    if stare.matrix[i][j] is True:
                        co += 1
                        if Stare.este_in_moara(stare.matrix, (i, j)):
                            co += 1
                        elif Stare.aproape_moara(stare.matrix, (i, j)):
                            co += 0.5
                    elif stare.matrix[i][j] is False:
                        co -= 1
                        if Stare.este_in_moara(stare.matrix, (i, j)):
                            co -= 1
                        elif Stare.aproape_moara(stare.matrix, (i, j)):
                            co -= 0.5
            return co #valoarea estimarii

        if self.euristica:
            return estimeaza_scor_by_pioni(stare)
        else:
            return estimeaza_scor_by_moara(stare)

    def mini_max(self, stare, adancime_ramasa, jucator_curent):

        # algoritmul minimax
        # stare: starea la care s-a ajuns
        # adancime_ramasa: adancimea ramasa(scade cu 1 la fiecare apel recursiv)
        #

        if stare.is_final_state() or adancime_ramasa == 0:
            stare.estimare = self.estimeaza_scor(stare)
            return stare
        else:
            #aplic algoritmul minimax pe toate mutarile posibile(calculand astfel subarborii lur)
            #scoruri = mutariCuEstimare in cod lab
            scoruri = [self.mini_max(x, adancime_ramasa - 1, not jucator_curent) for x in stare.generare_succesori()]
            self.nr_noduri_ai_curent += len(scoruri)
            if jucator_curent == self.jucator_ai:
                # daca jucatorul e JMAX aleg starea-fiica cu estimarea maxima
                stare_aleasa = max(scoruri, key=lambda stare_x: stare_x.estimare)
            else:
                # daca jucatorul e JMIN aleg starea-fiica cu estimarea minima
                stare_aleasa = min(scoruri, key=lambda stare_x: stare_x.estimare)
            stare.estimare = stare_aleasa.estimare
            if adancime_ramasa < self.adancime_maxima:
                return stare
            else:
                return stare_aleasa

    def alpha_beta(self, stare, alpha, beta, adancime_ramasa, jucator_curent):

        #  Algoritmul alpha-beta. Listele succesorilor se sorteaza in prealabil pt a asigura o taiere optima (alpha>=beta)
        #  stare: starea la care s-a ajuns
        #  adancime_ramasa: adancimea ramasa(scade cu 1 la fiecare apel recursiv)

        if stare.is_final_state() or adancime_ramasa == 0:
            stare.estimare = self.estimeaza_scor(stare)
            return stare

        elif alpha > beta:
            return stare    #este intr-un interval invalid deci nu o mai procesez

        else:
            stare_aleasa = stare
            if jucator_curent == self.jucator_ai:
                estimare_curenta = float('-inf')

                for stare_noua in sorted(stare.generare_succesori(), key=lambda stare_x: self.estimeaza_scor(stare_x), reverse=True):
                    # calculeaza estimarea pentru starea noua, realizand subarborele
                    stare_noua_cu_aproximare = self.alpha_beta(stare_noua, alpha, beta, adancime_ramasa - 1, not jucator_curent)
                    self.nr_noduri_ai_curent += 1

                    if estimare_curenta < stare_noua_cu_aproximare.estimare:
                        stare_aleasa = stare_noua_cu_aproximare
                        estimare_curenta = stare_noua_cu_aproximare.estimare
                    if alpha < stare_noua_cu_aproximare.estimare:
                        alpha = stare_noua_cu_aproximare.estimare
                        if alpha >= beta:
                            break
            else:
                estimare_curenta = float('inf')
                for stare_noua in sorted(stare.generare_succesori(), key=lambda stare_x: self.estimeaza_scor(stare_x)):
                    stare_noua_cu_aproximare = self.alpha_beta(stare_noua, alpha, beta, adancime_ramasa - 1, not jucator_curent)
                    self.nr_noduri_ai_curent += 1
                    if estimare_curenta > stare_noua_cu_aproximare.estimare:
                        stare_aleasa = stare_noua_cu_aproximare
                        estimare_curenta = stare_noua_cu_aproximare.estimare
                    if beta > stare_noua_cu_aproximare.estimare:
                        beta = stare_noua_cu_aproximare.estimare
                        if alpha >= beta:
                            break
            stare.estimare = stare_aleasa.estimare
            if adancime_ramasa < self.adancime_maxima:
                return stare
            else:
                return stare_aleasa

    def finalizare(self, forced_quit=False):  #10

        # afiseaza statisticile de final si blocheaza tabla prin self.finalizat
        # forced_quit: daca jocul s-a incheiat folosind butonul, inainte de finalizare este True; altfel False


        if (not self.finalizat) and (self.stare_curenta.is_final_state() or forced_quit):  #verifica daca jocul a fost incheiat fortat sau nu
            self.finalizat = True
            if self.algoritm > 0 and self.co_apeluri_ai > 0:
                print("Statistici Timp AI: min={}, max={}, avg={}, mediana={}".format(min(self.t_ai), max(self.t_ai), round(sum(self.t_ai) / self.co_apeluri_ai, 5), statistics.median(self.t_ai)))
                print("Statistici Nr noduri create de AI: min={}, max={}, avg={}, mediana={}".format(min(self.nr_noduri_ai), max(self.nr_noduri_ai), round(sum(self.nr_noduri_ai) / self.co_apeluri_ai, 5), statistics.median(self.nr_noduri_ai)))


            print("Timp total de joc: {}s".format(time.time() - self.t0))
            print("AI apelat de {} ori".format(self.co_apeluri_ai))
            print("Om-ul a avut {} mutari".format(self.co_apeluri_om))


            if not forced_quit: #daca nu a fost inchis fortat, atunci va afisa castigatorul sau remiza
                if self.stare_curenta.piese_albe_pe_tabla >= 3 > self.stare_curenta.piese_negre_pe_tabla:
                    print("A castigat jucatorul ALB")
                    self.exit_button.configure(bg='white')
                elif self.stare_curenta.piese_negre_pe_tabla >= 3 > self.stare_curenta.piese_albe_pe_tabla:
                    print("A castigat jucatorul NEGRU")
                    self.exit_button.configure(bg='black')
                else:
                    print("REMIZA")
                    self.exit_button.configure(bg='purple')


if __name__ == "__main__":

#1 + 2
    tip_algoritm = 2
    raspuns_valid = False
    while not raspuns_valid:
        tip_algoritm = input("Algorimul folosit? (raspundeti cu 0, 1 sau 2)\n 0.Om vs Om\n 1.Minimax\n 2.Alpha-beta\n ")
        if tip_algoritm in ['0', '1', '2']:
            raspuns_valid = True
        else:
            print("Nu ati ales o varianta corecta...")

    jucator = '1'
    if tip_algoritm != '0': #diferit de om vs om
        raspuns_valid = False
        while not raspuns_valid:
            jucator = input("Ce jucator alegeti? (raspundeti cu 0, 1 sau 2)\n 0.negru\n 1.alb\n 2.AI vs AI\n ")
            if jucator in ['0', '1', '2']:
                raspuns_valid = True
            else:
                print("Nu ati ales o varianta corecta...")

    nivel = '0'
    if tip_algoritm != '0':
        raspuns_valid = False
        while not raspuns_valid:
            nivel = input("Nivel dificultate? (raspundeti cu 1, 2, 3 sau 4)\n 1.Usor\n 2.Mediu\n 3.Dificil\n 4.Expert\n ")
            if nivel in ['1', '2', '3', '4']:
                raspuns_valid = True
            else:
                print("Nu ati ales o varianta corecta...")

    euristica = '1'
    if tip_algoritm != '0' and jucator != '2':  #nu e om vs om + nu e ai vs ai
        raspuns_valid = False
        while not raspuns_valid:
            euristica = input("Euristica? (raspundeti cu 0 sau 1)\n 0.Usor(dupa moara)\n 1.Greu(dupa pioni)\n ")
            if euristica in ['0', '1']:
                raspuns_valid = True
            else:
                print("Nu ati ales o varianta corecta...")

    MorrisBoard(algoritm=int(tip_algoritm), jucator_om=int(jucator), adancime_maxima=int(nivel), euristica=bool(int(euristica)))
