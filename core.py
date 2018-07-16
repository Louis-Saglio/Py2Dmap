import tkinter as _tk
from random import choices
from typing import Tuple, Union, Any


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


class Cell:
    def __init__(self, mother: "Map", position: Position, value: Any):
        self.value = value
        self.mother = mother
        self.position = position
        self.stack = []
        self.frame = None

    @property
    def color(self):
        # raise NotImplementedError
        return "#" + "".join(choices("0123456789ABCDEF", k=6))

    def configure_gui(self):
        if self.frame is None:
            self.frame = _tk.Frame(
                self.mother, height=self.mother.cell_size, width=self.mother.cell_size, background=self.color
            )
        else:
            self.frame.configure(background=self.color)
        self.frame.grid(row=self.position[0], column=self.position[1])

    def __hash__(self):
        return hash((hash(self.mother), hash(self.value), hash(self.position)))


class Map(_tk.Tk):
    def __init__(self, width: int, height: int):
        super().__init__()
        self.width = width
        self.height = height

        self.cell_size = 10

        self.cells = set()
        for i in range(self.width):
            for j in range(self.height):
                self.cells.add(Cell(self, Position((i, j)), None))

    def configure_gui(self):
        for cell in self.cells:
            cell.configure_gui()


def test():
    Direction((0, -1))
    p = Position((5, 3))
    m = Map(40, 52)
    Cell(m, p, None)
    m.configure_gui()
    m.mainloop()


if __name__ == "__main__":
    test()
