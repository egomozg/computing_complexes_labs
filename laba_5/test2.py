class Element:
    def __init__(self, start_node, end_node):
        self.start_node = start_node
        self.end_node = end_node
    
    def get_start_node(self):
        return self.start_node
    
    def get_end_node(self):
        return self.end_node

def dfs(graph, node, visited):
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)

def count_branches(elements):
    graph = {}
    removable_nodes = set()  # Множество для хранения узлов, в которые входят всего два ребра
    for element in elements:
        start_node = element.get_start_node()
        end_node = element.get_end_node()
        if start_node not in graph:
            graph[start_node] = set()
        if end_node not in graph:
            graph[end_node] = set()
        graph[start_node].add(end_node)
        graph[end_node].add(start_node)
    
    for node, neighbors in graph.items():
        if len(neighbors) == 2:
            removable_nodes.add(node)
    
    # Удаляем устраняемые узлы из графа
    for node in removable_nodes:
        for neighbor in graph[node]:
            graph[neighbor].remove(node)
        del graph[node]
    
    # Проверка на пустой граф
    start_node = next(iter(graph.keys()), None)
    if start_node is None:
        return 0  # Если граф пуст, возвращаем 0 ветвей
    
    visited = set()
    dfs(graph, start_node, visited)
    
    return len(visited)

# Пример использования:

# Создание элементов схемы
elements = [
    Element(1, 2),
    Element(2, 3),
    Element(3, 4),
    Element(4, 1),
    Element(1, 2)
]

# Определение количества ветвей
branches_count = count_branches(elements)
print("Количество ветвей в замкнутой схеме с учетом устраняемых узлов:", branches_count)
