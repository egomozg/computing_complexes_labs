class Edge:
    def __init__(self, start_node, end_node):
        self.start_node = start_node
        self.end_node = end_node

    def get_start_node(self):
        return self.start_node

    def get_end_node(self):
        return self.end_node

def count_branches(edges):
    # Список множеств узлов, представляющих ветви
    branches = []

    for edge in edges:
        start_node = edge.get_start_node()
        end_node = edge.get_end_node()

        # Проверяем, пересекается ли ребро с каким-либо из существующих множеств узлов
        intersected_branch = None
        for branch in branches:
            if start_node in branch or end_node in branch:
                intersected_branch = branch
                break

        if intersected_branch is not None:
            # Обновляем множество узлов для пересекающейся ветви
            intersected_branch.add(start_node)
            intersected_branch.add(end_node)
        else:
            # Добавляем новое множество узлов для новой ветви
            branches.append(set([start_node, end_node]))

    # Количество ветвей равно количеству множеств узлов в списке
    return len(branches)

# Пример использования
# edges = [Edge(1, 2), Edge(2, 3), Edge(3, 4), Edge(4, 1)]
edges = [Edge(1, 2), Edge(2, 3), Edge(3, 4), Edge(4, 1), Edge(5, 6), Edge(6, 7), Edge(7, 8), Edge(8, 5)]
print(count_branches(edges))  # Вывод: 3