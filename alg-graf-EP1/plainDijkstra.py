from collections import namedtuple
from typing import List
from heapq import heappop, heappush

Edge = namedtuple("Edge", ["v", "dist", "time"])

## minha primeira implementacao do algoritmo de dijkstra!!! (engracado que a primeira vez que a programei foi pra ser usada em uma versao derivada mais complexa, no caso a constrainedDijkstra)
def dijkstra(n: int, adjList: List[List[Edge]], src: int, target: int, h: int):
    dist_so_far = [float('inf')]*(n+1)
    dist_so_far[src] = 0
    visited = [False]*(n+1)
    pred = [None]*(n+1)

    queue = [(dist_so_far[src], src)]

    while (queue):
        _, u = heappop(queue)
        if u == target: break
        if visited[u]: continue
        visited[u] = True
        for v, dist, time in adjList[u]:
            if dist_so_far[u]+dist < dist_so_far[v]:
                dist_so_far[v] = dist_so_far[u]+dist
                pred[v] = u
                heappush(queue, (dist_so_far[v], v))