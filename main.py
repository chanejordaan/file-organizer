import json
import os
from pathlib import Path
import shutil
from tkinter import filedialog, messagebox
import customtkinter

CONFIG_DIR = Path.home() / "file_organizer"
CONFIG_FILE = CONFIG_DIR / "rules.json"


# sorting rules (categories)
DEFAULT_RULES = {
    "Audio": [".mp3", ".wav"],
    "Documents": [".pdf", ".docx", ".xlsx"],
    "Images": [".jpg", ".jpeg", ".png"],
    "Installers": [".exe", ".msi"],
    "Zipped": [".zip"],
}


def load_rules():
    try:
        with open(CONFIG_FILE, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {k: list(v) for k, v in DEFAULT_RULES.items()}


def save_rules(rules):
    CONFIG_DIR.mkdir(exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(rules, f, indent=2)


def parse_extensions(text):
    # turns text into extensions into a dictionary
    extensions = []
    for part in text.replace(";", ",").split(","):
        part = part.strip().lower()
        if not part:
            continue
        if not part.startswith("."):
            part = "." + part
        extensions.append(part)
    return extensions 


def organize(folder, rules):
    # initialize variables
    folder = Path(folder)
    moved = 0

    for item in folder.iterdir(): # loop over files
        if not item.is_file(): # exclude folders
            continue

        for category, extensions in rules.items():
            if item.suffix.lower() in extensions:
                target = folder / category
                target.mkdir(exist_ok=True)
                shutil.move(str(item), str(target / item.name))
                moved += 1
                break

    return moved


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("File Organizer")
        self.geometry("560x480")
        self.rows = []

        customtkinter.CTkLabel(
            self, text="Categories and their extensions (comma-separated)"
        ).pack(pady=(15, 5))

        self.list_frame = customtkinter.CTkScrollableFrame(self)
        self.list_frame.pack(fill="both", expand=True, padx=15, pady=5)

        for category, extensions in load_rules().items():
            self.add_row(category, ", ".join(extensions))

        buttons = customtkinter.CTkFrame(self, fg_color="transparent")
        buttons.pack(pady=10)

        customtkinter.CTkButton(
            buttons, text="+ Add category", command=self.add_row
        ).grid(row=0, column=0, padx=5)
        
        customtkinter.CTkButton(
            buttons, text="Save", command=self.save
        ).grid(row=0, column=1, padx=5)
        
        customtkinter.CTkButton(
            buttons, text="Organize a folder", command=self.run
        ).grid(row=0, column=2, padx=5)


    def add_row(self, category="", extensions=""):
        row = customtkinter.CTkFrame(self.list_frame, fg_color="transparent")
        row.pack(fill="x", pady=3)

        name = customtkinter.CTkEntry(row, width=130, placeholder_text="Category")
        name.pack(side="left", padx=(0, 5))

        exts = customtkinter.CTkEntry(row, placeholder_text=".mp3, .wav")
        exts.pack(side="left", fill="x", expand=True, padx=(0, 5))

        if category:
            name.insert(0, category)
        if extensions:
            exts.insert(0, extensions)

        entry = (row, name, exts)
        customtkinter.CTkButton(
            row, text="✕", width=30, fg_color="gray40",
            command=lambda: self.remove_row(entry),
        ).pack(side="left")

        self.rows.append(entry)


    def remove_row(self, entry):
        entry[0].destroy()
        self.rows.remove(entry)


    def collect_rules(self):
        # Read the rows into a dict. Returns None if something is invalid.
        rules = {}
        for _, name, exts in self.rows:
            category = name.get().strip()
            extensions = parse_extensions(exts.get())

            if not category and not extensions:
                continue
            if not category or not extensions:
                messagebox.showerror(
                    "Incomplete row", "Every category needs a name and at least one extension."
                )
                return None
            if any(c in category for c in '\\/:*?"<>|'):
                messagebox.showerror(
                    "Invalid name", f'"{category}" contains characters not allowed in folder names.'
                )
                return None

            rules.setdefault(category, []).extend(extensions)
        return rules


    def save(self):
        rules = self.collect_rules()
        if rules is None:
            return
        save_rules(rules)
        messagebox.showinfo("Saved", "Your categories have been saved.")


    def run(self):
        rules = self.collect_rules()
        if rules is None:
            return
        save_rules(rules)

        folder = filedialog.askdirectory(title="Choose a folder to organize")
        if not folder:
            return
        count = organize(folder, rules)
        messagebox.showinfo("Done", f"Moved {count} files.")


customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("blue")

App().mainloop()
