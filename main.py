import sys
import pygame
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                             QVBoxLayout, QMessageBox)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QIcon
import os


class PomodoroTimer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("icon.png"))

        self.work_duration = 25 * 60
        self.break_duration = 5 * 60
        self.is_work_time = True
        self.remaining_time = self.work_duration

        self.init_ui()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        # Initialize pygame mixer
        pygame.mixer.init()
        self.sound = pygame.mixer.Sound(self.get_resource_path("beep.wav"))

    def init_ui(self):
        self.setWindowTitle("Pomodoro Timer")
        self.setFixedSize(400, 300)
        self.setStyleSheet("background-color: #2c3e50; color: white;")

        self.layout = QVBoxLayout()
        self.layout.setSpacing(20)
        self.layout.setAlignment(Qt.AlignCenter)

        self.timer_label = QLabel(self.format_time(self.remaining_time), self)
        self.timer_label.setStyleSheet("font-size: 64px; font-weight: bold;")
        self.layout.addWidget(self.timer_label)

        self.start_button = QPushButton("Start", self)
        self.start_button.setStyleSheet(self.button_style())
        self.start_button.clicked.connect(self.start_timer)
        self.layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.setStyleSheet(self.button_style())
        self.stop_button.clicked.connect(self.stop_timer)
        self.layout.addWidget(self.stop_button)

        self.reset_button = QPushButton("Reset", self)
        self.reset_button.setStyleSheet(self.button_style())
        self.reset_button.clicked.connect(self.reset_timer)
        self.layout.addWidget(self.reset_button)

        self.setLayout(self.layout)

        self.show()

    def button_style(self):
        return """
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 20px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """

    def start_timer(self):
        if not self.timer.isActive():
            self.remaining_time = self.work_duration if self.is_work_time else self.break_duration
            self.timer_label.setText(self.format_time(self.remaining_time))
            self.timer.start(1000)

    def update_timer(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.timer_label.setText(self.format_time(self.remaining_time))
        else:
            self.timer.stop()
            self.is_work_time = not self.is_work_time
            self.notify_user()
            self.sound.play()
            self.start_timer()

    def stop_timer(self):
        self.timer.stop()

    def reset_timer(self):
        self.timer.stop()
        self.remaining_time = self.work_duration
        self.timer_label.setText(self.format_time(self.remaining_time))

    def notify_user(self):
        message = "Back to work!" if self.is_work_time else "Time for a break!"
        QMessageBox.information(self, "Pomodoro Timer", message)

    def format_time(self, seconds):
        mins, secs = divmod(seconds, 60)
        return f"{mins:02}:{secs:02}"

    def get_resource_path(self, relative_path):
        if hasattr(sys, "_MEIPASS"):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pomodoro = PomodoroTimer()
    sys.exit(app.exec_())
