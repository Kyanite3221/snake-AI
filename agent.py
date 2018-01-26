from gameobjects import GameObject
from move import Direction
from move import Move


class Agent:
    def __init__(self):
        self.head_position = None
        self.snake_body = []

    global target_food
    global own_head
    global runs
    global points
    global scorenow
    global time
    own_head=[]
    runs = 0
    points = 0
    target_food=[]
    time=5
    def get_move(self, board, score, turns_alive, turns_to_starve, direction):
        """This function behaves as the 'brain' of the snake. You only need to change the code in this function for
        the project. Every turn the agent needs to return a move. This move will be executed by the snake. If this
        functions fails to return a valid return (see return), the snake will die (as this confuses its tiny brain
        that much that it will explode). The starting direction of the snake will be North.

        :param board: A two dimensional array representing the current state of the board. The upper left most
        coordinate is equal to (0,0) and each coordinate (x,y) can be accessed by executing board[x][y]. At each
        coordinate a GameObject is present. This can be either GameObject.EMPTY (meaning there is nothing at the
        given coordinate), GameObject.FOOD (meaning there is food at the given coordinate), GameObject.WALL (meaning
        there is a wall at the given coordinate. TIP: do not run into them), GameObject.SNAKE_HEAD (meaning the head
        of the snake is located there) and GameObject.SNAKE_BODY (meaning there is a body part of the snake there.
        TIP: also, do not run into these). The snake will also die when it tries to escape the board (moving out of
        the boundaries of the array)

        :param score: The current score as an integer. Whenever the snake eats, the score will be increased by one.
        When the snake tragically dies (i.e. by running its head into a wall) the score will be reset. In ohter
        words, the score describes the score of the current (alive) worm.

        :param turns_alive: The number of turns (as integer) the current snake is alive.

        :param turns_to_starve: The number of turns left alive (as integer) if the snake does not eat. If this number
        reaches 1 and there is not eaten the next turn, the snake dies. If the value is equal to -1, then the option
        is not enabled and the snake can not starve.

        :param direction: The direction the snake is currently facing. This can be either Direction.NORTH,
        Direction.SOUTH, Direction.WEST, Direction.EAST. For instance, when the snake is facing east and a move
        straight is returned, the snake wil move one cell to the right.

        :return: The move of the snake. This can be either Move.LEFT (meaning going left), Move.STRAIGHT (meaning
        going straight ahead) and Move.RIGHT (meaning going right). The moves are made from the viewpoint of the
        snake. This means the snake keeps track of the direction it is facing (North, South, West and East).
        Move.LEFT and Move.RIGHT changes the direction of the snake. In example, if the snake is facing north and the
        move left is made, the snake will go one block to the left and change its direction to west.
        """
        global scorenow
        global own_head
        global target_food
        global time
        scorenow=score

        if (self.head_position == None):
            self.head_position = self.find_head(board)
            self.snake_body.insert(0, self.head_position)

        coordinates=[]

        """find food and head or take them from the global variables"""
        if (len(own_head)<1 and len(target_food)<1) \
                or ( len(own_head)>0 and own_head[0]==target_food[0] and own_head[1]==target_food[1] ) or time == 0:
            coordinates=locate_food(board,0)
            own_head = coordinates[:2]
            target_food = coordinates[2:]
            time=1
        else:
            coordinates=list(own_head)
            coordinates.append(target_food[0])
            coordinates.append(target_food[1])


        """first two are for the snake, the other two are for the nearest food"""
        """print('snake head is on',coordinates[0],',',coordinates[1],'\nnearest Food',coordinates[2],',',coordinates[3])
"""
        desision = a_star_search(board, coordinates, direction)

        result = self.determine_direction(desision, direction)

        """update the snake's head location"""
        self.update_location(direction, own_head, result)
        time-=1

        self.head_position = (own_head[0], own_head[1])
        self.snake_body.insert(0, self.head_position)
        if (not board[own_head[x]][own_head[y]] == GameObject.FOOD):
            del self.snake_body[-1]

        return result

    def determine_direction(self, desision, direction):
        if direction == desision:
            """print("Goal is straight ahead", direction,desision)"""

            result = Move.STRAIGHT
        if direction == Direction.NORTH:
            if desision == Direction.EAST:
                """print("Goal is to the right")"""
                result = Move.RIGHT
            elif desision == Direction.SOUTH:
                """print("\n!!!!!!!!!!!!!!!!!NOT YET IMPLEMENTED!!!!!!!!!!!!!!!!!!!!!!\n")"""
                # I want it to go to the biggest open space and slither through it
                result = Move.RIGHT
            elif desision == Direction.WEST:
                """print("Goal is to the left")"""
                result = Move.LEFT

        elif direction == Direction.EAST:
            if desision == Direction.SOUTH:
                """print("Goal is to the right")"""
                result = Move.RIGHT
            elif desision == Direction.WEST:
                """print("\n!!!!!!!!!!!!!!!!!NOT YET IMPLEMENTED!!!!!!!!!!!!!!!!!!!!!!\n")"""
                # I want it to go to the biggest open space and slither through it
                result = Move.RIGHT
            elif desision == Direction.NORTH:
                """print("Goal is to the left")"""
                result = Move.LEFT

        elif direction == Direction.SOUTH:
            if desision == Direction.WEST:
                """print("Goal is to the right")"""
                result = Move.RIGHT
            elif desision == Direction.NORTH:
                """print("\n!!!!!!!!!!!!!!!!!NOT YET IMPLEMENTED!!!!!!!!!!!!!!!!!!!!!!\n")"""
                # I want it to go to the biggest open space and slither through it
                result = Move.RIGHT
            elif desision == Direction.EAST:
                """print("Goal is to the left")"""
                result = Move.LEFT

        elif direction == Direction.WEST:
            if desision == Direction.NORTH:
                """print("Goal is to the right")"""
                result = Move.RIGHT
            elif desision == Direction.EAST:
                """print("\n!!!!!!!!!!!!!!!!!NOT YET IMPLEMENTED!!!!!!!!!!!!!!!!!!!!!!\n")"""
                # I want it to go to the biggest open space and slither through it
                result = Move.RIGHT
            elif desision == Direction.SOUTH:
                """print("Goal is to the left")"""
                result = Move.LEFT
        return result

    def update_location(self, direction, own_head, result):
        if result == Move.STRAIGHT:
            if direction == Direction.NORTH:
                own_head[1] -= 1
            elif direction == Direction.EAST:
                own_head[0] += 1
            elif direction == Direction.SOUTH:
                own_head[1] += 1
            elif direction == Direction.WEST:
                own_head[0] -= 1

        elif result == Move.LEFT:
            if direction == Direction.NORTH:
                """moving West next"""
                own_head[0] -= 1
            elif direction == Direction.EAST:
                """moving North next"""
                own_head[1] -= 1
            elif direction == Direction.SOUTH:
                """moving East next"""
                own_head[0] += 1
            elif direction == Direction.WEST:
                """moving South next"""
                own_head[1] += 1

        elif result == Move.RIGHT:
            if direction == Direction.NORTH:
                """moving East next"""
                own_head[0] += 1
            elif direction == Direction.EAST:
                """moving South next"""
                own_head[1] += 1
            elif direction == Direction.SOUTH:
                """moving West next"""
                own_head[0] -= 1
            elif direction == Direction.WEST:
                """moving North next"""
                own_head[1] -= 1

    def on_die(self):
        """This function will be called whenever the snake dies. After its dead the snake will be reincarnated into a
        new snake and its life will start over. This means that the next time the get_move function is called,
        it will be called for a fresh snake. Use this function to clean up variables specific to the life of a single
        snake or to host a funeral.
        """
        print('noob')
        global own_head
        global target_food
        global points
        global runs
        global scorenow
        print("own head:",own_head,"\ntarget food:",target_food)
        target_food=[]
        own_head = []
        runs+=1
        points+=scorenow
        scorenow = 0
        print("this is the ",runs," th run.\nAverage points:",points/runs)

        pass

