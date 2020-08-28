# Imports
import numpy as np
import random as rnd


class Sensor:
    """
    Creates a sensor object which grants the sensor readings based on given probabilities.
    """
    def __init__(self, world):
        """
        Initialize parameters based on given probabilities.
        :param world: Needs a world which it lives in. (numpy array).
        """
        self.world = world
        self.p_true_reading = 0.1
        self.p_1_off = 0.05
        self.p_2_off = 0.025

    def sensor_reading(self, world):
        """
        Returns the sensor reading.
        :param world: World which sensor lives in.
        :return: Sensor reading based on given information. May return true location, neighbour location,
        second neighbour location or no information.
        """
        u = rnd.random()
        picked_neighbour = world.pick_rnd_neighbours()
        if u < self.p_true_reading:
            return world.robot.loc
        elif u < self.p_true_reading + self.p_1_off*len(world.robot.neighbours):
            return picked_neighbour[0]
        elif u < self.p_true_reading + self.p_1_off*len(world.robot.neighbours) + self.p_2_off*len(world.robot.second_neighbours):
            return picked_neighbour[1]
        else:
            return None


class Robot:
    """
    Class for Robot object. Robot needs a world, a location and a heading. The robot object also keeps track of
    its neighbours.
    """

    def __init__(self, world):
        """
        Initialize starting location, heading and neighbours.
        :param world: Needs world which the robot lives in.
        """
        self.world = world
        self.height, self.width = np.shape(world)
        self.loc = [rnd.choice(np.arange(self.width)), rnd.choice(np.arange(self.height))]
        self.heading = self.valid_random_heading()
        self.neighbours, self.second_neighbours = self.get_neighbours(self.loc[0], self.loc[1])

    def move(self):
        """
        Moves the robot. The robot has a 30 % chance of randomly changing heading. It will also change heading if it
        cannot move along its current heading. Otherwise the robot simply moves on step ahead. New neighbours are
        calculated.
        """
        if rnd.random() < 0.3 or self.invalid_heading(self.heading):
            self.heading = self.valid_random_heading()
        x, y = self.loc
        moves = [(x, y+1), (x+1, y), (x, y-1), (x-1, y)]
        self.loc = moves[self.heading]
        self.neighbours, self.second_neighbours = self.get_neighbours(self.loc[0], self.loc[1])

    def valid_random_heading(self):
        """
        Function which set a new random heading to the robot. The heading is guaranteed to be valid.
        """
        headings = np.arange(4)
        rnd.shuffle(headings)
        for heading in headings:
            if not self.invalid_heading(heading):
                return heading

    def invalid_heading(self, heading):
        """
        Helper function to valid_random_heading. Checks if the robot is directly staring at a wall. Returns True if so,
        False else.
        """
        valid = 0
        if heading == 0 and self.loc[1] == self.height - 1:
            valid += 1
        elif heading == 1 and self.loc[0] == self.width - 1:
            valid += 1
        elif heading == 2 and self.loc[1] == 0:
            valid += 1
        elif heading == 3 and self.loc[0] == 0:
            valid += 1
        return bool(valid)

    def get_neighbours(self, x, y):
        """
        Finds all neighbouring points and second neighbouring points.
        :param x: x-coordinate
        :param y: y-coordinate
        :return  neighbours, second_neighbours: Neighbours and second neighbours.
        """
        possible_neighbours = [(n_x, n_y) for n_x in range(x - 1, x + 2) for n_y in range(y - 1, y + 2)]
        possible_neighbours.remove((x, y))

        possible_second_neighbours = [(n_x, n_y) for n_x in range(x - 2, x + 3) for n_y in range(y - 2, y + 3)]
        for neighbour in possible_neighbours:
            possible_second_neighbours.remove(neighbour)

        possible_second_neighbours.remove((x, y))

        neighbours = []
        second_neighbours = []

        for (n_x, n_y) in possible_neighbours:
            if self.inside(n_x, n_y):
                neighbours.append((n_x, n_y))

        for (n_x, n_y) in possible_second_neighbours:
            if self.inside(n_x, n_y):
                second_neighbours.append((n_x, n_y))

        return neighbours, second_neighbours

    def inside(self, x, y):
        """
        Checks if a coordinate is inside the world.
        :param x: x-coordinate
        :param y: y-coordinate
        :return: True if inside the world, False else.
        """
        if (0 <= x <= self.width - 1) and (0 <= y <= self.height - 1):
            return True
        return False
