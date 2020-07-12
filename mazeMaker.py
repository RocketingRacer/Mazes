from random import randint
import numpy as np
import pygame,sys
def make(id,x,y):
    print("Starting..."+str(id))
    #x = int(input("Y: "))
    #y = int(input("X: "))
    bounds = (x,y-1)
    board = [[True for e in range(y-1)]for i in range(x)]
    #board[x][y]
    startPos = [0,1]
    visited = [[False for e in range(y)]for i in range(x)]
    running = True
    jmpStack = [startPos]
    board[startPos[0]][startPos[1]] = False
    while(len(jmpStack)>0):
        #print(len(jmpStack))
        pos = jmpStack[-1]
        p2 =[]
        dTried = {0:False,1:False,2:False,3:False}
        success = False
        while not(dTried[0] and dTried[1] and dTried[2] and dTried[3]):
            r = randint(0,3)
            dTried[r]=True
            #print(dTried)
            if r == 0:
                if pos[0]-2 > 0 and visited[pos[0]-2][pos[1]] == False and visited[pos[0]-1][pos[1]]==False: #left is unvisited and on the board
                    board[pos[0]-1][pos[1]] = False
                    board[pos[0]-2][pos[1]] = False
                    visited[pos[0]-1][pos[1]] = True
                    pos = [pos[0]-2,pos[1]]
                    success = True
                    #print("Left")
                    break
            elif r == 1:
                if pos[0]+2< bounds[0] and visited[pos[0]+2][pos[1]] == False and visited[pos[0]+1][pos[1]]==False: #right is unvisited and on the board
                    board[pos[0]+1][pos[1]] = False
                    board[pos[0]+2][pos[1]] = False
                    visited[pos[0]+1][pos[1]] = True
                    pos = [pos[0]+2,pos[1]]
                    success = True
                    #print("Right")
                    break
            elif r == 2:
                if pos[1] -2 > 0 and visited[pos[0]][pos[1]-2] == False and visited[pos[0]][pos[1]-1]==False: #up is unvisited and on the board
                    board[pos[0]][pos[1]-1] = False
                    board[pos[0]][pos[1]-2] = False
                    visited[pos[0]][pos[1]-1] = True
                    pos = [pos[0],pos[1]-2]
                    success = True
                    #print("UP")
                    break
            else:
                if pos[1] + 2 < bounds[1] and visited[pos[0]][pos[1]+2] == False and visited[pos[0]][pos[1]+1]==False: #down is unvisited and on the board
                    board[pos[0]][pos[1]+1] = False
                    board[pos[0]][pos[1]+2] = False
                    visited[pos[0]][pos[1]+1] = True
                    pos = [pos[0],pos[1]+2]
                    success = True
                    #print("Down")
                    break
        if success:
            visited[pos[0]][pos[1]] = True
            board[pos[0]][pos[1]] = False
            jmpStack.append(pos)
        else:
            jmpStack.pop(-1)

    for x in range(len(board[0])-1,0,-1):
        if board[-2][x] == False:
            board[-1][x] = False
            end = [len(board)-1,x]
            #print("removed",end)
            break
    if len(board)%2 ==1:
        for x in board:
            x.append(True)
            bounds[1] = bounds[1]+1
    board.insert(0,[True for t in range(bounds[1])])
    board[startPos[0]][startPos[1]]=False
    idealH = 2160
    h = idealH/len(board)
    sr =(int(h*len(board[0])),int(h*len(board)))
    print(sr)
    btext = ""
    overlay = pygame.Surface((len(board[0]),len(board)))
    overlay.fill((0,0,0))
    windowPixels = pygame.PixelArray(overlay)
    xc = 0
    for x in board:
        yc = 0
        for y in x:
            if y:
                btext += "*"
            else:
                btext+=" "
                windowPixels[yc,xc]=((255,255,255))
            yc = yc+1
        btext+="\n"
        xc = xc+1
    windowPixels.close()
    overlay = pygame.transform.scale(overlay,sr)
    pygame.image.save(overlay,"maze"+str(id)+"Blank.jpg")



    outPut = open("maze"+str(id)+".txt",'w')
    s = ""
    s+= str(bounds[1]) + " " + str(bounds[0]+1) + "\n"
    s+= str(startPos[1]) + " " + str(startPos[0])+"\n"
    s+= str(end[1]) + " " + str(end[0]+1)+"\n"
    s+= btext
    s = s[:-1]
    outPut.write(s)
    outPut.close()
    print("DONE!")
def main():
    f = int(input("Enter number 1-5: "))
    x = 2**(f+2)
    make(str(f).rjust(2,"0"),x,x)
if __name__ == "__main__":
    pygame.init()
    main()
