__author__ = "Jakub Franěk"
__email__ = "tofugangsw@gmail.com"

from re import compile


################################################################################

class CrateMover(object):
    """
    Superclass for CrateMover9000 and CrateMover9001. It loads the input file
    and allows access to the string made of top crate of each stack.
    """

    INPUT_FILE_PATH = "src/day_05/input.txt"

################################################################################

    def __init__(self):
        """
        Processes the input file and creates the starting stacks of crates and
        saves instructions for the cargo crane.
        """

        with open(self.INPUT_FILE_PATH, "r") as f:
            lines = f.readlines()
            # find the line with column labels
            labels_line_index = tuple(filter(
                lambda i: all(char.isdecimal() or char.isspace()
                              for char in lines[i].strip()),
                range(len(lines))))[0]

            # get index of every column; crate names are also at these indexes
            pattern = compile(r"(\d+)")
            labels = pattern.findall(lines[labels_line_index])
            columns = (lines[labels_line_index].index(label)
                       for label in labels)

            # get crate names and arrange them to stacks
            self._stacks = []
            for column in columns:
                self._stacks.append([])
                for line_index in reversed(range(labels_line_index)):
                    char = lines[line_index][column]
                    if char.isalpha():
                        self._stacks[-1].append(char)
                    else:
                        break

            # finally, load the rest of the input file; those are the
            # instructions for the CrateMover cargo crane
            self._instructions = lines[labels_line_index + 2:]

################################################################################

    @property
    def top_crates(self) -> str:
        """
        The Elves just need to know which crate will end up on top of each
        stack.

        :return: string made of top crate in each stack
        """

        return "".join(self._stacks[i][-1] for i in range(len(self._stacks)))

################################################################################


################################################################################

class CrateMover9000(CrateMover):
    """
    Used in puzzle 1.
    """

################################################################################

    def follow_instructions(self) -> None:
        """
        In each step of the procedure, a quantity of crates is moved from one
        stack to a different stack. Crates are moved one at a time, so the first
        crate to be moved ends up below the following crates.
        """

        pattern = compile(r"(\d+)")

        for instruction in self._instructions:
            numbers = pattern.findall(instruction)
            crate_count = int(numbers[0])
            stack_from = int(numbers[1]) - 1
            stack_to = int(numbers[2]) - 1

            for _ in range(crate_count):
                crate = self._stacks[stack_from].pop()
                self._stacks[stack_to].append(crate)

################################################################################


################################################################################

class CrateMover9001(CrateMover):
    """
    The CrateMover 9001 is notable for many new and exciting features: air
    conditioning, leather seats, an extra cup holder, and the ability to pick up
    and move multiple crates at once. Used in puzzle 2.
    """

################################################################################

    def follow_instructions(self) -> None:
        """
        In each step of the procedure, a quantity of crates is moved from one
        stack to a different stack. Moved crates stay in the same order.
        """

        pattern = compile(r"(\d+)")

        for instruction in self._instructions:
            numbers = pattern.findall(instruction)
            crate_count = int(numbers[0])
            stack_from = int(numbers[1]) - 1
            stack_to = int(numbers[2]) - 1

            crates_to_move = self._stacks[stack_from][-crate_count:]
            self._stacks[stack_from] = self._stacks[stack_from][:-crate_count]
            self._stacks[stack_to] += crates_to_move

################################################################################
