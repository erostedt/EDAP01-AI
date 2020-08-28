"""
Code for Home Assignment 3 for the course EDAP01 - Artificial Intelligence given at LTH.

Task: Self localization of robot given a world and sensor data. Location prediction based on the forward algorithm.

The code is split up into 4 classes spread out over 4 files. HMM.py contains the class HMM which
contains the hidden markov model for the prediction. World.py has the class World which constructs a world object.
Robot.py has two classes:  Robot constructs a Robot and moves the robot. Sensor creates a sensor object which grants the
sensor readings. Lastly Main.py runs the self localization algorithm, counts how accurate the predictions are and plots
number of occurrences for each tile in the world.

Author Eric Rostedt.
"""

# Imports
from HMM import HMM
from World import World
import numpy as np
import matplotlib.pyplot as plt
import random as rnd


def run_localization():
    """
    Runs the algorithm. Creates a world with a robot and a sensor inside and a model. Calculates average manhattan
    distance of the predicted position and the actual position and the ratio of correctly guessed positions.
    Lastly displays the number of occurrences for each tile.
    """
    width, height = 8, 8
    steps = 100

    world = World(width, height)
    hmm = HMM(world)
    plot_world = np.zeros((width, height))
    correct_guesses = 0
    correct_guesses_random = 0

    error = 0
    error_random = 0
    for step in range(steps):
        guessed_pos = hmm.guess_pos()
        world.robot.move()
        correct_pos = world.robot.loc
        random_guess = (rnd.randint(0, width-1), rnd.randint(0, height-1))
        plot_world[correct_pos[0], correct_pos[1]] += 1
        error += np.linalg.norm(np.asarray(correct_pos) - np.asarray(guessed_pos), 1)
        error_random += np.linalg.norm(np.asarray(correct_pos) - np.asarray(random_guess), 1)

        if correct_pos == guessed_pos:
            correct_guesses += 1

        if correct_pos == random_guess:
            correct_guesses_random += 1

    print('Average error: {} \n'. format(error/steps))
    print('Correct guessed: {} \n'.format(correct_guesses/steps))

    print('Average error for random guess: {} \n'.format(error_random / steps))
    print('Correct guessed for random guess: {} \n'.format(correct_guesses_random / steps))

    fig, ax = plt.subplots()
    ax.matshow(plot_world)

    for x in range(width):
        for y in range(height):
            ax.text(x, y, str(int(plot_world[y, x])), ha='center', va='center')
    plt.show()


if __name__ == '__main__':
    run_localization()
