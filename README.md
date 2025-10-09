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

<img width="895" height="637" alt="image" src="https://github.com/user-attachments/assets/821ffbbc-668a-4619-9649-f2c99995deb2" />
<img width="890" height="631" alt="image" src="https://github.com/user-attachments/assets/53cad833-0d38-476f-9424-ed882547f319" />
<img width="518" height="752" alt="image" src="https://github.com/user-attachments/assets/6e6c9e77-28bd-42a9-9990-0f19e5a2f08a" />


<img width="926" height="628" alt="image" src="https://github.com/user-attachments/assets/a870f524-607b-4ec0-a93c-bb7c6778dd4e" />
<img width="886" height="635" alt="image" src="https://github.com/user-attachments/assets/b4635eef-f3e4-4056-9ac9-49c4fa99549d" />
<img width="903" height="639" alt="image" src="https://github.com/user-attachments/assets/d6d880bd-2b5e-4dcd-9b1d-109e50d54ed8" />
<img width="898" height="654" alt="image" src="https://github.com/user-attachments/assets/cbcc38f1-82c2-4743-a3df-f50dbe392fae" />










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

