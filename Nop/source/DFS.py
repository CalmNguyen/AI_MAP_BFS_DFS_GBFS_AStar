#Hàm này để đọc file mê cung
import time
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

def maze(filename):
    f = open(filename, 'r')
    matrix=[]
    data = f.readline()
    data=data.replace('\n','')
    j=0
    start=[]
    end=[]
    while True:
        data = f.readline()
        data=data.replace('\n','')
        if data == '':
            break
        matrix.append([])
        for i in range(len(data)):
            if(data[i]=='x'):
                matrix[j].append(0)
            elif(data[i]=='S'):
                matrix[j].append(3)
                start.append(j)
                start.append(i)
            elif(data[i]=='E'):
                matrix[j].append(4)
                end.append(j)
                end.append(i)
            else:
                matrix[j].append(1)
        j+=1
    f.close()
    return matrix,start,end
#Hàm này tìm điểm thoát ma trận 'e'
def start_point(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if(matrix[i][j]==3):
                return [i,j]
def next_point(i,j,matrix):
    column=len(matrix[0])
    current=len(matrix)
    #right
    if(j+1<column):
        if(matrix[i][j+1]!=0):
            return [i,j+1]
    #down
    if(i+1<current):
        if(matrix[i+1][j]!=0):
            return [i+1,j]
    #left
    if(j-1>=0):
        if(matrix[i][j-1]!=0):
            return [i,j-1]
    #up
    if(i-1>=0):
        # có thể đi được
        if(matrix[i-1][j]!=0):
            return [i-1,j]
    
    return [i,j]
#DFS này ưu tiên qua phải>xuống>trái>lên
def DFS(matrix1):
    #không thay đổi mảng ban đầu
    matrix=matrix1[:]
    for i in range(len(matrix1)):
        matrix[i]=matrix1[i][:]
    column=len(matrix[0])
    current=len(matrix)
    stack=[]
    #Duyệt từ e đến s
    present=start_point(matrix)
    stack.append(present)
    matrix[present[0]][present[1]]=0
    i=0
    #present là điểm đang xét
    while(True):
        #Trường hợp không tìm được điểm đi tiếp theo
        if(present==next_point(present[0],present[1],matrix)):
            if(len(stack)!=0):
                stack.pop()
                #Trở về điểm trước đó
                present=stack[len(stack)-1]
            else:
                print("Khong tim thay")
        #Nếu vẫn có điểm tiếp theo
        else:
            present=next_point(present[0],present[1],matrix)
            stack.append(present)
            if(matrix[present[0]][present[1]]==4):
                return stack
            matrix[present[0]][present[1]]=0
#Ghi ra file, mô tả đường đi
def output(matrix1,stack):
    matrix=matrix1
    s=stack[-1]
    e=stack[0]
    j=stack[0]
    for i in stack:
        #i là điểm sau j là điểm trước tính từ 's'
        if(i[1]==j[1]):
            if(i[0]<j[0]):#Điểm tiếp theo nằm phía dưới
                matrix[i[0]][i[1]]='^'
            else:#Phía trên
                matrix[i[0]][i[1]]='v'
        elif(i[0]==j[0]):
            if(i[1]<j[1]):#bên phải
                matrix[i[0]][i[1]]='<'
            else:#bên trái
                matrix[i[0]][i[1]]='>'
        j=i
    matrix[s[0]][s[1]]='S'
    matrix[e[0]][e[1]]='E'
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if(matrix[i][j]==1):
                matrix[i][j]=' '
            elif(matrix[i][j]==0):
                matrix[i][j]='x'
    return matrix
matrix,start,end=maze('maze1.txt')
start_time=time.time()
print(start_time)
stack= DFS(matrix)
end_time=time.time()
print(end_time)
print("Chi phi", len(stack)-1)
print("Thoi gian chay:", end_time-start_time)
output=output(matrix,stack)


visualize_maze(matrix, [], start, end, stack)
            



