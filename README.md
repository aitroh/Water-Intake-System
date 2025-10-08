# Water Intake System

A simple desktop application to log and manage daily water intake, built with Python and PyQt6.

---

## Project Overview

This Water Intake System lets users record how much water they drink, view their intake history, and manage logged entries using a lightweight GUI. It is implemented in Python with PyQt6 for the interface and a local SQLite (or similar) database for storage.

## Features

* Log water intake (add amount in ml).
* View intake report
* delete existing entries.
* Simple, clean GUI interface styled via `styles.py`.

## Code Structure

* `main.py` — application entry point (starts the GUI).
* `GUI.py` — main window and widget logic (buttons, forms, interactions).
* `database.py` — handles storage, retrieval, and database operations.
* `styles.py` — CSS-like styling for the PyQt6 widgets.

## Screenshots

*(Add images to the `screenshots/` folder and update this section with GitHub image links.)*

## How to run the program

1. Install Python 3.8+ (recommended).
2. (Optional) Create and activate a virtual environment:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

3. Install the required packages. If you have a `requirements.txt`, run:

```bash
pip install -r requirements.txt
```

If there is no `requirements.txt`, install at least PyQt6:

```bash
pip install PyQt6
```

4. Run the application from the project root:

```bash
python main.py
# or, if your entry is inside an `app/` folder:
python app/main.py
```

## Notes / Troubleshooting

* If the GUI fails to launch, ensure PyQt6 is installed and that you're running the correct Python interpreter.
* If you see database errors, check `database.py` to confirm the database file path and permissions.
* You can modify `styles.py` to change the look and feel of the app.

## License

This project currently has no license specified. If you'd like to add one, consider using the MIT License by adding a `LICENSE` file.

## Credits / About

Based on a simple water tracking concept — created by the repository owner. Feel free to fork and improve.

---

*This README was written to match the style of the `My-Daily-Journal` example (structure and sections inspired by that README).*
