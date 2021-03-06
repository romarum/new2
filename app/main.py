from AStar import *
import bottle
import copy
import math
import os
import sys

SNEK_BUFFER = 3
ID = 'new2'
SNAKE = 1
WALL = 2
FOOD = 5
GOLD = 7

SAFTEY = 3

def goals(data):
    result = data['food']
    if data['mode'] == 'advanced':
        result.extend(data['gold'])
    return result


def direction(from_cell, to_cell):
    dx = to_cell[0] - from_cell[0]
    dy = to_cell[1] - from_cell[1]

    if dx == 1:
        return 'right'
    elif dx == -1:
        return 'left'
    elif dy == -1:
        return 'up'
    elif dy == 1:
        return 'down'

def distance(p, q):
    dx = abs(p[0] - q[0])
    dy = abs(p[1] - q[1])
    return dx + dy;

def closest(items, start):
    closest_item = None
    closest_distance = 10000

    # TODO: use builtin min for speed up
    for item in items:
        item_distance = distance(start, item)
        if item_distance < closest_distance:
            closest_item = item
            closest_distance = item_distance

    return closest_item

def init(data):
    print('data is ', data)
    allsnakes=[];
    mysnakeID = data['you']['id']
    snakes  = data['snakes']
    print('snakes are ', snakes)
    width  = data ['width']
    height = data ['height']
    print('width ', width)
    print('height ', height)
    grid = [[0 for col in xrange(data['height'])] for row in xrange(data['width'])]
    for snek in data['snakes']['data']:
        snekCoords = []
        if snek['id']==mysnakeID:
            mysnake = snek
            allsnakes.append(snek)
            print('My snake is ', mysnake)
        for coord in snek['body']['data']:
            grid[coord['x']][coord['y']] = SNAKE
            snekCoords.append([coord['x'],coord['y']])
        snek['coords'] = snekCoords
#    if data['mode'] == 'advanced':
#        for wall in data['walls']:
#            grid[wall[0]][wall[1]] = WALL
#        for g in data['gold']:
#            grid[g[0]][g[1]] = GOLD

    for food in data['food']['data']:
        grid[food['x']][food['y']] = FOOD
    return mysnake, allsnakes, grid

@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.get('/')

def index():
    print ('WORKING ON GET REQUEST')
    head_url = '%s://%s/static/Traitor.gif' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )
    return {
        'color': '#00ff00',
        'head': head_url
    }


@bottle.post('//start')
def start():
    data = bottle.request.json

    # TODO: Do things with data
    print ('WORKING ON START REQUEST')

    return {
        'name': 'Daredevils',
        'color': '#4265F4',
        'head_type': 'fang',
        'tail_type': 'regular',
        'taunt': 'battlesnake-python!',
        'secondary_color': '#FF00FF'
    }

