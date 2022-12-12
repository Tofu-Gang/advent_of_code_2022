__author__ = "Jakub Franěk"
__email__ = "tofugangsw@gmail.com"

from typing import Tuple, Union
from src.day_12.node import Node


################################################################################

class HeightMap(object):
    """
    Height map class. Initially, grid of nodes is loaded from the input file.
    Then, neighbouring nodes are linked together. This state can be reached
    anytime by resetting the map (method reset()). In this state, the map is
    ready for one run of Dijkstra algorithm and find the shortest path from the
    starting node to the end node. The starting node can be any node in the
    grid. However, only nodes with the lowest elevation of zero are used as
    possible starting nodes in the puzzle 2.
    """

    INPUT_FILE_PATH = "src/day_12/input.txt"

################################################################################

    def __init__(self):
        """
        Load all the nodes from the input file and store them in a grid. Then,
        link neighbouring nodes together.
        """

        self._start_node = None
        self._end_node = None
        self._map = []

        self._load_nodes()
        self._load_neighbours()

################################################################################

    def _load_nodes(self) -> None:
        """
        Load nodes from the input file and store them in a grid.
        """

        with open(self.INPUT_FILE_PATH, "r") as f:
            for line in f.read().split():
                row = []
                for name in line:
                    node = Node(name)
                    row.append(node)

                    if name == Node.START_POSITION:
                        self._start_node = node
                    elif name == Node.END_POSITION:
                        self._end_node = node
                self._map.append(tuple(row))
            self._map = tuple(self._map)

################################################################################

    def _load_neighbours(self) -> None:
        """
        Link neighbouring nodes together.
        """

        for row in range(len(self._map)):
            for column in range(len(self._map[row])):
                node = self._map[row][column]

                try:
                    up = self._map[row - 1][column]
                    if node.elevation + 1 >= up.elevation:
                        node.add_neighbour(up)
                except IndexError:
                    pass

                try:
                    down = self._map[row + 1][column]
                    if node.elevation + 1 >= down.elevation:
                        node.add_neighbour(down)
                except IndexError:
                    pass

                try:
                    left = self._map[row][column - 1]
                    if node.elevation + 1 >= left.elevation:
                        node.add_neighbour(left)
                except IndexError:
                    pass

                try:
                    right = self._map[row][column + 1]
                    if node.elevation + 1 >= right.elevation:
                        node.add_neighbour(right)
                except IndexError:
                    pass

################################################################################

    def reset(self) -> None:
        """
        Reset the heightmap so another Dijkstra algorithm run can be executed.
        """

        for row in self._map:
            for node in row:
                node.reset()

################################################################################

    def dijkstra(self, start_node: Node = None) -> None:
        """
        Dijkstra algorithm to find the shortest path from the specified starting
        node to the end node.
        """

        if start_node is not None:
            current = start_node
        else:
            # for puzzle 1, one node is hardcoded as a starting node
            current = self._start_node

        unvisited = [current]
        current.distance_from_start = 0

        while True:
            unvisited_neighbours = tuple(filter(
                lambda node: not node.is_visited,
                current.neighbours))

            for neighbour in unvisited_neighbours:
                tentative_distance = current.distance_from_start + 1

                if tentative_distance < neighbour.distance_from_start:
                    neighbour.distance_from_start = tentative_distance
                    unvisited.append(neighbour)

            current.mark_visited()
            unvisited.remove(current)

            if current is self._end_node:
                # end node reached and shortest path was found
                break
            else:
                try:
                    current = sorted(
                        unvisited,
                        key=lambda node: node.distance_from_start)[0]
                except IndexError:
                    # end node cannot be reached
                    break

################################################################################

    @property
    def distance(self) -> Union[int, float]:
        """
        :return: shortest distance from the starting node to the end node,
        either an integer (end node was reached) or infinity (float, end node
        cannot be reached)
        """

        return self._end_node.distance_from_start

################################################################################

    def possible_starts(self) -> Tuple[Node, ...]:
        """
        :return: all potential starting nodes to be used in puzzle 2
        """

        return tuple(filter(lambda node: node.elevation == 0,
                            (node for row in self._map for node in row)))

################################################################################
