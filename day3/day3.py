import unittest
from functools import reduce

BITS = 0
DIAGNOSTICS = 0


def report(raw_report):
    global BITS, DIAGNOSTICS
    lines = raw_report.readlines()
    trimmed_lines = list(map(lambda x: x.strip(), lines))
    BITS = len(trimmed_lines[0])
    DIAGNOSTICS = len(lines)
    return trimmed_lines

def gamma_rate(diagnostics):
    gamma = 0
    for bit in range(BITS):
        if most_common_value(diagnostics, bit)=='1':
            gamma += value_of_bit(bit)
    return gamma


def value_of_bit(bit):
    return (2 ** (BITS - bit - 1))


def epsilon_rate(diagnostics):
    return 2 ** BITS - 1 - gamma_rate(diagnostics)

def rating_for(diagnostics, select_bit):
    oxygen_diagnostics = diagnostics
    for bit in range(BITS):
        selected_bit = select_bit(oxygen_diagnostics, bit)
        oxygen_diagnostics = filter_for_matching_bit(oxygen_diagnostics, bit, selected_bit)
        if len(oxygen_diagnostics)==1:
            return int(oxygen_diagnostics[0], 2)
    return None

def oxygen_generator_rating(diagnostics):
    return rating_for(diagnostics, most_common_value)

def co2_scrubber_rating(diagnostics):
    return rating_for(diagnostics, least_common_value)


def filter_for_matching_bit(diagnostics, bit, value):
    filtered = filter(lambda item: item[bit] == value, diagnostics)
    return list(filtered)


def single_bit_diagnostics(diagnostics, bit):
    return list(map(lambda item: item[bit], diagnostics))


def most_common_value(diagnostics, bit):
    single_bit = single_bit_diagnostics(diagnostics, bit)
    sum_of_bits = reduce(lambda prev, current: int(prev) + int(current), single_bit)
    return '1' if sum_of_bits >= len(diagnostics)/2 else '0'


def least_common_value(diagnostics, bit):
    return '0' if most_common_value(diagnostics, bit)=='1' else '1'


class Day3(unittest.TestCase):

    def setUp(self) -> None:
        self.diagnostic_report = open('diagnostic_report_test')

    def tearDown(self) -> None:
        self.diagnostic_report.close()

    def test_read_diagnostic_report(self):
        lines = report(self.diagnostic_report)
        self.assertEqual(12, len(lines))
        self.assertEqual(5, len(lines[0]))
        self.assertEqual('00100', lines[0])

    def test_gamma_rate(self):
        gamma = gamma_rate(report(self.diagnostic_report))
        self.assertEqual(22, gamma)

    def test_epsilon_rate(self):
        epsilon = epsilon_rate(report(self.diagnostic_report))
        self.assertEqual(9, epsilon)

    def test_oxygen_generator_rating(self):
        oxygen = oxygen_generator_rating(report(self.diagnostic_report))
        self.assertEqual(23, oxygen)

    def test_co2_scrubber_rating(self):
        co2_scrubber = co2_scrubber_rating(report(self.diagnostic_report))
        self.assertEqual(10, co2_scrubber)

    def test_filter_for_matching_bit(self):
        result = filter_for_matching_bit(['10', '01'], 0, '1')
        self.assertEqual(['10'], result)

    def test_most_common_value(self):
        result = most_common_value(report(self.diagnostic_report), 0)
        self.assertEqual('1', result)

    def test_least_common_value(self):
        result = least_common_value(report(self.diagnostic_report), 0)
        self.assertEqual('0', result)

    def test_most_common_value_smaller_set(self):
        result = most_common_value(['10', '10', '01'], 0)
        self.assertEqual('1', result)

    def test_most_common_value_tie(self):
        result = most_common_value(['10', '10', '01', '01'], 0)
        self.assertEqual('1', result)

    def test_single_bit(self):
        result = single_bit_diagnostics(report(self.diagnostic_report), 0)
        self.assertEqual(['0', '1', '1', '1', '1', '0', '0', '1', '1', '1', '0', '0'], result)


if __name__ == '__main__':
    print("Advent of Code – Day 3: Binary Diagnostic")
    print("\nWhat is the power consumption of the submarine?")

    report = report(open('diagnostic_report'))
    gamma = gamma_rate(report)
    epsilon = epsilon_rate(report)
    print(f"gamma rate: {gamma}, epsilon rate: {epsilon}: power consumption: {gamma * epsilon}")

    print("\nWhat is the life support rating?")

    oxygen = oxygen_generator_rating(report)
    co2 = co2_scrubber_rating(report)
    print(f"oxygen generator rating: {oxygen}, co2 scrubber rating: {co2}: life support rating: {oxygen * co2}")