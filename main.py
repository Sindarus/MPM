from numpy import matrix
import matplotlib.pyplot as plt

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
nb_pas = int(T/pas)                       #nombre de pas pour arriver a T
w = (2*pi)/T                            #oméga

#initialisations
base_de_temps = [pas * i for i in range(nb_pas)]    #liste qui vaut [0, pas, 2*pas, 3*pas, ...] utile pour plot
x0 = [1, 0]                                 #position de la navette au temps 0
xp0 = [0, 0]                                #x prime au temps 0
u = [[0, 0] for i in range(nb_pas)]        #poussée au cours du temps (on l'initialise a 0)

#résolutions
x = [[0,0] for i in range(nb_pas)]               #position de la navette au cours du temps (on met des 0 en attendant d'avoir les vraies valeurs)
xp = [[0,0] for i in range(nb_pas)]              #x prime au cours du temps
xpp = [[0,0] for i in range(nb_pas)]             #x prime prime au cours du temps

#étape 1
print("ETAPE 1\n")
x[0] = x0
xp[0] = xp0

for i in range(nb_pas):
    #on calcule xpp a l'itération i
    xpp[i] = [3 * w**2 * x[i][0] + 2*w+xp[i][1] + u[i][0]   ,
              -2 * w * xp[i][0] + u[i][1]                    ]

    if(i != nb_pas-1):    # pour la derniere itération, on ne calcule pas ca :
        #on calcule xp a l'itération i+1
        xp[i+1][0] = xp[i][0] + pas * xpp[i][0]
        xp[i+1][1] = xp[i][1] + pas * xpp[i][1]

        #on calcule x a l'itéarion i+1
        x[i+1][0] = x[i][0] + pas * xp[i][0]
        x[i+1][1] = x[i][1] + pas * xp[i][1]

print("PLOT\n");

#===============================================
print("x = " + str(x))
# print("xp = " + str(xp))
# print("xpp = " + str(xpp))

#===============================================
# x_to_print = [x[i][0] for i in range(nb_pas)]
# y_to_print = [x[i][1] for i in range(nb_pas)]
# print(x_to_print)
# print(y_to_print)

#===============================================
fig = plt.figure()

# ax1 = fig.add_subplot(311)
# plt.plot(base_de_temps, xpp)
# plt.xlabel("temps")
# plt.ylabel("xpp")

# ax2 = fig.add_subplot(312)
# plt.plot(base_de_temps, xp)
# plt.xlabel("temps")
# plt.ylabel("xp")




plt.plot(
    ( [x[i][0] for i in range(nb_pas)] ),
    ( [x[i][1] for i in range(nb_pas)] )
)
plt.xlabel("x")
plt.ylabel("y")

plt.show()