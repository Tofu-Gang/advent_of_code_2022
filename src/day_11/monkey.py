__author__ = "Jakub Franěk"
__email__ = "tofugangsw@gmail.com"

from typing import Tuple, Callable


################################################################################

class Monkey(object):
    """
    Monkey class. Every monkey has its name, test divisor and a counter of
    inspected items, all accessible via respective properties. Furthermore, it
    has a list of items, which lists our worry level for each item the monkey is
    currently holding in the order they will be inspected. Our worry level
    changes when the monkey inspects an item; this is controlled by a lambda
    function called operation. After the inspection, we are so relieved that the
    monkey did not damage the item that our worry level is:
    -divided by three and rounded down to the nearest integer (puzzle 1)
    -set to a result of a modulo operation, using all monkeys test divisors lcm
     (puzzle 2)
    After the worry level is adjusted, the monkey decides where to throw the
    item next based on whether the worry level is divisible by the monkey's test
    divisor.
    """

################################################################################

    def __init__(self, name: str,
                 starting_items: Tuple[int],
                 operation: Callable,
                 test_divisor: int,
                 test_true_monkey_name: str,
                 test_false_monkey_name: str):
        """
        :param name: monkey name
        :param starting_items: starting items of the monkey
        :param operation: how the worry level changes when the monkey inspects
        an item
        :param test_divisor: used to decide where to throw the item next
        :param test_true_monkey_name: recipient monkey name if the test result
        is True
        :param test_false_monkey_name: recipient monkey name if the test result
        is False
        """

        self._name = name
        self._items = list(starting_items)
        self._operation = operation
        self._test_divisor = test_divisor
        self._destination_monkeys = {
            True: test_true_monkey_name,
            False: test_false_monkey_name
        }
        self._inspected_items_count = 0
        self._test_divisors_lcm = None

################################################################################

    @property
    def name(self) -> str:
        """
        :return: monkey name
        """

        return self._name

################################################################################

    @property
    def test_divisor(self) -> int:
        """
        :return: test divisor used to determine where to throw an item next
        """

        return self._test_divisor

################################################################################

    @property
    def has_items(self) -> bool:
        """
        :return: True if the monkey has at least one item, False otherwise
        """

        return len(self._items) > 0

################################################################################

    @property
    def inspected_items_count(self) -> int:
        """
        :return: total number of inspected items
        """

        return self._inspected_items_count

################################################################################

    def set_test_divisors_lcm(self, test_divisors_lcm: int) -> None:
        """
        Used to adjust our worry level after the monkey inspected an item
        (puzzle 2 only).

        :param test_divisors_lcm: least common multiple of all the monkeys test
        divisors
        """

        self._test_divisors_lcm = test_divisors_lcm

################################################################################

    def throw(self) -> Tuple[int, str]:
        """
        Count the inspected item and adjust our worry level after the
        inspection. Get the test result and determine the recipient monkey.
        Throw the item to the recipient monkey.

        :return: tuple where first value is the new worry level of the thrown
        item and the second one is the name of the recipient monkey
        """

        self._inspected_items_count += 1
        worry_level_after_inspection = self._operation(self._items[0])
        if self._test_divisors_lcm is not None:
            # puzzle 2
            worry_level_after_inspection %= self._test_divisors_lcm
        else:
            # puzzle 1
            worry_level_after_inspection //= 3
        test_result = worry_level_after_inspection % self._test_divisor == 0
        recipient_monkey_name = self._destination_monkeys[test_result]
        self._items.pop(0)
        return worry_level_after_inspection, recipient_monkey_name

################################################################################

    def catch(self, item: int) -> None:
        """
        Catch the item. It will be inspected after the items the monkey already
        has.

        :param item: thrown item (integer, our worry level about this item)
        """

        self._items.append(item)

################################################################################
