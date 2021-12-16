import curses
from curses.textpad import rectangle
from time import sleep

import pyperclip


class OctopusGrid():
    def __init__(self, puzzle_input, screen_y, screen_x, name):
        self.grid = {}
        self.step_nr = 0
        self.total_flashes = 0
        self.name = name
        y = 0
        for line in iter(puzzle_input.readline, ''):
            x = 0
            for char in list(line.strip()):
                self.grid |= {(y, x): int(char)}
                x += 1
            y += 1
        GRID_W = x * 2 + 1
        GRID_H = y
        CAPTION_H = 2
        FRAME_W = 1
        FRAME_H = 1
        self.window = curses.newwin(GRID_H + CAPTION_H + FRAME_H * 2, GRID_W + FRAME_W * 2, screen_y, screen_x)
        self.window_grid = curses.newwin(GRID_H, GRID_W, screen_y + FRAME_H, screen_x + FRAME_W)

    def all_octopuses(self, func):
        for y in range(10):
            for x in range(10):
                energy = self.octo_energy((y, x))
                func(y, x, energy)

    def draw(self):
        self.window.clear()
        rectangle(self.window, 0, 0, self.window_grid.getmaxyx()[0] + 1, self.window_grid.getmaxyx()[1] + 1)
        self.all_octopuses(lambda y, x, octo: self.window_grid.addch(y, x * 2 + 1, str(octo), curses.color_pair(octo+100)))
        self.window.addstr(0, 1, f" {self.name}: ")
        self.window.addstr(12, 1, f"Steps  : {self.step_nr:>12}")
        self.window.clrtoeol()
        self.window.addstr(13, 1, f"Flashes: {self.total_flashes:>12}")
        self.window.clrtoeol()
        self.window.refresh()
        self.window_grid.refresh()

    def octo_energy(self, octo):
        return self.grid.get(octo)

    def step(self):
        self.increase_energy()
        self.flash_octopuses()
        self.reset_octopuses()
        self.step_nr += 1
        self.draw()

    def set_octo_energy(self, octo, energy):
        self.grid.update({octo: energy})

    """
    First, the energy level of each octopus increases by 1.
    """

    def increase_energy(self):
        self.all_octopuses(lambda y, x, octo: self.set_octo_energy((y, x), octo + 1))

    """
    Then, any octopus with an energy level greater than 9 flashes. 
    This increases the energy level of all adjacent octopuses by 1, including octopuses that are diagonally adjacent. 
    If this causes an octopus to have an energy level greater than 9, it also flashes. This process continues as long as
     new octopuses keep having their energy level increased beyond 9. (An octopus can only flash at most once per step.)
    """

    def flash_octopuses(self):
        self.all_octopuses(lambda y, x, octo: self.flash_octopus((y, x), octo))

    def reset_octopuses(self):
        pass

    def flash_octopus(self, center_octopus, center_octopus_energy):
        if center_octopus_energy > 9:
            self.total_flashes += 1
            self.set_octo_energy(center_octopus, 0)
            for surrounding_octopus in self.surrounding_octopuses(center_octopus):
                if (surrounding_energy := self.octo_energy((surrounding_octopus))) != 0:
                    self.set_octo_energy(surrounding_octopus, surrounding_energy + 1)
                self.flash_octopus(surrounding_octopus, self.octo_energy(surrounding_octopus))
        pass

    def surrounding_octopuses(self, octopus):
        y = octopus[0]
        x = octopus[1]
        octos = [(y - 1, x - 1), (y - 1, x), (y - 1, x + 1),
                 (y, x - 1), (y, x + 1),
                 (y + 1, x - 1), (y + 1, x), (y + 1, x + 1)]
        return filter(lambda octo: self.octo_energy(octo) is not None, octos)

    def in_sync(self):
        return all(self.octo_energy(octo) == 0 for octo in self.grid.keys())


def pyFromHex(param):
    return tuple(round(int(param[i:i+2], 16) * 1000/255) for i in (0, 2, 4))


def main(stdscr):
    # Clear screen
    stdscr.clear()
    curses.curs_set(0)
    # https://coolors.co/03071e-370617-6a040f-9d0208-d00000-dc2f02-e85d04-f48c06-faa307-ffba08
    curses.init_color(100, *pyFromHex('03071e'))
    curses.init_color(101, *pyFromHex('370617'))
    curses.init_color(102, *pyFromHex('6a040f'))
    curses.init_color(103, *pyFromHex('9d0208'))
    curses.init_color(104, *pyFromHex('d00000'))
    curses.init_color(105, *pyFromHex('dc2f02'))
    curses.init_color(106, *pyFromHex('e85d04'))
    curses.init_color(107, *pyFromHex('f48c06'))
    curses.init_color(108, *pyFromHex('faa307'))
    curses.init_color(109, *pyFromHex('ffba08'))
    curses.init_pair(100, 109, curses.COLOR_BLACK)
    curses.init_pair(101, 100, curses.COLOR_BLACK)
    curses.init_pair(102, 101, curses.COLOR_BLACK)
    curses.init_pair(103, 102, curses.COLOR_BLACK)
    curses.init_pair(104, 103, curses.COLOR_BLACK)
    curses.init_pair(105, 104, curses.COLOR_BLACK)
    curses.init_pair(106, 105, curses.COLOR_BLACK)
    curses.init_pair(107, 106, curses.COLOR_BLACK)
    curses.init_pair(108, 107, curses.COLOR_BLACK)
    curses.init_pair(109, 108, curses.COLOR_BLACK)

    stdscr.addstr(0, 0, "Advent of Code – Day 11: Dumbo Octopus", curses.A_BOLD)
    stdscr.addstr(18, 0, "Press any key to start…", curses.A_BOLD)
    stdscr.clrtoeol()
    stdscr.refresh()
    stdscr.getkey()
    stdscr.addstr(18, 0, "Thinking…", curses.A_BOLD)
    stdscr.clrtoeol()
    stdscr.refresh()
    with open('example.txt') as puzzle_input:
        example_octopuses = OctopusGrid(puzzle_input, 3, 3, 'Example')
        example_octopuses.draw()
        for steps in range(100):
            sleep(10 / 100)
            example_octopuses.step()

    with open('puzzle_input.txt') as puzzle_input:
        puzzle_octopuses = OctopusGrid(puzzle_input, 3, 33, 'Puzzle')
        puzzle_octopuses.draw()
        for steps in range(100):
            sleep(10 / 100)
            puzzle_octopuses.step()

    pyperclip.copy(puzzle_octopuses.total_flashes)
    stdscr.addstr(18, 0, "The puzzle's solution has been copied to the clipboard. Press any key…", curses.A_BOLD)
    stdscr.refresh()
    stdscr.getkey()
    stdscr.addstr(18, 0, "Thinking…", curses.A_BOLD)
    stdscr.clrtoeol()
    stdscr.refresh()

    while True:
        example_in_sync = example_octopuses.in_sync()
        puzzle_in_sync = puzzle_octopuses.in_sync()
        if example_in_sync and puzzle_in_sync:
            break
        sleep(10 / 100)
        if not example_in_sync:
            example_octopuses.step()
        if not puzzle_in_sync:
            puzzle_octopuses.step()

    pyperclip.copy(puzzle_octopuses.step_nr)
    stdscr.addstr(18, 0, "The puzzle's solution has been copied to the clipboard. Press any key…", curses.A_BOLD)
    stdscr.refresh()
    stdscr.getkey()


curses.wrapper(main)
