from gameobjects import GameObject
from move import Direction
from move import Move


class Agent:
    global target_food
    global own_head
    own_head=[]
    target_food=[]
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
        global own_head
        global target_food
        coordinates=[]
        if (len(own_head)<1 and len(target_food)<1) \
                or ( len(own_head)>0 and own_head[0]==target_food[0] and own_head[1]==target_food[1]):
            print("updating head and body location")
            coordinates=locate_food(board,0)
            own_head = coordinates[:2]
            target_food = coordinates[2:]
        else:
            coordinates=list(own_head)
            coordinates.append(target_food[0])
            coordinates.append(target_food[1])


        """first two are for the snake, the other two are for the nearest food"""
        """print('snake head is on',coordinates[0],',',coordinates[1],'\nnearest Food',coordinates[2],',',coordinates[3])
"""
        desision = a_star_search(board, coordinates, direction)

        if direction == desision:
            """print("Goal is straight ahead", direction,desision)"""

            result = Move.STRAIGHT

        if direction == Direction.NORTH:
            if desision == Direction.EAST:
                """print("Goal is to the right")"""
                result = Move.RIGHT
            elif desision == Direction.SOUTH:
                """print("\n!!!!!!!!!!!!!!!!!NOT YET IMPLEMENTED!!!!!!!!!!!!!!!!!!!!!!\n")"""
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
                result = Move.RIGHT
            elif desision == Direction.SOUTH:
                """print("Goal is to the left")"""
                result = Move.LEFT

        """update the snake's head location"""
        if result == Move.STRAIGHT:
            if direction == Direction.NORTH:
                own_head[1]-=1
            elif direction == Direction.EAST:
                own_head[0]+=1
            elif direction == Direction.SOUTH:
                own_head[1]+=1
            elif direction == Direction.WEST:
                own_head[0]-=1

        elif result == Move.LEFT:
            if direction == Direction.NORTH:
                """moving West next"""
                own_head[0] -=1
            elif direction == Direction.EAST:
                """moving North next"""
                own_head[1]-=1
            elif direction == Direction.SOUTH:
                """moving East next"""
                own_head[0]+=1
            elif direction == Direction.WEST:
                """moving South next"""
                own_head[1]+=1

        elif result == Move.RIGHT:
            if direction == Direction.NORTH:
                """moving East next"""
                own_head[0]+=1
            elif direction == Direction.EAST:
                """moving South next"""
                own_head[1]+=1
            elif direction == Direction.SOUTH:
                """moving West next"""
                own_head[0]-=1
            elif direction == Direction.WEST:
                """moving North next"""
                own_head[1]-=1


        return result

    def on_die(self):
        """This function will be called whenever the snake dies. After its dead the snake will be reincarnated into a
        new snake and its life will start over. This means that the next time the get_move function is called,
        it will be called for a fresh snake. Use this function to clean up variables specific to the life of a single
        snake or to host a funeral.
        """
        print('kutnoob')
        global own_head
        global target_food
        target_food=[]
        own_head = []
        pass

def locate_food(board,indicator):
    """here I determine where the nearest food is"""
    snakex=0
    snakey=0
    foodx=[]
    foody=[]
    """find all food and the head of the snek"""
    for x in range(len(board)):
        for y in range(len(board[x])):
            if board[x][y] == GameObject.SNAKE_HEAD:
                snakex=x
                snakey=y
            if board[x][y] == GameObject.FOOD:
                foodx.append(x)
                foody.append(y)

    """"find nearest food"""
    distance = 9999
    chosenfood=0
    for i in range(len(foodx)):
        curdistance = h([snakex,snakey],[foodx[i],foody[i]])
        if curdistance < distance:
            chosenfood=i
            distance= curdistance

    if indicator == 1:
        print("!!!!!!!!!!!TODO!!!!!!!!!")
        final_food=0
        for i in range(len(foodx)):
            curdistance = abs(foodx[i] - snakex) + abs(foody[i] - snakey)
            if curdistance < distance and i != chosenfood:
                final_food = i
                distance = curdistance
        return [snakex, snakey, foodx[final_food], foody[final_food]]
    return [snakex,snakey,foodx[chosenfood],foody[chosenfood]]

