import sys
import pymysql.cursors
from image_generator import ImageGenerator
from settings import GetDB, DBInfo
import time

from PyQt6.QtCore import QSize, Qt, QTimer
from PyQt6.QtWidgets import QMessageBox, QDialog, QProgressBar, QComboBox, QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QGridLayout, QHBoxLayout, QLabel
from PyQt6.QtGui import QPixmap, QPalette, QColor

from datetime import datetime, timedelta

class FirstWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.conn = GetDB().conn
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        self.setupUI()
        self.second_window = SecondWindow()

    def setupUI(self):
        self.setGeometry(800, 200, 300, 300)
        self.setWindowTitle("BeYourself")
        self.setFixedSize(QSize(400, 600))

        # Title (QLabel)
        label = QLabel("BeYourself")
        font = label.font()
        font.setPointSize(30)
        label.setFont(font)
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        # Generated Picture (QLabel)
        picture = QLabel()
        picture.setPixmap(QPixmap(f'image/{ig.random_generate()}'))
        picture.setScaledContents(True)

        # Feeling Today (QLabel + QCombobox)
        label1 = QLabel("feeling..")
        font1 = label1.font()
        font1.setPointSize(11)
        label1.setFont(font1)
        label1.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        self.box_feeling = QComboBox()
        self.box_feeling.addItems(["Terrific!", "Good!", "Bad..", "Depressed.."])
        self.box_feeling.activated.connect(self.check_index)

        layout_2 = QHBoxLayout()
        layout_2.addWidget(label1, 2)
        layout_2.addWidget(self.box_feeling, 8)

        # Wakeup TIme (QLabel + QCombobox)
        label2 = QLabel("woke up..")
        label2.setFont(font1)
        label2.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        self.box_wakeup = QComboBox()
        self.box_wakeup.addItems(["06:00", "06:30", "07:00", "07:30", "08:00", "08:30~"])
        self.box_wakeup.activated.connect(self.check_index)

        layout_3 = QHBoxLayout()
        layout_3.addWidget(label2, 2)
        layout_3.addWidget(self.box_wakeup, 8)

        # Today's Goal (QLabel + QCombobox)
        label3 = QLabel("today I'll..")
        label3.setFont(font1)
        label3.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        layout_4 = QHBoxLayout()
        layout_4.addWidget(label3, 2)
        layout_4.addWidget(self.box_goal, 8)

        self.box_goal = QComboBox()
        self.box_goal.addItems(["study 6 hours", "study 8 hours", "study 10 hours", "study 12 hours"])
        self.box_wakeup.activated.connect(self.check_index)


        # Button to Second Page (QPushButton)
        button_start = QPushButton("Let's Go!")
        button_start.clicked.connect(self.make_query_sub)
        button_start.clicked.connect(self.show_second_window)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(label, 1)
        layout.addWidget(picture, 4)
        layout.addLayout(layout_2, 1)
        layout.addLayout(layout_3, 1)
        layout.addLayout(layout_4, 1)
        layout.addWidget(button_start, 1)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def show_second_window(self):
        self.hide()
        self.second_window.show()

    def check_index(self):
        index_feeling = self.box_feeling.currentIndex()
        index_wakeup = self.box_wakeup.currentIndex()
        index_goal = self.box_goal.currentIndex()
        return (index_feeling, index_wakeup, index_goal)

    def make_query_sub(self):
        indices = self.check_index()
        today = datetime.now().date()
        today_year = int(str(today)[:4])
        today_month = int(str(today)[5:7])
        today_day = int(str(today)[9:11])

        feeling = indices[0]+1
        wakeup_time = datetime(today_year, today_month, today_day, 6, 00) + timedelta(minutes = 30 * (indices[1]))
        goal_time = 2*indices[2]+6

        SQL = f'''
            INSERT INTO sub (date_, feeling, wakeup_time, goal_time)
            VALUES (%s, %s, %s, %s);
        '''

        self.cursor.execute(SQL, [today, feeling, wakeup_time, goal_time])
        self.conn.commit()
        row = self.cursor.fetchone()


class SecondWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUI()
        self.conn = GetDB().conn
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)

    def get_goal_time(self):
        today = datetime.now().date()
        SQL = "SELECT goal_time FROM sub WHERE date_ = %s;"
        self.cursor.execute(SQL, [today])
        self.conn.commit()
        row = self.cursor.fetchone()
        return int(row['goal_time'])

    def setupUI(self):
        self.setGeometry(800, 200, 300, 300)
        self.setWindowTitle("BeYourself")
        self.setFixedSize(QSize(400, 600))

        label = QLabel("BeYourself")
        font = label.font()
        font.setPointSize(30)
        label.setFont(font)
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        progress = QLabel("progress!")
        font1 = progress.font()
        font1.setPointSize(30)
        progress.setFont(font1)

        # 1. ProgressBar

        self.progress_bar = QProgressBar(self)
        self.timer = QTimer()
        self.timer.timeout.connect(self.time_count)
        self.step = 0


        # 2. Dropbox
        box = QComboBox()
        box.addItems(["Computer Science", "Problem Solving", "Book/Tech Blog", "Project"])

        # 3-1. Button
        button_start = QPushButton("Start")
        button_start.clicked.connect(self.start_progress)

        # 3-2. Button
        button_stop = QPushButton("End")
        button_stop.clicked.connect(self.stop_progress)


        layout_1 = QHBoxLayout()
        layout_1.addWidget(button_start)
        layout_1.addWidget(button_stop)

        # 4. Button
        button_stats = QPushButton("Statistics")

        # 5. Button
        button_final = QPushButton("This is for today!")
        button_final.clicked.connect(self.button_final_clicked)

        layout = QVBoxLayout()
        layout.addWidget(label)
        # layout.addWidget(self.progress_bar, 4)
        layout.addWidget(box)
        layout.addLayout(layout_1)
        layout.addWidget(button_stats)
        layout.addWidget(button_final)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def time_count(self):
        self.step = self.step + 1
        time.sleep(1)
        self.progress_bar.setValue(self.step)

    def start_progress(self):
        if self.timer.isActive():
            dig = QMessageBox(self)
            dig.setWindowTitle("ERROR!")
            dig.setText("You Pushed the Wrong Button.")
            dig.exec()
            return

        self.timer.start()
        now = datetime.now()
        today = now.date()
        print(today)
        SQL5 = f"SELECT * FROM main WHERE date_ = %s ORDER BY start_time DESC LIMIT 1;"
        self.cursor.execute(SQL5, [today])
        self.conn.commit()
        row = self.cursor.fetchone()

        if not row:
            pass

        else:
            print('x')
            SQL0 = '''
                SELECT start_time
                FROM main
                WHERE end_time IS NULL AND study_or_rest = 0
                ORDER BY start_time DESC
                LIMIT 1;
            '''
            self.cursor.execute(SQL0)
            self.conn.commit()
            row = self.cursor.fetchone()

            past = row['start_time']
            diff = (now - past).seconds

            SQL1 = f'''
                    UPDATE main
                    SET end_time = %s, net_time = %s
                    WHERE end_time IS NULL AND study_or_rest = 0;
            '''

            self.cursor.execute(SQL1, [now, diff])
            self.conn.commit()
            rew = self.cursor.fetchone()

        SQL3 = f'''
            INSERT INTO main (date_, study_or_rest, start_time, end_time, net_time)
            VALUES (%s, %s, %s, %s, %s);
        '''

        self.cursor.execute(SQL3, [today, 1, now, None, None ])
        self.conn.commit()
        row = self.cursor.fetchone()

    def stop_progress(self):
        if not self.timer.isActive():
            dig = QMessageBox(self)
            dig.setWindowTitle("ERROR!")
            dig.setText("You Pushed the Wrong Button.")
            dig.exec()
            return

        self.timer.stop()

        now = datetime.now()
        today = now.date()
        SQL0 = '''
            SELECT start_time
            FROM main
            WHERE end_time IS NULL AND study_or_rest = 1
        '''
        self.cursor.execute(SQL0)
        self.conn.commit()
        row = self.cursor.fetchone()

        past = row['start_time']
        diff = (now-past).seconds

        SQL1 = f'''
                UPDATE main
                SET end_time = %s, net_time = %s
                WHERE end_time IS NULL AND study_or_rest = 1;
        '''

        self.cursor.execute(SQL1, [now, diff])
        self.conn.commit()
        rew = self.cursor.fetchone()


        SQL2 =  '''
            INSERT INTO main (date_, study_or_rest, start_time, end_time, net_time)
            VALUES (%s, %s, %s, %s, %s);
        '''

        self.cursor.execute(SQL2, [today, 0, now, None, None])
        self.conn.commit()
        row = self.cursor.fetchone()



    def button_final_clicked(self, clicked):
        if self.timer.isActive():
            dig = QMessageBox(self)
            dig.setWindowTitle("WAIT!")
            dig.setText("WAIT! Timer is on. You should press end button before you leave.")
            dig.exec()
        else:
            now = datetime.now()
            today = now.date()
            print(today)
            SQL5 = f"SELECT * FROM main WHERE date_ = %s ORDER BY start_time DESC LIMIT 1;"
            self.cursor.execute(SQL5, [today])
            self.conn.commit()
            row = self.cursor.fetchone()

            if not row:
                pass

            else:

                SQL = '''
                    DELETE FROM main
                    WHERE study_or_rest = 0
                    ORDER By start_time DESC
                    LIMIT 1;
                
                '''

                self.cursor.execute(SQL)
                self.conn.commit()
                row = self.cursor.fetchone()


            dig = QMessageBox(self)
            dig.setWindowTitle("BYE!")
            dig.setText("SEE YOU TOMORROW!")
            dig.exec()
            self.close()


if __name__ == "__main__":
    ig = ImageGenerator()
    app = QApplication(sys.argv)
    window = FirstWindow()
    window.show()
    app.exec()
