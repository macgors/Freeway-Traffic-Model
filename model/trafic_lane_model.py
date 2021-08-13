import numpy as np
import random as rnd
import time
import matplotlib.pyplot as plt
from copy import copy


class TrafficLaneSimulation:
    def __init__(
        self,
        length,
        slowDownProbability,
        density,
        maxSpeed,
        rubberneckProbability=0.0,
        epsilon=10,
    ):
        self.length = length
        self.slowDownProbability = slowDownProbability
        self.density = density
        self.lane = [-1 for _ in range(length)]
        self.maxSpeed = maxSpeed
        self.counter = 0
        self.rubberneckProbability = rubberneckProbability
        self.epsilon = epsilon
        self.rubberneckPosition = length // 2
        self.deerPositon = length // 2

        carsNumber = int(self.density * self.length)

        indexes = np.random.choice(range(self.length), carsNumber, replace=False)

        for i in indexes:
            self.lane[i] = rnd.randint(0, self.maxSpeed + 1)

    def iteration(self, deerPresent=False):
        def getNextCarDistance(curIdx):
            for dist in range(1, self.maxSpeed + 1):
                checkedIdx = (curIdx + dist) % self.length
                if self.lane[checkedIdx] > -1:
                    return dist
            return np.inf

        for idx, speed in enumerate(self.lane):
            if speed < 0:
                continue

            nextCarDistance = getNextCarDistance(idx)
            if nextCarDistance > speed + 1 and speed < self.maxSpeed:
                speed += 1
            elif nextCarDistance <= speed:
                speed = nextCarDistance - 1

            if (
                rnd.random() < self.rubberneckProbability
                and idx > self.rubberneckPosition - self.epsilon
                and idx <= self.rubberneckPosition
            ):
                speed = speed // 2

            if (
                deerPresent
                and idx > self.rubberneckPosition - self.epsilon
                and idx <= self.rubberneckPosition
            ):
                speed = 0

            if rnd.random() < self.slowDownProbability and speed > 0:
                speed -= 1

            self.lane[idx] = speed

        updatedLane = [-1 for _ in range(self.length)]
        for idx, speed in enumerate(self.lane):
            if speed < 0:
                continue

            newIdx = idx + speed
            if newIdx >= self.length:
                self.counter += 1
            relIdx = newIdx % self.length

            updatedLane[int(relIdx)] = speed

        self.lane = updatedLane

    def __str__(self):
        return f"{''.join('.' if int(x) == -1 else str(int(x)) for x in self.lane)}\
        {sum(1 if x > -1 else 0 for x in self.lane )}"


def main():
    simulationsNumber = 1
    iterationsNumber = 300
    xs = []
    ys = []
    includeDeer = False

    for d in [0.2]:
        print(d)
        cars = []
        for _ in range(simulationsNumber):
            simulation = TrafficLaneSimulation(
                length=300,
                slowDownProbability=0.25,
                density=d,
                maxSpeed=5,
                rubberneckProbability=0.0,
                epsilon=40,
            )

            for iteration in range(iterationsNumber):
                simulation.iteration(includeDeer and iteration == 100)
                cars.append([1 if el >= 0 else 0 for el in simulation.lane])

    fig, ax = plt.subplots()
    ax.invert_yaxis()
    im = ax.imshow(
        cars,
        interpolation="nearest",
        origin="lower",
    )

    plt.xlabel("Space [road cell]")
    plt.ylabel("Time [iterations]")
    plt.gca().invert_yaxis()
    plt.show()


if __name__ == "__main__":
    main()
