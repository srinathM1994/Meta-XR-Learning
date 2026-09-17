from pathlib import Path
import tkinter as tk
from tkinter import messagebox, filedialog
import os
import sys

from analyze_demo_5 import (
    generate_preview,
    read_artist_decisions,
    execute_renaming
)


def run_analysis():
    try:
        folders = get_target_folders()

        total_folders = 0

        for folder in folders:
            generate_preview(folder)
            total_folders += 1

        result_label.config(
            text=f"Analysis completed.\n"
                 f"{total_folders} folder(s) processed.\n"
                 f"Check Status before renaming."
        )

    except Exception as error:

        result_label.config(
            text="Analysis failed."
        )

        messagebox.showerror(
            "Analysis Error",
            str(error)
        )


def open_status():

    try:

        folders = get_target_folders()

        if not folders:
            messagebox.showwarning(
                "No Folder",
                "No folders found."
            )
            return

        for folder in folders:

            report_file = folder / "report.csv"

            if report_file.exists():

                os.startfile(report_file)

        result_label.config(
            text="Report opened.\n"
                 "Edit the Status column and save the CSV."
        )

    except Exception as error:

        messagebox.showerror(
            "Status Error",
            str(error)
        )

def rename_files():
    try:
        folders = get_target_folders()

        total_folders = 0
        total_renamed = 0
        total_skipped = 0
        total_conflicts = 0

        for folder in folders:

            report_file = folder / "report.csv"

            if not report_file.exists():
                continue

            decisions = read_artist_decisions(report_file)

            stats = execute_renaming(folder, decisions)

            total_folders += 1
            total_renamed += stats["renamed"]
            total_skipped += stats["skipped"]
            total_conflicts += stats["conflicts"]

        result_label.config(
            text=(
                f"Rename completed.\n\n"
                f"Folders processed: {total_folders}\n"
                f"Files renamed: {total_renamed}\n"
                f"Files skipped: {total_skipped}\n"
                f"Conflicts: {total_conflicts}"
            )
        )

    except Exception as error:
        result_label.config(text="Rename failed.")
        messagebox.showerror("Rename Error", str(error))

def select_folder():
    folder = filedialog.askdirectory()

    if folder:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, folder)

def get_target_folders():
    path_text = path_entry.get().strip()

    if not path_text:

        if getattr(sys, "frozen", False):
            app_folder = Path(sys.executable).parent
        else:
            app_folder = Path(__file__).parent

        return [app_folder]

    if path_text.endswith("*\\"):
        base_path = Path(path_text[:-2])

        if not base_path.exists():
            raise FileNotFoundError(
                f"Path does not exist:\n{base_path}"
            )

        if not base_path.is_dir():
            raise NotADirectoryError(
                f"Path is not a folder:\n{base_path}"
            )

        return [
            base_path,
            *[
                folder
                for folder in base_path.rglob("*")
                if folder.is_dir()
            ]
        ]

    folder = Path(path_text)

    if not folder.exists():
        raise FileNotFoundError(
            f"Path does not exist:\n{folder}"
        )

    if not folder.is_dir():
        raise NotADirectoryError(
            f"Path is not a folder:\n{folder}"
        )

    return [folder]

# --------------------------------------------------
# GUI
# --------------------------------------------------

window = tk.Tk()

window.title("Asset_Renamer")
window.geometry("600x830")
window.configure(bg="#333333")

###########
path_label = tk.Label(
    window,
    text="Path",
    font=("Arial", 16, "bold"),
    bg="#333333",
    fg="white"
)

path_label.pack(pady=(20, 5))


path_frame = tk.Frame(
    window,
    bg="#333333"
)

path_frame.pack(pady=5)


path_entry = tk.Entry(
    path_frame,
    font=("Arial", 12),
    width=35
)

path_entry.pack(side="left", padx=5)


browse_button = tk.Button(
    path_frame,
    text="Browse",
    font=("Arial", 11),
    command=lambda: select_folder()
)

browse_button.pack(side="left")
########
title_label = tk.Label(
    window,
    text="Asset_Renamer",
    font=("Arial", 28, "bold"),
    bg="#333333",
    fg="white"
)

title_label.pack(pady=30)

#########
########

run_button = tk.Button(
    window,
    text="Run",
    font=("Arial", 22, "bold"),
    width=15,
    height=2,
    command=run_analysis
)

run_button.pack(pady=20)


status_button = tk.Button(
    window,
    text="Status",
    font=("Arial", 22, "bold"),
    width=15,
    height=2,
    command=open_status
)

status_button.pack(pady=20)


rename_button = tk.Button(
    window,
    text="Rename",
    font=("Arial", 22, "bold"),
    width=15,
    height=2,
    command=rename_files
)

rename_button.pack(pady=20)


result_title = tk.Label(
    window,
    text="Result",
    font=("Arial", 18, "bold"),
    bg="#333333",
    fg="white"
)

result_title.pack(pady=(60, 5))


result_label = tk.Label(
    window,
    text="Ready",
    font=("Arial", 14),
    width=45,
    height=4,
    bg="#222222",
    fg="white",
    wraplength=450
)

result_label.pack(pady=5)

window.mainloop()

