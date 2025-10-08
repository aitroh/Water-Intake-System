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


First, Install the requirements.

```bash
pip install -r requirements.txt
```

If you hadn't downloaded `requirements.txt`, install these

```bash
pip install PyQt6 matplotlib plyer
```
To run the application, simply type this in your terminal:

```bash
python main.py
```

