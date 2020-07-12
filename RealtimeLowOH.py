import numpy as np
import math
import pygame,sys
import colorsys
import time
from datetime import datetime, timedelta
clearColor = [192,0,255]
wallColor = [0,0,0]
pathColor = [255,180,200]
attemptColor = [255,0,200]
textColor = [255,255,255]
textBackground = [0,0,120]
aproxH = 900 #aproximate width
def niceTime(timedif):
    s = int(timedif%60)
    m = (timedif//60)%60
    h = (timedif//(60*60))%24
    d = int(timedif)//(60*60*24)
    return str(d)+" days,"+str(h)+" hours, "+str(m)+" minuits, "+str(s)+" seconds"
def times(n):
    scale = int(size/n[0])
    return tuple([n[0]*scale,n[1]*scale])

def findPath(mazeArray,dim,start,end,overlay,window,sr):
    cropPos = [0,0]
    StartTime = int(time.time())

    colour = pathColor
    h = int(aproxH/dim[1])
    stack = []
    visited = [[False for x in range(dim[1])]for z in range(dim[0])]
    pos = start
    stack.append(pos)
    attempted = [[False for x in range(dim[1])]for z in range(dim[0])]
    #print(pos)
    visited[pos[0]][pos[1]]= True
    #print(mazeArray)
    #repeat = 0
    images = []
    fcount = 0
    prevDif = 0
    windowHeader = pygame.display.get_caption()
    windowHeader = windowHeader[0] + " Runtime: "
    #print(end)
    while pos != end and len(stack) > 0:
        CurrentTime = time.time()
        if CurrentTime - StartTime > prevDif+1:
            prevDif = CurrentTime-StartTime
            pygame.display.set_caption(windowHeader+niceTime(prevDif))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        #repeat = repeat + 1
        pos = stack[-1]
        forward = False
        #print(pos)
        #print(visited)
        if not pos[0]+1 > len(mazeArray)-1:
            if mazeArray[pos[0]+1][pos[1]] == True and visited[pos[0]+1][pos[1]] == False:
                pos = [pos[0]+1,pos[1]]
                visited[pos[0]][pos[1]] = True
                forward = True
        if not pos[1]+1 > len(mazeArray[0])-1 and forward == False:
            if mazeArray[pos[0]][pos[1]+1] and visited[pos[0]][pos[1]+1] == False:
                pos = [pos[0],pos[1]+1]
                visited[pos[0]][pos[1]] = True
                forward = True
        if not pos[1]-1 < 0 and forward == False:
            if mazeArray[pos[0]][pos[1]-1] == True and visited[pos[0]][pos[1]-1] == False:
                pos = [pos[0],pos[1]-1]
                visited[pos[0]][pos[1]] = True
                forward = True

        if not pos[0]-1 < 0 and forward == False:
            if mazeArray[pos[0]-1][pos[1]] == True and visited[pos[0]-1][pos[1]] == False:
                pos = [pos[0]-1,pos[1]]
                visited[pos[0]][pos[1]] = True
                forward = True
        if forward == True:
            stack.append(pos)
            colour[0] = (colour[0]+1)%256
            colourRGB = colorsys.hsv_to_rgb(colour[0]/255,colour[1]/255,colour[2]/255)
            colourRGB2 = [colourRGB[i]*255 for i in range(3)]
            windowPixels = pygame.PixelArray(overlay)
            windowPixels[pos[1],pos[0]]=(colourRGB2[0],colourRGB2[1],colourRGB2[2])
            windowPixels.close()


        else:
            stack.pop(-1)
            colour[0] = (colour[0]-1)%256
            attempted[pos[0]][pos[1]]=True
            windowPixels = pygame.PixelArray(overlay)
            windowPixels[pos[1],pos[0]]=(255,255,255)
            windowPixels.close()
        cropSize = aproxH/2
        if abs(cropPos[0]-pos[0]) > cropSize/2 or abs(cropPos[1]-pos[1]) > cropSize/2:
            cropPos= pos
        if dim[0] > sr[0]/2:
            croppedLayer = pygame.Surface((cropSize,cropSize))
            croppedLayer.blit(overlay,(0,0),(cropPos[1]-cropSize/2,cropPos[0]-cropSize/2,cropSize,cropSize))
            overlayS = pygame.transform.scale(croppedLayer,sr)
        else:
            overlayS = pygame.transform.scale(overlay,sr)
        window.blit(overlayS,(0,0))
        #pygame.time.wait(10)
        pygame.display.update()
    return colour


def main():
    clamp = lambda n, minn, maxn: max(min(maxn, n), minn)
    f = int(input("Select Maze Number 1-5: "))
    x = 2**(f+2)
    #mazeMakerAnime.MazeMaker.make(str(f).rjust(2,"0"),x,x)
    g = str(f).rjust(2,"0")
    fname = "maze"+g
    mdata = open(fname+".txt")
    maze = mdata.read()
    lines = maze.split("\n")
    start= [int(lines[1].split(" ")[0]),int(lines[1].split(" ")[1])]
    end = [int(lines[2].split(" ")[1]),int(lines[2].split(" ")[0])]
    maze = lines[3:]

    numx = int(len(maze))
    numy = int(len(maze[0]))
    dim = (numx,numy)
    numy = numy+2

    mazeArray = [[False for x in range(len(maze[z]))]for z in range(len(maze))]
    h = aproxH/numy
    sr =(int(h*numx),int(h*numy))
    window = pygame.display.set_mode(sr)
    pygame.display.set_caption("Maze Solver!")
    window.fill((0,0,0))
    overlay = pygame.Surface((numx,numy))
    #print(start[0])
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if maze[y][x] != '*':
                mazeArray[y][x] = True
                windowPixels = pygame.PixelArray(overlay)
                windowPixels[x,y]=(255,255,255)
                windowPixels.close()

    windowPixels = windowPixels = pygame.PixelArray(overlay)
    windowPixels[start[0],start[1]]=(0,255,0)
    windowPixels.close()

    endingCol =findPath(mazeArray,dim,start,end,overlay,window,sr)
    #print(endingCol)
    window.fill((0,0,0))
    overlayS = pygame.transform.scale(overlay,sr)
    window.blit(overlayS,(0,0))
    pygame.display.flip()
    pygame.image.save(window,fname+"SOLVED.jpg")
    position = [0,0]
    SpeedtextX = int(sr[0]/5)
    SpeedtextY = int(sr[1]-sr[1]/16)
    PostextX = int(sr[0]-sr[0]/8)
    PostextY = int(sr[1]/16)
    cropArea = 128
    speed = 16
    font = pygame.font.Font('freesansbold.ttf', 25)
    showSpeed = True
    firstTime = True
    while 1:
        if firstTime:
            cropSize = cropArea
            croppedLayer = pygame.Surface((cropSize,cropSize))
            croppedLayer.blit(overlay,(0,0),(position[0]-cropSize/2,position[1]-cropSize/2,cropSize,cropSize))
            overlayS = pygame.transform.scale(croppedLayer,sr)
            SpeedInd = font.render("View Mode: Speed = "+str(speed),True,textColor,textBackground)
            SpeedIndRect = SpeedInd.get_rect()
            SpeedIndRect.center=(SpeedtextX,SpeedtextY)
            PosInd = font.render("Position: ("+str(position[0])+","+str(position[1])+")",True,textColor,textBackground)
            PosIndRect = PosInd.get_rect()
            PosIndRect.center =(PostextX,PostextY)
            ZoomInd = font.render("Area: "+str(cropArea),True,textColor,textBackground)
            ZoomIndRect = ZoomInd.get_rect()
            ZoomIndRect.center =(PostextX,PostextY+30)
            keysPressed = []
            window.blit(overlayS,(0,0))
            if showSpeed:
                window.blit(PosInd,PosIndRect)
                window.blit(SpeedInd,SpeedIndRect)
                window.blit(ZoomInd, ZoomIndRect)
                pygame.display.flip()
            else:
                pygame.display.update()
            firstTime = False
        pygame.time.wait(50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    position[1] = clamp(position[1]-speed,0,overlay.get_height())
                if event.key == pygame.K_a:
                    position[0] = clamp(position[0]-speed,0,overlay.get_width())
                if event.key == pygame.K_s:
                    position[1] = clamp(position[1]+speed,0,overlay.get_height())
                if event.key == pygame.K_d:
                    position[0] = clamp(position[0]+speed,0,overlay.get_width())
                if event.key == pygame.K_h: showSpeed = not showSpeed
                if event.key == pygame.K_EQUALS: cropArea = clamp(cropArea - speed,1,900)
                if event.key == pygame.K_MINUS: cropArea = clamp(cropArea + speed,1,900)
                if event.key == pygame.K_KP_PLUS: speed = speed*2
                if event.key == pygame.K_KP_MINUS: speed = speed//2
                if event.key == pygame.K_f:
                     cropArea = max(overlay.get_height(),overlay.get_width())
                     position = [overlay.get_height()//2,overlay.get_width()//2]
                cropSize = cropArea
                croppedLayer = pygame.Surface((cropSize,cropSize))
                croppedLayer.blit(overlay,(0,0),(position[0]-cropSize/2,position[1]-cropSize/2,cropSize,cropSize))
                overlayS = pygame.transform.scale(croppedLayer,sr)
                SpeedInd = font.render("View Mode: Speed = "+str(speed),True,textColor,textBackground)
                SpeedIndRect = SpeedInd.get_rect()
                SpeedIndRect.center=(SpeedtextX,SpeedtextY)
                PosInd = font.render("Position: ("+str(position[0])+","+str(position[1])+")",True,textColor,textBackground)
                PosIndRect = PosInd.get_rect()
                PosIndRect.center =(PostextX,PostextY)
                ZoomInd = font.render("Area: "+str(cropArea),True,textColor,textBackground)
                ZoomIndRect = ZoomInd.get_rect()
                ZoomIndRect.center =(PostextX,PostextY+30)
                keysPressed = []
                window.blit(overlayS,(0,0))
                if showSpeed:
                    window.blit(PosInd,PosIndRect)
                    window.blit(SpeedInd,SpeedIndRect)
                    window.blit(ZoomInd, ZoomIndRect)
                    pygame.display.flip()
                    #print("Update")
                else:
                    pygame.display.update()
                    #print("Update")


if __name__ =="__main__":
    pygame.init()
    main()
