from random import randint
from time import sleep

from core import Map, Pawn, Direction, BaseCell


class Unit(Pawn):
    @property
    def color(self):
        return "#123AAE"

    def run(self):
        self.move_towards(Direction((randint(-1, 1), randint(-1, 1))))
        sleep(0.05)


class Cell(BaseCell):
    @property
    def color(self):
        if self._stack:
            return "#122112"
        else:
            return "#AAAAAA"


m = Map(30, 50, Cell)
for i in range(10):
    m.add_pawn(Unit(), (15, 25))
u = Unit()
m.add_pawn(u, (14, 14))
m.remove_pawn(u)
m.mainloop()
