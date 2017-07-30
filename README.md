# music-list-generator

   Do you like when your favorite music is cut befor the end? Me neither.

   This project will allow you to play music for a fix duration, without having to cut the last music before the end. Very useful for studying, for exemple: you set a time limit, and the program will find a list of music to play. When the music stops, it's time!

# how to use it
1)Change the files to put your name everywhere instead of mine (as in /home/user/Musique).\
location : \
->line 104 of AG_generator_of_list_of_music.py\
and\
->lines 39 and 69 of database.py\
\
2)Run database.py\
Check in a file called musique.sq3 is in your folder called "Musique".\
\
3)Run AG_generator_of_list_of_music.py. It should play music.

# dependences
   This program needs some dependences to works. To install them on debian (linux):\
\
sudo apt-get update\
then\
sudo apt-get install mediainfo mplayer\
\
You also have to be able to use "import sqlite3" with python 3:\
sudo apt-get install sqlite3\
\
Feel free to report any problem.