@bottle.post('//move')
def move():
    print ('PRINTING DATA')
    data = bottle.request.json
    print (data)

    snek, allsnakes, grid = init(data)
    ID = snek['id']

    #data['mode'] = 'beginner'
    #foreach snake
    for enemy in allsnakes:
        print('Snake ', enemy)
        if (enemy['id'] == ID):
            ourHealth = enemy['health']
            print('ourHealth is ', ourHealth)
            #print('our snake is ', enemy)
            continue
        
        #print "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"        
        #grid[enemy['coords'][0][0]*2-enemy['coords'][1][0]][enemy['coords'][0][1]*2 - enemy['coords'][1][1]] = GOLD
        #data['gold'].append([enemy['coords'][0][0]*2 - enemy['coords'][1][0],enemy['coords'][0][1]*2 - enemy['coords'][1][1]])

   
        #if distance(snek['coords'][0], enemy['coords'][0]) > SNEK_BUFFER:
        #    continue

        
        if (len(enemy['coords']) >= len(snek['coords'])-1):
            #dodge
            #try:
                #if enemy['coords'][0][1] < data['height']-1:
                #grid[enemy['coords'][0][0]][enemy['coords'][0][1]+1] = SAFTEY             
                #if enemy['coords'][0][1] > 0:
                #grid[enemy['coords'][0][0]][enemy['coords'][0][1]-1] = SAFTEY
                #if enemy['coords'][0][0] < data['width']-1:
                #grid[enemy['coords'][0][0]+1][enemy['coords'][0][1]] = SAFTEY
                #if enemy['coords'][0][0] > 0:
                #grid[enemy['coords'][0][0]-1][enemy['coords'][0][1]] = SAFTEY
                
            #try:
                #grid[enemy['coords'][0][0]][enemy['coords'][0][1]] = SAFTEY
            #except:
            #    pass
            try:
                grid[enemy['coords'][0][0]][enemy['coords'][0][1]+1] = SAFTEY
            except:
                pass
            try:
                grid[enemy['coords'][0][0]][enemy['coords'][0][1]-1] = SAFTEY
            except:
                pass
            try:
                grid[enemy['coords'][0][0]+1][enemy['coords'][0][1]] = SAFTEY
            except:
                pass
            try:
                grid[enemy['coords'][0][0]-1][enemy['coords'][0][1]] = SAFTEY
            except:
                pass
            try:
                grid[enemy['coords'][0][0]+1][enemy['coords'][0][1]+1] = SAFTEY
            except:
                pass
            try:
                grid[enemy['coords'][0][0]-1][enemy['coords'][0][1]-1] = SAFTEY
            except:
                pass
            try:
                grid[enemy['coords'][0][0]+1][enemy['coords'][0][1]-1] = SAFTEY
            except:
                pass
            try:
                grid[enemy['coords'][0][0]-1][enemy['coords'][0][1]+1] = SAFTEY
            except:
                pass
            grid[enemy['coords'][1][0]][enemy['coords'][1][1]] = 1
            grid[enemy['coords'][0][0]][enemy['coords'][0][1]] = 1
            
            #for cords in enemy['coords']:
             #   x=cords[0]
              #  y=cords[1]
               # try:
               #     grid[x-1][y] = SAFTEY
               # except:
               #     pass
               # try:
               #     grid[x+1][y] = SAFTEY
               # except:
               #     pass
               # try:
               #     grid[x][y-1] = SAFTEY
               # except:
               #     pass
               # try:
               #     grid[x][y+1] = SAFTEY
               # except:
               #     pass

            

    #print('grid is ',grid)
    snek_head = snek['coords'][0]
    #print('snekHead is ', snek['coords'][0])
    #print('snek head makred as ', grid[snek['coords'][0][0]][snek['coords'][0][1]])
    snek_neck = snek['coords'][1]
    snek_coords = snek['coords']
    print('snake coords are ', snek_coords)
    path = None
    middle = [data['width'] / 2, data['height'] / 2]
    #foods = sorted(data['food'], key = lambda p: distance(p,snek_head ))
    #golds = sorted(data['gold'], key = lambda p: distance(p,snek_head ))

    bestScore=4
    if (ourHealth > 100):
        bestScore=10
        
    bestGoals=[]
    print('best goals are',bestGoals)
    #print grid
    for col in xrange(data['height']):
        for row in xrange(data['width']):
            if grid[row][col]> bestScore:
                bestScore = grid[row][col]
                
    for col in xrange(data['height']):
        for row in xrange(data['width']):
            if grid[row][col]== bestScore:
                bestGoals.append([row,col])
                
    #print "BS",bestScore
    #print "BG",bestGoals   
    
    ##print foods
    #if data['mode'] == 'advanced':
        #foods = data['gold'] + foods #+ heads
        #print("")
    foods = sorted(bestGoals, key = lambda p: distance(p,snek_head ))
    print('best goals are ', foods)
        
    for food in foods:
        ##print food
        tentative_path = a_star(snek_head, food, grid, snek_coords)
        
        if not tentative_path:
            print ('no path to food')
            continue

        print('for food ', food)
        print('temporary path is ', tentative_path)
        
        path_length = len(tentative_path)
        snek_length = len(snek_coords) + 1
        print('this path has length is ', path_length)
        #dead = False
        #for enemy in data['snakes']:
        #    if enemy['id'] == ID:
        #        continue
        #    if path_length > distance(enemy['coords'][0], food):
        #        dead = True
        #if dead:
        #    continue

        # Update snek
        print('after path length 0')
        print('path length is ', path_length)
        print('snek length is ', snek_length)
        if path_length < snek_length:
            remainder = snek_length - path_length
            new_snek_coords = list(reversed(tentative_path)) + snek_coords[:remainder]
        else:
            new_snek_coords = list(reversed(tentative_path))[:snek_length]

        if grid[new_snek_coords[0][0]][new_snek_coords[0][1]] == FOOD:
            # we ate food so we grow
            new_snek_coords.append(new_snek_coords[-1])

        # Create a new grid with the updates snek positions
        new_grid = copy.deepcopy(grid)

        for coord in snek_coords:
            new_grid[coord[0]][coord[1]] = 0
        for coord in new_snek_coords:
            new_grid[coord[0]][coord[1]] = SNAKE

        ##printg(grid, 'orig')
        ##printg(new_grid, 'new')

        ##print snek['coords'][-1]
        foodtotail = a_star(food,new_snek_coords[-1],new_grid, new_snek_coords)
        if foodtotail:
            path = tentative_path
            break
        ##print "no path to tail from food"

    ##print grid
    print('path before if ',path)
    if not path:
        path = a_star(snek_head, snek['coords'][-1], grid, snek_coords)
    print('path after if ',path)

    despair = not (path and len(path) > 1)
    print('despair first time', despair)

    if despair:
        for neighbour in neighbours(snek_head,grid,0,snek_coords, [1,2,3]):
            path = a_star(snek_head, neighbour, grid, snek_coords)
            print ('i\'m scared')
            break

    despair = not (path and len(path) > 1)

    print('despair second time time', despair)
    if despair:
        for neighbour in neighbours(snek_head,grid,0,snek_coords, [1,2]):
            path = a_star(snek_head, neighbour, grid, snek_coords)
            print ('lik so scared')
            break

    print('path before asserts ', path)
    if path:
        assert path[0] == tuple(snek_head)
        assert len(path) > 1

    print('path after asserts ', path)
    print(grid)
    moveTo = ''
    try:
        moveTo = direction(path[0], path[1])
        print('move to from try ',moveTo)
    
    except:
        try:
            if (grid[snek['coords'][0][0] + 1][snek['coords'][0][1]] != 1):
                moveTo = "right"
        except:
            pass
        try:
            if (grid[snek['coords'][0][0] - 1][snek['coords'][0][1]] != 1):
                moveTo = "left"
        
        except:
            pass
        try:
            if (grid[snek['coords'][0][0]][snek['coords'][0][1]+1] != 1):
                moveTo = "down"
        except:
            pass
        try:
            if (grid[snek['coords'][0][0]][snek['coords'][0][1]-1] != 1):
                moveTo = "up"
        except:
            pass
        print('move to ',moveTo)
    return {
        'move': moveTo,
        'taunt': 'Whatever'
    }
    

@bottle.post('/end')
def end():
    data = bottle.request.json

    # TODO: Do things with data

    return {
        'taunt': 'battlesnake-python!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
