from gameobjects import GameObject
from move import Move, Direction


class Agent:
    def __init__(self):
        self.calculated_path = []
        self.head_position = None
        self.snake_body = []

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

        if (self.head_position == None):
            self.head_position = self.find_head(board)
            self.snake_body.insert(0, self.head_position)

        if len(self.calculated_path) < 1:
            #tail_position = board.snake.body_parts[-1]
            for food_location in self.locate_food(board):
                calculated_path = self.calculate_path(self.head_position, food_location, board, direction)
                if not calculated_path == None:
                    self.calculated_path = calculated_path
                    break

        if (len(self.calculated_path) < 1):
            return Move.STRAIGHT

        next_step = self.calculated_path[0][1]
        self.head_position = self.calculated_path[0][0]
        del self.calculated_path[0]

        self.snake_body.insert(0, self.head_position)
        (head_x, head_y) = self.head_position
        if (not board[head_x][head_y] == GameObject.FOOD):
            del self.snake_body[-1]

        return self.move_in_direction(direction, next_step)

    def calculate_path(self, position, goal, board, direction):
        open_set = [position]
        closed_set = []

        parent_of = dict()
        cost_to = dict()
        cost_to_goal_through = dict()

        cost_to[position] = 0
        cost_to_goal_through[position] = self.estimate_heuristic(position, goal)
        parent_of[position] = (None, direction)

        while (len(open_set) > 0) :
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
            child_state = tuple(map(sum, zip(parent_state, move)))	
            (x, y) = child_state
            if (not x in range(0, len(board)) or not y in range(0, len(board[0]))):
                continue

            game_object = board[x][y]
            if (game_object == GameObject.EMPTY or game_object == GameObject.FOOD):
                children.insert(-1, (child_state, self.xy_to_direction(move)))

        return children

    def estimate_heuristic(self, position, goal):
        (x1, y1) = position
        (x2, y2) = goal
        return abs(x1 - x2) + abs(y1 - y2)

    def move_in_direction(self, current_direction, desired_direction):
        move_value = desired_direction.value - current_direction.value
        if (move_value**2 == 9):
            move_value = -(move_value / 3)
        elif (move_value**2 == 4):
            """trying to do illegal move..."""
            move_value = 0
        return Move(move_value)

    def xy_to_direction(self, xy):
        (x, y) = xy
        direction_value = x**2 * (-x + 2) + y**2 * (y + 1)
        return Direction(direction_value)

    def find_head(self, board):
        for (i, x) in enumerate(board):
            if (GameObject.SNAKE_HEAD in x):
                return (i, x.index(GameObject.SNAKE_HEAD))

        return (-1, -1)

    def locate_food(self, board):
        food_locations = []
        for x in range(len(board)):
            for y in range(len(board[x])):
                if (board[x][y] == GameObject.FOOD):
                    food_locations.insert(-1, (x, y))
        return food_locations

    def on_die(self):
        """This function will be called whenever the snake dies. After its dead the snake will be reincarnated into a
        new snake and its life will start over. This means that the next time the get_move function is called,
        it will be called for a fresh snake. Use this function to clean up variables specific to the life of a single
        snake or to host a funeral.
        """
        self.calculated_path = []
        self.head_position = None
        self.snake_body = []
