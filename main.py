import sys
from PySide6.QtWidgets import QApplication
from main_window import MainWindow
from constant import WINDOWS_ICON_PATH
from PySide6.QtGui import QIcon
from display import Display
from info import Info
from styles import setupTheme


if __name__ == '__main__':

    # Criando aplicação
    app = QApplication(sys.argv)
    setupTheme()
    window = MainWindow()

    # Definindo o ícone
    icon = QIcon(str(WINDOWS_ICON_PATH))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)

    # Info
    info = Info('2.0 ^ 10.0 = 1024')
    window.addToVLayout(info)

    # Display
    display = Display()
    window.addToVLayout(display)

    # Execução
    window.adjustFixedSize()
    window.show()
    app.exec()