def a_star_search(board,coordinates,direction):
    checked=[]
    queue=[]
    """expand the head node of the snake"""
    if coordinates[0]+1 < len(board) \
            and (board[coordinates[0]+1][coordinates[1]] == GameObject.EMPTY
                 or board[coordinates[0]+1][coordinates[1]] == GameObject.FOOD):
        queue.append([coordinates[0]+1,coordinates[1],h([coordinates[0]+1,coordinates[1]],[coordinates[2],coordinates[3]]), Direction.EAST])
    """east"""

    if coordinates[1] + 1 < len(board)and (board[coordinates[0]][coordinates[1]+1] == GameObject.EMPTY
                 or board[coordinates[0]][coordinates[1]+1] == GameObject.FOOD):
        heur = h([coordinates[0],coordinates[1]+1],[coordinates[2],coordinates[3]])
        if len(queue)>0 and heur < queue[0][2]:
            queue.insert(0,[coordinates[0], coordinates[1] + 1,
                          heur, Direction.SOUTH])
        else:
            counter = 0
            while counter<len(queue) and heur > queue[counter][2]:
                counter+=1
            if counter<len(queue):
                queue.insert(counter, [coordinates[0], coordinates[1] + 1, heur, Direction.SOUTH])
            else:
                queue.append([coordinates[0], coordinates[1] + 1, heur, Direction.SOUTH])
                """South"""

    if coordinates[0] - 1 >= 0 and (board[coordinates[0]-1][coordinates[1]] == GameObject.EMPTY
                 or board[coordinates[0]-1][coordinates[1]] == GameObject.FOOD):
        heur = h([coordinates[0] - 1, coordinates[1]], [coordinates[2], coordinates[3]])
        if len(queue)>0 and heur < queue[0][2]:
            queue.insert(0,[coordinates[0] - 1, coordinates[1],
                           heur, Direction.WEST])
        else:
            counter = 1
            while counter < len(queue) and heur > queue[counter][2]:
                counter += 1
            if counter < len(queue):
                queue.insert(counter, [coordinates[0] - 1, coordinates[1], heur, Direction.WEST])
            else:
                queue.append([coordinates[0] - 1, coordinates[1], heur, Direction.WEST])
                """West"""

    if coordinates[1] - 1 >= 0 and (board[coordinates[0]][coordinates[1]-1] == GameObject.EMPTY
                 or board[coordinates[0]][coordinates[1]-1] == GameObject.FOOD):
        heur = h([coordinates[0], coordinates[1] - 1],[ coordinates[2], coordinates[3]])
        if len(queue)>0 and heur < queue[0][2]:
            queue.insert(0,[coordinates[0], coordinates[1] - 1,
                           heur, Direction.NORTH])
        else:
            counter = 1
            while counter < len(queue) and heur > queue[counter][2]:
                counter += 1
            if counter < len(queue):
                queue.insert(counter, [coordinates[0], coordinates[1] - 1, heur, Direction.NORTH])
            else:
                queue.append([coordinates[0], coordinates[1] - 1, heur, Direction.NORTH])
                """North"""
    node_depth=1
    """first nodes expanded"""
    """print(node_depth," node level expanded:", queue)"""

    if len(queue) < 1:
        """print("no availible nodes")"""
        return Direction.NORTH
    return queue[0][3]

def h(node,goal):
    """print("recieved node:",node[0],",",node[1],"\nand goal:",goal[0],",",goal[1])"""
    total = abs(node[0]-goal[0])+abs(node[1]-goal[1])
    """print( total)"""
    return total