from time import sleep

from core import Map, Pawn, Direction, BaseCell


class Unit(Pawn):
    @property
    def color(self):
        return "#123AAE"

    def run(self):
        self.move(Direction((1, 1)))
        sleep(0.01)


class Cell(BaseCell):
    @property
    def color(self):
        if self._stack:
            return "#122112"
        else:
            return "#AAAAAA"


m = Map(30, 50, Cell)
for i in range(1):
    m.add_pawn(Unit(), (15, 25))
m.mainloop()
