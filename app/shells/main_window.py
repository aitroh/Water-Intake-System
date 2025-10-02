from PyQt6.QtWidgets import QMainWindow
from app.features.view import WaterDashboard

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Water Intake - Dashboard")
        self.setCentralWidget(WaterDashboard())