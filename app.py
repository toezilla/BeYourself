import sys
import pymysql.cursors
from image_generator import ImageGenerator
from settings import GetDB, DBInfo
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
        label_title = QLabel("BeYourself")
        font_title = label_title.font()
        font_title.setPointSize(30)
        label_title.setFont(font_title)
        label_title.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        # Generated Picture (QLabel)
        picture = QLabel()
        picture.setPixmap(QPixmap(f'image/{ig.random_generate()}'))
        picture.setScaledContents(True)

        # Feeling Today (QLabel + QCombobox)
        label_feeling = QLabel("feeling..")
        font_inside = label_feeling.font()
        font_inside.setPointSize(11)
        label_feeling.setFont(font_inside)
        label_feeling.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        self.combobox_feeling = QComboBox()
        self.combobox_feeling.addItems(["Terrific!", "Good!", "Bad..", "Depressed.."])
        self.combobox_feeling.activated.connect(self.check_index)

        layout_feeling = QHBoxLayout()
        layout_feeling.addWidget(label_feeling, 2)
        layout_feeling.addWidget(self.combobox_feeling, 8)

        # Wakeup TIme (QLabel + QCombobox)
        label_wakeup = QLabel("woke up..")
        label_wakeup.setFont(font_inside)
        label_wakeup.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        self.combobox_wakeup = QComboBox()
        self.combobox_wakeup.addItems(["06:00", "06:30", "07:00", "07:30", "08:00", "08:30~"])
        self.combobox_wakeup.activated.connect(self.check_index)

        layout_wakeup = QHBoxLayout()
        layout_wakeup.addWidget(label_wakeup, 2)
        layout_wakeup.addWidget(self.combobox_wakeup, 8)

        # Today's Goal (QLabel + QCombobox)
        label_goal = QLabel("today I'll..")
        label_goal.setFont(font_inside)
        label_goal.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        self.combobox_goal = QComboBox()
        self.combobox_goal.addItems(["study 6 hours", "study 8 hours", "study 10 hours", "study 12 hours"])
        self.combobox_goal.activated.connect(self.check_index)

        layout_goal = QHBoxLayout()
        layout_goal.addWidget(label_goal, 2)
        layout_goal.addWidget(self.combobox_goal, 8)

        # Button to Second Page (QPushButton)
        button_start = QPushButton("Let's Go!")
        button_start.clicked.connect(self.make_query_sub)
        button_start.clicked.connect(self.show_second_window)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(label_title, 1)
        layout.addWidget(picture, 4)
        layout.addLayout(layout_feeling, 1)
        layout.addLayout(layout_wakeup, 1)
        layout.addLayout(layout_goal, 1)
        layout.addWidget(button_start, 1)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def show_second_window(self):
        self.hide()
        self.second_window.show()

    def check_index(self):
        index_feeling = self.combobox_feeling.currentIndex()
        index_wakeup = self.combobox_wakeup.currentIndex()
        index_goal = self.combobox_goal.currentIndex()
        print(index_feeling, index_wakeup, index_goal)
        return (index_feeling, index_wakeup, index_goal)

    def make_query_sub(self):
        today = datetime.now().date()
        check_SQL = f'''
                SELECT *
                FROM sub
                WHERE date_ = {today}
                '''
        self.cursor.execute(check_SQL)
        self.conn.commit()
        row = self.cursor.fetchone()

        if row is not None:
            indices = self.check_index()

            today_year = int(str(today)[:4])
            today_month = int(str(today)[5:7])
            today_day = int(str(today)[8:10])

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
        self.conn = GetDB().conn
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        self.setupUI()

    def get_goal_time(self):
        today = datetime.now().date()
        SQL = "SELECT goal_time FROM sub ORDER BY id LIMIT 1;"
        self.cursor.execute(SQL)
        self.conn.commit()
        row = self.cursor.fetchone()
        return int(row['goal_time'])

    def setupUI(self):
        self.setGeometry(800, 200, 300, 300)
        self.setWindowTitle("BeYourself")
        self.setFixedSize(QSize(400, 600))

        # Title(QLabel)
        label_title = QLabel("BeYourself")
        font_title = label_title.font()
        font_title.setPointSize(30)
        label_title.setFont(font_title)
        label_title.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        # 1. Progress(QLabel)
        label_progress = QLabel("progress!")
        font_inside = label_progress.font()
        font_inside.setPointSize(10)
        label_progress.setFont(font_inside)


        # 2.1 ProgressBar(QProgressBar)
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        # 2.2 Timer(QTimer)
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.time_count)

        # 3. Dropbox
        self.dropbox_subjects = QComboBox()
        self.dropbox_subjects.addItems(["Computer Science", "Problem Solving", "Book/Tech Blog", "Project"])


        # 4-1. Button
        button_start = QPushButton("Start")
        button_start.clicked.connect(self.start_progress)

        # 4-2. Button
        button_stop = QPushButton("End")
        button_stop.clicked.connect(self.stop_progress)

        layout_buttons = QHBoxLayout()
        layout_buttons.addWidget(button_start)
        layout_buttons.addWidget(button_stop)

        # 4. Button
        button_stats = QPushButton("Statistics")

        # 5. Button
        button_final = QPushButton("This is for today!")
        button_final.clicked.connect(self.button_final_clicked)

        layout = QVBoxLayout()
        layout.addWidget(label_title)
        layout.addWidget(self.progress_bar, 4)
        layout.addWidget(self.dropbox_subjects)
        layout.addLayout(layout_buttons)
        layout.addWidget(button_stats)
        layout.addWidget(button_final)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def time_count(self):
        self.step = self.progress_bar.value()
        self.step += 1
        self.progress_bar.setValue(self.step)

    def start_progress(self):
        if self.timer.isActive():
            dig = QMessageBox(self)
            dig.setWindowTitle("ERROR!")
            dig.setText("You Pushed the Wrong Button.")
            dig.exec()
            return

        self.progress_bar.setMaximum(self.get_goal_time() * 3600)
        self.timer.start(1000)
        now = datetime.now()
        today = now.date()
        SQL5 = f"SELECT * FROM main WHERE date_ = %s ORDER BY start_time DESC LIMIT 1;"
        self.cursor.execute(SQL5, [today])
        self.conn.commit()
        row = self.cursor.fetchone()

        if not row:
            pass

        else:
            SQL6 = '''
                    SELECT *
                    FROM main
                    ORDER BY ID
                    LIMIT 1;
                    '''
            self.cursor.execute(SQL5, [today])
            self.conn.commit()
            row1 = self.cursor.fetchone()

            if row1['study_or_rest'] == 0:
                SQL0 = '''
                    SELECT start_time
                    FROM main
                    ORDER BY id DESC
                    LIMIT 1;
                '''
                self.cursor.execute(SQL0)
                self.conn.commit()
                row2 = self.cursor.fetchone()

                past = row2['start_time']
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
            INSERT INTO main (date_, study_or_rest, study_category, start_time, end_time, net_time)
            VALUES (%s, %s, %s, %s, %s, %s);
        '''

        self.index = self.dropbox_subjects.currentIndex()
        self.cursor.execute(SQL3, [today, 1, self.index+1, now, None, None ])
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
        diff = (now-past)

        SQL1 = f'''
                UPDATE main
                SET end_time = %s, net_time = %s
                WHERE end_time IS NULL AND study_or_rest = 1;
                '''

        self.cursor.execute(SQL1, [now, diff])
        self.conn.commit()
        rew = self.cursor.fetchone()


        SQL2 =  '''
            INSERT INTO main (date_, study_or_rest, study_category, start_time, end_time, net_time)
            VALUES (%s, %s, %s, %s, %s,%s);
        '''

        self.cursor.execute(SQL2, [today, 0, 0, now, None, None])
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
