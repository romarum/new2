from AStar import *
import bottle
import copy
import math
import os
import sys

SNEK_BUFFER = 3
ID = ''
SNAKE = 1
WALL = 2
FOOD = 5
GOLD = 6
OLDMODE = False
SAFTEY = 3

def getTaunt():
    try:
        tauntArray = ["What the Fudge?", "I don\'t give a Donald Duck!", "Fudge nuggets","Son of a biscuit", "Son of a witch", "Tell your Mother to call me, she got the number", "Suck on my tail", "What kind of food is that? I am gonna puke", "Get out of my way", "You suck at this dude", "" ]
        tauntNumber = randint(0, len(tauntArray))
        returnTaunt = tauntArray[tauntNumber]
    
    except Exception:
        returnTaunt = "You got a problem?"

    return returnTaunt


def goals(data):
    result = data['food']
    #if data['mode'] == 'advanced':
    try:
        result.extend(data['gold'])
    except:
        print("no gold")
    return result


def direction(from_cell, to_cell):
    dx = to_cell[0] - from_cell[0]
    dy = to_cell[1] - from_cell[1]
	
    if (OLDMODE):
		
    	if dx == 1:
    		return 'east'
    	elif dx == -1:
    		return 'west'
    	elif dy == -1:
    		return 'north'
    	elif dy == 1:
    		return 'south'
    else:
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
    ID = data['you']
    grid = [[0 for col in xrange(data['height'])] for row in xrange(data['width'])]
	
    print "GRID WO SNAKES", grid
    for snek in data['snakes']:
        if snek['id']== ID:
            mysnake = snek
        for coord in snek['coords']:
            grid[coord[0]][coord[1]] = SNAKE
            print "GRID WITH SNAKES",grid

    ourHealth = 100
    #ourHealth = mysnake["health_points"]
    
    if (ourHealth > 60):
        FOOD = 4
    elif (ourHealth >= 40):
        FOOD = 5
    elif (ourHealth < 40):
        FOOD = 7
    print("***************")
    print(ourHealth)
    print(FOOD)
    print("***************")

    #if data['mode'] == 'advanced':
    if True:
        try:
            for wall in data['walls']:
                grid[wall[0]][wall[1]] = WALL
        except:
            print("no walls found")
        try:    
            for g in data['gold']:
                grid[g[0]][g[1]] = GOLD
        except:
            print("No gold")
        

    for f in data['food']:
        grid[f[0]][f[1]] = FOOD

    return mysnake, grid

@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.get('/')
def index():
    head_url = '%s://%s/static/Traitor.gif' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )
    return {
        'color': '#00ff00',
        'head': head_url
    }


@bottle.post('/start')
def start():
    data = bottle.request.json
    # TODO: Do things with data
    return {
        'name': 'Daredevils',
        'taunt': 'Let\'s CRUSH those worms!',
        'color': '#4286F4',
        'head_type': 'fang',
        'tail_type': 'regular'
    }
# DATA OBJECT
# {
#     "game": "hairy-cheese",
#     "mode": "advanced",
#     "turn": 4,
#     "height": 20,
#     "width": 30,
#     "snakes": [
#         <Snake Object>, <Snake Object>, ...
#     ],
#     "food": [
#         [1, 2], [9, 3], ...
#     ],
#     "walls": [    // Advanced Only
#         [2, 2]
#     ],
#     "gold": [     // Advanced Only
#         [5, 5]
#     ]
# }

#SNAKE
# {
#     "id": "1234-567890-123456-7890",
#     "name": "Well Documented Snake",
#     "status": "alive",
#     "message": "Moved north",
#     "taunt": "Let's rock!",
#     "age": 56,
#     "health": 83,
#     "coords": [ [1, 1], [1, 2], [2, 2] ],
#     "kills": 4,
#     "food": 12,
#     "gold": 2
# }

@bottle.post('/move')
def move():
    data = bottle.request.json
    snek, grid = init(data)

    #foreach snake
    for enemy in data['snakes']:
        if (enemy['id'] == ID):
            continue
        
        print "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"        
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
                
            try:
                grid[enemy['coords'][0][0]][enemy['coords'][0][1]] = SAFTEY
            except:
                pass
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
            
    snek_head = snek['coords'][0]
    snek_neck = snek['coords'][1]
    snek_coords = snek['coords']
    path = None
    middle = [data['width'] / 2, data['height'] / 2]
    foods = sorted(data['food'], key = lambda p: distance(p,snek_head ))
    print('foods is ', foods)
    #golds = sorted(data['gold'], key = lambda p: distance(p,snek_head ))
    bestScore=4
    bestGoals=[]
    #print grid
    for col in xrange(data['height']):
        for row in xrange(data['width']):
            if grid[row][col]> bestScore:
                bestScore = grid[row][col]
                
    for col in xrange(data['height']):
        for row in xrange(data['width']):
            if grid[row][col]== bestScore:
                bestGoals.append([row,col])
                
    print "BS",bestScore
    print "BG",bestGoals   
    
    #print foods
    if True:
        #data['mode'] == 'advanced':
        #foods = data['gold'] + foods #+ heads
        
        foods = sorted(bestGoals, key = lambda p: distance(p,snek_head ))

    
    for food in foods:
        #print food
        tentative_path = a_star(snek_head, food, grid, snek_coords)
        if not tentative_path:
            #print "no path to food"
            continue

        path_length = len(tentative_path)
        snek_length = len(snek_coords) + 1
		
        
        #dead = False
        #for enemy in data['snakes']:
        #    if enemy['id'] == ID:
        #        continue
        #    if path_length > distance(enemy['coords'][0], food):
        #        dead = True
        #if dead:
        #    continue

        # Update snek
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

        #printg(grid, 'orig')
        #printg(new_grid, 'new')

        #print snek['coords'][-1]
        foodtotail = a_star(food,new_snek_coords[-1],new_grid, new_snek_coords)
        if foodtotail:
            path = tentative_path
            break
        #print "no path to tail from food"

    #print grid
    print('path before if not path', path)
    if not path:
        path = a_star(snek_head, snek['coords'][-1], grid, snek_coords)

    
    print('path after if not path', path)
    
    despair = not (path and len(path) > 1)

    if despair:
        for neighbour in neighbours(snek_head,grid,0,snek_coords, [1,2,3]):
            path = a_star(snek_head, neighbour, grid, snek_coords)
            #print 'i\'m scared'
            break

    despair = not (path and len(path) > 1)


    if despair:
        for neighbour in neighbours(snek_head,grid,0,snek_coords, [1,2]):
            path = a_star(snek_head, neighbour, grid, snek_coords)
            #print 'lik so scared'
            break

    if path:
        assert path[0] == tuple(snek_head)
        assert len(path) > 1
    taunt = getTaunt()
    print('path is ', path)
    print(taunt)
	
    return {
        'move': direction(path[0], path[1]),
        'taunt': taunt
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
