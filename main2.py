#!/usr/bin/python
# -*- coding: utf-8 -*-

from numpy import matrix
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy

# w=int(input("Rentrer la valeur de w : "))

# #x = matrix(str(x)+' '+str(dx)+' '+str(y)+' '+str(dy))
# #u = matrix(str(ux)+' '+str(uy))

# A = matrix('0 1 0 0; '+str(3*w*w)+' 0 0 '+str(2*w)+'; 0 0 0 1; 0 '+str(-2*w)+' 0 0')
# B = matrix('0 1 0 0; 0 0 0 1')

# print (A[3, 1])
# print (A)
# print (B)


#DEBUT =======================================
#configuration du problème
pi = 3.1415926
T = 5480                                #T
pas = 1                                 #pas pour Euler, en seconde
nb_pas = int(T/pas)                     #nombre de pas pour arriver a T
i_max = nb_pas-1                        #index max du temps
w = (2*pi)/T                            #oméga
e = 0.001
rho = 0.03

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

x0 = matrix([[1],
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

#initialisations
print("ETAPE 1\n") #=============================================
x[0] = x0
for i in range(nb_pas):
    xp[i] = np.dot(A, x[i]) + np.dot(B, u[i])

    if(i != nb_pas-1):    # pour la derniere itération, on ne calcule pas ca :
        x[i+1] = x[i] + pas * xp[i]

print("ETAPE 2\n") #=============================================
p[i_max] = deepcopy(x[i_max])

i = i_max
while i >= 0:
    pp[i] = - np.dot(At, p[i])
    if i != 0:  #pour la dernière itération, on fait pas ca :
        p[i-1] = p[i] - pas * pp[i]
    i = i - 1

print("ETAPE 3\n") #=============================================
for i in range(nb_pas):
    gradJu[i] = e*u[i] + np.dot(Bt, p[i])

print("ETAPE 4\n") #=============================================
for i in range(nb_pas):
    u2[i] = u[i] - rho*gradJu[i]

print("Preparation de l'itération suivante") #===================
u = deepcopy(u2)


print("PLOT\n");

fig = plt.figure()

#plot étape1
plt.plot(
   [float(x[i][0][0]) for i in range(nb_pas)],
   [float(x[i][2][0]) for i in range(nb_pas)]
)
plt.xlabel("x de x")
plt.ylabel("y de x")

plt.show()

#plot étape2
plt.plot(
   [float(p[i][1][0]) for i in range(nb_pas)],
   [float(p[i][3][0]) for i in range(nb_pas)]
)
plt.xlabel("x de p")
plt.ylabel("y de p")

plt.show()

#plot étape3
plt.plot(
   [float(gradJu[i][0][0]) for i in range(nb_pas)],
   [float(gradJu[i][1][0]) for i in range(nb_pas)]
)
plt.xlabel("x de gradJu")
plt.ylabel("y de gradJu")

plt.show()

#plot étape4
plt.plot(
   [float(u2[i][0][0]) for i in range(nb_pas)],
   [float(u2[i][1][0]) for i in range(nb_pas)]
)
plt.xlabel("x de u2")
plt.ylabel("y de u2")

plt.show()