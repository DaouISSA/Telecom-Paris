def fonct(S,x):
    i=0
    j=len(S)-1
    while i<=j:
        if S[i]+S[j]==x:
            return True
        elif S[i]+S[j]<x:
            i+=1
        else:
            j-=1
    return False

S=[4,5,6,7,8,9,10]
x=4
#print(fonct(S,x))
def f2(x,y):
    if x==0 or y==0:
        return 0
    elif x==1:
        return f2(x,y-1)
    else:
        return f2(x-1,y)
#print(f2(12,4))

def f3(x,y):
    if x==y:
        return 0
    else:
        return 1+f3(x+1,y+2)
def f4(x,y):
    if x<y:
        return x
    else:
        return f4(f3(x,y),y)
def f5(x,y):
    if y==0:
        return 0
    else:
        return f5(y,f4(x,y))
print(f5(100,20))
