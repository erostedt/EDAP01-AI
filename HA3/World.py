# Imports
from Robot import Robot, Sensor
import numpy as np
from random import choice


class World:
    """
    Constructs world object with certain width and height. World has both a robot and a sensor inside.
    """
    def __init__(self, width, height):
        """
        Initialize world size and world. Lastly a robot and sensor is created in the world.
        :param width: World width
        :param height: World height
        """
        self.width = width
        self.height = height
        self.world = np.zeros((height, width))
        self.robot = Robot(self.world)
        self.sensor = Sensor(self.world)

    def pick_rnd_neighbours(self):
        """
        Function that chooses a random neighbour and a random second neighbour to the robot.
        :return: Random neighbour and random second neighbour.
        """
        return choice(self.robot.neighbours), choice(self.robot.second_neighbours)
