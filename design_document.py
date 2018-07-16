from core import Map, Pawn

map = Map(8, 5)


class Unit(Pawn):
    @property
    def color(self):
        return "#12FFFAE"

    @property
    def position(self):
        return 1, 5


u = Unit()
map.add_unit(u)
u.move("up", 1)
