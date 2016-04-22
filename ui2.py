#!/usr/bin/python
# -*- coding: utf-8 -*-

from tkinter import *
from numpy import *
import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt

REFRESH_TIME = 10
OFFSET_X =200
OFFSET_Y = 200
MULTIPLIER = 100

class UI:
    def __init__(self):
        self.resoudre()
        self.plot_moi()

        self.init_ui()
        self.sprite_iss = self.canvas.create_oval(0,0,0,0, fill="green")
        self.sprite_shuttle = self.canvas.create_oval(0,0,0,0, fill="red")

        # elf.canvas.delete(self.sprite)

        self.root.after(1, self.my_loop)
        self.root.mainloop()

    def resoudre(self):
        #DEBUT =======================================
        #################################################
        ## CONFIG #######################################
        #################################################
        pi = 3.1415926

        T = 1
        w = (2*pi)/T                            #oméga

        e = 0.001
        rho = 0.03
        pas = 0.005                             #pas pour Euler, en seconde
        nb_boucle = 100

        Tmax = 1*T
        nb_pas = int(Tmax/pas)                  #nombre de pas pour arriver a Tmax
        self.nb_pas = nb_pas
        i_max = nb_pas-1                        #index max du temps

        x_depart = 0.1                            #x1 de départ
        ###################################################

        #initialisations
        A = matrix([[0, 1, 0, 0],
                    [3*w**2, 0, 0, 2*w],
                    [0, 0, 0, 1],
                    [0, -2*w, 0, 0]])
        At = np.transpose(A)

        B = matrix([[0, 0],
                    [1, 0],
                    [0, 0],
                    [0, 1]])
        Bt = np.transpose(B)

        x0 = matrix([[x_depart],
                    [0],
                    [0],
                    [0]])

        #x au cour du temps
        x = [matrix([[0],
                     [0]])
            for i in range(nb_pas)
            ]

        #x prime au cour du temps
        xp = [matrix([[0],
                     [0]])
            for i in range(nb_pas)
            ]

        #u au cour du temps
        u = [matrix([[0],
                     [0]])
            for i in range(nb_pas)
            ]

        #u(n+1) au cour du temps (pour étape 4)
        u2 = [matrix([[0],
                     [0]])
            for i in range(nb_pas)
            ]

        #p au cour du temps
        p = [matrix([[0],
                     [0]])
            for i in range(nb_pas)
            ]

        #grad(J(u)) au cour du temps (pour étape 3)
        gradJu = [matrix([[0],
                      [0]])
              for i in range(nb_pas)
             ]

        # METHODE ==========================================================================
        for k in range(nb_boucle):
            print("Itération " + str(k))
            #initialisations
            #print("ETAPE 1") #=============================================
            x[0] = x0
            for i in range(nb_pas):
                xp = np.dot(A, x[i]) + np.dot(B, u[i])  #dérivée au point x
                x2 = x[i] + xp * pas/2                  #x+1/2 (x intermédiaire)
                xp2 = np.dot(A, x2) + np.dot(B, u[i])   #dérivée au point x+1/2

                if(i != nb_pas-1):    # pour la derniere itération, on ne calcule pas ca :
                    x[i+1] = x[i] + pas * xp2

            #print("ETAPE 2") #=============================================
            p[i_max] = deepcopy(x[i_max])

            i = i_max
            while i >= 0:
                pp = - np.dot(At, p[i])
                p2 = p[i] - pp * pas/2
                pp2 = - np.dot(At, p2)

                if i != 0:  #pour la dernière itération, on fait pas ca :
                    p[i-1] = p[i] - pas * pp2
                i = i - 1

            #print("ETAPE 3") #=============================================
            for i in range(nb_pas):
                gradJu[i] = e*u[i] + np.dot(Bt, p[i])

            #print("ETAPE 4") #=============================================
            for i in range(nb_pas):
                u[i] = u[i] - rho*gradJu[i]

        # changement de base ===============================================================
        print("Changement de coordonnées")
        #x dans la base de la terre
        self.x_mieux = [0 for i in range(nb_pas)]
        self.y_mieux = [0 for i in range(nb_pas)]
        self.x_iss = [0 for i in range(nb_pas)]
        self.y_iss = [0 for i in range(nb_pas)]

        for i in range(nb_pas):
            x1 = float(x[i][0][0])
            x2 = float(x[i][2][0])
            self.x_mieux[i] = x1*cos(w*i*pas) - x2*sin(w*i*pas) + cos(w*i*pas)
            self.y_mieux[i] = x1*sin(w*i*pas) - x2*cos(w*i*pas) + sin(w*i*pas)
            self.x_iss[i] = cos(w*i*pas)
            self.y_iss[i] = sin(w*i*pas)

    def my_loop(self):
        time = self.slider.get()
        self.show_iss_at(
            OFFSET_X + self.x_iss[time]*MULTIPLIER,
            OFFSET_Y + self.y_iss[time]*MULTIPLIER)
        self.show_shuttle_at(
            OFFSET_X + self.x_mieux[time]*MULTIPLIER,
            OFFSET_Y + self.y_mieux[time]*MULTIPLIER)

        self.root.after(REFRESH_TIME, self.my_loop)

    def show_iss_at(self, x, y):
        self.canvas.delete(self.sprite_iss)
        self.sprite_iss = self.canvas.create_oval(x-3, y-3, x+3, y+3, fill="green")

    def show_shuttle_at(self, x, y):
        self.canvas.delete(self.sprite_shuttle)
        self.sprite_shuttle = self.canvas.create_oval(x-3, y-3, x+3, y+3, fill="red")

    def init_ui(self):
        self.root = Tk()

        self.canvas = Canvas(self.root, width=600, height=600, background='white')
        self.canvas.pack(side="top")

        self.quit_button = Button(self.root, text="QUIT", fg="red", command=exit)
        self.quit_button.pack()

        self.slider = Scale(self.root, from_=0, to=self.nb_pas-1, orient=HORIZONTAL)
        self.slider.pack()

    def plot_moi(self):
        fig = plt.figure()

        plt.plot(self.x_mieux, self.y_mieux, "r",
                 self.x_iss, self.y_iss, "g")
        plt.xlabel("x")
        plt.ylabel("y")

        plt.show()


my_ui = UI()