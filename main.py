import atexit
import base64
import datetime
import os
import pathlib
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image
from PIL.ExifTags import TAGS

APP_VERSION = "1.0"
DEVELOPER_NAME = "Programmer-Timmy"

from PIL import Image
from PIL.ExifTags import TAGS
import datetime

use_month_names = False  # Set to True to use month names, False to use numbers
sort_videos = False
sort_pictures = True

def get_image_taken_date(image_path):
    try:
        img = Image.open(image_path)
        exif_data = img.getexif()
        if not exif_data:
            file_stat = os.stat(image_path)
            creation_time = datetime.datetime.fromtimestamp(file_stat.st_ctime)
            print(f"Gebruik van bestandsinformatie: {creation_time}")
            return creation_time.year, creation_time.month, creation_time.day

        # Probeer meerdere tijd-tags
        for tag_id in [36867, 36868, 306]:  # DateTimeOriginal, DateTimeDigitized, DateTime
            creation_time = exif_data.get(tag_id)
            if creation_time:
                print(f"Gevonden tag {tag_id}: {creation_time}")
                try:
                    creation_time = datetime.datetime.strptime(creation_time, '%Y:%m:%d %H:%M:%S')
                    return creation_time.year, creation_time.month, creation_time.day
                except ValueError:
                    print(f"Datumformaat ongeldig: {creation_time}")

    except Exception as e:
        print(f"Fout bij het uitlezen van de afbeelding: {e}")

    return None, None, None

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
        c_year, c_month, c_day = get_image_taken_date(x)

        if c_year is not None:
            image_info.append((x, c_year, c_month, c_day))

    for image_path, year, month, day in image_info:
        # Create subdirectories for each year, month, and day in the same location as the original images
        year_folder = os.path.join(os.path.dirname(image_path), str(year))
        month_name = month_names[month] if use_month_names else str(month)
        month_folder = os.path.join(year_folder, month_name)
        day_folder = os.path.join(month_folder, str(day))

        os.makedirs(day_folder, exist_ok=True)

        # Move images to their corresponding day folders
        destination_path = os.path.join(day_folder, os.path.basename(image_path))
        shutil.move(image_path, destination_path)

    messagebox.showinfo("Complete", "Images are sorted.")


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
                                        "Are you sure you want to organize: {} imagesip".format(count),
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
        result = messagebox.askquestion("Organize images",
                                        "Are you sure you want to organize: {} images in {}".format(count, folder),
                                        icon='warning')
        if result == 'yes':
            organize_images(images)
        else:
            return
    else:
        messagebox.showinfo("Info", "No images found in the folder.")

def undo():
#     let the user select the dir that needs to be undone
# if the dir exist then we will grab all the images in that dir (also the subdirs) and move them to the selected dir parent
    folder = filedialog.askdirectory(title="Select a Folder to Undo")
    if not folder:
        messagebox.showinfo("Info", "No folder selected.")
        return

    parent_folder = os.path.dirname(folder)
    for root, dirs, files in os.walk(folder, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            shutil.move(file_path, parent_folder)

        for dir in dirs:
            dir_path = os.path.join(root, dir)
            remove_directory(dir_path)
    # Remove the now empty folder
    try:
        os.rmdir(folder)
        messagebox.showinfo("Complete", "Undo operation completed.")
    except OSError:
        messagebox.showerror("Error", "Could not remove the folder. It may not be empty or does not exist.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
def remove_directory(path: str):
    """Remove a directory and all its contents."""
    if os.path.exists(path):
        shutil.rmtree(path)
    else:
        print(f"Directory {path} does not exist.")


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
root.title("Image sorter")

root.iconbitmap('temp_icon.ico')

label = tk.Label(root, text="Select Images or Select a Folder", font=("Segoe UI", 14))
label.pack()

frame = tk.Frame(root)
frame.pack(expand=True)

style = ttk.Style()
style.configure("TButton", padding=10, font=("Segoe UI", 12), relief="flat", borderwidth=0)

style.map("TButton", foreground=[('pressed', 'black'), ('active', 'black')],
          background=[('pressed', 'blue'), ('active', 'lightblue')])

button_images = ttk.Button(frame, text="Select Images", compound=tk.TOP, command=select_images)
button_images.pack(side=tk.LEFT)

button_folder = ttk.Button(frame, text="Select Folder", compound=tk.TOP, command=select_folder)
button_folder.pack(side=tk.LEFT)

button_undo = ttk.Button(frame, text="Undo", compound=tk.TOP, command=undo)
button_undo.pack(side=tk.LEFT)

# checkbock of usage of month names
check_var = tk.BooleanVar(value=use_month_names)
checkbutton = ttk.Checkbutton(root, text="Use Month Names", variable=check_var,
                               command=lambda: globals().__setitem__('use_month_names', check_var.get()))

# # checkboxs of sorting of video's
# check_sv_var = tk.BooleanVar(value=sort_videos)
# checkbutton_sv = ttk.Checkbutton(root, text="Sort Videos", variable=check_sv_var,
#                                  command=lambda: globals().__setitem__('sort_videos', check_sv_var.get()))

checkbutton.pack(pady=10)



root.mainloop()
