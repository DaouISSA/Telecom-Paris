# include <stdio.h>
# include <stdlib.h>
# include <string.h>
# include <unistd.h>
# include <sys/types.h>
# include <sys/wait.h>
# include <sys/stat.h>


# define MAX 5
int data[MAX];
int t=-1;

void op1(int x){
    if(t<MAX-1){
    
        data[++t]=x;
    }
    else{
        printf("Pile pleine\n");
    }
}
int op2(){
    if(t==-1){
        printf("Pile vide\n");
        return -1;
    }
    else{
        return data[--t];
    }
}

void main() {
    op1(20);
    op1(30);
    printf("%d\n",op2());
    return 0
}

