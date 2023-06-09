from PySide6.QtWidgets import QLineEdit
from constant import BIG_FONT_SIZE, TEXT_MARGIN, MINIMUM_WIDTH
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeyEvent
from utils import isEmpty, isNumOrDot


class Display(QLineEdit):

    eqPressed = Signal()
    delPressed = Signal()
    clearPressed = Signal()
    inputPressed = Signal(str)
    operatorPressed = Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        self.setStyleSheet(f'font-size: {BIG_FONT_SIZE}px')
        self.setMinimumHeight(BIG_FONT_SIZE * 2)
        self.setMinimumWidth(MINIMUM_WIDTH)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setTextMargins(TEXT_MARGIN, TEXT_MARGIN, TEXT_MARGIN, TEXT_MARGIN)

    
        
