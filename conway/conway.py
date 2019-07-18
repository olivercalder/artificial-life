#   File: final.py
#   Created by: Oliver Calder, November 2018
#
#   Generous thanks to Jeff Ondich for providing invaluable guidance and help
#       with this project and many others, and for introducing me to the wonders
#       of computer science through his course (the first of many, I hope).
#   Acknowledgements to John Zelle for creating the graphics.py library and the
#       textbook "Python Programming: An Introductio to Computer Science", which
#       has been the foundation of my knowledge of coding and computer science.
#   Acknowledgements as well to John Conway, whose iconic "Game of Life" is the
#       inspiration for this program.
#
#
#   Version 1.0.20181119.1
#       - Added controls to mouse and keyboard event handlers
#       - Program works
#   Version 0.8.20181119
#       - Added Button class
#       - Added Grid.clear() and Grid.randomize() methods
#       - Added pause_notifier for grid
#       - Added Grid.get_width_pixels() and Grid.get_height_pixels()
#       - Added Grid.step() method
#   Version 0.7.20181117
#       - Fixed updating problem by re-implementing grid.prepare_next in
#           addition to grid.update() in the time handler
#       - Removed redundant adjacency checking within update() method, both for
#           speed purposes and accuracy
#   Version 0.6.20181116
#       - Created CalderWin class based on GraphWin, which contains handlers for
#           time, mouse clicks, and key presses
#       - Transferred initial parameters and grid creation from main to
#           ConwayWin
#       - Fixed very slow check_click() method by adding
#           convert_pixels_to_coords() method in Grid class
#               - If coords are not in range of grid, then does nothing
#               - If coords are in range of grid, then uses
#                   convert_coords_to_slot() and toggles square directly
#   Version 0.5.20181115.3
#       - Added while loop in main() for modifying initial grid setup by
#           processing clicks [BROKEN]
#       - Added while loop in main() for updating the grid based on the rules,
#           [Works when tested with random initial conditions]
#   Version 0.4.20181115.2
#       - Created functioning main to draw blank grid and check next state
#       - Fixed Grid square creation parameters
#       - Fixed various bugs and syntax errors
#       - Fixed error where square checked adjacent squares immediately, before
#           the other squares had finished drawing themselves
#   Version 0.3.20181115.1
#       - Added coordinates for adjacent squares
#       - Added wrap_or_trunc parameter and tests for check_adj for
#       - Added toggle_lines method for Grid
#       - Added draw methods for Grid and Square
#   Version 0.2.20181114
#       - Added grid positon coordinates as parameter for Square
#       - Added check methods and update method for squares
#       - Added parameter for modified rules
#       - Added convert_coords_to_slot function
#       - Added get_color method for grid
#   Version 0.1.20181112
#       - GUI based on graphics.py by John M. Zelle
#       - Added Grid and Square classes

try:
    from tkinter import *
except:
    from Tkinter import *
from calder_graphics import *
from random import randint
import sys

class Controls:

    def __init__(self, win, grid, controls_buffer):
        self.win = win
        self.grid = grid
        self.controls_buffer = controls_buffer
        self.button_x = self.grid.get_width_pixels() + self.controls_buffer/2
        self.button_width = self.controls_buffer * 2/3
        self.button_height = self.button_width / 2
        self.purposes = ['Play/Pause', 'Step', 'Clear Grid', 'Randomize']
        self.buttons = []
        button_y = 0
        for purpose in self.purposes:
            button_y += self.button_height + 50
            button_center = Point(self.button_x, button_y)
            button = Button(self.win, self.grid, purpose, button_center, self.button_width, self.button_height)
            self.buttons.append(button)

    def check_click(self, point):
        for button in self.buttons:
            if button.check_if_clicked(point):
                if button.purpose == 'Play/Pause':
                    self.grid.toggle_pause()
                elif button.purpose == 'Step':
                    self.grid.step()
                elif button.purpose == 'Clear Grid':
                    self.grid.clear()
                elif button.purpose == 'Randomize':
                    self.grid.randomize()


class Button:

    def __init__(self, win, grid, purpose, center, width, height, color='lightgray'):
        self.win = win
        self.grid = grid
        self.purpose = purpose
        self.center = center
        self.width = width
        self.height = height
        self.color = color
        self.top_left = Point(self.center.getX() - self.width/2, self.center.getY() - self.height/2)
        self.bottom_right = Point(self.center.getX() + self.width/2, self.center.getY() + self.height/2)
        self.rect = Rectangle(self.top_left, self.bottom_right)
        self.rect.setFill(color)
        self.rect.draw(self.win)
        self.label = Text(self.center, self.purpose)
        self.label.draw(self.win)

    def check_if_clicked(self, point):
        found = False
        if self.top_left.getX() <= point.getX() <= self.bottom_right.getX():
            if self.top_left.getY() <= point.getY() <= self.bottom_right.getY():
                found = True
        return found


