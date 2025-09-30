from os import path
import tkinter
from tkinter import messagebox
import subprocess
from customtkinter import LEFT, CTkFrame, CTkImage, CTkButton, CTkLabel, CTkScrollableFrame, filedialog
from PIL import Image

root = tkinter.Tk()
root.title('wallker')
root.config(bg='black')

# image buttons
image_paths   = []
image_buttons = []

# functions
def set_directory() -> None:
    directory = filedialog.askdirectory()
    get_images(directory)

def set_wallpaper(path: str) -> None:
    response = messagebox.askyesno(
        message= 'Are you sure you want to set this image as the wallpaper?',
        icon='question'
    )

    if response:
        subprocess.run(
            [
                f'hyprctl hyprpaper preload {path} && hyprctl hyprpaper wallpaper ", {path}"',
            ],
            shell=True,
            stdout=subprocess.DEVNULL
            
        )
    else:
        pass





def set_image_btn_command():
    for btn in image_buttons:
        index = image_buttons.index(btn)
        btn.configure(command=lambda i=index: set_wallpaper(image_paths[i]))
        btn.pack(pady=10)

def get_images(directory: str):
    result = subprocess.run(
        f'ls {directory}', 
        capture_output=True, 
        shell=True, 
        text=True
    ).stdout

    images = result.split()

    for image in images:
        image_path = f'{directory}/{image}'
        image_paths.append(image_path)
        img = Image.open(image_path)
        ctk_img = CTkImage(light_image=img, dark_image=img, size=(250,250))
        image_buttons.append(CTkButton(
            body_frame, 
            text="",
            image=ctk_img, 
        ))

    set_image_btn_command()


# frames
header_frame = CTkFrame(root)
body_frame = CTkScrollableFrame(root)

header_frame.pack()
body_frame.pack(fill='both', expand=True)

# widgets
select_directory_btn = CTkButton(
    header_frame,
    text='Select',
    command=set_directory
)
select_directory_btn.pack(side=LEFT)


root.mainloop()
