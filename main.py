import sys
from PySide6.QtWidgets import QApplication, QLabel
from main_window import MainWindow
from constant import WINDOWS_ICON_PATH
from PySide6.QtGui import QIcon


if __name__ == '__main__':
    # Criando aplicação
    app = QApplication(sys.argv)
    window = MainWindow()

    label1 = QLabel('Teste')
    label1.setStyleSheet('font-size: 50px;')
    window.addWidgetToVLayout(label1)

    # Definindo o ícone
    icon = QIcon(str(WINDOWS_ICON_PATH))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)

    # Execução
    window.adjustFixedSize()
    window.show()
    app.exec()