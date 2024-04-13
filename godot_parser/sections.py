from typing import Any, List, Optional, TypeVar
from dataclasses import dataclass, field


from .objects import ExtResource, SubResource
from .util import stringify_object

__all__ = [
    "GDSectionHeader",
    "GDSection",
    "GDNodeSection",
    "GDExtResourceSection",
    "GDSubResourceSection",
    "GDResourceSection",
]


@dataclass
class GDSectionHeader:
    """
    Represents the header for a section

    example::

        [node name="Sprite" type="Sprite" index="3"]
    """

    title: str
    name: Optional[str] = None
    id: Optional[int] = None
    path: Optional[str] = None
    type: Optional[str] = None
    format: Optional[int] = None
    load_steps: Optional[int] = None
    parent: Optional[str] = None
    index: Optional[str] = None
    instance: Optional[ExtResource] = None
    groups: Optional[List[str]] = None
    attributes: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.id is not None:
            self.attributes["id"] = self.id
        if self.path is not None:
            self.attributes["path"] = self.path
        if self.type is not None:
            self.attributes["type"] = self.type
        if self.format is not None:
            self.attributes["format"] = self.format
        if self.load_steps is not None:
            self.attributes["load_steps"] = self.load_steps

    def get(self, k: str, default: Any = None) -> Any:
        return self.attributes.get(k, default)

    @classmethod
    def from_parser(cls, parse_result) -> "GDSectionHeader":
        print(f"DEBUG | parse_result: {parse_result}")
        title = parse_result[0]
        header = cls(title)
        for attribute in parse_result[1:]:
            header.attributes[attribute[0]] = attribute[1]
        return header

    def __str__(self) -> str:
        attribute_str = ""
        if self.attributes:
            attribute_str = " " + " ".join(
                [
                    "{}={}".format(k, stringify_object(v))
                    for k, v in self.attributes.items()
                ]
            )
        return "[" + self.title + attribute_str + "]"

    def __getitem__(self, k: str) -> Any:
        return self.attributes[k]

    def __setitem__(self, k: str, v: Any) -> None:
        self.attributes[k] = v

    def __delitem__(self, k: str):
        try:
            del self.attributes[k]
        except KeyError:
            pass

    def __repr__(self) -> str:
        return f"GDSectionHeader({self})"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, GDSectionHeader):
            return False
        return self.title == other.title and self.attributes == other.attributes

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)


@dataclass
class GDSection:
    header: GDSectionHeader = field(default=GDSectionHeader(title="section"))
    properties: dict[str, Any] = field(default_factory=dict)

    def __getitem__(self, k: str) -> Any:
        return self.properties[k]

    def __setitem__(self, k: str, v: Any) -> None:
        self.properties[k] = v

    def __delitem__(self, k: str) -> None:
        try:
            del self.properties[k]
        except KeyError:
            pass

    def get(self, k: str, default: Any = None) -> Any:
        return self.properties.get(k, default)

    @classmethod
    def from_parser(cls, parse_result) -> "GDSection":
        print(f"DEBUG | GDSection.from_parser | parse_result: {parse_result}")
        header_title = parse_result[0]
        header = GDSectionHeader(title=header_title)
        section = cls(header=header)
        for k, v in parse_result[1:]:
            section[k] = v
        return section

    def __str__(self) -> str:
        ret = str(self.header)
        if self.properties:
            ret += "\n" + "\n".join(
                [
                    "%s = %s" % (k, stringify_object(v))
                    for k, v in self.properties.items()
                ]
            )
        return ret

    def __repr__(self) -> str:
        return "%s(%s)" % (type(self).__name__, self.__str__())

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, GDSection):
            return False
        return self.header == other.header and self.properties == other.properties

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)


@dataclass
class GDExtResourceSection(GDSection):
    """Section representing an [ext_resource]"""

    header: GDSectionHeader = field(default=GDSectionHeader(title="ext_resource"))

    @property
    def path(self) -> str:
        return self.header["path"]

    @path.setter
    def path(self, path: str) -> None:
        self.header["path"] = path

    @property
    def type(self) -> str:
        return self.header["type"]

    @type.setter
    def type(self, type: str) -> None:
        self.header["type"] = type

    @property
    def id(self) -> int:
        return self.header["id"]

    @id.setter
    def id(self, id: int) -> None:
        self.header["id"] = id

    @property
    def reference(self) -> ExtResource:
        return ExtResource(_id=self.id)


class GDSubResourceSection(GDSection):
    """Section representing a [sub_resource]"""

    def __init__(self, type: str, id: int, **kwargs):
        super().__init__(GDSectionHeader("sub_resource", type=type, id=id), **kwargs)

    @property
    def type(self) -> str:
        return self.header["type"]

    @type.setter
    def type(self, type: str) -> None:
        self.header["type"] = type

    @property
    def id(self) -> int:
        return self.header["id"]

    @id.setter
    def id(self, id: int) -> None:
        self.header["id"] = id

    @property
    def reference(self) -> SubResource:
        return SubResource(_id=self.id)


@dataclass
class GDNodeSection(GDSection):
    """Section representing a [node]"""

    @classmethod
    def ext_node(cls):
        # header = GDSectionHeader(
        #     "node", name=name, instance=instance, parent=parent, index=index
        # )
        header = GDSectionHeader(title="node")
        return cls(header=header)

    @property
    def name(self) -> str:
        return self.header.title

    @name.setter
    def name(self, name: str) -> None:
        self.header.title = name

    @property
    def type(self) -> Optional[str]:
        return self.header.type

    @type.setter
    def type(self, type: Optional[str]) -> None:
        if type is None:
            self.header.type = None
            del self.header.type
        else:
            self.header.type = type
            self.instance = None

    @property
    def parent(self) -> Optional[str]:
        return self.header.parent

    @parent.setter
    def parent(self, parent: Optional[str]) -> None:
        if parent is None:
            self.header.parent = None
            del self.header.parent
        else:
            self.header.parent = parent

    @property
    def instance(self) -> Optional[int]:
        resource = self.header.instance
        if resource is not None:
            return resource.id
        return None

    @instance.setter
    def instance(self, instance: Optional[int]) -> None:
        if instance is None:
            self.header.instance = None
            del self.header.instance
        else:
            self.header.instance = ExtResource(instance)
            self.type = None

    @property
    def index(self) -> Optional[int]:
        idx = self.header.index
        if idx is not None:
            return int(idx)
        return None

    @index.setter
    def index(self, index: Optional[int]) -> None:
        if index is None:
            self.header.index = None
            del self.header.index
        else:
            self.header.index = str(index)

    @property
    def groups(self) -> Optional[List[str]]:
        return self.header.get("groups")

    @groups.setter
    def groups(self, groups: Optional[List[str]]) -> None:
        if groups is None:
            self.header.groups = None
            del self.header.groups
        else:
            self.header.groups = groups


@dataclass
class GDResourceSection(GDSection):
    """Represents a [resource] section"""

    pass
