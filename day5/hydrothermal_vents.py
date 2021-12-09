import itertools
import unittest

X = 0
Y = 1


class VentWarningSystem():
    def __init__(self):
        self.vents = []

    def addVents(self, vents):
        for line in iter(vents.readline, ''):
            self.addVent(line)

    def addVent(self, vent):
        v = Vent(vent)
        if v.is_horizontal() or v.is_vertical():
            self.vents.append(v)

    def count_dangerous_areas(self):
        return len(self.dangerous_areas())

    def dangerous_areas(self):
        dangerous_areas = set()
        for v1 in self.vents:
            for v2 in itertools.takewhile(lambda v2: v2 is not v1, self.vents):
                print (f"  v2: {v2}")
                if (points := v1.intersection_points(v2)):
                    dangerous_areas.update(points)
        return dangerous_areas


class Vent(object):
    def __init__(self, vent_line):
        s = vent_line.split(' -> ')
        self.from_ = self.point_from_string(s[0])
        self.to_ = self.point_from_string(s[1])

    def __str__(self):
        return f"{self.from_} -> {self.to_}"

    @staticmethod
    def point_from_string(s):
        return tuple(map(lambda x: int(x), s.split(',')))

    def is_horizontal(self):
        return self.from_[Y] == self.to_[Y]

    def is_vertical(self):
        return self.from_[X] == self.to_[X]

    def starts_on_same(self, v2, axis):
        return self.from_[axis] == v2.from_[axis]

    def max(self, axis):
        return max(self.from_[axis], self.to_[axis])

    def min(self, axis):
        return min(self.from_[axis], self.to_[axis])

    def intersects(self, v2):
        if self.is_horizontal() and v2.is_horizontal():
            return self.line_overlaps(v2, X)
        elif self.is_vertical() and v2.is_vertical():
            return self.line_overlaps(v2, Y)
        else:
            return self.lines_crosses(v2)

    def line_overlaps(self, v2, axis):
        return self.starts_on_same(v2, 1-axis) and not (
                self.max(axis) < v2.min(axis) or self.min(axis) > v2.max(axis))

    def lines_crosses(self, v2):
        return self.method_name(v2) if self.is_horizontal() else v2.method_name(self)

    def method_name(self, v2):
        return self.min(X) <= v2.min(X) and v2.max(X) <= self.max(X) and \
                v2.min(Y) <= self.min(Y) and self.max(Y) <= v2.max(Y)

    def intersections(self, v2):
        intersections = 0
        if not self.intersects(v2):
            return 0
        if (self.is_horizontal() and v2.is_vertical()) or (self.is_vertical() and v2.is_horizontal()):
            return 1
        for p1 in self.points():
            for p2 in v2.points():
                intersections += 1 if p1 == p2 else 0
        print(f"Found {intersections} dangerous points for {self} and {v2}")
        return intersections

    def intersection_points(self, v2):
        if not self.intersects(v2):
            return []
        elif self.is_horizontal() and v2.is_vertical():
            return [(v2.from_[X], self.from_[Y])]
        elif self.is_vertical() and v2.is_horizontal():
            return [(self.from_[X], v2.from_[Y])]
        else:
            intersections = []
            for p1 in self.points():
                for p2 in v2.points():
                    if p1 == p2:
                        intersections.append(p1)
            return intersections

    def points(self):
        if self.is_horizontal():
            return iter([tuple([x, self.from_[Y]]) for x in range(self.min(X), self.max(X)+1)])
        elif self.is_vertical():
            return iter([tuple([self.from_[X], y]) for y in range(self.min(Y), self.max(Y)+1)])


