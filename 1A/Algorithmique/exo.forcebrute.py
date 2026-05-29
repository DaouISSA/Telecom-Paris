def f(s,p):
    n=len(s)
    m=len(p)
    for i in range(n-m+1):
        j=0
        while j<m and s[i+j]==p[j] :
            j+=1
        if j==m:
            return i
    return -1
s="abracadabra"
p="cadr"
print(f(s,p))