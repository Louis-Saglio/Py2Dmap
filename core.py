import tkinter as _tk
from typing import Tuple, Union


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


class BaseCell:
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
        pawn.cell = self

    def remove(self, pawn: "Pawn"):
        self._stack.remove(pawn)
        self.update_gui()
        pawn.cell = None

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

    def get_cell_by_direction(self, direction: Direction, default=BadPositionException) -> "BaseCell":
        position = self.position + direction
        cell = self.mother.cells.get(position, default)
        if cell is not BadPositionException:
            return cell
        raise BadPositionException(
            f"Position {position} does not exist. Maximum {self.mother.width - 1}, {self.mother.height - 1}"
        )

    def __hash__(self):
        return hash((hash(self.mother), hash(self.position)))

    def __repr__(self):
        return f"{self.__class__.__name__}{{stack : {self._stack}, position : {self.position}}}"


class Map(_tk.Tk):
    def __init__(self, width: int, height: int, cell_class: type):
        super().__init__()
        self.width = width
        self.height = height
        self.cell_size = 10

        self.pawns = set()

        self.cells = {}
        for i in range(self.width):
            for j in range(self.height):
                position = Position((i, j))
                self.cells[position]: BaseCell = cell_class(self, position)

    def add_pawn(self, pawn: "Pawn", position: Tuple[int, int]):
        cell = self.cells[Position(position)]
        cell.put(pawn)
        self.pawns.add(pawn)

    def remove_pawn(self, pawn: "Pawn"):
        self.pawns.remove(pawn)
        pawn.cell.remove(pawn)

    def mainloop(self, n=0):
        while True:
            pawns = self.pawns.copy()
            for pawn in pawns:
                if pawn in self.pawns:
                    try:
                        pawn.run()
                        self.update()
                    except _tk.TclError:
                        exit()

    def __repr__(self):
        return f"Map:{id(self)}"


class Pawn:
    def __init__(self):
        self.cell: BaseCell = None

    @property
    def color(self):
        raise NotImplementedError

    def go_to(self, next_cell: BaseCell):
        self.cell.remove(self)
        next_cell.put(self)

    def move_towards(self, direction: Direction):
        self.go_to(self.cell.get_cell_by_direction(direction))

    def run(self):
        raise NotImplementedError

    def __repr__(self):
        return f"{self.__class__.__name__}:{id(self)}"
