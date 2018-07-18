import tkinter as _tk
from random import randint
from time import sleep
from typing import Tuple, Union, Any


class MoveException(BaseException):
    pass


class BadPositionException(BaseException):
    pass


class InvalidColor(BaseException):
    pass


class Direction:
    def __init__(self, vector: Tuple[Union[int, float], Union[int, float]]):
        self.vector = vector

    def __repr__(self):
        return f"Direction{{{self.vector}}}"


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

    def __repr__(self):
        return f"Position{{{self[0], self[1]}}}"


class Cell:
    def __init__(self, mother: "Map", position: Position):
        self.mother = mother
        self.position = position
        self._stack = []
        self.frame = None
        self.update_gui()

    def put(self, pawn: "Pawn"):
        # todo : move to Pawn ?
        self._stack.append(pawn)
        self.update_gui()
        pawn._cell = self

    def remove(self, pawn: "Pawn"):
        self._stack.remove(pawn)
        self.update_gui()
        pawn._cell = None

    @property
    def color(self):
        raise NotImplementedError

    def update_gui(self):
        if self.color is None:
            raise InvalidColor(f"Can't use {self.color} as a valid color")
        if self.frame is None:
            self.frame = _tk.Frame(
                self.mother, height=self.mother.cell_size, width=self.mother.cell_size, background=self.color
            )
        else:
            self.frame.configure(background=self.color)
        self.frame.grid(row=self.position[0], column=self.position[1])

    def get_cell_by_direction(self, direction: Direction) -> "Cell":
        try:
            position = self.position + direction
            return self.mother.cells[position]
        except KeyError:
            raise BadPositionException(
                f"Position {position} does not exist. Minimum {self.mother.width}, maximum {self.mother.height}"
            )

    def __iter__(self):
        for pawn in self._stack:
            yield pawn

    def __hash__(self):
        return hash((hash(self.mother), hash(self.position)))

    def __repr__(self):
        return f"Cell{{stack : {self._stack}, position : {self.position}}}"


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
                self.cells[position] = Cell(self, position)

    def add_pawn(self, pawn: "Pawn", position: Tuple[int, int]):
        cell = self.cells[Position(position)]
        cell.put(pawn)

    def mainloop(self, n=0):
        while True:
            for cell in self.cells.values():
                for pawn in cell:
                    pawn.run()
                    self.update()

    def __repr__(self):
        return "Map"
    #     return f"Map{{ {self.width, self.height} {self.cells}}}"


class Pawn:
    def __init__(self):
        self._cell: Cell = None

    @property
    def color(self):
        raise NotImplementedError

    def move(self, direction: Direction):
        if self._cell is None:
            raise MoveException("Can't move because this pawn is not positioned")
        next_cell = self._cell.get_cell_by_direction(direction)  # Do not corrupt self._cell if an error is incoming
        self._cell.remove(self)
        next_cell.put(self)

    def run(self):
        raise NotImplementedError

    def __repr__(self):
        return f"{self.__class__.__name__}:{id(self)}"


def test():
    m = Map(30, 50)
    m.add_pawn(Pawn(), (15, 25))
    m.mainloop()


if __name__ == "__main__":
    test()
