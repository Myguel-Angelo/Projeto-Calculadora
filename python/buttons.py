from typing import TYPE_CHECKING

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QGridLayout, QWidget
from PySide6.QtWidgets import QPushButton

from utils import MEDIUM_SIZE
from utils import isNumOrDot, isEmpty, isEqualORC, isValidNumber, convertToNumber

if TYPE_CHECKING:
    from display import Display
    from display import MiniDisplay
    from window import MainWindow

class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure()
    
    def configure(self, size=MEDIUM_SIZE):
        font = self.font()
        font.setPixelSize(size)
        self.setFont(font)
        self.setMinimumSize(50, 50)

class ButtonsGrid(QGridLayout):
    def __init__(self, display: "Display", info: "MiniDisplay", window: "MainWindow", *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._gridMask = [
            ["C", "⌫", "^", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["N", "0", ".", "="],
        ]
        self.display = display
        self.info = info
        self.window = window
        self.display = display
        
        self._leftNumber = None
        self._rightNumber = None
        self._operator = None
        self._equation = ""
        
        self._connectSignals()
        self._fabricButtons()
        
        self._operations = {
            "+": lambda: self._leftNumber+self._rightNumber,
            "-": lambda: self._leftNumber-self._rightNumber,
            "*": lambda: self._leftNumber*self._rightNumber,
            "/": lambda: self._leftNumber/self._rightNumber
        }
        
    @property
    def equation(self):
        return self._equation
    
    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)
    
    def _connectSignals(self):
        self.display.eqPressed.connect(self._equalClicked)
        self.display.delPressed.connect(self.display.backspace)
        self.display.escPressed.connect(self._clear)
        self.display.inputPressed.connect(self._insertText)
        self.display.opPressed.connect(self._selectOperator)
    
    def _fabricButtons(self):
        for row, item in enumerate(self._gridMask):
            for column, buttonText in enumerate(item):
                button = Button(buttonText)
                if not isNumOrDot(buttonText) and not isEmpty(buttonText):
                    self._configCssAndSlot(button, buttonText)
                    
                self.addWidget(button, row, column)
                numberButtonSlot = self._makeSlot(self._insertText, buttonText)
                self._connectButton(button, numberButtonSlot)
    
    def _connectButton(self, button: Button, slot):
        button.clicked.connect(slot)
    
    def _configCssAndSlot(self, button: Button, buttonText: str):
        if isEqualORC(buttonText):
            button.setProperty("cssClassSpecial", "specialButton")
        else:
            button.setProperty("cssClassOprations", "oprationButton")
        
        if buttonText == "C":
            self._connectButton(button, self._clear)
        if buttonText == "⌫":
            button.configure(18)
            self._connectButton(button, self.display.backspace)
        if buttonText in "+-*/^":
            operatorSlot = self._makeSlot(self._selectOperator, buttonText)
            self._connectButton(button, operatorSlot)
        if buttonText == "=":
            self._connectButton(button, self._equalClicked)
        if buttonText == "N":
            self._connectButton(button, self._invertNumber)
    
    
    def _makeSlot(self, func, *args, **kwargs):
        @Slot(bool)
        def realSlot(_):
            func(*args, **kwargs)
        return realSlot
    
    @Slot()
    def _insertText(self, text):
        futureDisplay = self.display.text() + text
        if isValidNumber(futureDisplay):
            self.display.insert(text)
        
        self.display.setFocus()
        return
    
    @Slot()
    def _clear(self):
        self._leftNumber = None
        self._rightNumber = None
        self._operator = None
        self.equation = ""
        self.display.clear()
        return
    
    @Slot()
    def _selectOperator(self, text: str):
        displayText = self.display.text()
        self.display.clear()
        
        if not isValidNumber(displayText) and self._leftNumber is None:
            self._showInfo("Você não digitou nada!")
            return
        
        if self._leftNumber is None:   
            self._leftNumber = convertToNumber(displayText)
        
        self._operator = text
        self.equation = f"{self._leftNumber} {self._operator}"
    
    @Slot()
    def _equalClicked(self):
        displayText = self.display.text()
        
        if self._operator is None or not isValidNumber(displayText):
            return
        
        self._rightNumber = convertToNumber(displayText)
        self.equation = f"{self._leftNumber} {self._operator} {self._rightNumber}"
        resultFloat = 0.0
        
        try:
            if self._operator == "^":
                resultFloat = self._leftNumber ** self._rightNumber
                self._continue(resultFloat)
                return
            
            resultFloat = self._operations[self._operator]()
            result = convertToNumber(str(resultFloat))
            
        except ZeroDivisionError:
            self.info.setText("Error")
            self._continue(self._leftNumber)
            self._showError("Erro ao dividir por Zero")
        except OverflowError:
            self.info.setText("Error")
            self._continue(self._leftNumber)
            self._showInfo("Essa conta não pode ser realizada\nO resultado é muito extenso")
            
        self._continue(result)
    
    @Slot()
    def _invertNumber(self):
        displayText = self.display.text()
        if not isValidNumber(displayText):
            return
        
        newNumber = -convertToNumber(displayText)
        self.display.setText(str(newNumber))
        
    def _continue(self, value):
        self.display.clear()
        self.info.setText(self.equation + " = " +str(value))
        self._leftNumber = value
        self._rightNumber = None
    
    def _showError(self, text):
        msgBox = self.window.makeMsgBox()
        msgBox.setText(text)
        msgBox.setIcon(msgBox.Icon.Warning)
        msgBox.exec()
    
    def _showInfo(self, text):
        msgBox = self.window.makeMsgBox()
        msgBox.setText(text)
        msgBox.setIcon(msgBox.Icon.Information)
        msgBox.exec()