from core import Map, Pawn, Direction

map = Map(8, 5)


class Unit(Pawn):
    @property
    def color(self):
        return "#12FFFAE"


UP = Direction((1, 1))
u = Unit()
map.add_pawn(u, (2, 3))
u.move(UP)
