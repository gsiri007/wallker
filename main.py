import tkinter
from tkinter import messagebox
from customtkinter import CTkFrame, CTkImage, CTkButton, CTkRadioButton, CTkScrollableFrame, filedialog
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

def set_wallpaper(path: str, mode: str) -> None:
    response = messagebox.askyesno(
        message= 'Are you sure you want to set this image as the wallpaper?',
        icon='question'
    )
    

    command = f'swww img --resize {mode} {path}'
    
    if response:
        subprocess.run(
            command,
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
header_frame = CTkFrame(root, fg_color='black')
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
open_directory_btn.grid(row=0, column=1)

mode = tkinter.StringVar(value="no") 
default_rbtn = CTkRadioButton(
    header_frame, 
    variable=mode, 
    value="no", 
    text="Default", 
    text_color="white"
)
crop_rbtn = CTkRadioButton(
    header_frame, 
    variable=mode,
    value="crop",
    text="Crop",
    text_color="white"
)
fit_rbtn = CTkRadioButton(
    header_frame, 
    variable=mode, 
    value="fit",
    text="Fit",
    text_color="white"
)
stretch_rbtn = CTkRadioButton(
    header_frame, 
    variable=mode, 
    value="stretch",
    text="Stretch",
    text_color="white"
)

default_rbtn.grid(row=1, column=0, pady=15)
crop_rbtn.grid(row=1, column=1, pady=15)
fit_rbtn.grid(row=1, column=2, pady=15)
stretch_rbtn.grid(row=1, column=3, pady=15)

def set_image_btn(image_path: str, ctk_img: CTkImage, cell: tuple):
    img_btn = CTkButton(
        body_frame, 
        text="",
        image=ctk_img, 
        command=lambda p=image_path:set_wallpaper(p, mode.get())
    )
    row, column = cell
    img_btn.grid(row=row, column=column, padx=25, pady=10)


if __name__ == '__main__':
    root.mainloop()
