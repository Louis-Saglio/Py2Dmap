import tkinter as _tk
from random import choices
from typing import Tuple, Union, Any


class MoveException(BaseException):
    pass


class Direction:
    def __init__(self, vector: Tuple[Union[int, float], Union[int, float]]):
        self.vector = vector


class Position:
    def __init__(self, position: Tuple[Union[int, float], Union[int, float]]):
        self._position = list(position)

    def __getitem__(self, item: int):
        return self._position[item]

    def __add__(self, direction: Direction):
        return Position((self._position[0] + direction.vector[0], self._position[1] + direction.vector[1]))

    def __hash__(self):
        return hash(tuple(self._position))

    def __eq__(self, other):
        return hash(self) == hash(other)


class Cell:
    def __init__(self, mother: "Map", position: Position, value: Any):
        self.value = value
        self.mother = mother
        self.position = position
        self.stack = []
        self.frame = None
        self.must_update_gui = True

    @property
    def color(self):
        raise NotImplementedError
        # return "#012345" if self.stack else "#543210"
        # return "#" + "".join(choices("0123456789ABCDEF", k=6))

    def update_gui(self):
        if self.frame is None:
            self.frame = _tk.Frame(
                self.mother, height=self.mother.cell_size, width=self.mother.cell_size, background=self.color
            )
        else:
            self.frame.configure(background=self.color)
        self.frame.grid(row=self.position[0], column=self.position[1])
        self.must_update_gui = False

    def get_cell_by_direction(self, direction: Direction) -> "Cell":
        return self.mother.cells[self.position + direction]

    def __hash__(self):
        return hash((hash(self.mother), hash(self.value), hash(self.position)))


class Map(_tk.Tk):
    def __init__(self, width: int, height: int):
        super().__init__()
        self.width = width
        self.height = height

        self.cell_size = 10

        self.cells = {}
        for i in range(self.width):
            for j in range(self.height):
                position = Position((i, j))
                self.cells[position] = Cell(self, position, None)

    def update_gui(self):
        for cell in self.cells.values():
            if cell.must_update_gui:
                cell.update_gui()

    def add_pawn(self, pawn: "Pawn", position: Tuple[int, int]):
        position_ = self.cells[Position(position)]
        position_.stack.append(pawn)
        pawn._cell = position_

    def mainloop(self, n=0):
        while True:
            for cell in self.cells.values():
                for pawn in cell.stack:
                    pawn.run()
                    self.update_gui()
                    self.update()


class Pawn:
    def __init__(self):
        self._cell: Cell = None

    def move(self, direction: Direction):
        if self._cell is None:
            raise MoveException(f"Can't move because this pawn is not positioned.")
        self._cell.stack.remove(self)
        self._cell.must_update_gui = True
        self._cell = self._cell.get_cell_by_direction(direction)
        self._cell.stack.append(self)
        self._cell.must_update_gui = True

    def run(self):
        raise NotImplementedError
        # self.move(Direction((randint(-1, 1), randint(1, 1))))
        # sleep(0.3)


def test():
    m = Map(30, 50)
    m.add_pawn(Pawn(), (15, 25))
    m.mainloop()


if __name__ == "__main__":
    test()
