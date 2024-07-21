import re
import qdarktheme
from pathlib import Path
from PySide6.QtCore import Qt

ROOT_DIR = Path(__file__).parent.parent
FILES_DIR = ROOT_DIR / "files"
WINDOW_ICON_PATH = FILES_DIR / "calculator_icon"

KEYS = Qt.Key

ALING_RIGHT = Qt.AlignmentFlag.AlignRight
MARGINS = [12,12,12,12]
MAX_SIZE = 35
MEDIUM_SIZE = 24
SMALL_SIZE = 18

BUTTONS_COLORS = {
    "aDefault": "#1e81b0",
    "aHover": "#136991",
    "aClick": "#105778",
    "bDefault": "#d98536",
    "bHover": "#b8712e",
    "bClick": "#915924",
}

StyleQSS = f"""
QPushButton[cssClassOprations="oprationButton"] {{
        color: #fff;
        background: {BUTTONS_COLORS['aDefault']};
    }}
    QPushButton[cssClassOprations="oprationButton"]:hover {{
        color: #fff;
        background: {BUTTONS_COLORS['aHover']};
    }}
    QPushButton[cssClassOprations="oprationButton"]:pressed {{
        color: #fff;
        background: {BUTTONS_COLORS['aClick']};
    }}
    QPushButton[cssClassSpecial="specialButton"] {{
        color: #fff;
        background: {BUTTONS_COLORS['bDefault']};
    }}
    QPushButton[cssClassSpecial="specialButton"]:hover {{
        color: #fff;
        background: {BUTTONS_COLORS['bHover']};
    }}
    QPushButton[cssClassSpecial="specialButton"]:pressed {{
        color: #fff;
        background: {BUTTONS_COLORS['bClick']};
    }}
"""

def setupTheme():
    qdarktheme.setup_theme(
        theme="dark",
        corner_shape="rounded",
        custom_colors={
            "[dark]": {
                "primary": "#1e81b0"
            },
            "[light]": {
                "primary": "#1e81b0"
            },
        },
        additional_qss=StyleQSS
    )


NUM_OR_DOT_REGEX = re.compile(r'^[0-9.]$')

def isValidNumber(string: str) -> bool:
    try:
        float(string)
        return True
    except ValueError:
        return False

def isNumOrDot(string: str):
    return bool(NUM_OR_DOT_REGEX.search(string))

def isEmpty(string: str):
    return len(string) == 0

def isEqualORC(string: str):
    return string == "C" or string == "="

def convertToNumber(string: str):
    number = float(string)
    if number.is_integer():
        number = int(number)
    
    return number
