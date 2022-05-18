# Itamar Laredo, 311547087
from app import App

if __name__ == '__main__':
    with open('input.txt') as file:
        line = file.readline()
    size = int(line.strip('\n'))
    app = App(size)
    app.mainloop()