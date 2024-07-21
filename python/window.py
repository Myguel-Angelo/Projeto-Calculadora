from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

class MainWindow(QMainWindow):
    """
    Classe principal da janela do aplicativo.
    Herda de QMainWindow e configura o widget central com um layout de caixa vertical.

    Atributos:
        myCentralWidget (QWidget): O widget central da janela principal.
        boxLayout (QVBoxLayout): O gerenciador de layout para o widget central.
    """

    def __init__(self, parent: QWidget | None = None, *args, **kwargs) -> None:
        """
        Inicializa a instância da MainWindow.
        """
        super().__init__(parent, *args, **kwargs)
        
        # Cria o widget central e define um layout vertical
        self.myCentralWidget = QWidget()
        self.vBoxLayout = QVBoxLayout()
        self.myCentralWidget.setLayout(self.vBoxLayout)
        self.setCentralWidget(self.myCentralWidget)
        
        # Define o título da janela
        self.setWindowTitle("Calculadora")
    
    def adjustFixedSize(self) -> None:
        """
        Ajusta o tamanho da janela e define um tamanho fixo.
        """
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())
    
    def addToWidgetLayout(self, widget: QWidget) -> None:
        """
        Adiciona um widget ao layout do widget central.
        """
        self.vBoxLayout.addWidget(widget)
    
    def makeMsgBox(self) -> QMessageBox:
        """
        Cria uma caixa de mensagem com a janela principal como seu pai.
        """
        return QMessageBox(self)
