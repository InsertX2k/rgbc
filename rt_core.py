# imports
import win32api, win32con
import pyautogui


def isScrollLockOn():
    """
    This is a function used to return the current state of the scroll lock button (or basically the keyboard RGB button)
    
    Returns 1 if enabled, otherwise returns 0
    """
    return win32api.GetKeyState(win32con.VK_SCROLL)



def Send_ScrollLock():
    """
    Sends the Scroll Lock key using a virtual keyboard, if fails, it returns False, otherwise returns True.
    """
    try:
        pyautogui.typewrite(['scrolllock'])
        return True
    except Exception:
        return False