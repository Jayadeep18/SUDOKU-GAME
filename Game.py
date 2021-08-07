import pygame
from pygame import KEYDOWN
from Solver import sol
from Solution import correct
from dokusan import generators
import numpy as np
import time
pygame.font.init()

print("CHOOSE DIFFICULTY LEVEL :")
print("1 FOR EASY")
print("2 FOR MEDIUM")
print("3 FOR HARD")
inp = input(print("Enter choice :"))
if(inp=='1') :
    n=80
elif(inp=='2') :
    n=110
elif(inp=='3') :
    n=150
else :
    n=90
b= np.array(list(str(generators.random_sudoku(avg_rank=n))))
b =list(map(int,b))
b=np.array(b)
b=b.reshape(9,9)
class Grid:
    '''
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
]'''
    board = b
    #print(board)
    #initializing 
    def __init__(self, rows, cols, ht, wt) :
        self.rows=rows
        self.cols=cols
        self.ht=ht
        self.wt=wt
        self.cubes= [[Cube(self.board[i][j],i,j,wt,ht) for j in range(cols)] for i in range(rows)]
        self.model= None
        self.selected= None

    #updating
    def update_model(self) :
        self.model =[[self.cubes[i][j]. value for j in range(self.cols)] for i in range(self.rows)]
    
    #places the entered digit (val) if it is a correct entry, else places 0
    def place(self,val) :
        row,col =self.selected
        if(self.cubes[row][col].value ==0) :
            self.cubes[row][col].set(val)
            self.update_model()

            if(correct(self.model,val,(row,col)) and sol (self.model)) :
                return True
            else :
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    #writes the entry as temporary in pencil at top for reference in the grid
    def sketch(self,val) :
        row,col = self.selected
        self.cubes[row][col].set_temp(val)

    #Draws the lines and the cubes
    def draw(self,win) :
        gap= self.wt /9
        #Grid Lines
        for i in range(self.rows+1) :
            if(i%3 ==0 and i!=0) :
                thick =4
            else :
                thick =1
            pygame.draw.line(win, (0,0,0), (0, i*gap), (self.wt, i*gap), thick)
            pygame.draw.line(win, (0,0,0), (i*gap, 0), (i*gap, self.ht), thick)

        #Cubes
        for i in range(self.rows) :
            for j in range(self.cols) :
                self.cubes[i][j].draw(win)

    #Deselects others and selectes the current cube
    def select(self, row, col) :
        for i in range(self.rows) :
            for j in range(self.cols) :
                self.cubes[i][j].selected = False
        self.cubes[row][col].selected = True
        self.selected = (row,col)

    #removes the value with the delete option if wrong val is entered
    def clear(self) :
        row,col = self.selected
        if(self.cubes[row][col].value == 0) :
            self.cubes[row][col].set_temp(0)

    
    def click(self, pos) :
        if(pos[0] < self.wt and pos[1] < self.ht) :
            gap = self.wt /9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))  #returns (row,col)
        else :
            return None
    
    #checks if game is over or not
    def is_finished(self) :
        for i in range(self.rows) :
            for j in range(self.cols) :
                if(self.cubes[i][j].value ==0) :
                    return False
            return True

'''
class grid ends
class cube begins
'''

class Cube :
    rows =9
    cols =9

    #initializing
    def __init__(self, value, row, col, wt, ht) :
        self.value=value
        self.row=row
        self.col=col
        self.wt=wt
        self.ht=ht
        self.temp=0
        self.selected=False

    #draw the selected red box, sets fonts and position of text (tmp and not tmp)
    def draw(self, win) :
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.wt / 9
        x = self.col *gap
        y = self.row *gap

        if(self.temp!=0 and self.value ==0) :
            text = fnt.render(str(self.temp),1,(128,128,128))
            win.blit(text,(x+5,y+5))
        elif not(self.value ==0) :
            text = fnt.render(str(self.value),1,(0,0,0))
            win.blit(text,(x+(gap/2 - text.get_width()/2), y+(gap/2 - text.get_width()/2)))

        if (self.selected) :
            pygame.draw.rect(win, (255,0,0),(x,y,gap,gap),3)

    #takes value to the box to check in other fn if correct
    def set(self,val) :
        self.value=val
    
    #takes temp value to be added to the box
    def set_temp(self, val) :
        self.temp=val

'''
class cube ends
'''

def redraw_window(win,board,time,strikes) :

    win.fill((255,255,255))
    #draw white
    fnt = pygame.font.SysFont("lobster", 35)
    text = fnt.render("Time: " + format_time(time),1,(0,0,0))
    win.blit(text,(540-160,560))
    #draw strikes
    text = fnt.render("X "*strikes,1,(255,0,0))
    win.blit(text,(20,560))
    #draw grid and board
    board.draw(win)

def format_time(secs) :
    sec=secs%60
    minute= secs//60
    hour=minute//60

    t=" "+ str(minute)+":"+str(sec)
    return t

def main():
    win= pygame.display.set_mode((540,600))
    pygame.display.set_caption("Sudoku Puzzle")
    board = Grid(9,9,540,540)
    key= None
    run= True
    start = time.time()
    strikes = 0
    while (run) :
        play_time= round(time.time()-start)
        for event in pygame.event.get() :
            if (event.type == pygame.QUIT) :
                run= False
            if (event.type == pygame.KEYDOWN) :
                if (event.key == pygame.K_1) :
                    key = 1
                if (event.key == pygame.K_2) :
                    key = 2
                if (event.key == pygame.K_3) :
                    key = 3
                if (event.key == pygame.K_4) :
                    key = 4
                if (event.key == pygame.K_5) :
                    key = 5
                if (event.key == pygame.K_6) :
                    key = 6
                if (event.key == pygame.K_7) :
                    key = 7
                if (event.key == pygame.K_8) : 
                    key = 8
                if (event.key == pygame.K_9) :
                    key = 9
                if (event.key == pygame.K_DELETE) :
                    board.clear()
                    key = None
                if (event.key == pygame.K_RETURN) :
                    i,j =board.selected
                    if (board.cubes[i][j].temp !=0) :
                        if (board.place(board.cubes[i][j].temp)) :
                            print ("Success")
                        else :
                            print("Wrong")
                            strikes += 1
                        key = None

                        if (board.is_finished()) :
                            print("Game Over, YOU WIN!!")
                            run= False
            if (event.type == pygame.MOUSEBUTTONDOWN) :
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if (clicked) :
                    board.select(clicked[0],clicked[1])
                    key = None
        
        if (board.selected and key != None) :
            board.sketch(key)
        
        redraw_window(win,board,play_time,strikes)
        pygame.display.update()


main()
#pygame.quit()



            