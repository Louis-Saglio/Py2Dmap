from time import sleep

from core import Map, Pawn, Direction


class Unit(Pawn):
    @property
    def color(self):
        return "#123AAE"

    def run(self):
        self.move(Direction((1, 1)))
        sleep(0.1)


m = Map(30, 50)
for i in range(1):
    m.add_pawn(Unit(), (15, 25))
m.mainloop()
