
board = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]


# checks if the inserted number is acceptable 
def correct(b,num,box) :
    for i in range(len(b)) :
        if(i!=box[0]) :
            if(b[i][box[1]]==num) :
                return False
    for j in range (len(b[0])) :
        if(j!=box[1]) :
            if(b[box[0]][j]==num) :
                return False
    x=box[1]//3
    y=box[0]//3

    for i in range(y*3,((y*3) +3)) :
        for j in range(x*3,((x*3)+3)) :
            if(i!=box[0] or j!=box[1]) :
                if(b[i][j]==num) :
                    return False
    return True

# prints the sudoku board
def print_sudoku(b):
    for i in range(len(b)) :
        if (i%3==0 and i!=0) :
            print("________________________")
        for j in range(len(b[0])) :
            if (j%3 == 0 and j!=0) :
                print(" | ", end="")
            if(j==8) :
                print(b[i][j])
            else :
                print(str(b[i][j])+" ", end="")


# finds the first empty space (zero) in the board
def find_blank(b) :
    for i in range(len(b)) :
        for j in range(len(b[0])) :
            if b[i][j]==0 :
                return (i,j)
    return False
