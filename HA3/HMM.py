# Imports
import numpy as np


class HMM:
    """
    Class which constructs a hidden markov model and predicts the robot location based on the forward algorithm.
    """
    def __init__(self, world):
        """
        Initialize the world, the number of headings as well as the transition matrix, no sensor reading matrix and
        the f vector.
        """
        self.world = world
        self.width = world.width
        self.height = world.height
        self.headings = 4
        self.Transition = self.construct_transition()
        self.no_reading_sensor_matrix = self.construct_no_reading_sensor_matrix()
        self.f = (1/(self.height*self.width * self.headings)) * np.ones((self.height*self.width * self.headings, 1))

    def construct_transition(self):
        """
        Constructs the transition matrix.
        :return transition: Transition matrix.
        """
        transition = np.zeros((self.height*self.width * self.headings, self.height*self.width * self.headings))

        for x in range(self.width):
            for y in range(self.height):
                for heading in range(self.headings):
                    # Due to the nature of the indexing, this shall grant the current state.
                    state = x*self.height*self.headings + y*self.headings + heading
                    moves = self.get_moves(x, y, heading)
                    for (new_x, new_y, new_heading), p in moves:
                        new_state = new_x*self.height*self.headings + new_y*self.headings + new_heading
                        transition[state, new_state] = p

        return transition

    def get_moves(self, x, y, heading):
        """
        Helper function to construct_transition. Grants the possible moves that the robot could take given a
        certain state and heading with corresponding probabilities (based on the given prob from the given task).
        :param x: x-coordinate.
        :param y: y-coordinate.
        :param heading: Heading.
        return moves: Possible moves for robot at (x, y) with direction=heading with corresponding probabilities.
        """
        possible_moves, attempted_move = self.get_possible_moves(x, y, heading)
        encountered_wall = False
        if attempted_move not in possible_moves:
            encountered_wall = True
        moves = []

        num_moves = len(possible_moves)

        for (new_x, new_y, head) in possible_moves:
            if head == heading and not encountered_wall:
                moves.append(((new_x, new_y, head), 0.7))
            elif head != heading:
                if encountered_wall:
                    moves.append(((new_x, new_y, head), 1/num_moves))
                else:
                    moves.append(((new_x, new_y, head), 0.3/(num_moves-1)))

        return moves

    def get_possible_moves(self, x, y, heading):
        """
        Helper function to get_moves. Grants the possible moves that the robot could take given a certain
        state and heading
        :param x: x-coordinate.
        :param y: y-coordinate.
        :param heading: Heading.
        return moves, attempted_move: Possible moves for robot at (x, y) with direction=heading as well as the
        attempted move (used for bayesian calculation if the robot encounters wall or not).
        """
        possible_moves = [(x, y+1, 0), (x+1, y, 1), (x, y-1, 2), (x-1, y, 3)]
        moves = []
        for (new_x, new_y, head) in possible_moves:
            if self.inside(new_x, new_y):
                moves.append((new_x, new_y, head))
        attempted_move = possible_moves[heading]
        return moves, attempted_move

    def inside(self, x, y):
        """
        Function which checks if coordinate (x, y) is inside the world.
        :param x: x-coordinate.
        :param y: y-coordinate.
        :return: True if the coordinate is inside the world, False else.
        """
        if (0 <= x <= self.width - 1) and (0 <= y <= self.height - 1):
            return True
        return False

    def construct_sensor_matrix(self, sensor_reading):
        """
        Constructs the sensor matrix given some sensor reading. If sensor reading is None, it returns the no sensor
        reading matrix.
        :param sensor_reading: Sensor_reading, either a coordinate or None.
        :return Om: sensor matrix Om.
        """
        if not sensor_reading:
            return self.no_reading_sensor_matrix
        Om = np.zeros((self.width*self.height * self.headings, self.width*self.height * self.headings))

        [x, y] = sensor_reading
        state = x*self.height*self.headings + y*self.headings

        for heading in range(self.headings):
            Om[state + heading, state + heading] = self.world.sensor.p_true_reading

        for (n_x, n_y) in self.world.robot.neighbours:
            state = n_x*self.height*self.headings + n_y * self.headings
            for heading in range(self.headings):
                Om[state + heading, state + heading] = self.world.sensor.p_1_off

        for (n_x, n_y) in self.world.robot.second_neighbours:
            state = n_x*self.height*self.headings + n_y * self.headings
            for heading in range(self.headings):
                Om[state + heading, state + heading] = self.world.sensor.p_2_off
        return Om

    def construct_no_reading_sensor_matrix(self):
        """
        Constructs the no reading sensor matrix. Diagonal matrix with probabilities dependent on number of neighbours
        and second neighbours, i.e If a the sensor has no reading, then the robot is probably near a corner/wall.
        :return Om: No reading sensor matrix Om.
        """
        Om = np.zeros((self.height * self.width * self.headings, self.height*self.width * self.headings))
        for state in range(self.height*self.width * self.headings):
            x = (state // self.headings) // self.height
            y = (state // self.headings) % self.height

            neighbours, second_neighbours = self.world.robot.get_neighbours(x, y)

            Om[state, state] = 1.0 - self.world.sensor.p_true_reading - self.world.sensor.p_1_off*len(neighbours) - self.world.sensor.p_2_off*len(second_neighbours)
        return Om

    def guess_pos(self):
        """
        Calculates best guess of robot location given some sensor reading.
        :return guess: best guess of robots location.
        """
        sensor_reading = self.world.sensor.sensor_reading(self.world)
        self.update_f(sensor_reading)
        guess, _ = self.get_most_probable()
        return guess

    def update_f(self, sensor_reading):
        """
        Updates f vector based on the forward algorithm.
        :param sensor_reading: Given sensor reading (coordinate or None).
        """
        Om = self.construct_sensor_matrix(sensor_reading)
        f = Om @ self.Transition.T @ self.f
        self.f = f

    def get_most_probable(self):
        """
        Finds element in f which is largest, then finds which coordinate (x,y) that corresponds to.
        :return (x, y), self.f[pos]: coordinate for most probable location (x, y) and value at that position.
        """
        pos = np.argmax(self.f)

        x = (pos // self.headings) // self.height
        y = (pos // self.headings) % self.height

        return (x, y), self.f[pos]