def locate_food(board,indicator):
    """here I determine where the nearest food is"""
    snakex=0
    snakey=0
    foodx=[]
    foody=[]
    """find all food and the head of the snek"""
    for x in range(len(board)):
        for y in range(len(board)):
            if board[x][y] == GameObject.SNAKE_HEAD:
                snakex=x
                snakey=y
            if board[x][y] == GameObject.FOOD:
                foodx.append(x)
                foody.append(y)
            y+=1
        x+=1

    """"find nearest food"""
    distance = 9999
    chosenfood=0
    for i in range(len(foodx)):
        curdistance = h([snakex,snakey],[foodx[i],foody[i]])
        if curdistance < distance:
            chosenfood=i
            distance= curdistance

    return [snakex,snakey,foodx[chosenfood],foody[chosenfood]]

def a_star_search(board,coordinates,direction):
    checked=[]
    queue=[]
    """expand the head node of the snake"""
    if coordinates[0]+1 < len(board) \
            and (board[coordinates[0]+1][coordinates[1]] == GameObject.EMPTY
                 or board[coordinates[0]+1][coordinates[1]] == GameObject.FOOD):
        queue.append([coordinates[0]+1,coordinates[1],h([coordinates[0]+1,coordinates[1]],[coordinates[2],coordinates[3]]), Direction.EAST,1])
        checked.append([coordinates[0]+1,coordinates[1]])
    """east"""

    if coordinates[1] + 1 < len(board)and (board[coordinates[0]][coordinates[1]+1] == GameObject.EMPTY
                 or board[coordinates[0]][coordinates[1]+1] == GameObject.FOOD):
        heur = h([coordinates[0],coordinates[1]+1],[coordinates[2],coordinates[3]])
        if len(queue)>0 and heur < queue[0][2]:
            queue.insert(0,[coordinates[0], coordinates[1] + 1,
                          heur, Direction.SOUTH,1])
        else:
            counter = 0
            while counter<len(queue) and heur > queue[counter][2]:
                counter+=1
            if counter<len(queue):
                queue.insert(counter, [coordinates[0], coordinates[1] + 1, heur, Direction.SOUTH,1])
            else:
                queue.append([coordinates[0], coordinates[1] + 1, heur, Direction.SOUTH,1])
                """South"""
        checked.append([coordinates[0], coordinates[1] + 1])

    if coordinates[0] - 1 >= 0 and (board[coordinates[0]-1][coordinates[1]] == GameObject.EMPTY
                 or board[coordinates[0]-1][coordinates[1]] == GameObject.FOOD):
        heur = h([coordinates[0] - 1, coordinates[1]], [coordinates[2], coordinates[3]])
        if len(queue)>0 and heur < queue[0][2]:
            queue.insert(0,[coordinates[0] - 1, coordinates[1],
                           heur, Direction.WEST,1])
        else:
            counter = 1
            while counter < len(queue) and heur > queue[counter][2]:
                counter += 1
            if counter < len(queue):
                queue.insert(counter, [coordinates[0] - 1, coordinates[1], heur, Direction.WEST,1])
            else:
                queue.append([coordinates[0] - 1, coordinates[1], heur, Direction.WEST,1])
                """West"""
        checked.append([coordinates[0] - 1, coordinates[1]])

    if coordinates[1] - 1 >= 0 and (board[coordinates[0]][coordinates[1]-1] == GameObject.EMPTY
                 or board[coordinates[0]][coordinates[1]-1] == GameObject.FOOD):
        heur = h([coordinates[0], coordinates[1] - 1],[ coordinates[2], coordinates[3]])
        if len(queue)>0 and heur < queue[0][2]:
            queue.insert(0,[coordinates[0], coordinates[1] - 1,
                           heur, Direction.NORTH,1])
        else:
            counter = 1
            while counter < len(queue) and heur > queue[counter][2]:
                counter += 1
            if counter < len(queue):
                queue.insert(counter, [coordinates[0], coordinates[1] - 1, heur, Direction.NORTH,1])
            else:
                queue.append([coordinates[0], coordinates[1] - 1, heur, Direction.NORTH,1])
                """North"""
        checked.append([coordinates[0], coordinates[1] - 1])

    """first nodes expanded"""
    """print(node_depth," node level expanded:", queue)"""


    """This is where the true a* part comes into play"""
    while len(queue)>0 and board[queue[0][0]][queue[0][1]] != GameObject.FOOD:
        currentNode=queue.pop(0)
        # print (currentNode)
        # check the north:
        if currentNode[1]-1 >= 0 \
            and (board[currentNode[0]][currentNode[1]-1] == GameObject.EMPTY
                       or board[currentNode[0]][currentNode[1]-1] == GameObject.FOOD) \
            and not checked.__contains__([currentNode[0],currentNode[1]-1]):
            checked.append([currentNode[0],currentNode[1]-1])
            # print(checked)
            value = f([currentNode[0],currentNode[1]-1],coordinates[2:4],currentNode[4])
            counter = 0
            while counter < len(queue) and value > queue[counter][2]:
                counter += 1
            if counter < len(queue):
                queue.insert(counter,[currentNode[0],currentNode[1]-1,value,currentNode[3],currentNode[4]+1])
            else:
                queue.append([currentNode[0],currentNode[1]-1,value,currentNode[3],currentNode[4]+1])

        # check the east
        if currentNode[0]+1 <len(board) \
            and (board[currentNode[0]+1][currentNode[1]] == GameObject.EMPTY
                       or board[currentNode[0]+1][currentNode[1]] == GameObject.FOOD) \
            and not checked.__contains__([currentNode[0]+1,currentNode[1]]):
            checked.append([currentNode[0]+1,currentNode[1]])
            # print(checked)
            value = f([currentNode[0]+1,currentNode[1]],coordinates[2:4],currentNode[4])
            counter = 0
            while counter < len(queue) and value > queue[counter][2]:
                counter += 1
            if counter < len(queue):
                queue.insert(counter,[currentNode[0]+1,currentNode[1],value,currentNode[3],currentNode[4]+1])
            else:
                queue.append([currentNode[0]+1,currentNode[1],value,currentNode[3],currentNode[4]+1])

        # check the south
        if currentNode[1]+1 < len(board) \
            and (board[currentNode[0]][currentNode[1]+1] == GameObject.EMPTY
                       or board[currentNode[0]][currentNode[1]+1] == GameObject.FOOD) \
            and not checked.__contains__([currentNode[0],currentNode[1]+1]):
            checked.append([currentNode[0],currentNode[1]+1])
            # print(checked)
            value = f([currentNode[0],currentNode[1]+1],coordinates[2:4],currentNode[4])
            counter = 0
            while counter < len(queue) and value > queue[counter][2]:
                counter += 1
            if counter < len(queue):
                queue.insert(counter,[currentNode[0],currentNode[1]+1,value,currentNode[3],currentNode[4]+1])
            else:
                queue.append([currentNode[0],currentNode[1]+1,value,currentNode[3],currentNode[4]+1])

        # check the west
        if currentNode[0]-1 >= 0 \
            and (board[currentNode[0]-1][currentNode[1]] == GameObject.EMPTY
                       or board[currentNode[0]-1][currentNode[1]] == GameObject.FOOD) \
            and not checked.__contains__([currentNode[0]-1,currentNode[1]]):
            checked.append([currentNode[0]-1,currentNode[1]])
            # print(checked)
            value = f([currentNode[0]-1,currentNode[1]],coordinates[2:4],currentNode[4])
            counter = 0
            while counter < len(queue) and value > queue[counter][2]:
                counter += 1
            if counter < len(queue):
                queue.insert(counter,[currentNode[0]-1,currentNode[1],value,currentNode[3],currentNode[4]+1])
            else:
                queue.append([currentNode[0]-1,currentNode[1],value,currentNode[3],currentNode[4]+1])


    # print(queue)
    global own_head
    if len(queue) < 1:
        # print("no availible nodes")
        if own_head[1]>1 and board[own_head[0]][own_head[1]-1] == GameObject.EMPTY :
            return Direction.NORTH
        if own_head[1]+1<len(board) and board[own_head[0]][own_head[1]+1] == GameObject.EMPTY :
            return Direction.SOUTH
        if own_head[0]>1 and board[own_head[0]-1][own_head[1]] == GameObject.EMPTY :
            return Direction.WEST
        if own_head[0]+1<len(board) and board[own_head[0]+1][own_head[1]] == GameObject.EMPTY :
            return Direction.EAST
        return Direction.NORTH
    return queue[0][3]

