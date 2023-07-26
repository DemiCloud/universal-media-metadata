#!./.venv/bin/python3
"""Internal Variables"""


class variable:
    """Class for module variables"""

    name = "Universal Media Metadata"

    class table:
        class title:
            justify = "left"
            style = "bold cyan"


constants = variable()
print(constants.table.title.justify)
