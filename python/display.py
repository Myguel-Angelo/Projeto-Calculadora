from PySide6.QtCore import Signal
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QWidget

from utils import ALING_RIGHT, KEYS, MARGINS, MAX_SIZE, SMALL_SIZE
from utils import isEmpty, isNumOrDot

class MiniDisplay(QLabel):
    def __init__(self, text: str, parent: QWidget | None = None):
        super().__init__(text, parent)
        self._configure()
    
    def _configure(self):
        self.setStyleSheet(f"font-size: {SMALL_SIZE}px")
        self.setAlignment(ALING_RIGHT)

class Display(QLineEdit):
    eqPressed = Signal()
    delPressed = Signal()
    escPressed = Signal()
    inputPressed = Signal(str)
    opPressed = Signal(str)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()
    
    def configStyle(self):
        self.setStyleSheet(f"font-size: {MAX_SIZE}px")
        self.setMinimumHeight(2*MAX_SIZE)
        self.setMinimumWidth(370)
        self.setAlignment(ALING_RIGHT)
        self.setTextMargins(*MARGINS)
    
    def keyPressEvent(self, event: QKeyEvent) -> None:
        text = event.text().strip()
        key = event.key()
        
        isEnter = key in [KEYS.Key_Enter, KEYS.Key_Return, KEYS.Key_Equal]
        isDelete = key in [KEYS.Key_Backspace, KEYS.Key_Delete]
        isEscape = key in [KEYS.Key_Escape, KEYS.Key_C]
        isOperator = key in [KEYS.Key_Plus, KEYS.Key_Minus, KEYS.Key_Slash, KEYS.Key_Asterisk, KEYS.Key_P]
        
        if isEnter:
            self.eqPressed.emit()
            return event.ignore()
        if isDelete:
            self.delPressed.emit()
            return event.ignore()
        if isEscape:
            self.escPressed.emit()
            return event.ignore()
        if isOperator:
            if text.upper() == "P":
                self.opPressed.emit("^")
            else:
                self.opPressed.emit(text)
            return event.ignore()
        
        if isEmpty(text):
            return event.ignore()
        
        if isNumOrDot(text):
            self.inputPressed.emit(text)
            return event.ignore()