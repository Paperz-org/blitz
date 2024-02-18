from rich import print

ZERO = [
    " ██████╗ ",
    "██╔═████╗",
    "██║██╔██║",
    "████╔╝██║",
    "╚██████╔╝",
    " ╚═════╝ ",
    "        ",
]
ONE = [" ██╗", "███║", "╚██║", " ██║", " ██║", " ╚═╝", "    "]
TWO = [
    "██████╗ ",
    "╚════██╗",
    " █████╔╝",
    "██╔═══╝ ",
    "███████╗",
    "╚══════╝",
    "        ",
]
THREE = [
    "██████╗ ",
    "╚════██╗",
    " █████╔╝",
    " ╚═══██╗",
    "██████╔╝",
    "╚═════╝ ",
    "        ",
]
FOUR = [
    "██╗  ██╗",
    "██║  ██║",
    "███████║",
    "╚════██║",
    "     ██║",
    "     ╚═╝",
    "        ",
]

FIVE = [
    "███████╗",
    "██╔════╝",
    "███████╗",
    "╚════██║",
    "███████║",
    "╚══════╝",
    "        ",
]

SIX = [
    " ██████╗ ",
    "██╔════╝ ",
    "███████╗ ",
    "██╔═══██╗",
    "╚██████╔╝",
    " ╚═════╝ ",
    "         ",
]

SEVEN = [
    "███████╗",
    "╚════██║",
    "    ██╔╝",
    "   ██╔╝ ",
    "   ██║  ",
    "   ╚═╝  ",
    "        ",
]

HEIGHT = [
    " █████╗ ",
    "██╔══██╗",
    "╚█████╔╝",
    "██╔══██╗",
    "╚█████╔╝",
    " ╚════╝ ",
    "        ",
]

NINE = [
    " █████╗ ",
    "██╔══██╗",
    "╚██████║",
    " ╚═══██║",
    " █████╔╝",
    " ╚════╝ ",
    "        ",
]

BLITZ = [
    "██████╗ ██╗     ██╗████████╗███████╗",
    "██╔══██╗██║     ██║╚══██╔══╝╚══███╔╝",
    "██████╔╝██║     ██║   ██║     ███╔╝ ",
    "██╔══██╗██║     ██║   ██║    ███╔╝  ",
    "██████╔╝███████╗██║   ██║   ███████╗",
    "╚═════╝ ╚══════╝╚═╝   ╚═╝   ╚══════╝",
    "                                    ",
]


POINT = ["   ", "   ", "   ", "   ", "██╗", "╚═╝", "   "]
SPACE = ["    ", "    ", "    ", "    ", "    ", "    ", "    "]


def print_version(version: str) -> None:
    # https://patorjk.com/software/taag/#p=display&f=ANSI%20Shadow&t=BLITZ%200.1.0
    major, minor, patch = version.split(".")
    ASCII_INT_MAPPING = {
        "0": ZERO,
        "1": ONE,
        "2": TWO,
        "3": THREE,
        "4": FOUR,
        "5": FIVE,
        "6": SIX,
        "7": SEVEN,
        "8": HEIGHT,
        "9": NINE,
    }
    major_ascii = [ASCII_INT_MAPPING[i] for i in major]
    minor_ascii = [ASCII_INT_MAPPING[i] for i in minor]
    patch_ascii = [ASCII_INT_MAPPING[i] for i in patch]
    major_list = ["".join(col) for col in zip(*major_ascii)]
    minor_list = ["".join(col) for col in zip(*minor_ascii)]
    patch_list = ["".join(col) for col in zip(*patch_ascii)]

    for line in zip(BLITZ, SPACE, major_list, POINT, minor_list, POINT, patch_list):
        print(f"[bold medium_purple1]{''.join(line)}[/bold medium_purple1]")
