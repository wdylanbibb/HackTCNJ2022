# Dungeon of Curses

Dungeon of Curses is a text-based top-down roguelike game, built by Elliot Topper and Dylan Bibb for HackTCNJ 2022.

The game is lighthearted game written in Python, and much of the development was focused on utilizing various resources in the game:

-   [curses](https://docs.python.org/3/library/curses.html)
-   [MealDB](https://www.themealdb.com/api.php) and [CocktailDB](https://www.thecocktaildb.com/api.php) APIs
-   [YAML file reading](https://pyyaml.org/)
-   [A\* pathfinding](https://pypi.org/project/pathfinding/)

There is also a public leaderboard API located at [https://dungeon-of-curses.herokuapp.com/highscores]

## Windows installation:

Make sure you have python 3.10 installed. ([Click here](https://www.python.org/downloads/) for download link)

To install necessary dependencies & run:

```
> Dungeonofcurses
```

## Linux installation:

Make sure you have python 3.10 installed. ([Click here](https://computingforgeeks.com/how-to-install-python-on-ubuntu-linux-system/) for intructions on Ubuntu)

Install `ncurses` using apt/pacman/whatever else you use for package management. For example, on Ubuntu, use

```
$ sudo apt-gt install libncurses-dev
```

to do so.

To install necessary dependencies & run:

```
$ python3.10 -m pip install users pyyaml requests pathfinding playsound soundfile pygame pillow

$ python3.10 main.py
```

## MacOS installation

Not sure tbh
