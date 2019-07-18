# conway
### _A python implementation of Conway's Game of Life._

Program filename: conway.py

Created by: Oliver Calder, November 2018

#### To Run:

`python3 conway.py [width] [height]`

#### To End:

Enter kill command in terminal: `^C`, which is `[Ctrl]+[C]`

#### Dependency Note:
This program requires the _tkinter_ module for python 3

For Ubuntu users: `sudo apt install python3-tk`

For Fedora users: `sudo dnf install python3-tkinter`

For Arch users: `sudo pacman -S tk`

--------------------------------------------------------------------------------

This program runs Conway's Game of Life using Python and a modified version of
    Zelle's graphics.py library, which is based on Tkinter.

The game begins paused, and can be controlled using the buttons to the right
    of the grid.
- The Play/Pause button toggles pause for the program.
  - Alternatively: `[Space]`
- The Step button steps one tick ahead in the program and then pauses.
  - Alternatively: `[.]`
- The Clear Grid button replaces all squares on the grid with blank squares.
  - Alternatively: `[C]`
- The Randomize button randomizes the grid.
  - Alternatively: `[R]`

Additional customization is available by calling ConwayWin with different
    parameters, but this level of control is not set up to be mutable once the
    game window is opened.

--------------------------------------------------------------------------------

Generous thanks to Jeff Ondich for providing invaluable guidance and help
    with this project and many others, and for introducing me to the wonders
    of computer science through his course (the first of many, I hope).

Acknowledgments to John Zelle for creating the graphics.py library and the
    textbook "Python Programming: An Introduction to Computer Science", which
    has been the foundation of my knowledge of coding and computer science.

Acknowledgments as well to John Conway, whose iconic "Game of Life" is the
    inspiration for this program.


Version 1.0.20181119.1
- Added controls to mouse and keyboard event handlers
- Program works

Version 0.8.20181119
- Added Button class
- Added Grid.clear() and Grid.randomize() methods
- Added pause_notifier for grid
- Added Grid.get_width_pixels() and Grid.get_height_pixels()
- Added Grid.step() method

Version 0.7.20181117
- Fixed updating problem by re-implementing grid.prepare_next in
        addition to grid.update() in the time handler
- Removed redundant adjacency checking within update() method, both for
        speed purposes and accuracy

Version 0.6.20181116
- Created CalderWin class based on GraphWin, which contains handlers for
        time, mouse clicks, and key presses
- Transferred initial parameters and grid creation from main to
        ConwayWin
- Fixed very slow check_click() method by adding
        convert_pixels_to_coords() method in Grid class
  - If coords are not in range of grid, then does nothing
  - If coords are in range of grid, then uses
            convert_coords_to_slot() and toggles square directly

Version 0.5.20181115.3
- Added while loop in main() for modifying initial grid setup by
        processing clicks [BROKEN]
- Added while loop in main() for updating the grid based on the rules,
        [Works when tested with random initial conditions]

Version 0.4.20181115.2
- Created functioning main to draw blank grid and check next state
- Fixed Grid square creation parameters
- Fixed various bugs and syntax errors
- Fixed error where square checked adjacent squares immediately, before
        the other squares had finished drawing themselves

Version 0.3.20181115.1
- Added coordinates for adjacent squares
- Added wrap_or_trunc parameter and tests for check_adj for
- Added toggle_lines method for Grid
- Added draw methods for Grid and Square

Version 0.2.20181114
- Added grid positon coordinates as parameter for Square
- Added check methods and update method for squares
- Added parameter for modified rules
- Added convert_coords_to_slot function
- Added get_color method for grid

Version 0.1.20181112
- GUI based on graphics.py by John M. Zelle
- Added Grid and Square classes
