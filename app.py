import sys
from PyQt5.QtCore import QSize, Qt, QTime
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QCheckBox, QTimeEdit
from PyQt5.QtGui import QFont


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        widget = QWidget()
        self.setWindowTitle("BeYourself")
        self.setFixedSize(QSize(500, 800))
        self.setCentralWidget(widget)

        layout = QGridLayout()

        label1 = QLabel("BeYourself", self)
        label2 = QLabel("I woke up at..", self)
        label3 = QLabel("Feeling Good?", self)

        label1.setAlignment(Qt.AlignCenter)
        label2.setAlignment(Qt.AlignCenter)
        label3.setAlignment(Qt.AlignCenter)

        label1.setFont(QFont('Sans-Serif', 30))

        timeedit = QTimeEdit(self)
        timeedit.setTime(QTime.currentTime())
        timeedit.setTimeRange(QTime(3, 00, 00), QTime(23, 30, 00))
        timeedit.setDisplayFormat('hh:mm:ss')

        checkbox1 = QCheckBox('now!', self)
        checkbox2 = QCheckBox('Refreshed!', self)
        checkbox3 = QCheckBox('Tired.....', self)

        button = QPushButton('GOGO', self)

        layout.addWidget(label1, 0, 0, 2, 3)

        layout.addWidget(label2, 2, 0)
        layout.addWidget(checkbox1, 2, 1)
        layout.addWidget(timeedit, 2, 2)

        layout.addWidget(label3, 3, 0)
        layout.addWidget(checkbox2, 3, 1)
        layout.addWidget(checkbox3, 3, 2)

        layout.addWidget(button, 4, 0, 1, 3)
        widget.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

