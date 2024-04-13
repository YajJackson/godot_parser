""" Wrappers for Godot's non-primitive object types """

from dataclasses import dataclass

__all__ = [
    "GDObject",
    "Vector2",
    "Vector3",
    "Color",
    "NodePath",
    "ExtResource",
    "SubResource",
]


@dataclass
class GDObject:
    """
    Base class for all GD Object types

    Can be used to represent any GD type. For example::

        GDObject('Vector2', 1, 2) == Vector2(1, 2)
    """

    name: str
    args: list

    @classmethod
    def from_parser(cls, parse_result) -> "GDObject":
        name = parse_result[0]
        args = parse_result[1:]
        return cls(name, args)

    def __str__(self) -> str:
        return f"{self.name}({', '.join(map(str, self.args))})"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        if not isinstance(other, GDObject):
            return False
        return self.name == other.name and self.args == other.args

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)


@dataclass
class Vector2(GDObject):
    _x: float
    _y: float

    def __init__(self, _x: float, _y: float):
        super().__init__(name="Vector2", args=[_x, _y])
        self._x = _x
        self._y = _y

    def __getitem__(self, idx) -> float:
        return self.args[idx]

    def __setitem__(self, idx: int, value: float):
        self.args[idx] = value

    @property
    def x(self) -> float:
        """Getter for x"""
        return self.args[0]

    @x.setter
    def x(self, x: float) -> None:
        """Setter for x"""
        self.args[0] = x

    @property
    def y(self) -> float:
        """Getter for y"""
        return self.args[1]

    @y.setter
    def y(self, y: float) -> None:
        """Setter for y"""
        self.args[1] = y


@dataclass
class Vector3(GDObject):
    _x: float
    _y: float
    _z: float

    def __init__(self, _x: float, _y: float, _z: float):
        super().__init__(name="Vector3", args=[_x, _y, _z])
        self._x = _x
        self._y = _y
        self._z = _z

    def __getitem__(self, idx: int) -> float:
        return self.args[idx]

    def __setitem__(self, idx: int, value: float) -> None:
        self.args[idx] = value

    @property
    def x(self) -> float:
        """Getter for x"""
        return self.args[0]

    @x.setter
    def x(self, x: float) -> None:
        """Setter for x"""
        self.args[0] = x

    @property
    def y(self) -> float:
        """Getter for y"""
        return self.args[1]

    @y.setter
    def y(self, y: float) -> None:
        """Setter for y"""
        self.args[1] = y

    @property
    def z(self) -> float:
        """Getter for z"""
        return self.args[2]

    @z.setter
    def z(self, z: float) -> None:
        """Setter for z"""
        self.args[2] = z


@dataclass
class Color(GDObject):
    _r: float
    _g: float
    _b: float
    _a: float

    def __init__(self, _r: float, _g: float, _b: float, _a: float):
        super().__init__(name="Color", args=[_r, _g, _b, _a])
        self._r = _r
        self._g = _g
        self._b = _b
        self._a = _a

        assert 0 <= self._r <= 1
        assert 0 <= self._g <= 1
        assert 0 <= self._b <= 1
        assert 0 <= self._a <= 1

    def __getitem__(self, idx: int) -> float:
        return self.args[idx]

    def __setitem__(self, idx: int, value: float) -> None:
        self.args[idx] = value

    @property
    def r(self) -> float:
        """Getter for r"""
        return self.args[0]

    @r.setter
    def r(self, r: float) -> None:
        """Setter for r"""
        self.args[0] = r

    @property
    def g(self) -> float:
        """Getter for g"""
        return self.args[1]

    @g.setter
    def g(self, g: float) -> None:
        """Setter for g"""
        self.args[1] = g

    @property
    def b(self) -> float:
        """Getter for b"""
        return self.args[2]

    @b.setter
    def b(self, b: float) -> None:
        """Setter for b"""
        self.args[2] = b

    @property
    def a(self) -> float:
        """Getter for a"""
        return self.args[3]

    @a.setter
    def a(self, a: float) -> None:
        """Setter for a"""
        self.args[3] = a


@dataclass
class NodePath(GDObject):
    _path: str

    def __init__(self, _path: str):
        super().__init__(name="NodePath", args=[_path])
        self._path = _path

    @property
    def path(self) -> str:
        """Getter for path"""
        return self.args[0]

    @path.setter
    def path(self, path: str) -> None:
        """Setter for path"""
        self.args[0] = path

    def __str__(self) -> str:
        return '%s("%s")' % (self.name, self.path)


@dataclass
class ExtResource(GDObject):
    _id: int

    def __init__(self, _id: int):
        super().__init__(name="ExtResource", args=[_id])
        self._id = _id

    @property
    def id(self) -> int:
        """Getter for id"""
        return self.args[0]

    @id.setter
    def id(self, id: int) -> None:
        """Setter for id"""
        self.args[0] = id


@dataclass
class SubResource(GDObject):
    _id: int

    def __init__(self, _id: int):
        super().__init__(name="SubResource", args=[_id])
        self._id = _id

    @property
    def id(self) -> int:
        """Getter for id"""
        return self.args[0]

    @id.setter
    def id(self, id: int) -> None:
        """Setter for id"""
        self.args[0] = id
