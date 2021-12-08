import math
import unittest


class BingoSubsystem(object):
    last_called_number: int

    def __init__(self, init):
        for line in iter(init.readline, '\n'):
            self.drawn_numbers = line.strip().split(',')
        self.boards = list(iter(lambda: self.read_board(init), ''))

    @staticmethod
    def read_board(init):
        board = ""
        for line in iter(init.readline, '\n'):
            board += line
        return '' if board == "" else Board(board)

    def first_winning_board(self):
        for drawn_number in self.drawn_numbers:
            self.last_called_number = int(drawn_number)
            for board in self.boards:
                board.mark(drawn_number)
                if board.wins():
                    return board

    def score(self, b=None):
        if b is None:
            b = self.first_winning_board()
        return self.last_called_number * b.unmarkedSum()

    # TODO - this needs to be refactored!
    def last_winning_board(self):
        for drawn_number in self.drawn_numbers:
            self.last_called_number = int(drawn_number)
            boards_that_won = 0
            for board in self.boards:
                board.mark(drawn_number)
                if board.wins():
                    boards_that_won += 1
            if boards_that_won == len(self.boards) - 1:
                for board in self.boards:
                    if not board.wins():
                        for drawn_number2 in self.drawn_numbers:
                            self.last_called_number = int(drawn_number2)
                            board.mark(drawn_number2)
                            if board.wins():
                                return board


class Board(object):
    def __init__(self, initial_board):
        self.numbers = initial_board.split()
        self.size = int(math.sqrt(len(self.numbers)))
        pass

    def mark(self, marked_number):
        self.numbers = ['X' if current_number == marked_number else current_number for current_number in self.numbers]

    def mark_all(self, marked_numbers):
        for marked_number in marked_numbers:
            self.mark(marked_number)

    def wins(self):
        return any(self.full_match(line) for line in self.rows() + self.cols())

    def full_match(self, line):
        return self.size == sum(1 if number == 'X' else 0 for number in line)

    def row(self, index):
        return self.numbers[slice(index * self.size, (index + 1) * self.size)]

    def rows(self):
        return [self.row(index) for index in range(self.size)]

    def col(self, index):
        return self.numbers[slice(index, None, self.size)]

    def cols(self):
        return [self.col(index) for index in range(self.size)]

    def unmarkedSum(self):
        sum = 0
        for number in self.numbers:
            sum += 0 if number == 'X' else int(number)
        return sum


class Day4Test(unittest.TestCase):

    def setUp(self) -> None:
        self.board = Board("""   22 13 17 11  0
                                 8  2 23  4 24
                                21  9 14 16  7
                                 6 10  3 18  5
                                 1 12 20 15 19""")
        with open('bingo_test') as fp:
            self.bingoSubsystem = BingoSubsystem(fp)

    def test_initial_board_dimensions(self):
        self.assertEqual(5, self.board.size)

    def test_marked_numbers(self):
        self.board.mark_all(['1', '2', '3', '4'])
        self.assertEqual(
            ['22', '13', '17', '11', '0', '8', 'X', '23', 'X', '24', '21', '9', '14', '16', '7', '6', '10', 'X', '18',
             '5', 'X', '12', '20', '15', '19'], self.board.numbers)

    def test_looses(self):
        self.assertFalse(self.board.wins())

    def test_wins_with_row(self):
        self.board.mark_all("21  9 14 16  7".split())
        self.assertTrue(self.board.wins())

    def test_wins_with_column(self):
        self.board.mark_all("11 4 16 18 15".split())
        self.assertTrue(self.board.wins())

    def test_row0(self):
        self.assertEqual(list("22 13 17 11  0".split()), self.board.row(0))

    def test_row1(self):
        self.assertEqual(list(" 8  2 23  4 24".split()), self.board.row(1))

    def test_col0(self):
        self.assertEqual(list("22 8 21 6 1".split()), self.board.col(0))

    def test_col3(self):
        self.assertEqual(list("11 4 16 18 15".split()), self.board.col(3))

    def test_game_setup_drawn_numbers(self):
        self.assertEqual("7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1".split(','),
                         self.bingoSubsystem.drawn_numbers)

    def test_game_setup_boards(self):
        self.assertEqual(3, len(self.bingoSubsystem.boards))
        self.assertEqual("22 13 17 11  0".split(), self.bingoSubsystem.boards[0].row(0))
        self.assertEqual(" 3 15  0  2 22".split(), self.bingoSubsystem.boards[1].row(0))
        self.assertEqual("14 21 17 24  4".split(), self.bingoSubsystem.boards[2].row(0))

    def test_game_first_winning_board(self):
        b = self.bingoSubsystem.first_winning_board()
        self.assertEqual("""     X  X  X  X  X
                                10 16 15  X 19
                                18  8  X 26 20
                                22  X 13  6  X
                                 X  X 12  3  X""".split(), b.numbers)

    def test_last_called_number(self):
        b = self.bingoSubsystem.first_winning_board()
        self.assertEqual(24, self.bingoSubsystem.last_called_number)

    def test_sum_of_unmarked(self):
        b = self.bingoSubsystem.first_winning_board()
        self.assertEqual(188, b.unmarkedSum())

    def test_score_of_winning_board(self):
        self.assertEqual(4512, self.bingoSubsystem.score(None))

    def test_game_last_winning_board(self):
        b = self.bingoSubsystem.last_winning_board()
        self.assertEqual("""     3 15  X  X 22
                                 X 18  X  X  X
                                19  8  X 25  X
                                20  X  X  X  X
                                 X  X  X 12  6""".split(), b.numbers)

    def test_score_of_last_winning_board(self):
        b = self.bingoSubsystem.last_winning_board()
        self.assertEqual(1924, self.bingoSubsystem.score(b))


if __name__ == '__main__':
    print("Advent of Code – Day 4: Play Bingo")
    with open('bingo') as fp:
        bingoSubsystem = BingoSubsystem(fp)
        print(f"The score of the winning board is {bingoSubsystem.score()}")
        print(bingoSubsystem.first_winning_board().numbers)
        last = bingoSubsystem.last_winning_board()
        print(f"The score of the last winning board is {bingoSubsystem.score(last)}")
        print(last.numbers)
