import tkinter
import subprocess
from customtkinter import CTkFrame, CTkImage, CTkButton, CTkLabel, CTkScrollableFrame, filedialog
from PIL import Image

root = tkinter.Tk()
root.title('wallker')
root.config(bg='black')

# functions
def set_directory():
    directory = filedialog.askdirectory()
    get_images(directory)

def get_images(directory: str):
    result = subprocess.run(
        f'ls {directory}', 
        capture_output=True, 
        shell=True, 
        text=True
    ).stdout

    images = result.split()

    for image in images:
        file_path = f'{directory}/{image}'
        img = Image.open(file_path)
        ctk_img = CTkImage(light_image=img, dark_image=img, size=(250,250))
        img_label = CTkButton(body_frame, image=ctk_img, text="")
        img_label.pack(pady=10)


# frames
header_frame = CTkFrame(root)
body_frame = CTkScrollableFrame(root)

header_frame.pack()
body_frame.pack(fill='both', expand=True)

# gui
select_directory_btn = CTkButton(
    header_frame,
    text='Select',
    command=set_directory
)
select_directory_btn.pack()



root.mainloop()
