import braille, braille.images
from tkinter import *
from tkinter import filedialog

class Globals:
    image: braille.Canvas = None
    lf = braille.AdaptiveThresholdFilter()
    file_path = None

root = Tk()
textwin = Toplevel(root)

inputx,inputy = Entry(root),Entry(root)
inputx.insert(0,"width")
inputy.insert(0,"height")
inputx.grid(row=0,column=0)
inputy.grid(row=0,column=1)

slider1 = Scale(root, to=50, orient="horizontal", length=200, label="Block size")
slider1.grid(row=1,columnspan=2)
slider2 = Scale(root, to=255, orient="horizontal", length=200, label="Constant")
slider2.grid(row=2,columnspan=2)
def select_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        Globals.file_path = file_path
        if not inputx.get().isdigit() or not inputy.get().isdigit():
            Globals.image = None
            return
        Globals.image = braille.Canvas(int(inputx.get()),int(inputy.get()))
        braille.images.add_image(Globals.image,file_path)

button1 = Button(root,text="Select image",command=select_image)
button1.grid(row=3,sticky="n")

text = Text(textwin, font=('Symbola',10))
text.pack(expand=True, fill=BOTH)

def render():
    if not inputx.get().isdigit() or not inputy.get().isdigit(): return
    if not Globals.image or int(inputx.get()) != Globals.image.w or int(inputy.get()) != Globals.image.h:
        if not Globals.file_path: return
        Globals.image = braille.Canvas(int(inputx.get()),int(inputy.get()))
        braille.images.add_image(Globals.image,Globals.file_path)
    text.delete("1.0",END)
    Globals.lf.block_size = slider1.get()
    Globals.lf.c = slider2.get()
    Globals.lf.apply_to_canvas(Globals.image)
    text.insert("1.0",Globals.image.str_without_color().replace(chr(10240),f"{chr(10240)}\u2006"))
    text.update_idletasks()

inputupdate = Button(root,text="Render",command=render)
inputupdate.grid(row=4,column=0)

def invertbtn():
    Globals.lf.invert = not Globals.lf.invert
    render()
def clip():
    render()
    root.clipboard_clear()
    root.clipboard_append(Globals.image.str_without_color())
invert = Button(root,text="Invert",command=invertbtn)
invert.grid(row=4,column=1)
copybtn = Button(root,text="Copy to clipboard",command=clip)
copybtn.grid(row=5,sticky="n")

root.mainloop()