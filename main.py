# imports
from tkinter import *
from tkinter import messagebox
# another imports.
import rt_core # rt_core import (see rt_core.py in this dir)
from pystray import Icon, MenuItem as item # pystray
import pystray
from PIL import Image # pillow
# from time import sleep # sleep function

# global var rgb_state
rgb_state = False

# defining the initializing method.
def initialize():
    global rgb_state
    """
    The initialization function - used to retrieve the current state of RGB Keyboard backlighting.

    This function returns True if Keyboard RGB is enabled, otherwise it returns False.
    """
    rgb_state = rt_core.isScrollLockOn()
    rgb_state = int(rgb_state) # -> converting rgb_state to an integer.
    if rgb_state == 1:
        # print("rgb is enabled")
        rgb_state = True
        status.configure(text="RGB is On", foreground='lightgreen')
        try:
            window.iconbitmap("rgbon.ico")
        except Exception as excpt1:
            messagebox.showerror("Unable to load icon file", f"Unable to load icon file for this window due to exception: \n{excpt1}\nThe program will continue without an icon file.")
    elif rgb_state == 0:
        # print("rgb is disabled")
        status.configure(text="RGB is Off", foreground='red')
        try:
            window.iconbitmap("rgboff.ico")
        except Exception as excpt1:
            messagebox.showerror("Unable to load icon file", f"Unable to load icon file for this window due to exception: \n{excpt1}\nThe program will continue without an icon file.")
        rgb_state = False
    else:
        # print("unable to retrieve rgb keyboard state.")
        status.configure(text="RGB is Unknown", foreground='orange')
        try:
            window.iconbitmap("rgboff.ico")
        except Exception as excpt1:
            messagebox.showerror("Unable to load icon file", f"Unable to load icon file for this window due to exception: \n{excpt1}\nThe program will continue without an icon file.")
        rgb_state = None

    window.after(100, initialize)





def withdraw_window():
    global rgb_state

    window.withdraw()
    def show_trayico():
        try:
            icon.stop()
        except Exception:
            pass
        def selfterminate():
                icon.stop()
                window.destroy()
        if rgb_state == True:
            tray_ico = Image.open("rgbon.ico")
        elif rgb_state == False:
            tray_ico = Image.open("rgboff.ico")
        else:
            tray_ico = Image.open("rgboff.ico")

        def show_window():
            icon.stop()
            window.deiconify()

        menu = (item('Quit', selfterminate), item('Enable Keyboard RGB', enable_rgb), item('Disable Keyboard RGB', disable_rgb), item("Show Window", show_window))
        icon = pystray.Icon("RGB Keyboard Controller v1.0", tray_ico, "RGB Keyboard Controller v1.0\nRunning", menu)
        icon.run()

    show_trayico()



def disable_rgb():
    global rgb_state
    print("Disabling Keyboard RGB...")
    # making sure rgb is not disabled.
    if rgb_state == False:
        messagebox.showinfo("RGB Disable", "Keyboard RGB is already disabled!")
    elif rgb_state == True:
        slock = rt_core.Send_ScrollLock()
        rgb_state = False
        if slock == False:
            messagebox.showerror("Exception","Unable to send Scrolllock signal to your keyboard")
        else:
            pass
    else:
        pass
        

def enable_rgb():
    global rgb_state
    print("Enabling Keyboard RGB...")
    # making sure rgb is not enabled.
    if rgb_state == True:
        messagebox.showinfo("RGB Enable", "Keyboard RGB is already enabled!")
    elif rgb_state == False:
        slock = rt_core.Send_ScrollLock()
        rgb_state = True
        if slock == False:
            messagebox.showerror("Exception","Unable to send Scrolllock signal to your keyboard")
        else:
            pass
    else:
        pass



def call_enable_rgb(keybinding_arg):
    enable_rgb()

def call_disable_rgb(keybinding_arg):
    disable_rgb()


window = Tk()
try:
    window.iconbitmap("rgbon.ico")
except Exception as excpt1:
    messagebox.showerror("Unable to load icon file", f"Unable to load icon file for this window due to exception: \n{excpt1}\nThe program will continue without an icon file.")
window.title("Generic RGB Keyboard Software - v1.0")
window.geometry("600x200")
window.configure(bg = "#222222")
canvas = Canvas(
    window,
    bg = "#222222",
    height = 200,
    width = 600,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"background.png")
background = canvas.create_image(
    300.0, 100.0,
    image=background_img)

img0 = PhotoImage(file = f"img0.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = disable_rgb,
    relief = "flat",
    cursor='hand2')

b0.place(
    x = 109, y = 140,
    width = 152,
    height = 34)

img1 = PhotoImage(file = f"img1.png")
b1 = Button(
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = enable_rgb,
    relief = "flat",
    cursor='hand2')

b1.place(
    x = 338, y = 140,
    width = 152,
    height = 34)

# status label
status = Label(
    window,
    text=f"RGB is Unknown",
    foreground='red',
    font=("Arial", 18),
    background='#222222'
)
status.place(x=230, y=90)


initialize()
window.after(100, initialize)
window.resizable(False, False)


window.bind("<F5>", call_disable_rgb)
window.bind("<F6>", call_enable_rgb)

# calling a different wm protocol.
window.protocol('WM_DELETE_WINDOW', withdraw_window)

window.mainloop()