class Square:

    def __init__(self, win, grid, square_size, grid_columns, grid_rows, number, grid_coords, rules):
        self.win = win
        self.grid = grid
        self.size = square_size
        self.grid_columns = grid_columns
        self.grid_rows = grid_rows
        self.number = number
        self.grid_coords = grid_coords
        self.rules = rules
        self.current = randint(0,2) #0
        self.next = randint(0,2) #0
        self.top_left = Point(self.grid_coords[0]*self.size, self.grid_coords[1]*self.size)
        self.bottom_right = Point((self.grid_coords[0]+1) * self.size - 1, (self.grid_coords[1]+1) * self.size - 1)
        self.rect = Rectangle(self.top_left, self.bottom_right)

    def getX(self):
        return self.grid_coords[0]

    def getY(self):
        return self.grid_coords[1]

    def check_self(self):
        return self.current

    def check_adj(self):
        wrap_or_trunc = self.grid.wrap_or_trunc
        x_pos = self.getX()
        y_pos = self.getY()
        adj_live = 0
        adjacent_coords = [[x_pos - 1, y_pos - 1],
                           [x_pos    , y_pos - 1],
                           [x_pos + 1, y_pos - 1],
                           [x_pos - 1, y_pos    ],
                           [x_pos + 1, y_pos    ],
                           [x_pos - 1, y_pos + 1],
                           [x_pos    , y_pos + 1],
                           [x_pos + 1, y_pos + 1]]
        for coord in adjacent_coords:
            x, y = coord[:]
            if x < 0 or x > self.grid.get_columns() - 1 or y < 0 or y > self.grid.get_rows() - 1:
                if wrap_or_trunc == 'wrap':
                    if x == -1:
                        x = self.grid.get_columns() - 1
                    elif x == self.grid.get_columns():
                        x = 0
                    if y == -1:
                        y = self.grid.get_rows() - 1
                    elif y == self.grid.get_rows():
                        y = 0
                elif wrap_or_trunc == 'trunc':
                    pass # do nothing, pretend the nonexistent square is dead
            slot = self.grid.convert_coords_to_slot(x, y)
            adj_live += self.grid.squares[slot].check_self()
        if self.current == 1 and adj_live in self.rules[0]:
            self.next = 1
        elif self.current == 0 and adj_live in self.rules[1]:
            self.next = 1
        else:
            self.next = 0

    def update(self):
        self.current = self.next
        self.update_color()

    def update_color(self):
        if self.current == 0:
            self.rect.setFill(self.grid.get_color('neg'))
        elif self.current == 1:
            self.rect.setFill(self.grid.get_color('pos'))
        self.rect.setOutline(self.grid.get_color('bord'))

    def flip_state(self):
        if self.current == 0:
            self.current = 1
            self.update_color()
        elif self.current == 1:
            self.current = 0
            self.update_color()

    def draw(self):
        self.update()
        self.rect.draw(self.win)


