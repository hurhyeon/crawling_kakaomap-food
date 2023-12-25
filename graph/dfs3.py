myGraph = {
    'A': ['B'],
    'B': ['A', 'C', 'H'],
    'C': ['B', 'D'],
    'D': ['C', 'E', 'G'],
    'E': ['D', 'F'],
    'F': ['E'],
    'G': ['D'],
    'H': ['B', 'I', 'J', 'M'],
    'I': ['H'],
    'J': ['H', 'K'],
    'K': ['J', 'L'],
    'L': ['K'],
    'M': ['H']
}
def my_dfs(graph, start_node):
    visited = list() # 방문한 노드를 담을 배열
    stack = list() # 정점과 인접한 방문 예정인 노드를 담을 배열

    stack.append(start_node) # 처음에는 시작 노드 담아주고 시작하기.

    while stack: # 더 이상 방문할 노드가 없을 때까지.
        node = stack.pop() # 방문할 노드를 앞에서 부터 하나씩 꺼내기.

        if node not in visited: # 방문한 노드가 아니라면
            visited.append(node) # visited 배열에 추가
            stack.extend(graph[node]) # 해당 노드의 자식 노드로 추가
            stack.extend(reversed(graph[node])) # 왼쪽부터 탐색

    print("dfs - ", visited)
    return visited
    
my_dfs(myGraph, 'G')