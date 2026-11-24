# File Organizer

A small desktop app for sorting files into category folders based on their file
extensions. You can edit the categories and extensions in the app.

## Requirements

- Python 3
- The Python `tkinter` GUI module
- The packages listed in `requirements.txt`

## Run

From the project directory, create and activate a virtual environment, then
install the dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

## Use

1. Edit the categories and comma-separated extensions as needed.
2. Select **Save** to save your rules, or **Organize a folder** to choose a
   folder to sort.

Files matching a rule are moved into a subfolder named for that category.
Organizing changes the selected folder, so review your rules and back up
important files first.

The rules are saved in `file_organizer/rules.json` under your home directory.
