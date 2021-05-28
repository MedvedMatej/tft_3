import ctypes
import random
import time

def click(x,y,mode='left'):
    if mode == 'left':
        code1 = 0x0002
        code2 = 0x0004
    elif mode == 'right':
        code1 = 0x0008
        code2 = 0x0010
    else:
        return 'Invalid mode input'

    y +=random.randint(3, 9)
    x +=random.randint(-10,0)

    x = int(x)
    y = int(y)

    # see http://msdn.microsoft.com/en-us/library/ms646260(VS.85).aspx for details
    ctypes.windll.user32.SetCursorPos(x, y)
    ctypes.windll.user32.mouse_event(code1, 0, 0, 0,0) # left down
    time.sleep(0.2)
    ctypes.windll.user32.mouse_event(code2, 0, 0, 0,0) # left up
    time.sleep(0.15)

    return time.time()