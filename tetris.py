import pygame
import random
from copy import deepcopy

pygame.init()

#variables
squares_height = 20
squares_width = 20
square = 30
screen_x = squares_width*square
screen_y = squares_height*square
x_start = 1/2*screen_x-0.5*square
y_start = 0
x_offset = 0
y_offset = 0
running = True
screen = pygame.display.set_mode((screen_x,screen_y))
clock = pygame.time.Clock()
tets=random.randint(0,6)                                 #list of rects of current tetromino (index from the move() function for the sublist including the positions of the rects for one tetromino)
rects=0
stop_time=0

#list of the landed tetrominos
landed_tetrominos = []
colours_landed = []

#grid squares for the whole screen
grid_squares = [pygame.Rect(i*square,j*square,square,square) for i in range(squares_width) for j in range(squares_height)]

#tetrominos
tetrominos_positions = [
    [(-1, 0), (0, 0), (1, 0), (2, 0)],  #I
    [(1, 0), (-1, 1), (0, 1), (1, 1)],  #L1
    [(2, 2), (0, 1), (1, 1), (2, 1)],   #L2
    [(0, 0), (1, 0), (0, 1), (1, 1)],   #O
    [(0, 0), (1, 0), (-1, 1), (0, 1)],  #S1
    [(1, 0), (0, 0), (2, 1), (1, 1)],   #S2
    [(0, 0), (-1, 1), (0, 1), (1, 1)],  #T
]

tetromino_colors = {
    0: (255, 0, 0),     #red for I
    1: (0, 255, 0),     #green for L1
    2: (0, 0, 255),     #blue for L2
    3: (255, 255, 0),   #yellow for O
    4: (255, 0, 255),   #pink for S2
    5: (148, 71, 230),  #purple for S2
    6: (52, 235, 235),  #turqouise for T
}


#functions

def draw_grid():
    '''
    drawing the grid
    '''
    [pygame.draw.rect(screen,(78,78,78), grid_rects, 1) for grid_rects in grid_squares]             # drawing grid from grid_square list

def move(y_offset,x_offset):     
    '''
    moves rects vertical per keydown and with constant speed downwards
    '''
    return [[pygame.Rect(x*square+screen_x/2-square+x_offset,y*square+y_offset,square,square) for x,y in tetrect_pos] for tetrect_pos in tetrominos_positions]

def collide_left():
    '''
    returns bool about whether the current tetromino collides with the left border
    '''
    for rect in moving_tetromino:
        if rect.x >= screen_x - square:
            return True  #collision with left border
    return False  #no collision with left border

def collide_right():
    '''
    returns bool about whether the current tetromino collides with the left border
    '''
    for rect in moving_tetromino:
        if rect.x <= 0:
            return True  #collision with right border
    return False  #no collision with right border

def collide_landed():
    '''
    returns bool about whether the current tetromino collides with another tetromino that already landed
    (rects relate to the points in the upper left corner, so we have to check whether the tetromino will touch the ground in the next step)
    '''
    global running #important because the variables in functions are only local if we don't set them global
    for rect in moving_tetromino:
        collision_rect = rect.copy()  #create copy of the rect
        collision_rect.y += square  #move rect one square down
        for list in landed_tetrominos:
            if collision_rect.collidelist(list) != -1 and not rect.y == 0:
                #collidelist returns index of the first colliding figure and -1 if theres no collision
                return True  #no collision with tetromino that has already landed in the next square
            elif collision_rect.collidelist(list) != -1 and rect.y == 0:
                running = False    
    return False  #collision with tetromino that has already landed in the next square

def collide_ground():
    '''
    returns bool about whether the current tetromino touches the ground
    '''
    for rect in moving_tetromino:
        if rect.bottom==screen_y:
            return True
    return False

def rotate_tetromino():
    '''
    Rotates the current tetromino clockwise
    '''
    rotated_positions = tetrominos_positions[tets].copy() #copy the rect positions of the current tetronimo
    for i in range(len(rotated_positions)):  
            x,y = rotated_positions[i]      #read x,y-positions from the rects of the current tetronimo
            rotated_positions[i] = y,-x     #rotate x,y-positons
    if not collide_left() and not collide_right():          #only rotate when not collide with the right or left border
        tetrominos_positions[tets] = rotated_positions

def full_rows():
    '''
    find full_rows and delete them 
    '''

    rows_to_remove = [row for row in range(screen_y - square, 0, -square) if sum(1 for tets in landed_tetrominos for rect in tets if rect.y == row) == squares_width]

    #append rects with y-value from row_to_remove list ro rects_to_remove list then remove rects from rects_to_remove list from the landed tetronimos list
    for row in rows_to_remove:
        for tets in landed_tetrominos:
            rects_to_remove = []
            [rects_to_remove.append(rect) for rect in tets if rect.y == row]
            [tets.remove(rect) for rect in rects_to_remove]
        for tets in landed_tetrominos: #move all the rects above the deleted row one square downwards
            for rect in tets:
                if rect.y <= row:
                    rect.y += square 

#more variables


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            #difference to pygame.key.get_pressed : checks how often a key gets pressed
            if event.key == pygame.K_LEFT and not collide_right():
                #moving the current tetromino one square to the left for every time pressing left if tetromino isn't already at the right border
                x_offset -= square
            elif event.key == pygame.K_RIGHT and not collide_left():
                #moving the current tetromino one square to the right for every time pressing right if tetromino isn't already at the right border
                x_offset += square
            #elif event.key == pygame.K_DOWN:
                #code to fasten up the tetromino to the ground
            elif event.key == pygame.K_UP:
                rotate_tetromino()
        

    screen.fill("black")


    #drawing the current moving tetromino
    moving_tetromino = [pygame.draw.rect(screen,tetromino_colors[tets],rects) for rects in move(y_offset,x_offset)[tets]]
    


    if not collide_ground() and not collide_landed():
        #continue to move down if there's no collision with the ground or a landed tetromino
        y_offset+=square
    else:
        #if there's a collision adding tetromino to the landed tetrominos
        landed_tetrominos.extend([moving_tetromino])
        colours_landed.extend([tetromino_colors[tets]])
        tets_next=random.randint(0,6)
        if tets_next!=tets:
            tets = tets_next
        else:
            if tets_next!=6:
                tets_next+=1
            else:
                tets_next-=1
            tets = tets_next
        
        y_offset,x_offset=0,0 #returning to start position for the new tetromino    
        x_offset=0
        moving_tetromino=[] #only one moving tetromino 

    #drawing the landed tetrominos
    [pygame.draw.rect(screen,colours_landed[i],landed_tetrominos[i][j]) for i in range(len(landed_tetrominos)) for j in range(len(landed_tetrominos[i]))]

    full_rows()

    draw_grid()

    pygame.display.flip()
    clock.tick(5)

pygame.quit()