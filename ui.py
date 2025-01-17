import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTimer
from app.monitor import get_system_usage
from app.recorder import Recorder

class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("System Monitor")
        self.layout = QVBoxLayout()
        self.recorder = Recorder()
        self.init_ui()

    def init_ui(self):
        self.cpu_label = QLabel("CPU: Loading...")
        self.ram_label = QLabel("RAM: Loading...")
        self.disk_label = QLabel("Disk: Loading...")
        self.start_button = QPushButton("Start Recording")
        self.stop_button = QPushButton("Stop Recording")
        self.stop_button.setVisible(False)

        self.layout.addWidget(self.cpu_label)
        self.layout.addWidget(self.ram_label)
        self.layout.addWidget(self.disk_label)
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.stop_button)

        self.setLayout(self.layout)
        self.start_button.clicked.connect(self.start_recording)
        self.stop_button.clicked.connect(self.stop_recording)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_usage)
        self.timer.start(1000)

    def update_usage(self):
        cpu, ram, disk = get_system_usage()
        self.cpu_label.setText(f"CPU: {cpu}%")
        self.ram_label.setText(f"RAM: {ram}%")
        self.disk_label.setText(f"Disk: {disk}%")
        if self.recorder.is_recording:
            self.recorder.record(cpu, ram, disk)

    def start_recording(self):
        self.recorder.start()
        self.start_button.setVisible(False)
        self.stop_button.setVisible(True)

    def stop_recording(self):
        self.recorder.stop()
        self.start_button.setVisible(True)
        self.stop_button.setVisible(False)

def start_app():
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
