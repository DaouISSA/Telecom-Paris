import numpy as np
import matplotlib.pyplot as plt


a=1.5
b=0.05
c=0.5
d=0.05
h=0.1

def proie(x,y):
    return x*(a-b*y)
def predateur(x,y):
    return -y*(c-d*x)

np.random.seed(0)
x = 10
y = 10
X = [x]
Y = [y]
for i in range(1000):
    x += h*proie(x,y)
    y += h*predateur(x,y)
    X.append(x)
    Y.append(y)
plt.plot(X,Y)
plt.show()




