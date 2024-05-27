import sys
import subprocess
import signal
import os  # Import the os module
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi


class NetworkChecker(QThread):
    status_changed = pyqtSignal(str)

    def __init__(self, ip):
        super().__init__()
        self.ip = ip

    def run(self):
        while True:
            status = self.check_network_status()
            self.status_changed.emit(status)
            self.msleep(1500)

    def check_network_status(self):
        try:
            result = subprocess.run(['ping', '-c', '1', self.ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
            if result.returncode == 0:
                return "Connected"
            else:
                return "Disconnected"
        except Exception as e:
            print("Error:", e)
            return "Disconnected"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("mainwindow.ui", self)
        self.setWindowTitle("Robot Controller")

        self.robot_on = False
        self.update_button_state()

        self.onButton.clicked.connect(self.toggle_robot)

        self.robot_ip = "192.168.196.233"

        self.network_checker = NetworkChecker(self.robot_ip)
        self.network_checker.status_changed.connect(self.update_status_label)
        self.network_checker.start()

        self.terminal_process_pid = None 
        self.terminal_process = None

    def update_button_state(self):
        if self.robot_on:
            self.onButton.setText("On")
            self.onButton.setStyleSheet("background-color: green")
        else:
            self.onButton.setText("Off")
            self.onButton.setStyleSheet("background-color: red")

    def toggle_robot(self):
        if self.Status.text() == "Status: Connected":
            self.robot_on = not self.robot_on
            self.update_button_state()

            if self.robot_on:
                print("Robot started")
                self.start_ros2_node()
            else:
                print("Robot stopped")
                self.stop_ros2_node()
        else:
            print("Cannot turn on robot. Communication is disconnected.")

    def update_status_label(self, status):
        self.Status.setText(f"Status: {status}")
        if status == "Connected":
            self.Status.setStyleSheet("color: green")
        else:
            self.Status.setStyleSheet("color: orange")
            if self.robot_on:
                self.robot_on = False
                self.update_button_state()
                print("Communication lost. Robot turned off.")
                self.stop_ros2_node()

    def start_ros2_node(self):
        bash_file = "robot_run.bash"

        self.terminal_process = subprocess.Popen(["gnome-terminal", "--", "bash", "-c", f"./{bash_file}; exec bash"])

        
    def stop_ros2_node(self):
        with open("terminal_pid.txt", "r") as f:
            terminal_pid = int(f.read())

        os.killpg(os.getpgid(terminal_pid), signal.SIGKILL)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())