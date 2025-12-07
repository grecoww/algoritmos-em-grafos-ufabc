#Como rodar para um exemplo?
#R: python park.py < examples/example1.txt

#dado o enunciado do problema, podemos entender que claramente se trata de um problema de achar
#as n-1 arestas (dentre as arestas validas dadas) que minimizem um custo e abranja todos os vertices do dado grafo
#e justamente isso eh o problema da minimum spanning tree (arvore minima geradora)
#sabemos que sao n-1 arestas, pois esse eh o minimo de arestas necessarias para conectar todos os vertices do grafo
#e sera necessariamente uma arvore

from collections import namedtuple
from typing import List
from collections import deque
Edge = namedtuple("Edge", ["v", "cost"])

def bfsAndLabel(F: List[List[Edge]], vertex: int, count: int, visited: List[bool], comp: List[int]):
    q = deque([vertex])
    visited[vertex] = True
    comp[vertex] = count

    while q:
        u = q.popleft()

        for v, _ in F[u]:
            if not visited[v]:
                visited[v] = True
                comp[v] = count
                q.append(v)

def countAndLabel(n: int, F: List[List[Edge]], comp):
    count = 0
    visited = [False for _ in range(n+1)]
    for v in range(1, n+1):
        if not visited[v]:
            count+= 1 # mesma coisa dos vertices, o primeiro componente comeca em 1 e nao 0 !!!
            #visitar e rotular todos os vertices de um componente:
            bfsAndLabel(F, v, count, visited, comp)
    return count

def addSafeEdges(n, F, G, comp, count):
    safe = [(0,0,float('inf')) for _ in range(count+1)]
        #precisamos encontrar os 'safe edges' e adicionar em F
    for u in range(1, n+1):
        for v, cost in G[u]:
            if comp[u] != comp[v] and cost < safe[comp[u]][2]:
                safe[comp[u]] = (u,v,cost)
    
    for index, (u,v,cost) in enumerate(safe):
        if index == 0 or (u,v,cost) == (0,0,float('inf')) or (v,cost) in F[u]: continue
        F[u].append((v,cost))

#Variacao do Boruvka
def minimumSpanningTree(n: int, G: List[List[Edge]]):
    comp = [-1 for _ in range(n+1)] #lista que fornece qual componente cada vertice faz parte (-1 para nenhum componente ainda)
    F = [[] for _ in range(n+1)]                    #grafo auxiliar que vai permitir expandir para a arvore geradora minima
                                                  #invariante: F sempre sera um subgrafo da arvore geradora minima de G
    count = countAndLabel(n, F, comp)

    while count != 1:
        #achamos os 'safe edges' e juntamos os componentes, oq criará componentes maiores, até uma hora ter apenas um (count = 1)
        addSafeEdges(n, F, G, comp, count)
        #contamos para ver quantos componentes temos depois da adicao
        count = countAndLabel(n, F, comp)

    totalCost = 0
    seen = set() #algumas arestas saem duplicadas e outras nao, devido a escolha do algoritmo, entao eh preciso lidar com esse caso
    for u in range(1, n+1):
        for v, cost in F[u]:
            if {u,v} not in seen:
                totalCost+=cost
            seen.add(frozenset({u,v}))

    return totalCost



MAINcount=1
while(True):
    #leitura de n e m
    dimensions = [int(x) for x in input().split()]
    if dimensions[0] == 0:
        break
    n, m = dimensions
    maxEdges = (n*(n-1))/2
    if not ( 0<n and 0<=m<=maxEdges): #checando os boundaries do problema para cada variavel
        raise ValueError("invalid value interval for n or m")

    #cria a lista de adjacencia com n vertices (obs: aqui optei por ignorar o indice 0 ja que os vertices comecam no 1)!!!
    adjList = [[] for _ in range(n+1)]

    #leitura das arestas
    for i in range(m):
        x,y,c = map(int, input().split())
        if not (1<=x<=n and 1<=y<=n and 0<=c and x!=y):
            raise ValueError("invalid value interval for x or y or c")
        
        #adiciona a aresta na lista de adj
        adjList[x].append(Edge(y,c))
        adjList[y].append(Edge(x,c))

    result = -1 if m < n-1 else minimumSpanningTree(n, adjList)
    print(f"Cenário {MAINcount}: {result}")

    MAINcount+=1

# analise de tempo:
#  Analisando de fora pra dentro:
#  O nosso algoritmo comeca com |V| componentes e a cada iteracao mais externa cada componente se junta a outro
#  no pior caso, cada componente se junta em forma de pares disjuntos (o que diminui na metade o numero de componentes a cada iteracao) (O(logV))
#  Agora tratando dos processamentos internos:
#  para o grafo F, sabemos que max|E(F)| = |V-1| (pela definicao de floresta), dessa forma o modulo countAndLabel - que opera apenas sobre F - eh O(V)
#  para o grafo G, as propriedades sao as usuais, e como varremos toda a lista de adjacencia G, temos O(V+E) para addSafeEdges
#  Alem de tudo isso, sabemos que |E(G)|>= |V-1|, portanto: O(V+E) = O(E)  
#  Finalmente, tudo isso nos leva a concluir que o algoritmo todo leva O(ElogV) de complexidade de tempo total.