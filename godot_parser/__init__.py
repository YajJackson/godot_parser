from .files import *
from .objects import *
from .sections import *
from .tree import *
from beartype.claw import beartype_this_package

beartype_this_package()

__version__ = "0.1.7"

parse = GDFile.parse

load = GDFile.load
