import random
import itertools
from tkinter import *
from tkinter.font import Font

from app import App


if __name__ == '__main__':
    with open('input.txt') as file:
        line = file.readline()
    size = int(line.strip('\n'))
    app = App(size)
    app.mainloop()