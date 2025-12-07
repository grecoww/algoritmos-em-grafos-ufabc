from collections import deque
def BFS(adjList: List[List[Edge]], src: int):
    dist = [float("inf")] * len(adjList)
    dist[src] = 0
    queue = deque()
    queue.append(src)

    while queue:
        u = queue.popleft()
        print(u, dist[u])

        for v, dist_edge, _ in adjList[u]:
            if dist[v] > dist[u]+dist_edge:
                dist[v] = dist[u]+dist_edge
                queue.append(v)

    return dist