class HydrothermalVentsTest(unittest.TestCase):

    def setUp(self) -> None:
        with open('lines_of_vents_test') as fp:
            self.vent_warning_system = VentWarningSystem()
            self.vent_warning_system.addVents(fp)

    def test_accepts_horizontal(self):
        vent_warning_system = VentWarningSystem()
        vent_warning_system.addVent('0,9 -> 5,9')
        self.assertEqual(1, len(vent_warning_system.vents))

    def test_accepts_vertical(self):
        vent_warning_system = VentWarningSystem()
        vent_warning_system.addVent('2,2 -> 2,1')
        self.assertEqual(1, len(vent_warning_system.vents))

    def test_ignores_diagonal(self):
        vent_warning_system = VentWarningSystem()
        vent_warning_system.addVent('8,0 -> 0,8')
        self.assertEqual(0, len(vent_warning_system.vents))

    def test_parse_vent(self):
        v = Vent('1,2 -> 3,4')
        self.assertTupleEqual(tuple([1, 2]), v.from_)
        self.assertTupleEqual(tuple([3, 4]), v.to_)

    def test_reads_vents(self):
        self.assertEqual(6, len(self.vent_warning_system.vents))

    def test_2horizontal_lines_intersect_left(self):
        v1 = Vent('3,4 -> 1,4')
        v2 = Vent('9,4 -> 3,4')
        self.assertTrue(Vent.intersects(v1, v2))

    def test_2horizontal_lines_intersect_outer(self):
        v1 = Vent('9,4 -> 1,4')
        v2 = Vent('8,4 -> 3,4')
        self.assertTrue(Vent.intersects(v1, v2))

    def test_2horizontal_lines_intersect_inner(self):
        v1 = Vent('3,4 -> 4,4')
        v2 = Vent('2,4 -> 5,4')
        self.assertTrue(Vent.intersects(v1, v2))

    def test_2horizontal_lines_intersect_right(self):
        v1 = Vent('5,4 -> 7,4')
        v2 = Vent('6,4 -> 3,4')
        self.assertTrue(Vent.intersects(v1, v2))

    def test_2horizontal_lines_dont_intersect_left(self):
        v1 = Vent('2,4 -> 1,4')
        v2 = Vent('4,4 -> 3,4')
        self.assertFalse(Vent.intersects(v1, v2))

    def test_2horizontal_lines_dont_intersect_right(self):
        v1 = Vent('5,4 -> 6,4')
        v2 = Vent('4,4 -> 3,4')
        self.assertFalse(Vent.intersects(v1, v2))

    def test_2vertical_lines_intersect_top(self):
        v1 = Vent('3,3 -> 3,4')
        v2 = Vent('3,4 -> 3,5')
        self.assertTrue(Vent.intersects(v1, v2))

    def test_crossing_lines_intersect(self):
        v1 = Vent('7,0 -> 7,4')
        v2 = Vent('9,4 -> 3,4')
        self.assertTrue(v1.intersects(v2))

    def test_crossing_lines_intersect2(self):
        v1 = Vent('9,4 -> 3,4')
        v2 = Vent('7,0 -> 7,4')
        self.assertTrue(v1.intersects(v2))

    def test_crossing_lines_dont_intersect(self):
        v1 = Vent('0,9 -> 5,9')
        v2 = Vent('2,2 -> 2,1')
        self.assertFalse(v1.intersects(v2))

    def test_count_overlap_horizontal1(self):
        self.assertIntersections(0, '0,5 -> 2,5', '3,5 -> 6,5')

    def test_count_overlap_horizontal2(self):
        self.assertIntersections(3, '0,5 -> 5,5', '3,5 -> 6,5')

    def test_count_overlap_horizontal3(self):
        self.assertIntersections(4, '3,5 -> 6,5', '3,5 -> 6,5')

    def test_count_overlap_horizontal4(self):
        self.assertIntersections(3, '4,5 -> 8,5', '3,5 -> 6,5')

    def test_count_overlap_horizontal5(self):
        self.assertIntersections(0, '7,5 -> 9,5', '3,5 -> 6,5')

    def test_count_overlap_vertical1(self):
        self.assertIntersections(0, '5,0 -> 5,2', '5,3 -> 5,6')

    def test_count_overlap_vertical2(self):
        self.assertIntersections(3, '5,0 -> 5,5', '5,3 -> 5,6')

    def test_count_overlap_vertical3(self):
        self.assertIntersections(1, '5,5 -> 5,5', '5,3 -> 5,6')

    def test_count_overlap_vertical4(self):
        self.assertIntersections(3, '5,4 -> 5,9', '5,3 -> 5,6')

    def test_count_overlap_vertical5(self):
        self.assertIntersections(0, '5,7 -> 5,9', '5,3 -> 5,6')







    def test_count_overlap_crossing_u2(self):
        self.assertIntersections(0, '3,5 -> 7,5', '2,3 -> 2,4')

    def test_count_overlap_crossing_u3(self):
        self.assertIntersections(0, '3,5 -> 7,5', '3,3 -> 3,4')

    def test_count_overlap_crossing_u5(self):
        self.assertIntersections(0, '3,5 -> 7,5', '5,3 -> 5,4')

    def test_count_overlap_crossing_u7(self):
        self.assertIntersections(0, '3,5 -> 7,5', '7,3 -> 7,4')

    def test_count_overlap_crossing_u8(self):
        self.assertIntersections(0, '3,5 -> 7,5', '8,3 -> 8,4')



    def test_count_overlap_crossing_ut2(self):
        self.assertIntersections(0, '3,5 -> 7,5', '2,3 -> 2,5')

    def test_count_overlap_crossing_ut3(self):
        self.assertIntersections(1, '3,5 -> 7,5', '3,3 -> 3,5')

    def test_count_overlap_crossing_ut5(self):
        self.assertIntersections(1, '3,5 -> 7,5', '5,3 -> 5,5')

    def test_count_overlap_crossing_ut7(self):
        self.assertIntersections(1, '3,5 -> 7,5', '7,3 -> 7,5')

    def test_count_overlap_crossing_ut8(self):
        self.assertIntersections(0, '3,5 -> 7,5', '8,3 -> 8,5')


    def test_count_overlap_crossing_x2(self):
        self.assertIntersections(0, '3,5 -> 7,5', '2,3 -> 2,8')

    def test_count_overlap_crossing_x3(self):
        self.assertIntersections(1, '3,5 -> 7,5', '3,3 -> 3,8')

    def test_count_overlap_crossing_x5(self):
        self.assertIntersections(1, '3,5 -> 7,5', '5,3 -> 5,8')

    def test_count_overlap_crossing_x7(self):
        self.assertIntersections(1, '3,5 -> 7,5', '7,3 -> 7,8')

    def test_count_overlap_crossing_x8(self):
        self.assertIntersections(0, '3,5 -> 7,5', '8,3 -> 8,8')


    def test_count_overlap_crossing_lt2(self):
        self.assertIntersections(0, '3,5 -> 7,5', '2,5 -> 2,8')

    def test_count_overlap_crossing_lt3(self):
        self.assertIntersections(1, '3,5 -> 7,5', '3,5 -> 3,8')

    def test_count_overlap_crossing_lt5(self):
        self.assertIntersections(1, '3,5 -> 7,5', '5,5 -> 5,8')

    def test_count_overlap_crossing_lt7(self):
        self.assertIntersections(1, '3,5 -> 7,5', '7,5 -> 7,8')

    def test_count_overlap_crossing_lt8(self):
        self.assertIntersections(0, '3,5 -> 7,5', '8,5 -> 8,8')


    def test_count_overlap_crossing_l2(self):
        self.assertIntersections(0, '3,5 -> 7,5', '2,6 -> 2,8')

    def test_count_overlap_crossing_l3(self):
        self.assertIntersections(0, '3,5 -> 7,5', '3,6 -> 3,8')

    def test_count_overlap_crossing_l5(self):
        self.assertIntersections(0, '3,5 -> 7,5', '5,6 -> 5,8')

    def test_count_overlap_crossing_l7(self):
        self.assertIntersections(0, '3,5 -> 7,5', '7,6 -> 7,8')

    def test_count_overlap_crossing_l8(self):
        self.assertIntersections(0, '3,5 -> 7,5', '8,5 -> 8,8')


    def test_dangerous_areas(self):
        areas = self.vent_warning_system.dangerous_areas()
        self.assertSetEqual({(3,4), (7,4), (0,9), (1,9), (2,9)}, areas)

    def assertIntersections(self, i, s, vent_line):
        v1 = Vent(s)
        v2 = Vent(vent_line)
        self.assertEqual(i, v1.intersections(v2))
        self.assertEqual(i, v2.intersections(v1))

    def test_count_intersections(self):
        self.assertEqual(5, self.vent_warning_system.count_dangerous_areas())

if __name__ == '__main__':
    print("Advent of Code – Day 5: Stay safe from vents")
    with open('lines_of_vents') as fp:
        vent_warning_system = VentWarningSystem()
        vent_warning_system.addVents(fp)
        dangerous_areas = vent_warning_system.count_dangerous_areas()
        print(f"WARNING: {dangerous_areas} dangerous areas ahead")
