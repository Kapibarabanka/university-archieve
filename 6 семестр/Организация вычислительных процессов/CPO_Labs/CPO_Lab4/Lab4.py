import copy

class Node:
    def __init__(self, idx, weight):
        self.idx = idx
        self.weight = weight
        self.t_level = 0
        self.critical_way = []

    def __str__(self):
        return "'{0}': {2}".format(self.idx, self.weight, self.t_level)

    def __repr__(self):
        return "'{0}': {2}".format(self.idx, self.weight, self.t_level)


data = []
with open("data.txt") as f:
    for line in f:
        data.append([int(x) for x in line.split()])

matrix = data[:-1]
weights = data[-1]

temp_matrix = copy.deepcopy(matrix)
# temp_weights = copy.deepcopy(weights)
removed_nodes = []

n = len(matrix)
nodes = [Node(i, weights[i]) for i in range(n)]


def get_roots_and_ends(m: list):
    roots = []
    ends = []
    for node in nodes:
        node.critical_way = [node.idx]
        node.t_level = 0
        if node.idx in removed_nodes:
            continue
        root_flag = True
        end_flag = True
        for other_node in nodes:
            if root_flag:
                root_flag = m[other_node.idx][node.idx] == 0
            if end_flag:
                end_flag = m[node.idx][other_node.idx] == 0
        if root_flag:
            roots.append(node)
        if end_flag:
            ends.append(node)
    return roots, ends


def get_levels(m: list):
    (roots, ends) = get_roots_and_ends(m)
    levels = [roots]
    current_level = 1
    free_nodes = list(filter(lambda node: node.idx not in removed_nodes and node not in roots, nodes))
    while len(free_nodes) > 0:
        levels.append([])
        for free_node in free_nodes:
            to_current_level = False
            # if current free node doesn't connected to any node in previous level, skip it
            for prev_node in levels[current_level - 1]:
                edge_weight = m[prev_node.idx][free_node.idx]
                if edge_weight > 0:
                    to_current_level = True

            if not current_level:
                continue

            # if current free node is connected to any at current level, skip it
            for node in levels[current_level]:
                if m[free_node.idx][node.idx] > 0 or m[node.idx][free_node.idx] > 0:
                    to_current_level = False
                    break

            if to_current_level:
                levels[current_level].append(free_node)
        for assigned_node in levels[current_level]:
            free_nodes.remove(assigned_node)
        current_level += 1

    return levels


def find_critical(m: list, levels: list):
    for i in range(1, len(levels)):
        for node in levels[i]:
            for prev_node in levels[i - 1]:
                edge_weight = m[prev_node.idx][node.idx]
                if edge_weight > 0:
                    if prev_node.t_level + prev_node.weight + edge_weight > node.t_level:
                        node.t_level = prev_node.t_level + prev_node.weight + edge_weight
                        node.critical_way = list(prev_node.critical_way)
                        node.critical_way.append(node.idx)

    last_node = max(levels[-1], key=lambda nod: nod.t_level)
    return last_node.critical_way


def zero_critical(way: list):
    for i in range(1, len(way)):
        matrix[way[i-1]][way[i]] = 0
    for i in range(n):
        if i in way:
            temp_matrix[i] = [0 for j in range(n)]
        for j in way:
            temp_matrix[i][j] = 0
    removed_nodes.extend(way)


def main():
    print("Матриця зв'язності: ")
    for row in matrix:
        for e in row:
            print("{0:<4}".format(e), end='')
        print()
    print("=" * (4 * n - 3))
    print("Ваги вершин: ")
    for w in weights:
        print("{0:<4}".format(w), end='')
    print()
    print("=" * (4 * n - 3))
    while len(removed_nodes) < n:
        levels = get_levels(temp_matrix)
        critical_way = find_critical(temp_matrix, levels)

        print("Розбиття по рівням (формат запису '<номер вершини>': <її t_level>)")
        for level in levels:
            print(" | ".join(map(lambda node: "{0:<8}".format(str(node)), level)))

        print("Критичний шлях:")
        print(" -> ".join(map(lambda node: "{0:^2}".format(node), critical_way)))

        print("Занулення критичного шляху.")
        zero_critical(critical_way)
        print("=" * (4 * n - 3))

    print("Матриця зв'язності після занулення всіх критичних шляхів: ")
    for row in matrix:
        for e in row:
            print("{0:<4}".format(e), end='')
        print()
    print("=" * (4 * n - 3))

    removed_nodes.clear()
    levels = get_levels(matrix)
    critical_way = find_critical(matrix, levels)
    print("Розбиття по рівням (формат запису '<номер вершини>': <її t_level>)")
    for level in levels:
        print(" | ".join(map(lambda node: "{0:<8}".format(str(node)), level)))

    print("Зона оптимального пошуку рішення:")
    print(" -> ".join(map(lambda node: "{0:^2}".format(node), critical_way)))

main()
