""" The grammar of low-level values in the GD file format """

from pyparsing import (
    DelimitedList,
    Forward,
    Group,
    Keyword,
    Opt,
    ParseResults,
    ParserElement,
    QuotedString,
    Suppress,
    Word,
    alphanums,
    alphas,
    common,
)

from .objects import GDObject


def parse_action_function(parse_results: ParseResults) -> bool:
    result = parse_results[0]
    if isinstance(result, bool):
        return result
    if isinstance(result, str):
        return result.lower() == "true"
    raise ValueError(f"Unexpected result: {result}")


boolean: ParserElement = (
    (Keyword("true") | Keyword("false"))
    .set_name("bool")
    .set_parse_action(parse_action_function)
)

null = Keyword("null").set_parse_action(lambda _: [None])


primitive = (
    null | QuotedString('"', escChar="\\", multiline=True) | boolean | common.number
)
value = Forward()
non_generic_types = Forward()

# Vector2( 1, 2 )
obj_type = (
    Word(alphas, alphanums).set_results_name("object_name")
    + Suppress("(")
    + DelimitedList(value)
    + Suppress(")")
).set_parse_action(GDObject.from_parser)

# [ 1, 2 ] or [ 1, 2, ]
list_ = (
    Group(
        Suppress("[") + Opt(DelimitedList(value)) + Opt(Suppress(",")) + Suppress("]")
    )
    .set_name("list")
    .set_parse_action(lambda p: p.as_list())
)
key_val = Group(QuotedString('"', escChar="\\") + Suppress(":") + value)

# {
# "_edit_use_anchors_": false
# }
dict_ = (
    (Suppress("{") + Opt(DelimitedList(key_val)) + Suppress("}"))
    .set_name("dict")
    .set_parse_action(lambda d: {k: v for k, v in d})
)

non_generic_types <<= primitive | list_ | dict_ | obj_type


# Handles constructs like Array[Object](...)
def parse_generic_type(parse_results: ParseResults):
    toks = parse_results.asList()
    type_name = toks[0]
    args = toks[1:]
    return (type_name, *args)


generic_type = (
    Word(alphas, alphanums + "[]")
    + Suppress("(")
    + Opt(DelimitedList(value, delim=","))
    + Suppress(")")
).set_parse_action(parse_generic_type)

# Exports
value <<= non_generic_types | generic_type
