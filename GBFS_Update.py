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
    bonus=[]
    for i in range(int(data)):
        data=f.readline()
        data=data.split(' ')
        bonus.append([int(data[0]),int(data[1]),int(data[2])])
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
            elif(data[i]=='+'):
                matrix[j].append(5)
            else:
                matrix[j].append(1)
        j+=1
    f.close()
    return matrix,start,end,bonus
#số bước đi ngắn nhất tới điểm e: dọc + ngang
def TinhHn(matrix,end):
    new=matrix.copy()
    t=0
    for i in range(len(matrix)):
        new[i]=matrix[i].copy()
    for i in range(len(matrix)):
        for j in range(len(new[0])):
            t = pow(end[0]-i,2)+pow(end[1]-j,2)
            new[i][j]= t
    return new

def next_point_Hn(i,j,matrix,Hn):
    column=len(matrix[0])
    current=len(matrix)
    min_Hn=999999
    toado_min=[i,j]
    #ss v right
    if(j+1<column):
        if(matrix[i][j+1]!=0):
            if(Hn[i][j+1]<min_Hn):
                min_Hn=Hn[i][j+1]
                toado_min=[i,j+1]
    #ss v down
    if(i+1<current):
        if(matrix[i+1][j]!=0):
            if(Hn[i+1][j]<min_Hn):
                min_Hn=Hn[i+1][j]
                toado_min=[i+1,j]
    #ss v left
    if(j-1>=0):
        if(matrix[i][j-1]!=0):
            if(Hn[i][j-1]<min_Hn):
                min_Hn=Hn[i][j-1]
                toado_min=[i,j-1]
    #ss v up
    if(i-1>=0):
        # đúng khi là 1 or 4
        if(matrix[i-1][j]!=0):
            if(Hn[i-1][j]<min_Hn):
                min_Hn=Hn[i-1][j]
                toado_min=[i-1,j]
    
    return toado_min
def tinh_kc(i,j):
    return sqrt(pow(i[0]-j[0],2)+pow(i[1]-j[1],2))

def bonus_gannhat(present,bonus):
    toado_min=present
    min=999999
    for i in range(len(bonus)):
        if(tinh_kc(present,bonus[i])<min):
            min=tinh_kc(present,bonus[i])
            toado_min=bonus[i]
    return toado_min

def go_bonus(present,end,bonus):
    if(tinh_kc(present,end)>tinh_kc(end,bonus)+tinh_kc(present,bonus)+bonus[2]):
        return True
    return False
#Duyệt từ start đến end dựa vào Hn để tìm bước đi tiếp theo
#Nếu kín đường dùng quay lui
def GBFS(matrix1,start,end,bonus1):
    bonus=bonus1[:]
    bonus_copy=bonus[:]
    matrix=matrix1[:]
    for i in range(len(matrix1)):
        matrix[i]=matrix1[i][:]
    Hn=[]
    Hn=TinhHn(matrix,end)
    stack=[]
    #Duyệt từ e đến s
    dich=end
    present=start
    stack.append(present)
    matrix[present[0]][present[1]]=0
    i=0
    b=[]
    #present là điểm đang xét
    while(True):
        #Trường hợp không tìm được điểm đi tiếp theo
        #Xét điểm bonus gần nhất nếu ước lượng chi phí tốt hơn thì ăn
        if(dich==end):
            b=bonus_gannhat(present,bonus)
            if(b!=present and [b[0],b[1]] not in stack):
                if(go_bonus(present,end,b)==True):
                    dich=[b[0],b[1]]
                    bonus.remove(b)
                    Hn=TinhHn(matrix,dich)
                    temp=b
        if(present==next_point_Hn(present[0],present[1],matrix,Hn)):
            if(len(stack)!=0):
                stack.pop()
                #Trở về điểm trước đó
                if(len(stack)!=0):
                    present=stack[len(stack)-1]
                else:
                    if(dich==end):
                        print("Không thấy lối ra")
                        return
                    else:
                        matrix=matrix1[:]
                        for i in range(len(matrix1)):
                            matrix[i]=matrix1[i][:]
                        dich=end
                        bonus_copy.remove(b)
                        bonus=bonus_copy[:]
                    Hn=TinhHn(matrix,dich)
        #Nếu vẫn có điểm tiếp theo
        else:
            present=next_point_Hn(present[0],present[1],matrix,Hn)
            stack.append(present)
            if(present==dich):              
                if(matrix[present[0]][present[1]]==4):
                    return stack
                else:
                    dich=end
                    Hn=TinhHn(matrix,dich)
            matrix[present[0]][present[1]]=0
def output(matrix1,stack):
    matrix=matrix1
    s=stack[-1]
    e=stack[0]
    j=stack[0]
    for i in stack:
        #i là điểm sau j là điểm trước tính từ 's'
        if(i[1]==j[1]):
            if(i[0]<j[0]):#Điểm tiếp theo nằm phía dưới
                matrix[i[0]][i[1]]='v'
            else:#Phía trên
                matrix[i[0]][i[1]]='^'
        elif(i[0]==j[0]):
            if(i[1]<j[1]):#bên phải
                matrix[i[0]][i[1]]='>'
            else:#bên trái
                matrix[i[0]][i[1]]='<'
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
def tinh_chi_phi(stack,bonus):
    chi=len(stack)-1
    for i in bonus:
        if([i[0],i[1]] in stack):
            chi+=i[2]
    return chi
matrix,start,end,bonus = maze('maze_map3.txt')
stack= GBFS(matrix,start,end,bonus)
print("Chi phi la: ", tinh_chi_phi(stack,bonus))
output=output(matrix,stack)
for i in bonus:
    matrix[i[0]][i[1]]='+'
visualize_maze(matrix,bonus,start,end,stack)



