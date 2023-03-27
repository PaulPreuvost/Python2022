from tkinter import *
from playsound import playsound
from tkinter.messagebox import *
from pathlib import Path

class case:
    def __init__(self,pion=0,player=0):
        self.__pion = pion
        self.__player = player

    def getPion(self):
        return self.__pion
    def setPion(self,x):
        self.__pion = x
    def getPlayer(self):
        return self.__player
    def setPlayer(self,x):
        self.__player = x

    def color(self):
        if   self.__player == 0:
            return "white"
        elif self.__player == 1:
            return "green"
        elif self.__player == 2:
            return "red"
        elif self.__player == 3:
            return "grey"
        elif self.__player == 4:
            return "purple"
        elif self.__player == 5:
            return "blue"
        elif self.__player == 6:
            return "#FF00EB"
        elif self.__player == 7:
            return "yellow"
        elif self.__player == 8:
            return "white"

class jeu:
    def __init__(self):
        self.__ligne = 0
        self.__colone = 0
        self.__joueur = 0
        self.__tours = 1
        self.__joueurRestant = []
        self.__grille = None
        self.__joueurEnCour = 0
        self.__division = False
        self.__kill =[]
        self.__infiniteBoucle = False
        self.__infiniteBoucleVariable = 0
    # tk inter fenetre parametre
    # les input et les label colone ligne et joueur
        self.__parametre = Tk()
        self.__parametre.config(bg="#CEC194")
        self.__parametre.geometry('500x400')
        self.__parametre.title("Paramètres du jeu")
        self.__parametre.iconbitmap("logo.ico")
        self.__parametre.resizable(False, False)
        self.nombreLigneEntry = Entry(self.__parametre, justify="center")
        self.nombreColoneEntry = Entry(self.__parametre, justify="center")
        self.nombreJoueurEntry = Entry(self.__parametre, justify="center")
        boutonLancementJeu=Button(self.__parametre, text="Lancement du jeu", command=self.verificationDonnee)
        boutonLancementSauvegarde=Button(self.__parametre, text="Charger une partie", command=self.lireSauvegarde)
        textLigneEntry = StringVar()
        textColoneEntry = StringVar()
        textJoueurEntry = StringVar()
        self.ligneTextEntry = Label(self.__parametre,fg = "#084351", textvariable=textLigneEntry,bg="#CEC194")
        self.coloneTextEntry = Label(self.__parametre,fg = "#084351", textvariable=textColoneEntry,bg="#CEC194")
        self.joueurTextEntry = Label(self.__parametre,fg = "#084351", textvariable=textJoueurEntry,bg="#CEC194")
        textLigneEntry.set("Nombre de lignes (3 et 10) :")
        textColoneEntry.set("Nombre de colonnes (3 et 12) :")
        textJoueurEntry.set("Nombre de joueurs (2 et 8) :")
        self.ligneTextEntry.pack()
        self.nombreLigneEntry.pack()
        self.coloneTextEntry.pack()
        self.nombreColoneEntry.pack()
        self.joueurTextEntry.pack()
        self.nombreJoueurEntry.pack()
        boutonLancementJeu.pack(side=TOP, padx=50, pady=10)
        boutonLancementSauvegarde.pack(side=TOP, padx=50, pady=10)
        
