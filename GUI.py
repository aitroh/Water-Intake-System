# GUI.py
"""
Updated GUI: same layout as before but adds:
- Percentage inside donut chart
- Thin QProgressBar below "Today: X / X ml"
- Auto updates when user logs intake
"""

from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox,
    QListWidget, QListWidgetItem, QSpinBox, QFrame, QMenu, QFileDialog,
    QProgressBar
)
from PyQt6.QtCore import Qt, QTimer
from database import Database
from styles import Styles
from datetime import date, datetime

import matplotlib
matplotlib.use("QtAgg")
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


# ---------- Donut chart with % inside ----------
class DonutCanvas(FigureCanvas):
    def __init__(self, parent=None, size=(3.0, 3.0), dpi=100):
        fig = Figure(figsize=size, dpi=dpi, tight_layout=True)
        super().__init__(fig)
        self.axes = fig.add_subplot(111)

    def plot_donut_percent(self, percent: float):
        self.axes.clear()
        pct = max(0.0, min(100.0, percent))
        remaining_pct = 100.0 - pct
        wedges = [pct, remaining_pct] if pct > 0 else [0.0001, 100.0]
        colors = ["#4fc3f7", "#2a2d33"]
        self.axes.pie(
            wedges,
            colors=colors,
            startangle=90,
            wedgeprops=dict(width=0.28, edgecolor='w')
        )
        # Draw % text in center
        self.axes.text(0, 0, f"{int(round(pct))}%", ha='center', va='center',
                       fontsize=22, color='white', weight='bold')
        self.axes.set_aspect('equal')
        self.axes.axis('off')
        self.draw()


