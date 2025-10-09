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

<img width="883" height="624" alt="image" src="https://github.com/user-attachments/assets/c7e0ba4b-0510-43d2-bbf3-d04e35175d9b" />
<img width="902" height="625" alt="image" src="https://github.com/user-attachments/assets/0542c04d-b30a-4257-9985-bff2ae47cb55" />

<img width="909" height="640" alt="image" src="https://github.com/user-attachments/assets/e134ba1e-8da8-445c-a479-525e1872b6fc" />
<img width="506" height="697" alt="image" src="https://github.com/user-attachments/assets/ffe1ae6f-4511-4e53-937d-e45a3f973c7a" />

<img width="205" height="146" alt="image" src="https://github.com/user-attachments/assets/66ac2f04-68d8-4e72-9720-b8e012a297b8" />
<img width="891" height="633" alt="image" src="https://github.com/user-attachments/assets/57afacc4-9fd6-444f-9022-e124d5d9a207" />







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