# les label pour les erreur colone ligne et joueur
        textLigneErreur = StringVar()
        textColoneErreur = StringVar()
        textJoueurErreur = StringVar()
        textSaveErreur = StringVar()
        self.verifLigneOk = Label(self.__parametre,fg = "#D34E37", textvariable=textLigneErreur,bg="#CEC194")
        self.verifColoneOk = Label(self.__parametre,fg = "#D34E37", textvariable=textColoneErreur,bg="#CEC194")
        self.verifJoueurOk = Label(self.__parametre,fg = "#D34E37", textvariable=textJoueurErreur,bg="#CEC194")
        self.verifSaveOk = Label(self.__parametre,fg = "#D34E37", textvariable=textSaveErreur,bg="#CEC194")
        textLigneErreur.set("Le nombre de lignes doit être compris entre 3 et 10")
        textColoneErreur.set("Le nombre de colonnes doit être compris entre 3 et 12")
        textJoueurErreur.set("Le nombre de joueurs doit être compris entre 2 et 8")
        textSaveErreur.set("La sauvegarde est introuvable")
        self.__parametre.mainloop()

    def verificationDonnee(self):
        self.verifLigneOk.forget()
        self.verifColoneOk.forget()
        self.verifJoueurOk.forget()
        self.__ligne  = self.nombreLigneEntry.get()
        self.__colone = self.nombreColoneEntry.get()
        self.__joueur = self.nombreJoueurEntry.get()
        condition1 = False
        condition2 = False
        condition3 = False
        # test si les 3 input sont bien remplis et que se sont des chiffres
        try:
            int(self.__ligne)
            ligneVerif = True
        except ValueError:
            ligneVerif = False
        try:
            int(self.__colone)
            coloneVerif = True
        except ValueError:
            coloneVerif = False
        try:
            int(self.__joueur)
            joueurVerif = True
        except ValueError:
            joueurVerif = False
        # si les 3 input sont bon alors test si les valeurs sont dans les limites et sauvegarder les donnees
        if (ligneVerif == True) and (coloneVerif == True) and (joueurVerif == True) :
            self.__ligne  = int(self.nombreLigneEntry.get())
            self.__colone = int(self.nombreColoneEntry.get())
            self.__joueur = int(self.nombreJoueurEntry.get())
            
            if self.__ligne<3 or self.__ligne>10:
                self.verifLigneOk.pack()
            else:
                condition1 = True
            if self.__colone<3 or self.__colone>12:
                self.verifColoneOk.pack()
            else:
                condition2 = True
            if self.__joueur<2 or self.__joueur>8:
                self.verifJoueurOk.pack()
            else:
                condition3 = True
        # enfin si les valeur sont dans les limites va fermer la fenetre set la grille et lancer le jeu
        if condition1 and condition2 and condition3:
            for i in range (1,self.__joueur+1):
                self.__joueurRestant.append(i)
            self.__parametre.destroy()
            self.__grille = [[case(0,0) for i in range(self.__colone)] for j in range(self.__ligne)]
            self.__joueurEnCour = 1
            self.lancementJeu()

    # tk inter fenetre jeu
    def lancementJeu(self):
        self.__jeu = Tk()
        self.__jeu.iconbitmap("logo.ico")
        self.__jeu.config(background="#CEC194")
        self.__jeu.title("Jeu de conquête")
        self.__jeu.resizable(False, False)
        playsound('sound\launch.mp3', block=False)
        self.__frameJeu= Frame(self.__jeu, background="#CEC194")
        self.__frameJeu.grid(row=0, column=0, rowspan=3)
        self.__canvas = Canvas(self.__frameJeu)
        self.__canvas.config(width=self.__colone * 40, height=self.__ligne * 40, bd=0)
        self.__canvas.pack()
        boutonSave=Button(self.__frameJeu, text="Sauvegarde", command=self.sauvegarde)
        boutonSave.pack(side=TOP,padx=10, pady=10)
        self.__frame2 = Frame(self.__jeu,background="#CEC194",bd=30)
        self.__frame2.grid(row=0, column=1)
        self.__textTours = StringVar()
        self.__textJoueurEnCour = StringVar()
        self.__textJoueurRestant = StringVar()
        self.__textTours.set(f"Tours : {self.__tours}")
        self.__textJoueurEnCour.set(f"Joueur actuel : {case(0,self.__joueurEnCour).color()}")
        self.__textJoueurRestant.set(f"Joueurs restants : {self.__joueurRestant}")
        self.labelTours = Label(self.__frame2,fg = "#D34E37",font="20", textvariable=self.__textTours,background="#CEC194")
        self.labelJoueurEnCours = Label(self.__frame2,fg = "#D34E37",font="20", textvariable=self.__textJoueurEnCour,background="#CEC194")
        self.labelJoueurRestant = Label(self.__frame2,fg = "#D34E37",font="20", textvariable=self.__textJoueurRestant,background="#CEC194")
        self.labelTours.pack()
        self.labelJoueurEnCours.pack()
        self.labelJoueurRestant.pack()
        self.affichage()
        self.__canvas.bind('<Button-1>',self.gameTurn)
        
        self.__jeu.mainloop()

    def affichage(self):
        for i in range(self.__ligne):
            for j in range(self.__colone):
                self.__canvas.create_rectangle(j * 40, i * 40, (j + 1) * 40,  (i + 1) * 40, 
                        fill="black", outline=case(0,self.__joueurEnCour).color())

                if self.__grille[i][j].getPion() == 3 :
                    self.__canvas.create_oval(j *40+5,i*40+5,(j+1)*40-25,(i+1)*40-25,
                        fill=self.__grille[i][j].color())
                    self.__canvas.create_oval(j *40+15,i*40+15,(j+1)*40-15,(i+1)*40-15,
                        fill=self.__grille[i][j].color())
                    self.__canvas.create_oval(j *40+25,i*40+25,(j+1)*40-5,(i+1)*40-5,
                        fill=self.__grille[i][j].color())

                elif self.__grille[i][j].getPion() == 2 :
                    self.__canvas.create_oval(j *40+5,i*40+5,(j+1)*40-25,(i+1)*40-25,
                        fill=self.__grille[i][j].color())
                    self.__canvas.create_oval(j *40+25,i*40+25,(j+1)*40-5,(i+1)*40-5,
                        fill=self.__grille[i][j].color())

                elif self.__grille[i][j].getPion() == 1 :
                    self.__canvas.create_oval(j *40+15,i*40+15,(j+1)*40-15,(i+1)*40-15,
                        fill=self.__grille[i][j].color())
                
        self.__textTours.set(f"Tours : {self.__tours}")
        self.__textJoueurEnCour.set(f"Joueur actuel : {case(0,self.__joueurEnCour).color()}")
        self.__textJoueurRestant.set(f"Joueurs restants : {self.__joueurRestant}")

    def gameTurn(self,event):
        self.__clicX=event.x//40
        self.__clicY=event.y//40
        if self.possible() == True:
            self.addPion()
            playsound('sound\moove.mp3', block=False)
            self.dispertion(self.__clicX,self.__clicY)
            while self.__division == True and self.__infiniteBoucle == False:
                self.__division = False
                for i in range(self.__colone):
                    for j in range(self.__ligne):
                        self.dispertion(i,j)
                        self.__infiniteBoucleVariable +=1
                if self.__infiniteBoucleVariable >= 1500:
                    self.__infiniteBoucle = True
                else:
                    self.__infiniteBoucle = False
            self.__infiniteBoucleVariable = 0
            for k in range(len(self.__joueurRestant)):
                if self.eliminate(k) == False:
                    self.__kill.append(k)
                    print("Le joueur",case(0,self.__joueurRestant[k]).color(),"a était éliminé par;",case(0,self.__joueurEnCour).color())
            for i in range(len(self.__kill)-1,-1,-1):
                del self.__joueurRestant[self.__kill[i]]
            self.__kill=[]
            if len(self.__joueurRestant)==1:
                print("Victoire")
                self.affichage()
                playsound('sound\win.mp3', block=False)
                replay = askyesno("Retry","Une autre partie ?",)
                if replay:
                    self.__jeu.destroy()
                    jeu()
                else:
                    self.__jeu.destroy()
            self.prochainJoueur()
            self.affichage()

    def possible(self):
        if self.__grille[self.__clicY][self.__clicX].getPion() == 0:
            return True
        else:
            return self.__grille[self.__clicY][self.__clicX].getPlayer() == self.__joueurEnCour

    def dispertion(self,x,y):
        corneur =((0,0),(0,self.__ligne-1),(self.__colone-1,0),(self.__colone-1,self.__ligne-1))
        coteX = (0,self.__colone-1)
        coteY = (0,self.__ligne-1)
        co = x,y
        pion = self.__grille[y][x].getPion()
        if co in corneur:
            emplacement = 1
        elif x in coteX or y in coteY:
            emplacement = 2
        else:
            emplacement = 3
        if (pion >= 2 and emplacement==1) or (pion >= 3 and emplacement == 2) or (pion >= 4 and emplacement == 3):
            self.__division = True
            # set les corneurs
            if x == 0:
                    piontVariable = self.__grille[y][x+1].getPion()
                    self.__grille[y][x+1].setPion(piontVariable+1)
                    self.__grille[y][x+1].setPlayer(self.__joueurEnCour)
                
            if x == self.__colone-1:
                    piontVariable = self.__grille[y][x-1].getPion()
                    self.__grille[y][x-1].setPion(piontVariable+1)
                    self.__grille[y][x-1].setPlayer(self.__joueurEnCour)
            if y == 0:
                    piontVariable = self.__grille[y+1][x].getPion()
                    self.__grille[y+1][x].setPion(piontVariable+1)
                    self.__grille[y+1][x].setPlayer(self.__joueurEnCour)
            if y == self.__ligne-1:
                    piontVariable = self.__grille[y-1][x].getPion()
                    self.__grille[y-1][x].setPion(piontVariable+1)
                    self.__grille[y-1][x].setPlayer(self.__joueurEnCour)
            # set les cotes
            if (x == 0 or x== self.__colone-1) and emplacement == 2:
                piontVariable = self.__grille[y+1][x].getPion()
                self.__grille[y+1][x].setPion(piontVariable+1)
                self.__grille[y+1][x].setPlayer(self.__joueurEnCour)
                piontVariable = self.__grille[y-1][x].getPion()
                self.__grille[y-1][x].setPion(piontVariable+1)
                self.__grille[y-1][x].setPlayer(self.__joueurEnCour)
            elif (y == 0 or y== self.__ligne-1) and emplacement == 2:
                piontVariable = self.__grille[y][x+1].getPion()
                self.__grille[y][x+1].setPion(piontVariable+1)
                self.__grille[y][x+1].setPlayer(self.__joueurEnCour)
                piontVariable = self.__grille[y][x-1].getPion()
                self.__grille[y][x-1].setPion(piontVariable+1)
                self.__grille[y][x-1].setPlayer(self.__joueurEnCour)
            # set le millieu et enleve le nombre de pion dans les cases
            if emplacement == 3:
                piontVariable = self.__grille[y+1][x].getPion()
                self.__grille[y+1][x].setPion(piontVariable+1)
                self.__grille[y+1][x].setPlayer(self.__joueurEnCour)
                piontVariable = self.__grille[y-1][x].getPion()
                self.__grille[y-1][x].setPion(piontVariable+1)
                self.__grille[y-1][x].setPlayer(self.__joueurEnCour)
                piontVariable = self.__grille[y][x+1].getPion()
                self.__grille[y][x+1].setPion(piontVariable+1)
                self.__grille[y][x+1].setPlayer(self.__joueurEnCour)
                piontVariable = self.__grille[y][x-1].getPion()
                self.__grille[y][x-1].setPion(piontVariable+1)
                self.__grille[y][x-1].setPlayer(self.__joueurEnCour)
                piontVariable = self.__grille[y][x].getPion()
                self.__grille[y][x].setPion(piontVariable-4)
            elif emplacement == 2:
                piontVariable = self.__grille[y][x].getPion()
                self.__grille[y][x].setPion(piontVariable-3)
            else:
                piontVariable = self.__grille[y][x].getPion()
                self.__grille[y][x].setPion(piontVariable-2)

    def prochainJoueur(self):
        if self.__joueurRestant.index(self.__joueurEnCour)+1 == len(self.__joueurRestant):
            self.__joueurEnCour = self.__joueurRestant[0]
            self.__tours+=1
        else:
            self.__joueurEnCour = self.__joueurRestant[self.__joueurRestant.index(self.__joueurEnCour)+1]
        
    def eliminate(self,k):
        if self.__tours > 1:
            for i in range(self.__ligne):
                for j in range(self.__colone):
                        if self.__grille[i][j].getPlayer() == self.__joueurRestant[k]:
                            return True
            return False
        else: return True

    def addPion(self):
        pionVariable = self.__grille[self.__clicY][self.__clicX].getPion()+1
        self.__grille[self.__clicY][self.__clicX].setPion(pionVariable)
        self.__grille[self.__clicY][self.__clicX].setPlayer(self.__joueurEnCour)

    def lireSauvegarde(self):
        save = Path(__file__).parent / "save.txt"
        conditionFichier = False
        try:
            open(save,'r')
            conditionFichier = True
        except:
            conditionFichier = False
        if conditionFichier == True:
            save=open(save,'r')
            content = save.readlines()
            varGrille = (content[0])
            self.__ligne = int(content[1])
            self.__colone = int(content[2])
            self.__joueur = int(content[3])
            self.__tours = int(content[4])
            self.__joueurRestant = eval(content[5])
            self.__joueurEnCour = int(content[6])
            save.close()
            a,b=0,1
            self.__grille=[]
            for j in range(self.__ligne):
                self.__grille.append([])
            for j in range(self.__colone):
                for i in range(self.__ligne):
                    self.__grille[i].append(case(eval(varGrille[a]),eval(varGrille[b])))
                    a+=2
                    b+=2
            self.__parametre.destroy()
            self.lancementJeu()
        else:
            self.verifSaveOk.pack()


    def sauvegarde(self):
        save = Path(__file__).parent / "save.txt"
        conditionFichier = False
        try:
            open(save,'w')
            conditionFichier = True
        except:
            conditionFichier = False
        
        if conditionFichier == True:
            save=open(save,'w')
            for i in range(self.__colone):
                    for j in range(self.__ligne):
                        save.write(f"{self.__grille[j][i].getPion()}{self.__grille[j][i].getPlayer()}")
            save.write(f"\n{self.__ligne}\n{self.__colone}\n{self.__joueur}\n{self.__tours}\n{self.__joueurRestant}\n{self.__joueurEnCour}")

            save.close()
    
jeu()