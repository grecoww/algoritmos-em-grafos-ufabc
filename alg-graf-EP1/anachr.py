# Como executar o codigo com um arquivo de exemplo?
# python3 anachr.py < examples/example1.txt 

from collections import namedtuple
from typing import List
Edge = namedtuple("Edge", ["v", "dist", "time"])

def constrainedBellman(n: int, adjList: List[List[Edge]], src: int, target: int, h: int):
    dp = [[float("inf")]*(n+1) for _ in range(h+1)]
    dp[0][src] = 0

    for t in range(1,h+1):

        for v in range(1, n+1):
            #comecamos com o valor da iteracao anterior (sem usar nenhuma aresta nova)
            dp[t][v] = dp[t-1][v]

        for u in range(1, n+1):
            for v, dist, time in adjList[u]:
                if time <= t:
                    # a nova recursao pode ser definida como ao inves de considerar o numero k de arestas, considerar o tempo gasto
                    # antes: dp[k][v] = min(dp[k-1][v], min(u->v)(dp[k-1][u] + dist(u,v)))
                    # depois (adaptando para o tempo gasto): dp[t][v] = min(dp[t-1][v], min(u->v)(dp[t-time][u] + dist(u,v)))
                    # alem disso defininmos dp[t][v] = inf caso t<0, e isso acontece quando time(v) > t
                    if dp[t-time][u]+dist < dp[t][v]:
                        dp[t][v] = dp[t-time][u]+dist
    
    # Melhor custo para target com tempo <= h
    bestDist = dp[h][target]
    bestTime = 0
    for t in range(1,h+1):
        if dp[t][target] == bestDist:
            bestTime = t
            break

    if bestDist == float("inf"):
        print("Impossivel")
    else:
        print(f"Possivel - {bestDist} km, {bestTime} min")  

count=1
while(True):
    #leitura das dimensoes n e m
    n, m = map(int, input().split())
    if not (0<=n<=100 and 0<=m<=10000 and m<=n*(n-1)): #tambem checando se m <= max_edges(n)
        raise ValueError("invalid value interval for n or m")
    if n==0:
        break

    #cria a lista de adjacencia com n vertices (obs: aqui optei por ignorar o indice 0 ja que os vertices comecam no 1)
    adjList = [[] for _ in range(n+1)]

    #leitura das arestas
    for i in range(m):
        x,y,c,t = map(int, input().split())
        if not (1<=x<=n and 1<=y<=n and 0<=c and 0<=t):
            raise ValueError("invalid value interval for x or y or c or t")
        
        #adiciona a aresta na lista de adj
        adjList[x].append(Edge(y,c,t))
        
    
    #leitura das entregas
    k = int(input())
    if not k>=0:
        raise ValueError("invalid value interval for k")
    
    print(f"Instancia {count}")
    for i in range(k):
        x,y,h = map(int, input().split())
        if not (1<=x<=n and 1<=y<=n and 0<=h<=6000):
            raise ValueError("invalid value interval for x or y or h")
        print(BFS(adjList, x))

    count+=1

# analise de tempo:
#  por conta das restricoes de valores impostas pelo exercicio:
#   n<<h
#   n<<m
#  portanto:
#   O(h(n+m))≈O(hm)