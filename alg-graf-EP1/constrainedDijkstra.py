#porque usei o lazy dijkstra (sem decrease-key)?: https://stackoverflow.com/a/18540646
def constrainedDijkstra(n: int, adjList: List[List[Edge]], src: int, target: int, h: int):
    dist_so_far = [float('inf')]*(n+1)
    time_so_far = [float('inf')]*(n+1)
    dist_so_far[src] = 0
    time_so_far[src] = 0

    visited = [False]*(n+1)

    queue = [(dist_so_far[src], time_so_far[src], src)]

    while (queue):
        _, _, u = heappop(queue)
        if u == target: break
        if visited[u]: continue
        visited[u] = True
        for v, dist, time in adjList[u]:
            if dist_so_far[u]+dist < dist_so_far[v] and time_so_far[u]+time <= h:
                dist_so_far[v] = dist_so_far[u]+dist
                time_so_far[v] = time_so_far[u]+time
                heappush(queue, (dist_so_far[v], time_so_far[v], v))

    if dist_so_far[target] == float('inf'):
        print("Impossivel")
        return

    print(f"Possivel - {dist_so_far[target]} km, {time_so_far[target]} min")