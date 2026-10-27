"""
Entelecheia colors for ParaView's Python shell.

ParaView highlights Python with pygments' built-in "default" style, so the
installer copies this file over pygments/styles/default.py inside ParaView's
bundled Python (the original is kept as default.py.orig).
Colors come from the terminal palette.
"""
from pygments.style import Style
from pygments.token import (Keyword, Name, Comment, String, Error, Number,
                            Operator, Generic, Whitespace, Punctuation)

__all__ = ['DefaultStyle']


class DefaultStyle(Style):
    name = 'default'
    background_color = "#161A1B"
    highlight_color = "#24404E"

    styles = {
        Whitespace:                "",
        Comment:                   "italic #6F7070",
        Comment.Preproc:           "noitalic #B59A5A",

        Keyword:                   "#B46CBC",          # magenta
        Keyword.Constant:          "#B59A5A",          # True / False / None
        Keyword.Namespace:         "#B46CBC",          # import / from
        Keyword.Type:              "#51A9A2",

        Operator:                  "#959393",
        Operator.Word:             "#B46CBC",          # and / or / not / in
        Punctuation:               "#959393",

        Name.Builtin:              "#51A9A2",          # cyan
        Name.Builtin.Pseudo:       "#B59A5A",          # self / cls
        Name.Function:             "#53A3C6",          # blue
        Name.Function.Magic:       "#53A3C6",
        Name.Class:                "bold #53A3C6",
        Name.Namespace:            "#53A3C6",
        Name.Decorator:            "#B59A5A",
        Name.Exception:            "#BF616A",
        Name.Variable.Magic:       "#B59A5A",

        String:                    "#73A569",          # green
        String.Doc:                "italic #73A569",
        String.Escape:             "#B59A5A",
        String.Interpol:           "#B59A5A",
        String.Affix:              "#B46CBC",          # f / r / b prefixes

        Number:                    "#B59A5A",          # yellow

        Generic.Heading:           "bold #53A3C6",
        Generic.Subheading:        "bold #B46CBC",
        Generic.Deleted:           "#BF616A",
        Generic.Inserted:          "#73A569",
        Generic.Error:             "#BF616A",
        Generic.Emph:              "italic",
        Generic.Strong:            "bold",
        Generic.Prompt:            "#6F7070",
        Generic.Output:            "#959393",
        Generic.Traceback:         "#BF616A",

        Error:                     "#BF616A",
    }
