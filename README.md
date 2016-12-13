# README
This game was made in 48 hours by Alexandre Mattenet (alex@mattenet.com)
for the Ludum Dare 37 compo.

## description
Garden of Eden is a game about loneliness and growing transgenic plants on mars.

It uses ideas from the book [The algorithmic beauty of plants](http://algorithmicbotany.org/papers/#abop) to simulate plants, and affect random mutations and gene crossing between different plant models.

All assets, including the music, were made by me.

I also used a [menu system made by GummBumm](http://code.google.com/p/simple-pygame-menu/) and an [input box made by Timothy Downs](http://www.pygame.org/pcr/inputbox/).

## how to run
The game is made with [pygame](http://www.pygame.org/hifi.html) and [numpy](http://www.numpy.org/) in [python 3](https://www.python.org/). If you have pygame, python3 and numpy installed, you should be able to run it. The main python file is game.py.

### linux
Make sure you have all dependencies installed:

- Ubuntu: `sudo apt-get install python3 python3-numpy python3-pip` and `sudo pip3 install pygame`.
- Arch Linux: `sudo pacman -S python-numpy python-pip` and `sudo pip3 install pygame`.

Then cd to the garden_of_eden directory and
```
$python3 game.py
```

### windows and mac
I don't know very well, try to install pygame, numpy and python from the links provided, ensuring that you're using version 3.something and not 2.7, then try to click on game.py

![screenshot 1](https://github.com/gadevoi/ludumdare37/blob/master/Screenshot_20161212_014217.png?raw=true)
![screenshot 2](https://github.com/gadevoi/ludumdare37/blob/master/Screenshot_20161212_014311.png?raw=true)
