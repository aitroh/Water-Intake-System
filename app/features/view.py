from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
from app.features.service import WaterService

class WaterDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.service = WaterService()
        self.daily_goal = 2000  # ml (default goal)
        self.init_ui()
        self.load_data()

    def init_ui(self):
        layout = QVBoxLayout()

        # Total Progress
        self.total_label = QLabel("Total: 0 / 2000 ml")
        layout.addWidget(self.total_label)

        # Quick Add Buttons
        self.add250_btn = QPushButton("+250ml")
        self.add500_btn = QPushButton("+500ml")

        self.add250_btn.clicked.connect(lambda: self.add_water(250))
        self.add500_btn.clicked.connect(lambda: self.add_water(500))

        layout.addWidget(self.add250_btn)
        layout.addWidget(self.add500_btn)

        # Log Table
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Time", "Amount (ml)"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        layout.addWidget(self.table)

        self.setLayout(layout)

    def load_data(self):
        logs = self.service.get_today_logs()
        total = self.service.get_today_total()
        self.total_label.setText(f"Total: {total} / {self.daily_goal} ml")

        self.table.setRowCount(len(logs))
        for row, log in enumerate(logs):
            self.table.setItem(row, 0, QTableWidgetItem(log.timestamp.strftime("%H:%M")))
            self.table.setItem(row, 1, QTableWidgetItem(str(log.amount)))

    def add_water(self, amount):
        self.service.add_water(amount)
        self.load_data()