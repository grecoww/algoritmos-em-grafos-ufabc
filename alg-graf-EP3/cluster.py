    # Como executar o codigo com um arquivo de exemplo?
    # python3 cluster.py < examples/example1.txt 

from collections import deque
from math import ceil, floor

SCALE = 1000


def add_edge(graph, u, v, cap):
    graph[u].append([v, cap, len(graph[v])])
    graph[v].append([u, 0, len(graph[u]) - 1])


def edmonds_karp(graph, s, t):
    n = len(graph)
    flow = 0

    while True:
        parent = [None] * n
        parent[s] = (-1, -1)
        q = deque([s])

        while q and parent[t] is None:
            u = q.popleft()
            for i, (v, cap, _) in enumerate(graph[u]):
                if cap > 0 and parent[v] is None:
                    parent[v] = (u, i)
                    q.append(v)

        if parent[t] is None:
            break

        # gargalo
        inc = float("inf")
        v = t
        while v != s:
            u, ei = parent[v]
            inc = min(inc, graph[u][ei][1])
            v = u

        # atualiza fluxo
        v = t
        while v != s:
            u, ei = parent[v]
            rev = graph[u][ei][2]

            graph[u][ei][1] -= inc
            graph[v][rev][1] += inc
            v = u

        flow += inc

    return flow


def viableSchedule(machines, tasks):
    n = len(tasks)

    # coleta eventos
    events = set()
    for p, r, d in tasks:
        events.add(r)
        events.add(d)

    events = sorted(events)
    intervals = [(events[i], events[i + 1]) for i in range(len(events) - 1)]

    k = len(intervals)

    S = 0
    T = 1 + n + k
    graph = [[] for _ in range(T + 1)]

    total_work = 0

    # fonte -> tarefas
    for i, (p, _, _) in enumerate(tasks):
        work = ceil(p * SCALE) # arredonda pra cima
        total_work += work
        add_edge(graph, S, 1 + i, work)

    # tarefas -> intervalos
    for i, (_, r, d) in enumerate(tasks):
        for j, (a, b) in enumerate(intervals):
            if a >= r and b <= d:
                dur = floor((b - a) * SCALE)
                if dur > 0:
                    add_edge(graph, 1 + i, 1 + n + j, dur)

    # intervalos -> sorvedouro
    for j, (a, b) in enumerate(intervals):
        dur = floor((b - a) * SCALE) # arredonda pra baixo
        add_edge(graph, 1 + n + j, T, machines * dur)

    flow = edmonds_karp(graph, S, T)
    return flow == total_work


count=1
while(True):
    m,n = map(int, input().split())
    if not (0<=m<=100 and 0<=n<=1000):
        raise ValueError("invalid value interval for n or m")
    if m==0 and n==0:
        break

    tasks = []

    for _ in range(n):
        p,r,d = input().split()
        p = float(p)
        r = int(r)
        d = int(d)
        if not (p>= 0 and r>=0 and d>=0):
            raise ValueError("invalid value interval for x or y or c or t")
        tasks.append((p, r, d))

    print(f"Instancia {count}")
    if viableSchedule(m, tasks):
        print("Viavel")
    else:
        print("Inviavel")    
    print()

    count+=1

# analise de tempo:
#
# n -> numero de tarefas e k -> nuumero de intervalos
# Temos k <= 2n - 1
#
# numero de nos:
# V = n + k + 2 = O(n)
#
# numero de arestas:
# - fonte -> tarefas: n
# - tarefas -> intervalos: até n*k = O(n^2)
# - intervalos -> sorvedouro: k
# Logo, E = O(n^2)
#
# O algoritmo de Edmonds-Karp roda em O(V * E^2),
# portanto:
#
# O(n * (n^2)^2) = O(n^5)
#
# Para n <= 100, o algoritmo eh viável, mas não escala bem.