# ---------- Report window ----------
from PyQt6.QtWidgets import QDialog
class ReportWindow(QDialog):
    def __init__(self, db: Database, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Intake Report")
        self.setMinimumSize(520, 500)
        self._build_ui()
        self.setStyleSheet("""
            QWidget { background: #1e1f23; color: #e6eef6; font-family: 'Segoe UI'; }
            QFrame#card { background: #2a2b2f; border-radius: 10px; padding: 12px; }
        """)

    def _build_ui(self):
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
        layout = QVBoxLayout()
        donut_card = QFrame()
        donut_card.setObjectName("card")
        v = QVBoxLayout()
        self.donut = DonutCanvas(self, size=(3.2, 3.2))
        v.addWidget(self.donut)
        self.rem_label = QLabel()
        self.target_label = QLabel()
        hl = QHBoxLayout()
        hl.addStretch(); hl.addWidget(self.rem_label); hl.addSpacing(20)
        hl.addWidget(self.target_label); hl.addStretch()
        v.addLayout(hl)
        donut_card.setLayout(v)
        layout.addWidget(donut_card)
        self.setLayout(layout)

    def refresh(self):
        target = self.db.get_daily_target_ml()
        today = date.today().isoformat()
        consumed = self.db.get_intake_for_date(today)
        remaining = max(0, target - consumed)
        pct = int(consumed / target * 100) if target > 0 else 0
        self.donut.plot_donut_percent(pct)
        self.rem_label.setText(f"Remaining\n{remaining} ml")
        self.target_label.setText(f"Target\n{target} ml")


# ---------- Main window ----------
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.setWindowTitle("Water Intake Tracker")
        self.setMinimumSize(900, 600)
        self._apply_dark_style()
        self._build_ui()
        self.refresh_ui()
        self.report_window = None

        # Refresh every 30 seconds
        self._refresh_timer = QTimer(self)
        self._refresh_timer.timeout.connect(self.refresh_ui)
        self._refresh_timer.start(30_000)

    def _apply_dark_style(self):
        self.setStyleSheet("""
            QWidget {
                background: #121216;
                color: #e6eef6;
                font-family: "Segoe UI", Roboto, Arial;
                font-size: 13px;
            }
            QFrame#card {
                background: #1f2226;
                border-radius: 10px;
                padding: 10px;
                border: 1px solid #2f3439;
            }
            QLabel#title { font-size: 20px; font-weight: 700; color: #ffffff; }
            QPushButton {
                padding: 6px 10px;
                border-radius: 8px;
                border: 1px solid #2f3439;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #1c8dbd, stop:1 #0f617e);
                color: white;
            }
            QPushButton#ghost {
                background: transparent;
                border: 1px solid #3a3f45;
                color: #e6eef6;
            }
            QListWidget {
                background: #151618;
                border: 1px solid #26292d;
                border-radius: 6px;
            }
            QProgressBar {
                border: 1px solid #2f3439;
                border-radius: 5px;
                background: #1a1b1f;
                height: 8px;
            }
            QProgressBar::chunk {
                background-color: #4fc3f7;
                border-radius: 5px;
            }
        """)

    def _build_ui(self):
        layout = QHBoxLayout()

        # Left column
        left_col = QVBoxLayout()
        title = QLabel("Water Intake Tracker"); title.setObjectName("title")
        left_col.addWidget(title)

        # Target
        t_card = QFrame(); t_card.setObjectName("card")
        tlay = QHBoxLayout()
        self.target_spin = QSpinBox(); self.target_spin.setRange(200, 10000)
        self.target_spin.setSingleStep(100); self.target_spin.setSuffix(" ml")
        self.target_btn = QPushButton("Set Target"); self.target_btn.setObjectName("ghost")
        tlay.addWidget(QLabel("Daily Target:")); tlay.addWidget(self.target_spin); tlay.addWidget(self.target_btn)
        t_card.setLayout(tlay)
        left_col.addWidget(t_card)

        # Log intake
        l_card = QFrame(); l_card.setObjectName("card")
        llay = QHBoxLayout()
        self.log_spin = QSpinBox(); self.log_spin.setRange(10, 2000)
        self.log_spin.setSingleStep(50); self.log_spin.setValue(250); self.log_spin.setSuffix(" ml")
        self.log_btn = QPushButton("Log Intake"); self.log_btn.setObjectName("ghost")
        llay.addWidget(QLabel("Amount:")); llay.addWidget(self.log_spin); llay.addWidget(self.log_btn)
        l_card.setLayout(llay)
        left_col.addWidget(l_card)

        # Status + progress
        self.status_label = QLabel("")
        left_col.addWidget(self.status_label)
        self.progress_bar = QProgressBar()
        left_col.addWidget(self.progress_bar)

        # Entries
        e_card = QFrame(); e_card.setObjectName("card")
        ev = QVBoxLayout()
        ev.addWidget(QLabel("Today's entries (right-click):"))
        self.entries = QListWidget()
        self.entries.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.entries.customContextMenuRequested.connect(self._show_entry_menu)
        ev.addWidget(self.entries)
        e_card.setLayout(ev)
        left_col.addWidget(e_card, 1)

        # Right column
        right_col = QVBoxLayout()
        donut_card = QFrame(); donut_card.setObjectName("card")
        dv = QVBoxLayout()
        self.donut = DonutCanvas(self, size=(2.6, 2.6))
        dv.addWidget(self.donut)
        self.rem_label = QLabel(); self.target_label = QLabel()
        hl = QHBoxLayout(); hl.addStretch(); hl.addWidget(self.rem_label)
        hl.addSpacing(20); hl.addWidget(self.target_label); hl.addStretch()
        dv.addLayout(hl)
        donut_card.setLayout(dv)
        right_col.addWidget(donut_card)

        # Buttons
        btn_card = QFrame(); btn_card.setObjectName("card")
        bl = QHBoxLayout()
        self.view_btn = QPushButton("View Report (separate window)")
        self.export_btn = QPushButton("Export CSV")
        bl.addWidget(self.view_btn); bl.addWidget(self.export_btn)
        btn_card.setLayout(bl)
        right_col.addWidget(btn_card)
        right_col.addStretch()

        layout.addLayout(left_col, 2)
        layout.addLayout(right_col, 1)
        self.setLayout(layout)

        # Connect
        self.target_btn.clicked.connect(self.set_target)
        self.log_btn.clicked.connect(self.log_intake)
        self.view_btn.clicked.connect(self.open_report_window)
        self.export_btn.clicked.connect(self.export_csv)

    # ---------- Core actions ----------
    def refresh_ui(self):
        target = self.db.get_daily_target_ml()
        today = date.today().isoformat()
        consumed = self.db.get_intake_for_date(today)
        remaining = max(0, target - consumed)
        pct = int(consumed / target * 100) if target > 0 else 0

        # Update visuals
        self.donut.plot_donut_percent(pct)
        self.status_label.setText(f"Today: {consumed} / {target} ml")
        self.progress_bar.setValue(pct)
        self.rem_label.setText(f"Remaining\n{remaining} ml")
        self.target_label.setText(f"Target\n{target} ml")

        # Entries
        self.entries.clear()
        for e in self.db.get_entries_for_date(today):
            ts = datetime.fromisoformat(e["timestamp"]).strftime("%H:%M:%S")
            item = QListWidgetItem(f"{e['id']} — {ts} — {e['amount_ml']} ml")
            item.setData(Qt.ItemDataRole.UserRole, e["id"])
            self.entries.addItem(item)

    def set_target(self):
        ml = int(self.target_spin.value())
        if ml <= 0:
            QMessageBox.warning(self, "Invalid", "Target must be positive.")
            return
        self.db.set_daily_target_ml(ml)
        QMessageBox.information(self, "Saved", f"Daily target set to {ml} ml")
        self.refresh_ui()

    def log_intake(self):
        amount = self.log_spin.value()
        if amount <= 0:
            QMessageBox.warning(self, "Invalid", "Enter amount > 0")
            return
        self.db.log_intake(amount)
        self.refresh_ui()

    def export_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export CSV", "water_history.csv", "CSV (*.csv)")
        if not path:
            return
        try:
            self.db.export_history_csv(path)
            QMessageBox.information(self, "Exported", f"History exported to:\n{path}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Export failed: {e}")

    # Context menu for entries
    def _show_entry_menu(self, pos):
        item = self.entries.itemAt(pos)
        if not item:
            return
        entry_id = item.data(Qt.ItemDataRole.UserRole)
        menu = QMenu(self)
        del_action = menu.addAction("Delete entry")
        act = menu.exec(self.entries.mapToGlobal(pos))
        if act == del_action:
            self.db.delete_entry(entry_id)
            self.refresh_ui()

    def open_report_window(self):
        if not self.report_window:
            self.report_window = ReportWindow(self.db, parent=self)
        self.report_window.refresh()
        self.report_window.show()
        self.report_window.raise_()
        self.report_window.activateWindow()

    def closeEvent(self, event):
        self.db.close()
        event.accept()
