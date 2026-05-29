import numpy as np
import matplotlib.pyplot as plt


#%%
path='C:/Users/daoui/OneDrive/Documents/Télécom Paris/Climat'
filename = path+'/data_tp5.csv'


temperature = []
solar= []
magnet= []

A=np.loadtxt(filename)
A=A.transpose()

temperature=A[0]
solar=A[1]
magnet=A[2]

index_t=np.arange(1900,2001)


#%%
plt.plot(index_t,temperature,'r-+', label="Temp�rature")
plt.plot(index_t,solar,'k', label="Activit� solaire")
plt.plot(index_t,magnet,'k--',  label="Activit� magn�tique")
plt.title('Quelques param�tres au cours du temps')
plt.xlabel('Ann�e')
plt.ylabel('Valeurs normalis�es')
plt.legend(loc="upper left")
plt.grid()
#plt.show()
    
    
#%%
def correlation(x,y):
    xb=np.mean(x)
    yb=np.mean(y)
    xc= x-xb
    yc= y-yb
    
    aux1=np.sum(xc*yc)
    aux2= np.sum(xc*xc)
    aux3= np.sum(yc*yc)
    
    c= aux1/np.sqrt(aux2*aux3)
    return c

c= correlation(magnet,solar)
print('La corr�lation entre la temp�rature et l\'activit� solaire est de :',c)


#%%
def r_square(y,y_hat):
    yb=np.mean(y)
    
    aux1=...
    aux2=...
     
    rs=1-aux1/aux2
    return rs

#%%
def regression(x,y):
    N=len(x)
   
    aux1=np.sum(x)
    aux2=np.sum(y)
    aux3=np.sum(y*x)
    aux4=np.sum(x*x)
    
    a=...
    b=...
    return a,b

#%%
def prediction(x,a,b):
    y=...
    return y

#%% R�ponse aux questions (corr�lation)


 

#%% R�ponse aux questions (r�gression)

