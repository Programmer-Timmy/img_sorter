import atexit
import tkinter as tk
from tkinter import filedialog, messagebox
import datetime
import pathlib
import os
import shutil
from tkinter import ttk
import base64


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
            ("Img files", (".png", ".jpg", ".web", "*.raw", "*.jpeg", "*.tiff", "*.tif")),
            ("All Files", "*.*")
        )
    )
    count = len(images)

    if images:
        result = messagebox.askquestion("Organize images",
                                        "Are you sure you want to organize: {} images".format(count),
                                        icon='warning')
        if result == 'yes':
            organize_images(images)
        else:
            return
    else:
        messagebox.showinfo("Info", "No images selected.")


def select_folder():
    folder = filedialog.askdirectory(title="Select a Folder with Images")
    images = [os.path.join(folder, filename) for filename in os.listdir(folder) if
              filename.lower().endswith((".png", ".jpg", ".web", "*.raw", "*.jpeg", "*.tiff", "*.tif"))]
    count = len(images)

    if images:
        result = messagebox.askquestion("Organize images", "Are you sure you want to organize: {} images in {}".format(count, folder), icon='warning')
        if result == 'yes':
            organize_images(images)
        else:
            return
    else:
        messagebox.showinfo("Info", "No images found in the folder.")

icon_base64 = """
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
"""

# Create a temporary icon file from the base64 data
with open("temp_icon.ico", "wb") as icon_file:
    icon_file.write(base64.b64decode(icon_base64))

def delete_temp_icon():
    if os.path.exists("temp_icon.ico"):
        os.remove("temp_icon.ico")

atexit.register(delete_temp_icon)

root = tk.Tk()
root.title("Main Window")

root.iconbitmap('temp_icon.ico')

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