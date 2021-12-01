# coding=utf-8
import unittest

def sweep(file):
    sonar_sweep_report = open('./' + file, 'r')
    measurements = sonar_sweep_report.readlines()
    return [int(single_measurement) for single_measurement in measurements]

def is_deeper(two_measures):
    return two_measures[1] > two_measures[0]

def count_deeper_measures(sonar_measures):
    count = 0
    for i in pairs(sonar_measures):
        if (is_deeper(i)):
            count+=1
    return count

# https://stackoverflow.com/a/5764806/1474250
def pairs(seq):
    i = iter(seq)
    prev = next(i)
    for item in i:
        yield prev, item
        prev = item

def three_item_window(seq):
    i = iter(seq)
    first = next(i)
    second = next(i)
    for item in i:
        yield (first, second, item)
        first = second
        second = item

def sliding_sums(sonar_measures):
    return map(lambda tuple: tuple[0] + tuple[1] + tuple [2], three_item_window(sonar_measures))

class MyTestCase(unittest.TestCase):
    def test_read_sweep_report(self):
        sonar_measures = sweep('sonar_sweep_report_test')
        self.assertEqual([199, 200, 208, 210, 200, 207, 240, 269, 260, 263], sonar_measures)

    def test_detect_deeper_measures(self):
        does_get_deeper = is_deeper((1, 2))
        self.assertEqual(True, does_get_deeper)

    def test_detect_shallower_measures(self):
        does_get_deeper = is_deeper((2, 1))
        self.assertEqual(False, does_get_deeper)

    def test_detect_equal_measures(self):
        does_get_deeper = is_deeper((2, 2))
        self.assertEqual(False, does_get_deeper)

    def test_count_deeper_measures(self):
        sonar_measures = sweep('sonar_sweep_report_test')
        deeper_measures = count_deeper_measures(sonar_measures)
        self.assertEqual(7, deeper_measures)

    def test_sliding_window(self):
        sonar_measures = sweep('sonar_sweep_report_test')
        sliding_sequence = three_item_window(sonar_measures)
        self.assertEqual(next(sliding_sequence),(199, 200, 208))
        self.assertEqual(next(sliding_sequence),(200,208,210))
        self.assertEqual(next(sliding_sequence),(208,210,200))
        self.assertEqual(next(sliding_sequence),(210,200,207))
        self.assertEqual(next(sliding_sequence),(200,207,240))
        self.assertEqual(next(sliding_sequence),(207,240,269))
        self.assertEqual(next(sliding_sequence),(240,269,260))
        self.assertEqual(next(sliding_sequence),(269,260,263))
        self.assertRaises(StopIteration, next, sliding_sequence)

    def test_sliding_sum(self):
        sonar_measures = sweep('sonar_sweep_report_test')
        sliding_sums1 = sliding_sums(sonar_measures)
        self.assertEqual(sliding_sums1, [607, 618, 618, 617, 647, 716, 769, 792])

    def test_count_deeper_measures_from_sliding_window(self):
        sonar_measures = sweep('sonar_sweep_report_test')
        deeper_measures = count_deeper_measures(sliding_sums(sonar_measures))
        self.assertEqual(5, deeper_measures)

if __name__ == '__main__':
    print("Advent of Code – Day 1")
    print("How many measurements are larger than the previous measurement?")

    sonar_measures = sweep('sonar_sweep_report')
    deeper_measures = count_deeper_measures(sonar_measures)

    print('The sonar sweep report shows {} times a deeper measurement!'.format(deeper_measures))

    deeper_measures_from_window = count_deeper_measures(sliding_sums(sonar_measures))

    print('When taking a sliding window into account, the report shows {} times deeper measures!'.format(deeper_measures_from_window))
