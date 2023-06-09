from typing import Optional
from PySide6.QtWidgets import QPushButton, QGridLayout
from constant import MEDIUM_FONT_SIZE
from utils import isEmpty, isNumOrDot, isValidNumber
from display import Display
from PySide6.QtCore import Slot
from typing import TYPE_CHECKING
from math import pow, sqrt


if TYPE_CHECKING:
    from display import Display
    from info import Info
    from main_window import MainWindow


class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(75, 75)


class ButtonsGrid(QGridLayout):
    def __init__(self, display: 'Display', info: 'Info', window: 'MainWindow', *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._gridMask = [
            ['C', '⌫', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['N', '0', '.', '='],
        ]
        self.display = display
        self.info = info
        self.window = window
        self._equation = ''
        self._equationInitialValue = 'Resultado'
        self._left = None
        self._right = None
        self._op = None

        self.equation = self._equationInitialValue
        self._makeGrid()


    @property
    def equation(self):
        return self._equation


    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)


    def _makeGrid(self):

        for i, row in enumerate(self._gridMask):
            for j, buttonText in enumerate(row):
                button = Button(buttonText)

                if not isNumOrDot(buttonText) and not isEmpty(buttonText):
                    button.setProperty('cssClass', 'specialButton')
                    self._configSpecialButton(button)

                self.addWidget(button, i, j)
                slot = self._makeSlot(self._insertToDisplay, buttonText)
                self._connectButtonClicked(button, slot)


    def _connectButtonClicked(self, button, slot):
        button.clicked.connect(slot)


    def _configSpecialButton(self, button):
        text = button.text()

        if text == 'C':
            self._connectButtonClicked(button, self._clear)

        if text in '+-/*^':
            self._connectButtonClicked(
                button, self._makeSlot(self._configLeftOp, text))

        if text == '=':
            self._connectButtonClicked(button, self._eq)

        if text == 'N':
            self._connectButtonClicked(button, self._invertNumber)

        if text == '⌫':
            self._connectButtonClicked(button, self.display.backspace)


    @Slot()
    def _makeSlot(self, func, *args, **kwargs):
        @Slot(bool)
        def realSlot(_):
            func(*args, **kwargs)
        return realSlot


    @Slot()
    def _invertNumber(self):
        displayText = self.display.text()

        if not isValidNumber(displayText):
            return
        
        number = -float(displayText)

        if number.is_integer():
            number = int(number)

        self.display.setText(str(number))

    @Slot()
    def _insertToDisplay(self, text):
        newDisplayValue = self.display.text() + text
        if not isValidNumber(newDisplayValue):
            return
        self.display.insert(text)


    @Slot()
    def _clear(self):
        self._left = None
        self._right = None
        self._op = None
        self.equation = self._equationInitialValue
        self.display.clear()


    @Slot()
    def _configLeftOp(self, text):
        displayText = self.display.text()  # número _left
        self.display.clear()  # limpa display

        if not isValidNumber(displayText) and self._left is None:
            self._showError('Você não digitou nada.')
            return

        if self._left is None:
            self._left = float(displayText)

        self._op = text
        self.equation = f'{self._left} {self._op} ??'


    @Slot()
    def _eq(self):
        displayText = self.display.text()

        if not isValidNumber(displayText):
            self._showError('Você não digitou o outro número da conta.')
            return

        self._right = float(displayText)
        self.equation = f'{self._left} {self._op} {self._right}'
        result = 'Error'

        try:
            if '^' in self.equation and isinstance(self._left, float):
                result = pow(self._left, self._right)
            else:
                result = eval(self.equation)
        except ZeroDivisionError:
            self._showError('Você está dividindo um número por zero.')
        except OverflowError:
            self._showError('Essa conta não pode ser realizada.')

        self.display.clear()
        self.info.setText(f'{self.equation} = {result}')
        self._left = result
        self._right = None

        if result == 'Error':
            self._left = None

    def _showError(self, text):
        msgBox = self.window.makeMsgBox()
        msgBox.setText(text)
        msgBox.setIcon(msgBox.Icon.Critical)
        msgBox.exec()

    def _showInfo(self, text):
        msgBox = self.window.makeMsgBox()
        msgBox.setText(text)
        msgBox.setIcon(msgBox.Icon.Information)
        msgBox.exec()
