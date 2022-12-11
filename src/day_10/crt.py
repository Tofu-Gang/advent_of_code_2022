__author__ = "Jakub Franěk"
__email__ = "tofugangsw@gmail.com"

from re import compile
from typing import Tuple


################################################################################

class CRT(object):
    """
    CRT class. After the instance is created, user should use the
    load_instructions() method to load and execute program from the input file.
    Then, signal_strengths_sum property gives us puzzle 1 solution and screen
    property solution to puzzle 2.
    """

    INPUT_FILE_PATH = "src/day_10/input.txt"
    NOOP_INSTRUCTION = "noop"
    ADD_VALUE_GROUP = "add_value"
    ADD_VALUE_PATTERN = compile(r"addx (?P<{}>-?\d+)".format(ADD_VALUE_GROUP))
    LIT_PIXEL = "#"
    DARK_PIXEL = "."

################################################################################

    def __init__(self):
        """
        Init the CRT: register X starts with value 1, CPU clock is on zero
        cycles. The screen is empty.
        """

        self._register_x = 1
        self._cycles_count = 0
        self._signal_strengths = []
        self._screen = ""

################################################################################

    def load_instructions(self) -> None:
        """
        Load the program from the input file. Manage clock ticks and
        instructions execution.
        """

        with open(self.INPUT_FILE_PATH, "r") as f:
            lines = f.readlines()
            for instruction in lines:
                result = self.ADD_VALUE_PATTERN.search(instruction)
                if result is not None:
                    # addx V:
                    # Takes two cycles to complete. After two cycles, the X
                    # register is increased by the value V. (V can be negative.)
                    self._tick()
                    self._tick()
                    value = int(result.group(self.ADD_VALUE_GROUP))
                    self._register_x += value

                if self.NOOP_INSTRUCTION in instruction:
                    # noop:
                    # Takes one cycle to complete. It has no other effect.
                    self._tick()

################################################################################

    @property
    def signal_strengths_sum(self) -> int:
        """
        :return: the sum of the interesting signal strengths (puzzle 1)
        """

        return sum(self._signal_strengths)

################################################################################

    @property
    def screen(self) -> str:
        """
        :return: image rendered by the program in the input file (puzzle 2)
        """

        return self._screen

################################################################################

    def _sprite(self) -> Tuple[int, ...]:
        """
        :return: three pixels positions based on register X value (the middle
        pixel of the sprite)
        """

        return self._register_x - 1, self._register_x, self._register_x + 1

################################################################################

    def _tick(self) -> None:
        """
        Manages one clock tick. Draws pixels on the screen (puzzle 2) and saves
        interesting signal strengths (puzzle 1).
        """

        # mod 40 because every screen line uses same pixel positions 0 - 39.
        if self._cycles_count % 40 in self._sprite():
            # current pixel IS part of the sprite in the current position
            self._screen += self.LIT_PIXEL
        else:
            # current pixel is NOT part of the sprite in the current position
            self._screen += self.DARK_PIXEL

        # clock ticks
        self._cycles_count += 1

        if self._cycles_count % 40 == 0:
            # start drawing a new line in the screen
            self._screen += "\n"

        if self._cycles_count == 20 or (self._cycles_count - 20) % 40 == 0:
            # an interesting signal strength; save it
            signal_strength = self._cycles_count * self._register_x
            self._signal_strengths.append(signal_strength)

################################################################################
