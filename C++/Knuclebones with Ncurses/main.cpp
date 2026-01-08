/*
Author: Andrea Lobo
Date: April 2025
Description: A game of knucklebones that used Ncurses to be played properly
*/

#include <ncurses.h>
#include <cstdlib>
#include <ctime>
#include <string>

// ------------------ Player Class ------------------
class Player {
public:
    Player(const std::string& name) : name(name), score(0) {}

    void add_to_score(int points) { score += points; }
    int get_score() const { return score; }
    std::string get_name() const { return name; }

private:
    std::string name;
    int score;
};

// ------------------ Dice Class ------------------
class Dice {
public:
    Dice() { std::srand(std::time(nullptr)); }

    int roll() { return std::rand() % 6 + 1; } // Random number [1, 6]

private:
    int current_value;
};

// ------------------ Grid Class ------------------
class Grid {
public:
    Grid() { 
        for (int i = 0; i < 3; ++i) 
            for (int j = 0; j < 3; ++j) 
                cells[i][j] = 0; 
    }

    bool place_dice(int row, int col, int value) {
        if (row < 0 || row >= 3 || col < 0 || col >= 3 || cells[row][col] != 0)
            return false;
        cells[row][col] = value;
        return true;
    }

    void display_grid(int start_y, int start_x) {
        for (int i = 0; i < 3; ++i) {
            for (int j = 0; j < 3; ++j) {
                mvprintw(start_y + i, start_x + j * 4, "[%d]", cells[i][j]);
            }
        }
    }

private:
    int cells[3][3];
};

// ------------------ Game Class ------------------
class Game {
public:
    Game() : current_player_index(0) {
        players[0] = Player("Player 1");
        players[1] = Player("Player 2");
    }

    void start() {
        initscr();
        noecho();
        cbreak();
        curs_set(0);
        keypad(stdscr, TRUE);
        start_color();
        init_pair(1, COLOR_RED, -1);
        init_pair(2, COLOR_BLUE, -1);

        bool running = true;
        while (running) {
            clear();
            display_game_state();
            take_turn();
            running = !check_win();
            switch_turn();
        }

        end_game();
        endwin();
    }

private:
    Player players[2];
    int current_player_index;
    Dice dice;
    Grid grid;

    void take_turn() {
        Player& current_player = players[current_player_index];
        attron(COLOR_PAIR(current_player_index + 1));
        mvprintw(1, 0, "%s's Turn!", current_player.get_name().c_str());
        attroff(COLOR_PAIR(current_player_index + 1));

        int roll = dice.roll();
        mvprintw(3, 0, "You rolled a %d!", roll);
        mvprintw(4, 0, "Enter row (0-2): ");
        int row = get_number_input();
        mvprintw(5, 0, "Enter column (0-2): ");
        int col = get_number_input();

        if (!grid.place_dice(row, col, roll)) {
            mvprintw(7, 0, "Invalid placement. Try again.");
            getch();
        } else {
            current_player.add_to_score(roll);
        }
    }

    void display_game_state() {
        mvprintw(0, 0, "Knucklebones Game");
        mvprintw(2, 0, "Scoreboard:");
        for (int i = 0; i < 2; ++i) {
            attron(COLOR_PAIR(i + 1));
            mvprintw(3 + i, 0, "%s: %d points", players[i].get_name().c_str(), players[i].get_score());
            attroff(COLOR_PAIR(i + 1));
        }
        mvprintw(6, 0, "Grid:");
        grid.display_grid(7, 2);
    }

    void switch_turn() {
        current_player_index = 1 - current_player_index;
    }

    int get_number_input() {
        int ch = getch();
        while (ch < '0' || ch > '2') {
            mvprintw(10, 0, "Invalid input. Enter a number (0-2): ");
            ch = getch();
        }
        return ch - '0';
    }

    bool check_win() {
        if (players[0].get_score() >= 50 || players[1].get_score() >= 50) {
            clear();
            mvprintw(0, 0, "Game Over!");
            if (players[0].get_score() > players[1].get_score()) {
                mvprintw(1, 0, "%s wins with %d points!", players[0].get_name().c_str(), players[0].get_score());
            } else if (players[1].get_score() > players[0].get_score()) {
                mvprintw(1, 0, "%s wins with %d points!", players[1].get_name().c_str(), players[1].get_score());
            } else {
                mvprintw(1, 0, "It's a tie!");
            }
            mvprintw(3, 0, "Press any key to exit.");
            getch();
            return true;
        }
        return false;
    }

    void end_game() {
        mvprintw(10, 0, "Thank you for playing!");
        refresh();
        getch();
    }
};

// ------------------ Main Function ------------------
int main() {
    Game game;
    game.start();
    return 0;
}