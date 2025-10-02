from os import path
import tkinter
from tkinter import messagebox
from customtkinter import LEFT, CTkFrame, CTkImage, CTkButton, CTkLabel, CTkScrollableFrame, filedialog
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

    for image in images:
        try:
            image_path = f'{directory}/{image}'
            img = Image.open(image_path)

            img.thumbnail((250, 250), Image.Resampling.BICUBIC)
            ctk_img = CTkImage(light_image=img, dark_image=img, size=(250,250))

            root.after(0, set_image_btn, image_path, ctk_img)
        except Exception as e:
            print(f'ERROR: {e}')


#############################################
#               GUI                         #
#############################################

header_frame = CTkFrame(root)
body_frame = CTkScrollableFrame(root)

header_frame.pack()
body_frame.pack(fill='both', expand=True)


select_directory_btn = CTkButton(
    header_frame,
    text='Select',
    command=set_directory
)
select_directory_btn.pack(side=LEFT)

def set_image_btn(image_path: str, ctk_img: CTkImage):
    img_btn = CTkButton(
        body_frame, 
        text="",
        image=ctk_img, 
        command=lambda p=image_path:set_wallpaper(p)
    )
    img_btn.pack(pady=10)

root.mainloop()
