import sys
from PyQt5.QtCore import QSize, Qt, QTime
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QCheckBox, QTimeEdit, QTextEdit
from PyQt5.QtGui import QFont


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        widget = QWidget()
        self.setWindowTitle("BeYourself")
        self.setFixedSize(QSize(500, 800))
        self.setCentralWidget(widget)

        layout = QGridLayout()

        # Title
        label1 = QLabel("BeYourself", self)
        label1.setFont(QFont('Sans-Serif', 30))
        label1.setAlignment(Qt.AlignCenter)
        layout.addWidget(label1, 0, 0, 2, 3)


        label2 = QLabel("I woke up at..", self)
        label2.setAlignment(Qt.AlignCenter)
        layout.addWidget(label2, 2, 0)

        label3 = QLabel("Feeling Good?", self)
        label3.setAlignment(Qt.AlignCenter)



        timeedit = QTimeEdit(self)
        timeedit.setTime(QTime.currentTime())
        timeedit.setTimeRange(QTime(3, 00, 00), QTime(23, 30, 00))
        timeedit.setDisplayFormat('hh:mm:ss')

        checkbox1 = QCheckBox('now!', self)
        checkbox2 = QCheckBox('Refreshed!', self)
        checkbox3 = QCheckBox('Tired.....', self)

        button = QPushButton('GOGO', self)
        button.clicked.connect(self.ButtonToBranch)




        layout.addWidget(checkbox1, 2, 1)
        layout.addWidget(timeedit, 2, 2)

        layout.addWidget(label3, 3, 0)
        layout.addWidget(checkbox2, 3, 1)
        layout.addWidget(checkbox3, 3, 2)

        layout.addWidget(button, 4, 0, 1, 3)
        widget.setLayout(layout)

    def ButtonToBranch(self):
        self.close()
        self.show_window = BranchWindow()
        self.show_window.show()


class BranchWindow(QMainWindow):
    def __init__(self):
        super(BranchWindow, self).__init__()
        self.initUI()

    def initUI(self):
        widget = QWidget()
        self.setWindowTitle("BeYourself")
        self.setFixedSize(QSize(500, 800))
        self.setCentralWidget(widget)

        layout = QGridLayout()

        study = 10
        rest = 2

        label1 = QLabel("Yesterday's Me", self)
        label2 = QLabel("Today's Me", self)
        label3 = QLabel(f"Stidied {study} hours")
        label4 = QLabel(f"Rested {rest} hours")
        label5 = QLabel("NULL")

        label1.setFont(QFont('Sans-Serif', 20))
        label2.setFont(QFont('Sans-Serif', 20))
        label1.setAlignment(Qt.AlignCenter)
        label2.setAlignment(Qt.AlignCenter)
        label3.setAlignment(Qt.AlignCenter)
        label4.setAlignment(Qt.AlignCenter)
        label5.setAlignment(Qt.AlignCenter)

        button = QPushButton('GoGo', self)

        textedit = QTextEdit(self)
        textedit.resize(1, 1)
        textedit.setAcceptRichText(False)

        layout.addWidget(label1, 0, 0, 1, 2)
        layout.addWidget(label5, 1, 0, 2, 1)
        layout.addWidget(label3, 1, 1)
        layout.addWidget(label4, 2, 1)

        layout.addWidget(label2, 3, 0, 1, 2)
        layout.addWidget(textedit, 4, 0, 1, 2)
        layout.addWidget(button, 5, 0, 1, 2)

        widget.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

