from StepperMotor import StepperMotor
import os
import numpy as np
import time
import pandas as pd


def draw_grid(step=256, width=16):
    left_motor = StepperMotor([7, 11, 13, 15])
    right_motor = StepperMotor([31, 33, 35, 37])
    
    for i in range(int(.5*step/width)):
        print('horizontal', i)
        left_motor.rotate(step)
        right_motor.rotate(-width)
        left_motor.rotate(-step)
        right_motor.rotate(-width)
    
    for i in range(int(.5*step/width)):
        print('vertical', i)
        right_motor.rotate(step)
        left_motor.rotate(width)
        right_motor.rotate(-step)
        left_motor.rotate(width)
        
    right_motor.rotate(step)
    left_motor.rotate(-step)
    right_motor.rotate(-step)
    left_motor.rotate(step)
    
    left_motor.close()
    right_motor.close()
        
        
def calibrate(iters=20):
    left_motor = StepperMotor([7, 11, 13, 15])
    right_motor = StepperMotor([31, 33, 35, 37])
    step = 512
    for i in range(iters):
        left_motor.rotate(step)
        right_motor.rotate(step)
        left_motor.rotate(-step)
        right_motor.rotate(-step)


def calibrate_diag(iters=20):
    left_motor = StepperMotor([7, 11, 13, 15])
    right_motor = StepperMotor([31, 33, 35, 37])
    step = 128
    for i in range(iters):
        for z in range(step):
            left_motor.rotate(2)
            right_motor.rotate(2)
        for z in range(step):
            left_motor.rotate(-2)
            right_motor.rotate(2)
        for z in range(step):
            left_motor.rotate(-2)
            right_motor.rotate(-2)
        for z in range(step):
            left_motor.rotate(2)
            right_motor.rotate(-2)


def spiral(x):
    left_motor = StepperMotor([7, 11, 13, 15])
    right_motor = StepperMotor([31, 33, 35, 37])
    step = 16
    ii = 1
    while ii < x:
        left_motor.rotate(ii*step)
        time.sleep(.1)
        right_motor.rotate(ii*step)
        time.sleep(.1)
        ii += 1
        left_motor.rotate(-ii*step)
        time.sleep(.1)
        right_motor.rotate(-ii*step)
        ii += 1
    left_motor.close()
    right_motor.close()


def arrow_control():
    print('Entering Arrow Control Mode...')
    left_motor = StepperMotor([7, 11, 13, 15])
    right_motor = StepperMotor([31, 33, 35, 37])
    import pygame
    pygame.init()
    # screen = pygame.display.set_mode([60, 60])
    # clock = pygame.time.Clock()
    # pygame.key.set_repeat(100, 100)
    pygame.key.set_repeat()
    step = 4
    counter = {
        'left': 0,
        'right': 0,
        'up': 0,
        'down': 0}
    
    while 1:
        # clock.tick(60) #60 FPS
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            print(counter)
            if event.type == pygame.KEYDOWN:
                
                if keys[pygame.K_RIGHT] + keys[pygame.K_UP] + keys[pygame.K_LEFT] + keys[pygame.K_DOWN] == 2:
                    x = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
                    y = keys[pygame.K_UP] - keys[pygame.K_DOWN]
                    # if np.sign(x) == -1 and random.random() < .05:
                    #        # drift correction
                    #        x += 1
                    print('x', x)
                    print('y', y)
                    x, y = int(x*step/(2**.5)), int(y*step/(2**.5))
                    for z in range(step):
                        left_motor.rotate(np.sign(x))
                        right_motor.rotate(np.sign(y))
                
                else:
                    if event.key == pygame.K_UP:
                        right_motor.rotate(step)
                        print("Up was pressed.")
                        counter['up'] += step

                    elif event.key == pygame.K_DOWN:
                        right_motor.rotate(-step)
                        print("Down was pressed.")
                        counter['down'] += step

                    elif event.key == pygame.K_LEFT:
                        left_motor.rotate(-step)
                        print("Left was pressed.")
                        counter['left'] += step
                    
                    elif event.key == pygame.K_RIGHT:
                        left_motor.rotate(step)
                        print("Right was pressed.")
                        counter['right'] += step
                        
                    elif event.key == pygame.K_ESCAPE:
                        left_motor.close()
                        right_motor.close()
                        pygame.quit()
                        return


def load_path(file):
    import pickle
    with open(os.path.join('Paths', file+'.p'), 'rb') as my_file:
        data = pickle.load(my_file)
    return data


def draw_from_cache(file):
    path = load_path(file)
    print(len(path))
    draw_path(path)
    return


def check_start(file, n=6):
    path = load_path(file)
    df = pd.DataFrame(path)
    lefts, downs = tuple(df.cumsum().min().values)
    rights, ups = tuple(df.cumsum().max().values)
    scaling = 26.*6./n
    print('Room Needed', '\n--------')
    print('left: ', lefts, 'approx. ', round(lefts/scaling, 2), 'cm')
    print('right:', rights, 'approx. ', round(rights/scaling, 2), 'cm')
    print('up:   ', ups, 'approx. ', round(ups/scaling, 2), 'cm')
    print('down: ', downs, 'approx. ', round(downs/scaling, 2), 'cm')
    return


def draw_path(path):
    left_motor = StepperMotor([7, 11, 13, 15])
    right_motor = StepperMotor([31, 33, 35, 37])
    step = 2
    reps = 2
    print('# of Steps: ', len(path))
    step_counter = 0
    for p in path:
        step_counter += 1
        if step_counter % 50:
            print(step_counter, '/', len(path))
        for rep in range(reps):
            # print('x','y',p)
            x = p[0]
            y = p[1]
            right_motor.rotate(-step*y)
            left_motor.rotate(step*x)
    left_motor.close()
    right_motor.close()


if __name__ == '__name__':
    arrow_control()  # if pictureDraw is run, go to arrow_control
