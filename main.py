from os import path
import tkinter
from tkinter import messagebox
from customtkinter import CTkFrame, CTkImage, CTkButton, CTkScrollableFrame, filedialog
from PIL import Image
import subprocess
import threading


#############################################
#             Initialization                #
#############################################


root = tkinter.Tk()
root.title('wallker')
root.config(bg='black')


#############################################
#             Functions                     #
#############################################


def set_directory() -> None:
    directory = filedialog.askdirectory()
    threading.Thread(
        target=get_images_async, 
        args=(directory,), 
        daemon=True
    ).start()

def set_wallpaper(path: str) -> None:
    response = messagebox.askyesno(
        message= 'Are you sure you want to set this image as the wallpaper?',
        icon='question'
    )

    if response:
        subprocess.run(
            f'hyprctl hyprpaper preload {path} && hyprctl hyprpaper wallpaper ", {path}"',
            shell=True,
            stdout=subprocess.DEVNULL
        )
    else:
        pass


def get_images_async(directory: str):
    result = subprocess.run(
        f'ls {directory}', 
        capture_output=True, 
        shell=True, 
        text=True
    ).stdout

    images = result.split()

    row = 0
    column = 0
    for image in images:
        extensions = ['png', 'jpg', 'jpeg', 'webp']
        if any(extension in image for extension in extensions):
            try:
                image_path = f'{directory}/{image}'
                img = Image.open(image_path)

                img.thumbnail((250, 250), Image.Resampling.BICUBIC)
                ctk_img = CTkImage(light_image=img, dark_image=img, size=(250,250))

                root.after(0, set_image_btn, image_path, ctk_img, (row, column))
            except Exception as e:
                print(f'ERROR: {e}')

            column += 1
            if column == 6:
                column = 0
                row += 1


#############################################
#               GUI                         #
#############################################


# frames
header_frame = CTkFrame(root)
body_frame = CTkScrollableFrame(root, fg_color='black')

header_frame.pack(pady=20)
body_frame.pack(fill='both', expand=True)

# widgets
open_directory_btn = CTkButton(
    header_frame,
    text='Open',
    command=set_directory,
    bg_color='grey',
    fg_color='grey',
    corner_radius=0
)
open_directory_btn.pack()

def set_image_btn(image_path: str, ctk_img: CTkImage, cell: tuple):
    img_btn = CTkButton(
        body_frame, 
        text="",
        image=ctk_img, 
        command=lambda p=image_path:set_wallpaper(p)
    )
    row, column = cell
    img_btn.grid(row=row, column=column, padx=25, pady=10)

root.mainloop()
