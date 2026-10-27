
from collections import defaultdict
import heapq

n = int(input("Enter number of modules: "))
m = int(input("Enter number of dependencies: "))

graph = defaultdict(set)
indegree = defaultdict(int)
modules = set()

print("Enter dependencies (A B means A depends on B):")

for _ in range(m):
    a, b = input().split()
    modules.update([a, b])

    # B must load before A
    if b not in graph[a]:
        graph[b].add(a)
        indegree[a] += 1

for module in modules:
    indegree[module] += 0

# Lexicographically smallest topological order
heap = []

for module in modules:
    if indegree[module] == 0:
        heapq.heappush(heap, module)

order = []

while heap:
    u = heapq.heappop(heap)
    order.append(u)

    for v in graph[u]:
        indegree[v] -= 1
        if indegree[v] == 0:
            heapq.heappush(heap, v)

if len(order) == len(modules):
    print("Loading order:", *order)
else:
    # Find one cycle using DFS
    visited = set()
    active = set()
    path = []
    cycle = []

    def dfs(u):
        global cycle

        visited.add(u)
        active.add(u)
        path.append(u)

        for v in graph[u]:
            if v not in visited:
                if dfs(v):
                    return True
            elif v in active:
                i = path.index(v)
                cycle.extend(path[i:] + [v])
                return True

        path.pop()
        active.remove(u)
        return False

    for module in sorted(modules):
        if module not in visited:
            if dfs(module):
                break

    print("CYCLE", *cycle)
