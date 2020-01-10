# Azul

This repository contains a simple implementation of the Azul board game, implemented in Python.

This implementation is a port of a [Racket](https://racket-lang.org/) implementation of Azul written
for a school project.

Note that:

* This implementation lacks documentation. If needed, they can be requested by an issue (or PR :} )
* Python used in this project is a bit awkward. This is due to direct translation of the original implementation.
* If you don't like anything about the interface, it should be trivial to change that (hopefully)
* Although this is a port, it is very likely I have messed up the translation somewhere. If you happen to find out, feel free to open an issue
  (and sorry if a bug causes issues :( ).

## Playing

Simply run `main.py` to play the game. Then, follow the instructions below to play.

## How To

![alt text](https://raw.githubusercontent.com/trajafri/Azul/master/images/PAzul.png "Prompt at the beginning of a 2v2 game")

Initially, a player is selected randomly. To make a move, enter the following:
* Factory Number: This is 1 based. To access the middle factory, simply type `m`. The program should handle errors when the factory number is incorrect (oob or if the factory chosen is empty).
* Tile Number: This is a number between 0-4 (these are the tiles seen on in the factories).
* Line Number: A number between 0-4. An out of bound line number will move the tiles to the overflow region.

An example input is as follows:
`1 4 1`

The above input will move the `4` tiles from `f-1` to staging line `1` of player 1.
