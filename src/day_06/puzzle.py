__author__ = "Jakub Franěk"
__email__ = "tofugangsw@gmail.com"

"""
--- Day 6: Tuning Trouble ---

The preparations are finally complete; you and the Elves leave camp on foot and 
begin to make your way toward the star fruit grove.

As you move through the dense undergrowth, one of the Elves gives you a handheld 
device. He says that it has many fancy features, but the most important one to 
set up right now is the communication system.

However, because he's heard you have significant experience dealing with 
signal-based systems, he convinced the other Elves that it would be okay to give 
you their one malfunctioning device - surely you'll have no problem fixing it.

As if inspired by comedic timing, the device emits a few colorful sparks.
"""

from src.utils.utils import print_puzzle_solution

INPUT_FILE_PATH = "src/day_06/input.txt"
START_OF_PACKET_MARKER_LENGTH = 4
START_OF_MESSAGE_MARKER_LENGTH = 14


################################################################################

def load_signal() -> str:
    """
    Loads the elves' signal from the input file.

    :return: elves' signal from the input file
    """

    with open(INPUT_FILE_PATH, "r") as f:
        return f.read().strip()


################################################################################

def marker_end_index(signal: str, marker_length: int) -> int:
    """
    Finds first N characters that are all different from each other in the
    signal. N is marker length:
    -4 start of packet marker; used in puzzle 1
    -14 start of message marker; used in puzzle 2
    Returns index of the end of the marker in the signal string.

    :param signal: elves' signal
    :param marker_length: marker length
    :return: the index of the last character of the marker
    """

    return next(filter(
        lambda i: len(set(list(signal[i - marker_length:i]))) == marker_length,
        range(marker_length, len(signal))))


################################################################################

def puzzle_01() -> None:
    """
    To be able to communicate with the Elves, the device needs to lock on to
    their signal. The signal is a series of seemingly-random characters that the
    device receives one at a time.

    To fix the communication system, you need to add a subroutine to the device
    that detects a start-of-packet marker in the datastream. In the protocol
    being used by the Elves, the start of a packet is indicated by a sequence of
    four characters that are all different.

    The device will send your subroutine a datastream buffer (your puzzle
    input); your subroutine needs to identify the first position where the four
    most recently received characters were all different. Specifically, it needs
    to report the number of characters from the beginning of the buffer to the
    end of the first such four-character marker.

    For example, suppose you receive the following datastream buffer:

    mjqjpqmgbljsphdztnvjfqwrcgsmlb

    After the first three characters (mjq) have been received, there haven't
    been enough characters received yet to find the marker. The first time a
    marker could occur is after the fourth character is received, making the
    most recent four characters mjqj. Because j is repeated, this isn't a
    marker.

    The first time a marker appears is after the seventh character arrives. Once
    it does, the last four characters received are jpqm, which are all
    different. In this case, your subroutine should report the value 7, because
    the first start-of-packet marker is complete after 7 characters have been
    processed.

    Here are a few more examples:

    -bvwbjplbgvbhsrlpgdmjqwftvncz: first marker after character 5
    -nppdvjthqldpwncqszvftbrmjlhg: first marker after character 6
    -nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg: first marker after character 10
    -zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw: first marker after character 11

    How many characters need to be processed before the first start-of-packet
    marker is detected?

    :return: None; Answer should be 1544.
    """

    signal = load_signal()
    print_puzzle_solution(
        marker_end_index(signal, START_OF_PACKET_MARKER_LENGTH))


################################################################################

def puzzle_02() -> None:
    """
    Your device's communication system is correctly detecting packets, but still
    isn't working. It looks like it also needs to look for messages.

    A start-of-message marker is just like a start-of-packet marker, except it
    consists of 14 distinct characters rather than 4.

    Here are the first positions of start-of-message markers for all of the
    above examples:

    -mjqjpqmgbljsphdztnvjfqwrcgsmlb: first marker after character 19
    -bvwbjplbgvbhsrlpgdmjqwftvncz: first marker after character 23
    -nppdvjthqldpwncqszvftbrmjlhg: first marker after character 23
    -nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg: first marker after character 29
    -zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw: first marker after character 26

    How many characters need to be processed before the first start-of-message
    marker is detected?

    :return: None; Answer should be 2145.
    """

    signal = load_signal()
    print_puzzle_solution(
        marker_end_index(signal, START_OF_MESSAGE_MARKER_LENGTH))

################################################################################
