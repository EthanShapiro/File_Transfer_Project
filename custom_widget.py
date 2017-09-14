from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QLabel, QApplication
from PyQt5.Qt import Qt, QRegExp, QRegExpValidator, QFont
import sys

class Window(QWidget):

    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        ipledit = ipLineEdit()
        layout.addWidget(ipledit)
        self.setLayout(layout)


class ipLineEdit(QWidget):

    line_edits = []
    spacers = '.'

    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        q_reg = QRegExp("\d{3}")
        for x in range(4):
            line_edit = QLineEdit()
            q_validator = QRegExpValidator(q_reg, line_edit)
            line_edit.setValidator(q_validator)
            line_edit.setFont(QFont(None, 13))
            line_edit.setMaximumWidth(34)
            line_edit.setMinimumWidth(34)

            self.layout.addWidget(line_edit)
            if x < 3:
                self.layout.addWidget(QLabel("."))

            self.line_edits.append(line_edit)
        self.layout.addStretch()
        self.setLayout(self.layout)

    def text(self):
        text = []
        for line_edit in self.line_edits:
            text.append(line_edit.text())
        return '.'.join(text)

app = QApplication([])
window = Window()
window.show()
sys.exit(app.exec())
