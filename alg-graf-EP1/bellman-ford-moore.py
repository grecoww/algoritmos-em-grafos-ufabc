def bellman_ford_moore(n: int, adjList: List[List[Edge]], src: int, target: int, h: int):
    dist_so_far = [float("inf")] * (n+1)
    dist_so_far[src] = 0

    for _ in range(n-1):
        for u in range(1, n+1):
            for v, dist, time in adjList[u]:
                if dist_so_far[u]+dist < dist_so_far[v]:
                    dist_so_far[v] = dist_so_far[u]+dist
    
    print(dist_so_far)

# meu primeiro bellman-ford-moore (!!!)