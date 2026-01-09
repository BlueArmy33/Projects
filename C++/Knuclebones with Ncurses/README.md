# Knucklebones Game in C++

A terminal based implementation of the Knucklebones dice game built using C++ and the ncurses library. The game features a turn based system for two players, a visual grid displayed in the terminal, and real time score tracking.

This project demonstrates object oriented programming, terminal user interface development, and game logic implementation in C++.

## Features

- Two player turn based gameplay
- Dice rolling with random values
- Terminal based grid display using ncurses
- Real time score tracking and win detection
- Colored player output for clarity
- Input validation for grid placement

## Tech Stack

- C++
- ncurses
- Standard C++ libraries

## How to Compile and Run

This program requires the ncurses library.

### Compile
```bash
g++ knucklebones.cpp -lncurses -o knucklebones
