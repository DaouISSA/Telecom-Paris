from random import randint
import numpy as np


def grains_david(T,N,B):
    x,y=N,B
    p,q=5,3 # p pour noir et q pour blanc
    while x+y>=2:
        i=randint(0,x+y-1)
        j=randint(0,x+y-1)
        if i==j:
            continue 
        if T[i]==T[j]:
            T.remove(T[i])
            T.remove(T[j-1])
            T.append(p)
            x=x-1
            
        else:
            T.remove(p)
            y=y-1
    return(T)
    


#print(grains_david([5,5,3,3,3,3,5,3,5,5],5,5))
x= [5,8]
x.append(8)
#print(x)



#print(grains(5,5))

# 2 ième exo


def tri_tableau(T):
    n=len(T)
    if n>1:
        L= T[:n//2] 
        R= T[n//2:] 
        tri_tableau(L)
        tri_tableau(R)
        i,j,k=0,0,0
        while i<len(L) and j<len(R):
            if L[i]<R[j]:
                T[k]=L[i]
                i=i+1
                k=k+1
            else:
                T[k]=R[j]
                j=j+1
                k=k+1
        while i<len(L):
            T[k]=L[i]
            i=i+1
            k=k+1
        while j<len(R):
            T[k]=R[j]
            j=j+1
            k=k+1
    return(T)

def fct(T):

    M=[]
    C=[]
    n=len(T)
    #print(R)
    while len(T)!=0:
        for i in range(len(T)-1):
            if T[i]!=T[i+1]:
                M.append(T[i])
                M.append(T[i+1])
                T.remove(T[i])
                T.remove(T[i+1])
                
            else:
                continue
            C=M
        
    return(M,C)
print(fct([1, 8, 5, 8, 6, 5, 7]))

def f(T):
    R=T
    return(R)
#print(f([1, 8, 5, 8, 6, 5, 7]))
def tri_tableau2(T):
    n=len(T)
    if n>1:
        L= T[:n//2] 
        R= T[n//2:] 
        tri_tableau(L)
        tri_tableau(R)
    return(L,R)

#print(tri_tableau2([1, 8, 5, 8, 6, 5, 7]))




            
def multi(T):
    n=len(T)
    L=np.zeros((n))
    for i in range(n):
        for j in range(n):
            if T[i]==T[j]:
                L[i]=L[i]+1
    return(max(L)>n/2)

    def rendu_monnaie(somme, pieces):
        rendu = []
        for piece in sorted(pieces, reverse=True):
            while somme >= piece:
                somme -= piece

                rendu.append(piece)
        if somme != 0:
            raise ValueError("La somme ne peut pas être rendue avec les pièces disponibles.")
        return rendu

    # Exemple d'utilisation
    # print(rendu_monnaie(67, [1, 2, 5, 10, 20, 50]))

#print(multi([3,5,3,5,5]))
                