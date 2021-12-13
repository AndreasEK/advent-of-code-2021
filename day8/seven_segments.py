def method_name():
    return sum(
        len(list(filter(lambda digit: len(digit) in [6], list(line.strip().split('|')[1].strip().split(' ')))))
        for line in iter(puzzle_input.readline, ''))


def input2(line):
    l = line.strip().split('|')
    return l[0].strip().split(' '), l[1].strip().split(' ')


def method2(unique_signal_patterns, four_digit_output_value):
    mapping = {}
    working_copy = [*unique_signal_patterns]
    working_copy2 = [*working_copy]
    while working_copy2:
        for pattern in working_copy2:
            match set(pattern), len(pattern):
                case _, 2:
                    mapping[1] = set(pattern)
                    working_copy.remove(pattern)
                case _, 3:
                    mapping[7] = set(pattern)
                    working_copy.remove(pattern)
                case _, 4:
                    mapping[4] = set(pattern)
                    working_copy.remove(pattern)
                case _, 7:
                    mapping[8] = set(pattern)
                    working_copy.remove(pattern)

                # 3 -> enthält '7' und länge 5
                case p, 5 if mapping.get(7) is not None and p.issuperset(mapping[7]):
                    mapping[3] = set(pattern)
                    working_copy.remove(pattern)

                # 0 -> enthält '7' aber nicht '3' und länge 6
                # 9 -> enthält '7' & '3' und länge 6
                # 6 -> enthält nicht '1' und länge 6
                case p, 6 if mapping.get(7) is not None and p.issuperset(mapping[7]) and mapping.get(
                        3) is not None and not p.issuperset(mapping[3]):
                    mapping[0] = set(pattern)
                    working_copy.remove(pattern)
                case p, 6 if mapping.get(7) is not None and p.issuperset(mapping[7]) and mapping.get(
                        3) is not None and p.issuperset(mapping[3]):
                    mapping[9] = set(pattern)
                    working_copy.remove(pattern)
                case p, 6 if mapping.get(1) is not None and not p.issuperset(mapping[1]):
                    mapping[6] = set(pattern)
                    working_copy.remove(pattern)
                # 5 -> in '6' enthalten und länge 5
                # 2 ->
                case p, 5 if mapping.get(6) is not None and p.issubset(mapping[6]):
                    mapping[5] = set(pattern)
                    working_copy.remove(pattern)
                case p, 5 if mapping.get(5) is not None and mapping.get(3) is not None:
                    mapping[2] = set(pattern)
                    working_copy.remove(pattern)
        working_copy2 = [*working_copy]
    result = 0
    while four_digit_output_value:
        result *= 10
        digit = four_digit_output_value.pop(0)
        for key, value in mapping.items():
            if set(digit) == value:
                result += key
    return result


if __name__ == '__main__':
    print("Advent of Code – Day 8: Seven Segment Search")
    with open('example.txt') as puzzle_input:
        counter = method_name()
        print(f"There were {counter}!")
    print("Example Part II")
    with open('example.txt') as puzzle_input:
        sum_of_output = 0
        for line in iter(puzzle_input.readline, ''):
            unique_signal_patterns, four_digit_output_value = input2(line)
            value = method2(unique_signal_patterns, four_digit_output_value)
            sum_of_output += value
            print(f"{unique_signal_patterns} | {four_digit_output_value} -> {value}")
        print(f"In sum, this is {sum_of_output}")
    with open('puzzle_part1.txt') as puzzle_input:
        counter = method_name()
        print(f"There were {counter}!")
    print("Part II")
    with open('puzzle_part1.txt') as puzzle_input:
        sum_of_output = 0
        for line in iter(puzzle_input.readline, ''):
            unique_signal_patterns, four_digit_output_value = input2(line)
            value = method2(unique_signal_patterns, four_digit_output_value)
            sum_of_output += value
            print(f"{unique_signal_patterns} | {four_digit_output_value} -> {value}")
        print(f"In sum, this is {sum_of_output}")
