__author__ = "Jakub Franěk"
__email__ = "tofugangsw@gmail.com"

from re import compile
from typing import Union
from scipy.spatial import distance


################################################################################

class Rope(object):
    """
    Rope class for making a generic rope with a specified number of knots. After
    the rope instance is created, user should use function follow_instructions()
    to simulate the movement of the head knot according to instructions in the
    input file. Then, the property tail_visited_count tells us the solution to
    both puzzles.
    """

    KEY_ROW = "ROW"
    KEY_COLUMN = "COLUMN"
    DIRECTION_RIGHT = "R"
    DIRECTION_LEFT = "L"
    DIRECTION_UP = "U"
    DIRECTION_DOWN = "D"

    # lambda functions for moving a knot
    INSTRUCTIONS = {
        DIRECTION_RIGHT: lambda coordinates: {
            Rope.KEY_ROW: coordinates[Rope.KEY_ROW],
            Rope.KEY_COLUMN: coordinates[Rope.KEY_COLUMN] + 1
        },
        DIRECTION_LEFT: lambda coordinates: {
            Rope.KEY_ROW: coordinates[Rope.KEY_ROW],
            Rope.KEY_COLUMN: coordinates[Rope.KEY_COLUMN] - 1
        },
        DIRECTION_UP: lambda coordinates: {
            Rope.KEY_ROW: coordinates[Rope.KEY_ROW] - 1,
            Rope.KEY_COLUMN: coordinates[Rope.KEY_COLUMN]
        },
        DIRECTION_DOWN: lambda coordinates: {
            Rope.KEY_ROW: coordinates[Rope.KEY_ROW] + 1,
            Rope.KEY_COLUMN: coordinates[Rope.KEY_COLUMN]
        }
    }

    # instructions parsing
    INPUT_FILE_PATH = "src/day_09/input.txt"
    DIRECTION_GROUP = "direction"
    COUNT_GROUP = "count"
    INSTRUCTION_PATTERN = compile(r"(?P<{}>.) (?P<{}>\d+)".format(
        DIRECTION_GROUP, COUNT_GROUP))

################################################################################

    def __init__(self, number_of_knots: int):
        """
        Creates a generic rope with a specified number of knots.

        :param number_of_knots: number of knots on the rope
        """

        self._knots = [{
            self.KEY_ROW: 0,
            self.KEY_COLUMN: 0
        } for _ in range(number_of_knots)]

        self._tail_visited = []

################################################################################

    @property
    def tail_visited_count(self) -> int:
        """
        :return: number of positions the tail of the rope visits at least once
        """

        return len(set(self._tail_visited))

################################################################################

    def follow_instructions(self) -> None:
        """
        Follow all the instructions in the input file. Move the head knot, then
        adjust positions of all other knots on the rope.
        """

        self._save_tail_visited_position()

        with open(self.INPUT_FILE_PATH, "r") as f:
            lines = f.readlines()

            for instruction in lines:
                result = self.INSTRUCTION_PATTERN.search(instruction)
                direction = result.group(self.DIRECTION_GROUP)
                count = int(result.group(self.COUNT_GROUP))

                for _ in range(count):
                    self._move_knot(0, direction)
                    self._adjust_knots()

################################################################################

    def _adjust_knots(self) -> None:
        """
        Adjust knots positions so all the knots are touching either vertically,
        horizontally or diagonally.
        """

        for i in range(len(self._knots) - 1):
            knots_distance = self._manhattan_distance(i, i + 1)
            directions = self._directions(i, i + 1)

            if (knots_distance == 2 and len(directions) == 1) \
                    or knots_distance == 3 or knots_distance == 4:
                # distance == 2 and len(directions) == 1:
                # both knots are on the same row or column one step from each
                # other (if there wasn't only one direction, the knots would be
                # touching diagonally and no movement would be required)
                #
                # distance == 3 or distance == 4:
                # diagonal movement required
                self._move_knot(i + 1, directions)

        # whether the tail really moved or not, save its position (it'll be made
        # into set anyway)
        self._save_tail_visited_position()

################################################################################

    def _move_knot(self, knot_index: int, directions: str) -> None:
        """
        Moves the specified knot in the specified direction(s).
        :param knot_index: index of the knot
        :param directions: direction(s) to move the knot
        """

        for direction in directions:
            movement_function = self.INSTRUCTIONS[direction]
            self._knots[knot_index] = movement_function(self._knots[knot_index])

################################################################################

    def _save_tail_visited_position(self) -> None:
        """
        Save the tail position. (The number of unique positions is both puzzles
        solution).
        """

        tail = self._knots[-1]
        self._tail_visited.append((tail[self.KEY_ROW], tail[self.KEY_COLUMN]))

################################################################################

    def _directions(self, head_index: int, tail_index: int) -> Union[str, None]:
        """
        :param head_index: index of the knot that acts as head
        :param tail_index: index of the knot that acts as tail
        :return: direction(s) in which the tail knot should move to catch up
        with the head knot (string) or None (no movement required)
        """

        head_row = self._knots[head_index][self.KEY_ROW]
        head_column = self._knots[head_index][self.KEY_COLUMN]
        tail_row = self._knots[tail_index][self.KEY_ROW]
        tail_column = self._knots[tail_index][self.KEY_COLUMN]

        if head_row == tail_row:
            # knots are on the same row, the tail should be moved left or right
            if head_column > tail_column:
                return self.DIRECTION_RIGHT
            elif head_column < tail_column:
                return self.DIRECTION_LEFT
            else:
                return None
        elif head_column == tail_column:
            # knots are on the same column, the tail should be moved up or down
            if head_row > tail_row:
                return self.DIRECTION_DOWN
            elif head_row < tail_row:
                return self.DIRECTION_UP
            else:
                return None
        elif head_row < tail_row and head_column > tail_column:
            # tail should move diagonally up and to the right
            return self.DIRECTION_UP + self.DIRECTION_RIGHT
        elif head_row < tail_row and head_column < tail_column:
            # tail should move diagonally up and to the left
            return self.DIRECTION_UP + self.DIRECTION_LEFT
        elif head_row > tail_row and head_column > tail_column:
            # tail should move diagonally down and to the right
            return self.DIRECTION_DOWN + self.DIRECTION_RIGHT
        elif head_row > tail_row and head_column < tail_column:
            # tail should move diagonally down and to the left
            return self.DIRECTION_DOWN + self.DIRECTION_LEFT
        else:
            return None

################################################################################

    def _manhattan_distance(self, knot_index_1: int, knot_index_2: int) -> int:
        """
        :param knot_index_1: index of the first knot
        :param knot_index_2: index of the second knot
        :return: manhattan distance of the two knots
        """

        knot_1_row = self._knots[knot_index_1][self.KEY_ROW]
        knot_1_column = self._knots[knot_index_1][self.KEY_COLUMN]
        knot_2_row = self._knots[knot_index_2][self.KEY_ROW]
        knot_2_column = self._knots[knot_index_2][self.KEY_COLUMN]

        return distance.cityblock((knot_1_row, knot_1_column),
                                  (knot_2_row, knot_2_column))

################################################################################