class Grid:

    def __init__(self, win, width=100, height=100, square_size=8, colors=['white', 'black', 'black'], rules=[[2,3],[3]], wrap_or_trunc='wrap', outline=True):
        self.win = win
        self.grid = self
        self.colors = colors
        self.rules = rules
        self.wrap_or_trunc = wrap_or_trunc
        self.outline = outline
        self.square_size = square_size
        self.columns = width
        self.rows = height
        self.win_label = "Conway's Game of Life"
        self.squares_total = self.columns * self.rows
        self.squares = []
        self.is_paused = True
        for slot in range(self.squares_total):
            x_pos = slot % self.columns
            y_pos = slot // self.columns
            grid_coords = [x_pos, y_pos]
            square = Square(self.win, self.grid, self.square_size, self.columns, self.rows, slot, grid_coords, self.rules)
            self.squares.append(square)
        self.draw()

    def get_columns(self):
        return self.columns

    def get_rows(self):
        return self.rows

    def get_width_pixels(self):
        return self.columns * self.square_size

    def get_height_pixels(self):
        return self.rows * self.square_size

    def get_color(self, neg_pos_bord):
        if neg_pos_bord == 'neg':
            return self.colors[0]
        elif neg_pos_bord == 'pos':
            return self.colors[1]
        elif neg_pos_bord == 'bord':
            if self.outline:
                try:
                    border = self.colors[2]
                except:
                    if self.colors[0] == 'black':
                        border = 'white'
                    else:
                        border = 'black'
                return border
            else:
                return self.colors[0]

    def toggle_lines(self):
        if self.outline == True:
            self.outline = False
        elif self.outline == False:
            self.outline == True
        for square in self.squares:
            outline_color = self.get_color('bord')
            square.rect.setOutline(outline_color)

    def prepare_next(self):
        for square in self.squares:
            square.check_adj()

    def update(self):
        for square in self.squares:
            square.update()

    def draw(self):
        for square in self.squares:
            square.draw()

    def clear(self):
        for square in self.squares:
            square.current = 0
            square.update_color()
        self.prepare_next()

    def randomize(self):
        for square in self.squares:
            square.current = randint(0, 2)
            square.update_color()
        self.prepare_next()

    def toggle_pause(self):
        self.is_paused = not self.is_paused

    def step(self):
        self.is_paused = True
        self.prepare_next()
        self.update()

    def convert_coords_to_slot(self, x_pos, y_pos):
        slot = int(self.get_columns() * y_pos + x_pos)
        return slot

    def convert_pixels_to_slot(self, point):
        x_pos = point.getX() // self.square_size
        y_pos = point.getY() // self.square_size
        if 0 <= x_pos < self.columns and 0 <= y_pos < self.rows:
            slot = self.convert_coords_to_slot(x_pos, y_pos)
            return slot
        else:
            return None

    def check_click(self, point):
        slot = self.convert_pixels_to_slot(point)
        if slot != None:
            self.squares[slot].flip_state()


class ConwayWin(GraphWin):

    def __init__(self, title="Conway's Game of Life", grid_width=100, grid_height=100, square_size=8, colors=['white', 'black', 'black'], rules=[[2,3], [3]], wrap_or_trunc='wrap', outline=True):
        self.title = title
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.square_size = square_size
        self.colors = colors
        self.rules = rules
        self.wrap_or_trunc = wrap_or_trunc
        self.outline = True
        self.controls_buffer = 300
        self.window_width = self.grid_width * self.square_size + self.controls_buffer
        self.window_height = self.grid_height * self.square_size
        GraphWin.__init__(self, self.title, self.window_width, self.window_height, autoflush=False)
        self.setBackground(self.colors[0])
        self.win = self
        self.tick = 1 #milliseconds
        self.grid = Grid(self.win, self.grid_width, self.grid_height, self.square_size, self.colors, self.rules, self.wrap_or_trunc, self.outline)
        self.controls = Controls(self.win, self.grid, self.controls_buffer)
        self.grid_center = Point(grid_width*square_size/2, grid_height*square_size/2)
        self.pause_notifier = Text(self.grid_center, 'Paused')
        self.pause_notifier.setStyle('italic')
        self.pause_notifier.setSize(36)
        self.pause_notifier.setTextColor('red')
        calder_root.after(self.tick, self.timer_handler)
        self.bind_all('<Button-1>', self.mouse_handler)
        self.bind_all('<Key>', self.key_handler)

    def timer_handler(self):
        if self.grid.is_paused == False:
            self.pause_notifier.undraw()
            self.grid.prepare_next()
            self.grid.update()
        else:
            self.pause_notifier.undraw()
            self.pause_notifier.draw(self.win)
        calder_root.after(self.tick, self.timer_handler)

    def mouse_handler(self, event):
        x = event.x
        y = event.y
        self.grid.check_click(Point(x, y))
        self.grid.prepare_next()
        self.controls.check_click(Point(x, y))

    def key_handler(self, event):
        if event.char == ' ':
            self.grid.toggle_pause()
        if event.char == '.':
            self.grid.step()
        if event.char == 'c':
            self.grid.clear()
        if event.char == 'r':
            self.grid.randomize()

def main():
    if len(sys.argv) == 3:
        grid_width = int(sys.argv[1])
        grid_height = int(sys.argv[2])
    elif len(sys.argv) == 2:
        grid_width = int(sys.argv[1])
        grid_height = int(sys.argv[1])
    else:
        grid_width = 100
        grid_height = 100
    square_size = 8
    colors = ['white', 'black', 'black']
    rules = [[2,3], [3]]
        # rules[0] is a list, [min, max], of the min and max possible numbers of
        #   neighbors needed to survive if cell is already alive.
        # rules[1] is a list, [int, int, ... int], with the possible neighbor values
        #   at which a dead cell will come to life.
    wrap_or_trunc = 'wrap'
    outline = True
    win = ConwayWin("Conway's Game of Life", grid_width, grid_height, square_size, colors, rules, wrap_or_trunc, outline)
    while win.winfo_exists():
        win.update()

if __name__ == '__main__':
    main()
