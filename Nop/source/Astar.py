import collections
import os
import matplotlib.pyplot as plt


def visualize_maze(matrix, bonus, start, end, route):
    """
    Args:
      1. matrix: The matrix read from the input file,
      2. bonus: The array of bonus points,
      3. start, end: The starting and ending points,
      4. route: The route from the starting point to the ending one, defined by an array of (x, y), e.g. route = [(1, 2), (1, 3), (1, 4)]
    """
    # 1. Define walls and array of direction based on the route
    walls = [(i, j) for i in range(len(matrix)) for j in range(len(matrix[0])) if matrix[i][j] == 'x']

    if route:
        direction = []
        for a in range(1, len(route)):
            if route[a][0] - route[a - 1][0] > 0:
                direction.append('v')  # ^
            elif route[a][0] - route[a - 1][0] < 0:
                direction.append('^')  # v
            elif route[a][1] - route[a - 1][1] > 0:
                direction.append('>')
            else:
                direction.append('<')

        direction.pop(0)

    # 2. Drawing the map
    ax = plt.figure(dpi=100).add_subplot(111)

    for i in ['top', 'bottom', 'right', 'left']:
        ax.spines[i].set_visible(False)
    plt.scatter([i[1] for i in walls], [-i[0] for i in walls],
                marker='X', s=100, color='black')

    plt.scatter([i[1] for i in bonus], [-i[0] for i in bonus],
                marker='P', s=100, color='green')

    plt.scatter(start[1], -start[0], marker='*',
                s=100, color='gold')

    if route:
        for i in range(len(route) - 2):
            plt.scatter(route[i + 1][1], -route[i + 1][0],
                        marker=direction[i], color='silver')

    plt.text(end[1], -end[0], 'EXIT', color='red',
             horizontalalignment='center',
             verticalalignment='center')
    plt.xticks([])
    plt.yticks([])
    plt.show()

    print(f'Starting point (x, y) = {start[0], start[1]}')
    print(f'Ending point (x, y) = {end[0], end[1]}')

    for _, point in enumerate(bonus):
        print(f'Bonus point at position (x, y) = {point[0], point[1]} with point {point[2]}')

def read_file(file_name: str = 'maze.txt'):
  f = open(file_name, 'r')
  n_bonus_points = int(next(f)[:-1])
  bonus_points = []
  for i in range(n_bonus_points):
    x, y, reward = map(int, next(f)[:-1].split(' '))
    bonus_points.append((x, y, reward))
  text = f.read()
  matrix=[list(i) for i in text.splitlines()]
  f.close()
  return bonus_points, matrix


# tao Node
class Node:
    def __init__(self, position: (), parent: ()):
        self.position = position
        self.parent = parent
        self.g = 0  # Distance to start node
        self.h = 0  # Distance to goal node
        self.f = 0  # Total cost

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f

    def __repr__(self):
        return ('({0},{0})'.format(self.position, self.f))

# Check
def add_to_open(open, neighbor):
    for node in open:
        if (neighbor == node and neighbor.f >= node.f):
            return False
    return True

# A* search
def astar_search(matrix, start, end):
    open = []
    closed = []

    start_node = Node(start, None)
    goal_node = Node(end, None)

    open.append(start_node)

    while len(open) > 0:
        open.sort()

        current_node = open.pop(0)

        closed.append(current_node)

        if current_node == goal_node:
            path = []
            while current_node != start_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]

        (x, y) = current_node.position

        neighbors = ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))

        for x2, y2 in neighbors:

            map_value = matrix[x2][y2]

            if (map_value == wall):
                continue

            neighbor = Node((x2, y2), current_node)

            if (neighbor in closed):
                continue

            neighbor.g = abs(neighbor.position[0] - start_node.position[0]) + abs(
                neighbor.position[1] - start_node.position[1])
            neighbor.h = abs(neighbor.position[0] - goal_node.position[0]) + abs(
                neighbor.position[1] - goal_node.position[1])
            neighbor.f = neighbor.g + neighbor.h

            if (add_to_open(open, neighbor) == True):
                open.append(neighbor)

    return None

bonus_points, matrix = read_file('maze_map_8.txt')
# 1, 2, 3, 4?, 5, 6, 7

print(f'The height of the matrix: {len(matrix)}')
print(f'The width of the matrix: {len(matrix[0])}')

wall, clear, goal = 'x', ' ', 'E'
width, height = len(matrix[0]), len(matrix)

for i in range(height):
    for j in range(width):
        if matrix[i][j] == 'S':
            start = (i, j)
        elif matrix[i][j] == 'E':
            end = (i, j)
        else:
            pass

path = astar_search(matrix, start, end)
path.insert(0, start)
print("Route to destination: ", path)
if len(path) == 1:
    print('Trackless')
else:
    print("Distance: ", len(path) - 1)

visualize_maze(matrix, bonus_points, start, end, path)