import sys
import win32gui
import win32con
import ctypes
import ctypes.wintypes


def window_enum_handler(hwnd_handle: int, ctx: any) -> bool:
    if not win32gui.IsWindowVisible(hwnd_handle):
        return True
    title = win32gui.GetWindowText(hwnd_handle)
    if not title.strip():
        return True
    hwnds.append(hwnd_handle)
    return True


def create_boolean(value: bool = False) -> ctypes.c_buffer:
    buffer = ctypes.c_buffer(4)
    if value:
        buffer[-1] = True
    return buffer


dwmapi = ctypes.windll.dwmapi
DwmSetWindowAttribute = dwmapi.DwmSetWindowAttribute
DwmSetWindowAttribute.argtypes = (
    ctypes.wintypes.HWND,
    ctypes.wintypes.DWORD,
    ctypes.wintypes.LPCVOID,
    ctypes.wintypes.DWORD
)
DwmSetWindowAttribute.restype = ctypes.c_long
hwnds = []
win32gui.EnumWindows(window_enum_handler, None)

total = len(hwnds)
for num, hwnd in enumerate(hwnds):
    print(f'[{num + 1}]: {win32gui.GetWindowText(hwnd)}')

user_input = input('Select window: ').lower().strip()
print('')
if not user_input.isdigit():
    sys.stderr.write('Not a number!\n')
    sys.exit(1)

key_id = int(user_input)
if not total >= key_id >=1:
    sys.stderr.write('Invalid id!\n')
    sys.exit(1)


hwnd = hwnds[key_id - 1]
boolean1 = create_boolean(True)
if DwmSetWindowAttribute(hwnd, 20, boolean1, ctypes.sizeof(boolean1)):
    sys.stderr.write('Error setting dark theme!\n')
    sys.exit(1)
boolean2 = create_boolean(True)
DwmSetWindowAttribute(hwnd, 19, boolean1, ctypes.sizeof(boolean2))
