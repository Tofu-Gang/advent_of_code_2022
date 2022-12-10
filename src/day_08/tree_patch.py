__author__ = "Jakub Franěk"
__email__ = "tofugangsw@gmail.com"

from math import prod


################################################################################

class TreePatch(object):
    """
    Tree patch is a grid of integers, ranged from 0 to 9 (the larger the number,
    the taller the tree is). It can count how many trees are visible outside the
    grid and a scenic score for each tree.
    """

    INPUT_FILE_PATH = "src/day_08/input.txt"

################################################################################

    def __init__(self):
        """
        First, load the tree patch from the input file. Then count and store all
        necessary to solve the puzzles.
        """

        self._load_tree_patch()
        self._count_grid_visibility()
        self._count_max_scenic_score()

################################################################################

    def _load_tree_patch(self) -> None:
        """
        Load the tree patch from the input file.
        """

        with open(self.INPUT_FILE_PATH, "r") as f:
            self._trees = tuple(
                tuple(map(lambda number: int(number), tuple(line.strip())))
                for line in f.readlines())

################################################################################

    def _count_grid_visibility(self) -> None:
        """
        Count how many trees are visible from outside the grid.
        """

        self._visible_count = 0

        for row in range(len(self._trees)):
            for column in range(len(self._trees[row])):
                if self._is_tree_visible(row, column):
                    self._visible_count += 1

################################################################################

    def _count_max_scenic_score(self) -> None:
        """
        Get the maximum scenic score from all trees in the patch.
        """

        self._max_scenic_score = max(self._get_scenic_score(row, column)
                                     for row in range(len(self._trees))
                                     for column in range(len(self._trees[row])))

################################################################################

    def _get_scenic_score(self, row: int, column: int) -> int:
        """
        Count scenic score of a single tree.

        :param row: tree row
        :param column: tree column
        :return: tree scenic score
        """

        tree = self._trees[row][column]

        left_visible_count = 0
        left = column - 1
        while left >= 0 and self._trees[row][left] < tree:
            left_visible_count += 1
            left -= 1
        if left >= 0:
            left_visible_count += 1

        right_visible_count = 0
        right = column + 1
        while right < len(self._trees[row]) and self._trees[row][right] < tree:
            right_visible_count += 1
            right += 1
        if right < len(self._trees[row]):
            right_visible_count += 1

        up_visible_count = 0
        up = row - 1
        while up >= 0 and self._trees[up][column] < tree:
            up_visible_count += 1
            up -= 1
        if up >= 0:
            up_visible_count += 1

        down_visible_count = 0
        down = row + 1
        while down < len(self._trees) and self._trees[down][column] < tree:
            down_visible_count += 1
            down += 1
        if down < len(self._trees):
            down_visible_count += 1

        return prod((left_visible_count,
                     right_visible_count,
                     up_visible_count,
                     down_visible_count))

################################################################################

    def _is_tree_visible(self, row: int, column: int) -> bool:
        """
        :param row: tree row
        :param column: tree column
        :return: True if the tree is visible from outside the grid, False
        otherwise
        """

        # from top or from bottom or from left or from right
        return all(self._trees[i][column] < self._trees[row][column]
                   for i in range(row)) \
            or all(self._trees[i][column] < self._trees[row][column]
                   for i in range(row + 1, len(self._trees))) \
            or all(self._trees[row][i] < self._trees[row][column]
                   for i in range(column)) \
            or all(self._trees[row][i] < self._trees[row][column]
                   for i in range(column + 1, len(self._trees[row])))

################################################################################

    @property
    def grid_visibility(self) -> int:
        """
        :return: how many trees are visible outside the grid
        """

        return self._visible_count

################################################################################

    @property
    def max_scenic_score(self) -> int:
        """
        :return: maximum scenic score from all the trees in the patch
        """

        return self._max_scenic_score

################################################################################
