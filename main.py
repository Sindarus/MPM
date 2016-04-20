from numpy import matrix

w=int(input("Rentrer la valeur de w : "))

#x = matrix(str(x)+' '+str(dx)+' '+str(y)+' '+str(dy))
#u = matrix(str(ux)+' '+str(uy))

A = matrix('0 1 0 0; '+str(3*w*w)+' 0 0 '+str(2*w)+'; 0 0 0 1; 0 '+str(-2*w)+' 0 0')
B = matrix('0 1 0 0; 0 0 0 1')

print (A[3, 1])
print (A)
print (B)