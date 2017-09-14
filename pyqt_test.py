from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QApplication, QHBoxLayout
from PyQt5.Qt import QRegExpValidator, QRegExp, QFont, Qt
import sys

class Test(QWidget):

    def __init__(self):
        super().__init__()

        layout = QGridLayout(self)

        # Add host and port labels to layout
        host_label = QLabel("Host:")
        host_label.setFont(QFont(None, 13))
        layout.addWidget(host_label, 0, 0)
        port_label = QLabel("Port:")
        port_label.setFont(QFont(None, 13))
        layout.addWidget(port_label, 0, 1)

        # Add host and port inputs
        ipv4_input = ipLineEdit()
        layout.addWidget(ipv4_input, 1, 0)
        port_input = QLineEdit()
        port_input.setFont(QFont(None, 13))
        layout.addWidget(port_input, 1, 1)

        # Add Connected Label
        connected_label = QLabel("Disconnected")
        connected_label.setFont(QFont(None, 13))
        connected_label.setObjectName('connected_label')
        connected_label.setStyleSheet('QLabel#connected_label {color: red}')
        layout.addWidget(connected_label, 2, 0)

        # Add Connection Details
        conn_details = QLabel("No Connection Details")
        conn_details.setFont(QFont(None, 13))
        layout.addWidget(conn_details, 3, 0)


class ipLineEdit(QWidget):

    line_edits = []
    spacers = '.'

    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        q_reg = QRegExp("\d{3}")
        for x in range(4):
            line_edit = QLineEdit()
            q_validator = QRegExpValidator(q_reg, line_edit)
            line_edit.setValidator(q_validator)
            line_edit.setFont(QFont(None, 13))
            line_edit.setMaximumWidth(35)
            line_edit.setMinimumWidth(35)

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
window = Test()
window.show()
sys.exit(app.exec())