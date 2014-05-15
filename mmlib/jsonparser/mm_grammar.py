from pyparsing import (
    Literal, alphas, nums, alphanums, OneOrMore, Word,
    ZeroOrMore, Forward, oneOf, Group, Optional, Combine, stringEnd,
    ParseException, ParseSyntaxException
)

def generate_reference_bnf():
    """
    Grammar for the references allowed in the schemes:

    item     :: {sublist|index|key|subdict}
    sublist :: '['{digit}':'[-]{digit}']'
    index    :: '['digit']'
    subdict  :: '{'words{,words}'}'

    words  :: alnum{alnum}
    alpha :: a | b | ... | z | A | B | ... | Z
    digit :: 0 | 1 | ... | 9
    alnum :: alpha | digit
    """
    lbracket = Literal("[").suppress()
    rbracket = Literal("]").suppress()
    quote = Literal('\'').suppress()
    dblquote = Literal('"').suppress()
    lbrace = Literal("{").suppress()
    rbrace = Literal("}").suppress()
    dash = Literal("-")
    colon = Literal(":")
    words = OneOrMore(Word(alphanums + "_-"))
    number = Combine(Optional(dash) + Word(nums))
    space = Literal(" ")
    commaSep = (Literal(",") + Optional(space)).suppress()
    bar = Literal("|").suppress()
    filter_fn = Combine(bar + words)

    # Wrapper functions for readability
    def braces(s):
        return lbrace + s + rbrace

    def brackets(s):
        return lbracket + s + rbracket

    def quotes(s):
        return quote + s + quote

    def dblquotes(s):
        return dblquote + s + dblquote

    # Dictionaries: ["some string"]
    # With optional filter function: ["some string"]|bool
    key = Group(\
            (brackets(quotes(words)) + Optional(filter_fn)) ^\
            (brackets(dblquotes(words)) + Optional(filter_fn))\
            )

    # Indexes: [5]
    index = Group(brackets(number))

    # Subrange: [5:-1]
    sublist = Group(brackets(Optional(number) + colon + Optional(number)))

    # Subdictionary: {"some string", "some otherstring"}, {"singleone"}
    subdictSingleQuotedSingle = braces(quotes(words))
    subdictSingleQuotedMultiple = braces(quotes(words) + OneOrMore(commaSep + quotes(words)))
    subdictDblQuotedSingle = braces(dblquotes(words))
    subdictDblQuotedMultiple = braces(dblquotes(words) + OneOrMore(commaSep + dblquotes(words)))
    subdict = Group(subdictSingleQuotedSingle ^ subdictSingleQuotedMultiple ^ \
                    subdictDblQuotedSingle ^ subdictDblQuotedMultiple)

    item = key("key") ^ \
           index("index") ^ \
           sublist("sublist") ^ \
           subdict("subdict")

    term = OneOrMore(item)
    return term

REFERENCE_BNF = generate_reference_bnf()
