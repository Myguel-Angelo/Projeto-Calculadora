import sys
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from buttons import ButtonsGrid
from display import Display
from display import MiniDisplay
from window import MainWindow
from utils import WINDOW_ICON_PATH, setupTheme

iconPath = str(WINDOW_ICON_PATH)

if __name__ == "__main__":
    application = QApplication(sys.argv)
    setupTheme()
    window = MainWindow()
    
    icon = QIcon(iconPath)
    window.setWindowIcon(icon)
    application.setWindowIcon(icon)
    
    myMiniDisplay = MiniDisplay("")
    window.addToWidgetLayout(myMiniDisplay)
    
    myDisplay = Display()
    window.addToWidgetLayout(myDisplay)
    
    myButtonsGrid = ButtonsGrid(myDisplay, myMiniDisplay, window)
    window.vBoxLayout.addLayout(myButtonsGrid)
    
    window.adjustFixedSize()
    window.show()
    application.exec()
