# styles.py
"""
Central Qt stylesheet. Slightly prettier UI.
"""

class Styles:
    @staticmethod
    def main_style() -> str:
        return """
        QWidget {
            font-family: "Segoe UI", Roboto, Arial;
            font-size: 13px;
            background: #f5f7fa;
        }
        QLabel#title {
            font-size: 20px;
            font-weight: 700;
            margin: 8px 0;
        }
        QFrame#card {
            background: #ffffff;
            border-radius: 10px;
            padding: 10px;
            border: 1px solid #e0e6ef;
        }
        QLabel {
            color: #222;
        }
        QLineEdit, QSpinBox, QTextEdit {
            font-size: 13px;
            padding: 6px;
            border: 1px solid #d6dfe9;
            border-radius: 6px;
            background: #fbfdff;
        }
        QPushButton {
            padding: 6px 10px;
            border-radius: 8px;
            border: 1px solid #c9d6ee;
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                       stop:0 #f8fbff, stop:1 #eef6ff);
        }
        QPushButton#primary {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                       stop:0 #5fc3ff, stop:1 #3b8fe6);
            color: white;
            font-weight: 600;
            border: none;
        }
        QListWidget {
            background: #fbfdff;
            border: 1px solid #e6eefb;
            border-radius: 6px;
        }
        QMenu {
            background: #ffffff;
            border: 1px solid #dfe8f8;
        }
        """
