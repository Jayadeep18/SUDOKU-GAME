from Solution import find_blank, correct,print_sudoku,board
#solves the sudoku
def sol(b) :
    box=find_blank(b)
    if not box :
        return True
    else :
        row= box[0]
        col= box[1]
    for i in range(1,10) :
        if(correct(b,i,box)) :
            b[row][col]=i
            if sol(b) :
                return True
            b[row][col]=0
    return False

'''
print("The puzzle was : \n")
print_sudoku(board)
sol(board)
print("\n\nThe solution is : \n")
print_sudoku(board)
'''