import time

def comp(l1, l2): #Compare 2 list if they are equal
    if l1 == l2:
        return 1
    return 0

DICT = {
    0: [0,0],
    1: [0,1],
    2: [0,2],
    3: [1,0],
    4: [1,1],
    5: [1,2],
    6: [2,0],
    7: [2,1],
    8: [2,2]
}

class Node:
    # Initialize the node with the data, level of the node and the calculated fvalue
    def __init__(self,data,level,fval):
        self.data = data
        self.level = level
        self.fval = fval

    # Generate child nodes from the given node by moving the blank space
    # either in the four directions {up,down,left,right}
    def generate_child(self):
            x,y = self.find(self.data,0)
            val_list = [[x,y-1],[x,y+1],[x-1,y],[x+1,y]] # val_list contains 4 movable directions
            children = []
            for i in val_list:
                child = self.shuffle(self.data,x,y,i[0],i[1])
                if child is not None:
                    child_node = Node(child,self.level+1,0)
                    children.append(child_node)
            return children

    # Move the blank space in the given direction and if the position value are out
    # of limits the return None       
    def shuffle(self,puz,x1,y1,x2,y2):
        if x2 >= 0 and x2 < len(self.data) and y2 >= 0 and y2 < len(self.data):
            temp_puz = []
            temp_puz = self.copy(puz)
            temp = temp_puz[x2][y2]
            temp_puz[x2][y2] = temp_puz[x1][y1]
            temp_puz[x1][y1] = temp
            return temp_puz
        else:
            return None

    # Copy function to create a similar matrix of the given node
    def copy(self,root):
        temp = []
        for i in root:
            t = []
            for j in i:
                t.append(j)
            temp.append(t)
        return temp    
                
    # Specifically used to find the position of the blank space
    def find(self,puz,x):
        for i in range(0,len(self.data)):
            for j in range(0,len(self.data)):
                if puz[i][j] == x:
                    return i,j

class Puzzle:
    # Initialize the puzzle size by the specified size,open and closed lists to empty
    def __init__(self,size):
        self.n = size # Size of puzzle
        self.open = [] # A list contains the state of puzzle is NOT checked 
        self.closed = [] # A list contains the state of puzzle is checked
        self.flag = False # flag whether the problem is solvable or not

    # Input the start puzzle
    def accept(self):
            puz = []
            for i in range(0,self.n):
                temp = [int(i) for i in input().split(" ")]
                puz.append(temp)
            return puz

    # Heuristic function to calculate hueristic value f(x) = h(x) + g(x)
    def f(self,start,goal): 
            return self.h(start.data,goal) + start.level

    # Calculates the different between the given puzzles using Manhattan distance formula
    def h(self,start,goal):
            temp = 0
            for i in range(0,self.n):
                for j in range(0,self.n):
                    if start[i][j] != 0 and start[i][j] != goal[i][j]:
                        temp = temp + (abs(DICT[start[i][j]][0] - i)**2 + abs(DICT[start[i][j]][1] - j)**2)
            return temp

    def initilize_goal(self):
        puz = [[0, 1, 2],
            [3, 4, 5],
            [6, 7, 8]
            ]
        return puz

    #Check whether the algorithm did check the node or not?
    def checkMatchedNodes(self, newNode):
        for i in self.closed:
            if(comp(i.data, newNode.data)):
                return True
        return False
                
    def process(self):
            print("Enter the start state matrix \n")
            start = self.accept()       
            goal = self.initilize_goal()
            start = Node(start,0,0)
            start.fval = self.f(start,goal)
            self.open.append(start) # Put the start node in the open list
            print("")
            while True:
                cur = self.open[0]
                self.closed.append(cur) # Add current node to closed list

                # print the current node
                for i in cur.data:
                    for j in i:
                        print(j,end=" ")
                    print("")
                print("-----")
                # If the difference between current and goal node is 0 we have reached the goal node
                if(self.h(cur.data,goal) == 0):
                    self.flag = True
                    return cur.level
                    break
                for i in cur.generate_child():
                    i.fval = self.f(i,goal)
                    if(self.checkMatchedNodes(i) == False):
                        self.open.append(i)
                del self.open[0]
                self.open.sort(key = lambda x:x.fval,reverse=False) # sort the open list based on f value 
            return self.flag

puz = Puzzle(3)
startTime = time.time()
game = puz.process()
endTime = time.time()
print(f"Solve the game with {game} steps" if game != False else "Not found")
print(f"After {endTime - startTime}")