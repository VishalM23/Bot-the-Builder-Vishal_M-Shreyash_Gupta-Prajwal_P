from random import randint
import time
def generator_util(nS, nL):
    start=time.perf_counter()
    #ladders
    
    small_ladders = int(.66*nL)
    large_ladders = nL-small_ladders
    
    ladders={}
    
    # generating small ladders
    count=0
    while(count!=nL):
        r1=randint(1,9)
        c1=randint(0,9)

        while((r1,c1)==(0,0) or (r1,c1)==(9,0) or ((r1,c1) in ladders.keys())):
            r1=randint(1,9)
            c1=randint(0,9)

        r2=randint(1,9)
        c2=randint(0,9)

        dist=abs(r1-r2) + abs(c1-c2)
        while((r1,c1)==(0,0) or (r1,c1)==(9,0) or (r1,c1)==(r2,c2) or ((r2,c2) in ladders.values()) or (r1<=r2)):
            r2=randint(1,9)
            c2=randint(0,9)
            if(time.perf_counter() - start >1):
                return;

        count+=1;
        ladders[(r1,c1)]=(r2,c2)
    count=0
    snakes={}
    while(count!=nS):
        r1=randint(1,9)
        c1=randint(0,9)

        while((r1,c1)==(0,0) or (r1,c1)==(9,0) or ((r1,c1) in snakes.keys()) or ((r1,c1) in ladders.keys())):
            r1=randint(1,9)
            c1=randint(0,9)
            if(time.perf_counter() - start >1):
                return;

        r2=randint(1,9)
        c2=randint(0,9)

        dist=abs(r1-r2) + abs(c1-c2)
        while((r1,c1)==(0,0) or (r1,c1)==(9,0) or (r1,c1)==(r2,c2) or ((r2,c2) in snakes.values()) or (r1>=r2)):
            r2=randint(1,9)
            c2=randint(0,9)
            if(time.perf_counter() - start >1):
                return;

        count+=1;
        snakes[(r1,c1)]=(r2,c2)
    return [ladders,snakes]


def SnL_generator(difficulty):
    if difficulty==1:
        nS = randint(3,5)
        nL = randint(5,10)
    elif difficulty==2:
        nS = randint(4,7)
        nL = randint(4,7)
    else:
        nS = randint(6,9)
        nL = randint(3,5)
        
    SL=generator_util(nS,nL)
    while(not SL):
        print("redoing")
        SL=generator_util(nS,nL)

    Grid = []
    for i in range(10):
        GridRow = []
        for j in range(10):
            GridRow.append("Empty")
        Grid.append(GridRow)
    Grid[0][0] = "End"
    Grid[9][0] = "Start"
    for (_key,_val) in SL[1].items():
        Grid[_key[0]][_key[1]]=[_val[0],_val[1],"S"]

    # #Ladders

    for (_key,_val) in SL[0].items():
        Grid[_key[0]][_key[1]]=[_val[0],_val[1],"L"]
    return Grid


# print(SnL_generator())