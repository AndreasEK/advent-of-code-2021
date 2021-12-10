from itertools import groupby


class ClassOfFish:
    def __init__(self, age, size):
        self.age = age
        self.size = size

    def __str__(self):
        return f"This class contains {self.size} {'fish' if self.size == 1 else 'fishes'} of age {self.age}."


class SchoolOfFish:

    def __init__(self, class_):
        self.classes = list(map(lambda x: ClassOfFish(int(x[0]), len(list(x[1]))), groupby(sorted(class_.split(',')))))

    def aged(self):
        classes = []
        for c in filter(lambda x: x.age == 0, self.classes):
            classes.append(ClassOfFish(8,c.size))
        for c in filter(lambda x: x.age not in [0,7], self.classes):
            new_age = c.age - 1
            new_size = c.size
            classes.append(ClassOfFish(new_age, new_size))
        classes.append(ClassOfFish(6, sum(c.size for c in filter(lambda x: x.age in [0,7], self.classes))))

        self.classes = classes


if __name__ == '__main__':
    print("Advent of Code – Day 6: School of Glowing Lanternfishes")
    print('EXAMPLE')
    school = SchoolOfFish('3,4,3,1,2')
    for i in range(80):
        school.aged();
    for x in school.classes:
        print(x)
    print(f"In total these account for {sum(c.size for c in school.classes)} fishes")

    print('PART I')
    school = SchoolOfFish('1,2,1,1,1,1,1,1,2,1,3,1,1,1,1,3,1,1,1,5,1,1,1,4,5,1,1,1,3,4,1,1,1,1,1,1,1,5,1,4,1,1,1,1,1,1,1,5,1,3,1,3,1,1,1,5,1,1,1,1,1,5,4,1,2,4,4,1,1,1,1,1,5,1,1,1,1,1,5,4,3,1,1,1,1,1,1,1,5,1,3,1,4,1,1,3,1,1,1,1,1,1,2,1,4,1,3,1,1,1,1,1,5,1,1,1,2,1,1,1,1,2,1,1,1,1,4,1,3,1,1,1,1,1,1,1,1,5,1,1,4,1,1,1,1,1,3,1,3,3,1,1,1,2,1,1,1,1,1,1,1,1,1,5,1,1,1,1,5,1,1,1,1,2,1,1,1,4,1,1,1,2,3,1,1,1,1,1,1,1,1,2,1,1,1,2,3,1,2,1,1,5,4,1,1,2,1,1,1,3,1,4,1,1,1,1,3,1,2,5,1,1,1,5,1,1,1,1,1,4,1,1,4,1,1,1,2,2,2,2,4,3,1,1,3,1,1,1,1,1,1,2,2,1,1,4,2,1,4,1,1,1,1,1,5,1,1,4,2,1,1,2,5,4,2,1,1,1,1,4,2,3,5,2,1,5,1,3,1,1,5,1,1,4,5,1,1,1,1,4')
    for i in range(80):
        school.aged();
    for x in school.classes:
        print(x)
    print(f"In total these account for {sum(c.size for c in school.classes)} fishes")

    print('PART II')
    for i in range(256-80):
        school.aged();
    for x in school.classes:
        print(x)
    print(f"In total these account for {sum(c.size for c in school.classes)} fishes")

