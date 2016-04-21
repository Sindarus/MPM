#!/usr/bin/python
# -*- coding: utf-8 -*-

from numpy import matrix, cos, sin
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy

#DEBUT =======================================
#configuration du problème
pi = 3.1415926

T = 1
w = (2*pi)/T                            #oméga

e = 0.001
rho = 0.03
pas = 0.005                             #pas pour Euler, en seconde
nb_boucle = 100

Tmax = 1*T
nb_pas = int(Tmax/pas)                  #nombre de pas pour arriver a Tmax
i_max = nb_pas-1                        #index max du temps

x_depart = 0.1                            #x1 de départ



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

#p au cour du temps (pour étape 2)
p = [matrix([[0],
             [0]])
    for i in range(nb_pas)
    ]

#p prime au cour du temps  (pour étape 2)
pp = [matrix([[0],
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
        xp[i] = np.dot(A, x[i]) + np.dot(B, u[i])

        if(i != nb_pas-1):    # pour la derniere itération, on ne calcule pas ca :
            x[i+1] = x[i] + pas * xp[i]

    #print("ETAPE 2") #=============================================
    p[i_max] = deepcopy(x[i_max])

    i = i_max
    while i >= 0:
        pp[i] = - np.dot(At, p[i])
        if i != 0:  #pour la dernière itération, on fait pas ca :
            p[i-1] = p[i] - pas * pp[i]
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
x_mieux = [0 for i in range(nb_pas)]
y_mieux = [0 for i in range(nb_pas)]
x_iss = [0 for i in range(nb_pas)]
y_iss = [0 for i in range(nb_pas)]

for i in range(nb_pas):
    x1 = float(x[i][0][0])
    x2 = float(x[i][2][0])
    x_mieux[i] = x1*cos(w*i*pas) - x2*sin(w*i*pas) + cos(w*i*pas)
    y_mieux[i] = x1*sin(w*i*pas) - x2*cos(w*i*pas) + sin(w*i*pas)
    x_iss[i] = cos(w*i*pas)
    y_iss[i] = sin(w*i*pas)

# PLOT ============================================================================
print("PLOT\n");

fig = plt.figure()

plt.plot(
   x_mieux,
   y_mieux,
   "r",
   x_iss,
   y_iss,
   "g"
)
plt.xlabel("x")
plt.ylabel("y")

plt.show()