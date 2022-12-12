__author__ = "Jakub Franěk"
__email__ = "tofugangsw@gmail.com"

from math import inf
from typing import Union, Tuple


################################################################################

class Node(object):
    """
    Node class that represents a square in heightmap of the surrounding area
    broken into a grid. The letter from input file is converted to a height -
    "a" is lowest, 0, and "z" is highest, 25. Every node is initially unvisited
    and its distance from the starting point in the map is infinity. After all
    nodes are loaded from the input file, they can all be linked with their
    neighbours. Nodes are neighbours if it is possible to traverse between them
    without using climbing tools - a node A is a neighbour of node B if height
    of A is at most one unit higher than that of node B.
    """

    MIN_HEIGHT = ord("a")
    MAX_HEIGHT = ord("z")
    START_POSITION = "S"
    END_POSITION = "E"

################################################################################

    def __init__(self, name: str):
        """
        Count the node elevation from the name. Mark it as unvisited and prepare
        the list of its neighbours. Its distance from the starting node is
        initially infinity.
        """

        if name.islower():
            self._elevation = ord(name) - self.MIN_HEIGHT
        elif name == self.START_POSITION:
            self._elevation = 0
        elif name == self.END_POSITION:
            self._elevation = self.MAX_HEIGHT - self.MIN_HEIGHT
        else:
            # should not happen
            self._elevation = None
        self._is_visited = False
        self._neighbours = []
        # accessing through property and setter is too slow
        self._distance_from_start = inf

################################################################################

    @property
    def distance_from_start(self) -> Union[int, float]:
        """
        :return: distance from start node, either number of steps (integer) or
        infinity (float)
        """

        return self._distance_from_start

################################################################################

    @distance_from_start.setter
    def distance_from_start(self, value: int) -> None:
        """
        Set the distance from the start node.
        :param value: new distance from the start node, either number of steps
        (integer, during Dijkstra algorithm run) or infinity (float, when the
        node is being reset)
        """

        self._distance_from_start = value

################################################################################

    @property
    def elevation(self) -> int:
        """
        :return: elevation of this square in the heightmap grid
        """

        return self._elevation

################################################################################

    @property
    def is_visited(self) -> bool:
        """
        :return: True if this node was already visited, False otherwise
        """

        return self._is_visited

################################################################################

    def mark_visited(self) -> None:
        """
        Minimum distance from the starting node already found, mark this node as
        visited.
        """

        self._is_visited = True

################################################################################

    @property
    def neighbours(self) -> Tuple["Node", ...]:
        """
        :return: tuple of neighbouring nodes
        """

        return tuple(self._neighbours)

################################################################################

    def add_neighbour(self, neighbour: "Node") -> None:
        """
        After all the nodes were created from the input file, use this method to
        link all the nodes to its neighbours.

        :param neighbour: neighbouring node
        """

        self._neighbours.append(neighbour)

################################################################################

    def reset(self) -> None:
        """
        Reset the node so another Dijkstra algorithm run can be started. A node
        is initially an infinity distant from the starting node and is marked as
        unvisited.
        """

        self._distance_from_start = inf
        self._is_visited = False

################################################################################
