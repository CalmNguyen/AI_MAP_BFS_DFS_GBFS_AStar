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

        #direction.pop(0)

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

def read_file(file_name: str = 'xx.txt'):
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

bonus_points, matrix = read_file('xx.txt')

print(f'The height of the matrix: {len(matrix)}')
print(f'The width of the matrix: {len(matrix[0])}')

def read_file(file_name: str = 'xx.txt'):
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

bonus_points, matrix = read_file('xx.txt')

def bfs(grid, start):
    queue = collections.deque([[start]])
    seen = set([start])

    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if grid[x][y] == goal:
            return path
        for x2, y2 in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
            if 0 <= x2 < height and 0 <= y2 < width and grid[x2][y2] != wall and (x2, y2) not in seen:
                queue.append(path + [(x2, y2)])
                seen.add((x2, y2))

wall, clear, goal = 'x', ' ', 'E'
width, height = len(matrix[0]), len(matrix)

for i in range(len(matrix)):
    for j in range(len(matrix[0])):
        if matrix[i][j] == 'S':
            start = (i, j)
        elif matrix[i][j] == 'E':
            end = (i, j)
        else:
            pass
import time
s=time.time()
path = bfs(matrix, start)
e=time.time()
print('Chi phi: ', e-s)
print("Route to destination: ", path)
print("Distance: ", len(path) - 1)
visualize_maze(matrix, bonus_points, start, end, path)
