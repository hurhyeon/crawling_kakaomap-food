k = 4 #k는 간선의 수

graph = {}
for _ in range(k):
        x, y = map(int, input().split())
        if x not in graph.keys():
            graph[x] = set([y])
        else:
            graph[x].add(y)
        if y not in graph.keys():
            graph[y] = set([x])
        else:
            graph[y].add(x)