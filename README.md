# CS550 Final: CLASSWORK

The prompt of this project was to solve a problem. We decided to solve the problem of boredom in class by hide games in a user's screen so that they could be played without other people knowing. 

## Getting Started

This program runs in Python 3.7 on MacOS or Windows and requires the Python Imaging Library (PIL) and PyGame installed on the device.
```
pip install pil
pip install pygame
```

## Operating Instructions

To start the program, run home.py using your command shell program.
```
python3 home.py
```
Once the program is running, the user has 3 seconds to go to their chosen background window before the program takes a screenshot that will be used as the backgroud of the game. There are three games to choose from, a "sneaky" snake game, a "buried" brick breaker game, and a multiplayer "groupwork" game. This can be chosen through the GUI after launch. The snake game is controlled using 'W' for up, 'M' for down, 'L' for left and 'A' for right. These controls were chosen to make it less obvious that the user is playing a game. For brick breaker the controls are just the arrow keys, left arrow for left, right arrow for right. For groupwork (2-player Pong), players use I, M and W, X to control their respective paddles. The cursor object, that is used in all games, changes depending on the user's OS. While playing, the user can minimize and pause the game by pressing esc and resume by reopening the window and pressing any movement key. The user can exit back to the main menu using esc when each game is over or paused. On the main menu, the user can quit by pressing esc. 
```
Sneaky Snake:
W - up
A - left
M - down
L - right
ESC - pause when game is running, exit to main menu when game is paused/over

Buried Brick:
LEFT ARROW - paddle left
RIGHT ARROW - paddle right
ESC - pause when game is running, exit to main menu when game is paused/over

Groupwork:
W - Player 1 Up
X - Player 1 Down
I - Player 2 Up
M - Player 2 Down
ESC - pause when game is running, exit to main menu when game is paused/over
```

## Learn more

There are two examples of translucency in this game,one using the alpha property of png files, and another using RGB manipulations of the background to emulate transparency and offset to emulate "diffraction" of light.