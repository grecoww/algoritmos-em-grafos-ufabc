def constrainedRecursion(s, adj, maxTime):
    n = len(adj)
    dist = [[float("inf")]*n for _ in range(maxTime+1)]
    dist[0][s] = 0
    print(dist[0], 0)

    for h in range(1, maxTime+1):
        for v in range(n):
            dist[h][v] = dist[h-1][v]

        for u in range(n):
            for v, w, time in adj[u]:
                if h-time >= 0 and dist[h][v] > dist[h-time][u]+w:
                    dist[h][v] = dist[h-time][u]+w
        print(dist[h], h)
    return dist[maxTime]

adj = {
    0: [(1, 5, 1), (2, 20, 4)],
    1: [(2, 7, 4)],
    2: []
}

print("resultado: ", constrainedRecursion(0, adj, 4))