def h(node,goal):
    """print("recieved node:",node[0],",",node[1],"\nand goal:",goal[0],",",goal[1])"""
    total = abs(node[0]-goal[0])+abs(node[1]-goal[1])
    """print( total)"""
    return total
def f(node,goal,previous_cost):
    return h(node,goal)+previous_cost

###############################THOMAS METHODS

    def find_head(self, board):
        for (i, x) in enumerate(board):
            if (GameObject.SNAKE_HEAD in x):
                return (i, x.index(GameObject.SNAKE_HEAD))

        return (-1, -1)

    def can_route_to_tail(self, position, direction, board):
        open_set = [position]
        closed_set = []

        parent_of = dict()
        cost_to = dict()
        cost_to_goal_through = dict()

        cost_to[position] = 0
        cost_to_goal_through[position] = self.estimate_heuristic(position, goal)
        parent_of[position] = (None, direction)

        while (len(open_set) > 0):
            d = {k:v for k, v in cost_to_goal_through.items() if k in open_set}
            parent_state = min(d, key=d.get)
            parent_direction = parent_of[parent_state][1]

            if (parent_state == goal):
                direction_to_goal = parent_of[goal][1]
                path_to_goal = [(goal, direction_to_goal)]

                while (not position == parent_of[path_to_goal[0][0]][0]):
                    parent_node = parent_of[path_to_goal[0][0]][0]
                    direction_to_parent = parent_of[parent_node][1]
                    path_to_goal.insert(0, (parent_node, direction_to_parent))

                return path_to_goal

            open_set.remove(parent_state)
            closed_set.insert(-1, parent_state)

            for (child_state, child_direction) in self.get_children(parent_state, board, parent_direction):
                if child_state in closed_set:
                    continue
                if child_state not in open_set:
                    open_set.insert(-1, child_state)

                tentative_cost = cost_to[parent_state] + 1
                if (child_state in cost_to and tentative_cost >= cost_to[child_state]):
                    continue

                parent_of[child_state] = (parent_state, child_direction)
                cost_to[child_state] = tentative_cost
                cost_to_goal_through[child_state] = tentative_cost + self.estimate_heuristic(child_state, goal)

        """failure"""
        return None

    def get_children(self, parent_state, board, direction):
        children = []

        for move in direction.get_xy_moves():
            child_state = tuple(map(sum, zip(parent_state, move))) #sum of two tuples	
            (x, y) = child_state
            if (not x in range(0, len(board)) or not y in range(0, len(board[0]))):
                continue

            game_object = board[x][y]
            if (not game_object == GameObject.WALL and not child_state in self.snake_body):
                children.insert(-1, (child_state, self.xy_to_direction(move)))

        return children
