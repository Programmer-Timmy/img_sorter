import tkinter as tk
from tkinter import filedialog, messagebox
import datetime
import pathlib
import os
import shutil
from tkinter import ttk


def organize_images(images):
    # Create a mapping from month numbers to month names
    month_names = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
    }

    image_info = []  # Create a list to store image path and creation date

    for x in images:
        path = pathlib.Path(x)

        current_timestamp = path.stat().st_ctime

        c_time = datetime.datetime.fromtimestamp(current_timestamp)
        c_year = c_time.year
        c_month = c_time.month
        c_day = c_time.day

        image_info.append((x, c_year, c_month, c_day))  # Store image path and creation date

    for image_path, year, month, day in image_info:
        # Create subdirectories for each year, month, and day in the same location as the original images
        year_folder = os.path.join(os.path.dirname(image_path), str(year))
        month_name = month_names[month]
        month_folder = os.path.join(year_folder, month_name)
        day_folder = os.path.join(month_folder, str(day))

        os.makedirs(day_folder, exist_ok=True)

        # Move images to their corresponding day folders
        destination_path = os.path.join(day_folder, os.path.basename(image_path))
        shutil.move(image_path, destination_path)


def select_images():
    images = filedialog.askopenfilenames(
        title="Select Images",
        filetypes=(
            ("Img files", ("*.png", "*.jpg", "*.web")),
            ("All Files", "*.*")
        )
    )

    if images:
        organize_images(images)
    else:
        messagebox.showinfo("Info", "No images selected.")


def select_folder():
    folder = filedialog.askdirectory(title="Select a Folder with Images")
    images = [os.path.join(folder, filename) for filename in os.listdir(folder) if
              filename.lower().endswith((".png", ".jpg", ".web"))]
    count = len(images)

    if images:
        result = messagebox.askquestion("Organize images", "Are you sure you want to organize: {} images in {}".format(count, folder), icon='warning')
        if result == 'yes':
            organize_images(images)
        else:
            return
    else:
        messagebox.showinfo("Info", "No images found in the folder.")

root = tk.Tk()
root.title("Main Window")

root.iconbitmap('icon.ico')

label = tk.Label(root, text="Select Images or Select a Folder", font=("Segoe UI", 14))
label.pack()

frame = tk.Frame(root)
frame.pack(expand=True)

style = ttk.Style()
style.configure("TButton", padding=10, font=("Segoe UI", 12), relief="flat", borderwidth=0)

style.map("TButton", foreground=[('pressed', 'black'), ('active', 'black')], background=[('pressed', 'blue'), ('active', 'lightblue')])

button_images = ttk.Button(frame, text="Select Images" , compound=tk.TOP, command=select_images)
button_images.pack(side=tk.LEFT)

button_folder = ttk.Button(frame, text="Select Folder", compound=tk.TOP, command=select_folder)
button_folder.pack(side=tk.LEFT)

root.mainloop()