Bullet Hell Engine
==================

Bullet Hell is a top-down style shooter game very similar to games like Galaga. Unlike games such as Galaga however, bullet hell shooters tend to have far more projectiles on screen at the same time, and turn into more of a dodging game. An example of such a game can be found [here](http://www.youtube.com/watch?v=w0vF-ixYAjY).

The purpose of this project is to build completly functional bullet hell libraries for Python that will allow other Python programers to come along and build their own games with it. Currently, this engine is entirely experimental, and changes may come that break and/or disable certain features that won't be re-enabled for long periods of time.

Running the Game
================

The game (the current test version) can be either started using either launcher.py or main.py. It is recommended that it be started with launcher, as this runs a few necessary checks before startup, however the main script can run on its own just as well. In order to run, both Python v2.7 ___and___ Pygame v1.9.2. These can be found here:

[Python v2.7](https://www.python.org/download/releases/2.7/)<br>
[Pygame v1.9.2](http://www.pygame.org/download.shtml)

Compiling/Setup
===============

The game uses a Cx_Freeze script to compile the game into a runnable executable. To run the setup script, make sure that it is in the same directory as launcher.py, open up either command prompt if on Windows, or terminal if on Unix, and type the following:

`setup.py build`

Once it is finished, it will create a folder named build_[month]-[day]-[year] with a number at the end if more than one build file has been created in one day. Inside will be both the source code and the compiled launcher.exe.

In order to run the setup script, Cx_Freeze is a required download. This can be found [here](http://sourceforge.net/projects/cx-freeze/files/).