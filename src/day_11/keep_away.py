__author__ = "Jakub Franěk"
__email__ = "tofugangsw@gmail.com"

from math import prod, lcm
from re import compile
from src.day_11.monkey import Monkey


################################################################################

class KeepAway(object):
    """
    Class for the game Keep Away. Monkey data are loaded automatically when the
    instance is created. User has to state if the test divisors lcm should be
    used (for puzzle 2 only). Then, we can play any number of rounds via the
    play_rounds() method and after the game ends, get the level of monkey
    business using the monkey_business property.
    """

    INPUT_FILE_PATH = "src/day_11/input.txt"

################################################################################

    def __init__(self, use_test_divisors_lcm: bool):
        """
        Load monkey data and set the test divisors lcm to every monkey, if the
        game should use it (for puzzle 2 only).

        :param use_test_divisors_lcm: True if the game should use test divisors
        lcm (for puzzle 2 only), False otherwise (puzzle 1)
        """

        # load monkeys
        self._monkeys = []
        with open(self.INPUT_FILE_PATH, "r") as f:
            for monkey_data in f.read().split("\n\n"):
                self._monkeys.append(self._load_monkey(monkey_data))

        if use_test_divisors_lcm:
            # for puzzle 2 only
            test_divisors_lcm = lcm(*(monkey.test_divisor
                                      for monkey in self._monkeys))
            for monkey in self._monkeys:
                monkey.set_test_divisors_lcm(test_divisors_lcm)

################################################################################

    def play_rounds(self, rounds_count: int) -> None:
        """
        Play specified number of rounds of Keep Away!

        :param rounds_count: number of game rounds
        """

        for _ in range(rounds_count):
            for monkey in self._monkeys:
                while monkey.has_items:
                    item, recipient_monkey_name = monkey.throw()
                    recipient_monkey = self._get_monkey_by_name(
                        recipient_monkey_name)
                    recipient_monkey.catch(item)

################################################################################

    @property
    def monkey_business(self) -> int:
        """
        :return: the level of monkey business
        """

        return prod(sorted(monkey.inspected_items_count
                           for monkey in self._monkeys)[-2:])

################################################################################

    def _get_monkey_by_name(self, monkey_name: str) -> Monkey:
        """
        :param monkey_name: name of the monkey that is looked for
        :return: monkey with the specified name
        """

        return next(filter(
            lambda monkey: monkey.name == monkey_name,
            self._monkeys))

################################################################################

    @staticmethod
    def _load_monkey(monkey_data: str) -> Monkey:
        """
        Load one monkey from the data from the input file.

        :param monkey_data: one monkey data from the input file
        :return: monkey object
        """

        monkey_name_group = "name"
        item_worry_level_group = "item"
        operation_group = "operation"
        test_group = "test"

        monkey_pattern = compile(
            r"Monkey (?P<{}>\d+):".format(monkey_name_group))
        starting_items_pattern = compile(r"Starting items: (?P<{}>.+)".format(
            item_worry_level_group))
        operation_pattern = compile(r"Operation: new = (?P<{}>.+)".format(
            operation_group))
        test_pattern = compile(
            r"Test: divisible by (?P<{}>\d+)".format(test_group))
        test_true_monkey_pattern = compile(
            r"If true: throw to monkey (?P<{}>\d+)"
            .format(monkey_name_group))
        test_false_monkey_pattern = compile(
            r"If false: throw to monkey (?P<{}>\d+)"
            .format(monkey_name_group))

        name = monkey_pattern.search(monkey_data).group(monkey_name_group)
        starting_items = tuple(map(
            lambda value: int(value),
            starting_items_pattern.search(monkey_data)
            .group(item_worry_level_group).split(",")))
        operation = lambda old: eval(
            operation_pattern.search(monkey_data).group(operation_group))
        test_divisor = int(test_pattern.search(monkey_data).group(test_group))
        test_true_monkey_name = test_true_monkey_pattern.search(monkey_data) \
            .group(monkey_name_group)
        test_false_monkey_name = test_false_monkey_pattern.search(monkey_data) \
            .group(monkey_name_group)

        return Monkey(name,
                      starting_items,
                      operation,
                      test_divisor,
                      test_true_monkey_name,
                      test_false_monkey_name)

################################################################################
