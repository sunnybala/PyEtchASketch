from stepperMotor import stepperMotor
import os
import numpy as np
import time
import pandas as pd

def draw_grid(step=256,width=16):
    leftMotor = stepperMotor([7,11,13,15])
    rightMotor = stepperMotor([31,33,35,37])
    
    for i in range(int(.5*step/width)):
        print('horizontal',i)
        leftMotor.rotate(step)
        rightMotor.rotate(-width)
        leftMotor.rotate(-step)
        rightMotor.rotate(-width)
    
    for i in range(int(.5*step/width)):
        print('vertical',i)
        rightMotor.rotate(step)
        leftMotor.rotate(width)
        rightMotor.rotate(-step)
        leftMotor.rotate(width)
        
    rightMotor.rotate(step)
    leftMotor.rotate(-step)
    rightMotor.rotate(-step)
    leftMotor.rotate(step)
    
    leftMotor.close()
    rightMotor.close()
        
        
def calibrate(iters = 20):
    leftMotor = stepperMotor([7,11,13,15])
    rightMotor = stepperMotor([31,33,35,37])
    step = 512
    for i in range(iters):
        leftMotor.rotate(step)
        rightMotor.rotate(step)
        leftMotor.rotate(-step)
        rightMotor.rotate(-step)

def calibrateDiag(iters = 20):
    leftMotor = stepperMotor([7,11,13,15])
    rightMotor = stepperMotor([31,33,35,37])
    step = 128
    for i in range(iters):
        for z in range(step):
                        leftMotor.rotate(2)
                        rightMotor.rotate(2)
        for z in range(step):
                        leftMotor.rotate(-2)
                        rightMotor.rotate(2)
        for z in range(step):
                        leftMotor.rotate(-2)
                        rightMotor.rotate(-2)
        for z in range(step):
                        leftMotor.rotate(2)
                        rightMotor.rotate(-2)

def spiral(x):
    leftMotor = stepperMotor([7,11,13,15])
    rightMotor = stepperMotor([31,33,35,37])
    step = 16
    ii = 1
    while ii < x:
        leftMotor.rotate(ii*step)
        time.sleep(.1)
        rightMotor.rotate(ii*step)
        time.sleep(.1)
        ii += 1
        leftMotor.rotate(-ii*step)
        time.sleep(.1)
        rightMotor.rotate(-ii*step)
        ii += 1
    leftMotor.close()
    rightMotor.close()
    
def arrowControl():
    print('Entering Arrow Control Mode...')
    leftMotor = stepperMotor([7,11,13,15])
    rightMotor = stepperMotor([31,33,35,37])
    # [31,33,35,37]
    import pygame, sys
    pygame.init()
    screen = pygame.display.set_mode([60,60])
    clock = pygame.time.Clock()
    pygame.key.set_repeat(100,100)
    step = 4
    counter = {
        'left':0,
        'right':0,
        'up':0,
        'down':0}
    
    while 1:
        #clock.tick(60) #60 FPS
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            print(counter)
            if event.type == pygame.KEYDOWN:
                
                if keys[pygame.K_RIGHT] + keys[pygame.K_UP] + keys[pygame.K_LEFT] + keys[pygame.K_DOWN] == 2:
                    x = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
                    y = keys[pygame.K_UP] - keys[pygame.K_DOWN]
                    #if np.sign(x) == -1 and random.random() < .05:
                    #        # drift correction
                    #        x += 1
                    print('x',x)
                    print('y',y)
                    x,y = int(x*step/(2**.5)), int(y*step/(2**.5))
                    for z in range(step):
                        leftMotor.rotate(np.sign(x))
                        rightMotor.rotate(np.sign(y))
                
                else:
                    if event.key == pygame.K_UP:
                        rightMotor.rotate(step)
                        #print("Up was pressed.")
                        counter['up'] += step

                    elif event.key == pygame.K_DOWN:
                        rightMotor.rotate(-step)
                        #print("Down was pressed.")
                        counter['down'] += step

                    elif event.key == pygame.K_LEFT:
                        leftMotor.rotate(-step)
                        #print("Left was pressed.")
                        counter['left'] += step
                    
                    elif event.key == pygame.K_RIGHT:
                        leftMotor.rotate(step)
                        #print("Right was pressed.")
                        counter['right'] += step
                        
                    elif event.key == pygame.K_ESCAPE:
                        leftMotor.close()
                        rightMotor.close()
                        pygame.quit()
                        return
            
    leftMotor.close()

import pickle
def load_path(file):
    with open(os.path.join('Paths',file+'.p'),'rb') as myfile:
        data = pickle.load(myfile)
    return data

def draw_from_cache(file):
    path = load_path(file)
    print(len(path))
    draw_path(path)
    return

def check_start(file,n=6):
    path = load_path(file)
    df = pd.DataFrame(path)
    lefts,downs = tuple(df.cumsum().min().values)
    rights,ups = tuple(df.cumsum().max().values)
    scaling = 26.*6./n
    print('Room Needed','\n--------')
    print('left: ',lefts,'approx. ',round(lefts/scaling,2),'cm')
    print('right:',rights,'approx. ',round(rights/scaling,2),'cm')
    print('up:   ',ups,'approx. ',round(ups/scaling,2),'cm')
    print('down: ',downs,'approx. ',round(downs/scaling,2),'cm')
    return

def draw_path(path):
    leftMotor = stepperMotor([7,11,13,15])
    rightMotor = stepperMotor([31,33,35,37])
    step = 2
    reps = 2
    print('# of Steps: ',len(path))
    stepcounter = 0
    for p in path:
        stepcounter += 1
        if stepcounter % 50:
            print(stepcounter,'/',len(path))
        for rep in range(reps):
        #print('x','y',p)
            x = p[0]
            y = p[1]
            rightMotor.rotate(-step*y)
            leftMotor.rotate(step*x)
    leftMotor.close()
    rightMotor.close()

arrowControl()