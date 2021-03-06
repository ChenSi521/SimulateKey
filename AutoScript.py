import ctypes
import time
import pyautogui
import random
import json
from MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5 import sip

key_dict = {"A": 0x1E, "B": 0x30, "C": 0x2E, "D": 0x20, "E": 0x12, "F": 0x21, "G": 0x22, "H": 0x23,
            "I": 0x17, "J": 0x24, "K": 0x25, "L": 0x26, "M": 0x32, "N": 0x31, "O": 0x18, "P": 0x19,
            "Q": 0x10, "R": 0x13, "S": 0x1F, "T": 0x14, "U": 0x16, "V": 0x2F, "W": 0x11, "X": 0x2D,
            "Y": 0x15, "Z": 0x2C}

SendInput = ctypes.windll.user32.SendInput

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions


def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def player_teleport(direction):
    pyautogui.keyDown(direction)
    # pyautogui.press("ctrl", presses=2, interval=.2)
    time.sleep(0.1)
    pyautogui.keyUp(direction)


class AutoScript:
    def __init__(self):
        self.init()
        self.get_script_json()

    def init(self):
        self.left_right_count = 0
        self.script_list = None

    def get_script_json(self):
        f = open("script_list.json", 'r')
        self.script_list = json.load(f)
        f.close()

    def buffer_time(self):
        sec = 3
        for n in range(sec):
            print('{}秒後開始'.format(sec - n))
            time.sleep(1)

    def script_process(self):
        for script in self.script_list:
            if script['name'] == 'auto_left_and_right':
                self.auto_left_and_right(do_sleep=script['sleep'])
            else:
                self.keybroad_controller(event=script['event'],
                                         do_sleep=script['sleep'],
                                         repeats=script['repeat'])

    def auto_left_and_right(self, do_sleep):
        if self.left_right_count % 2 == 1:
            print('left')
            player_teleport("left")
            time.sleep(do_sleep)
            # time.sleep(0.5 * random.random())
        else:
            print('right')
            player_teleport("right")
            time.sleep(do_sleep)
            # time.sleep(0.5 * random.random())
        self.left_right_count += 1
        print('auto_left_and_right: {}'.format(self.left_right_count))


    def keybroad_controller(self, event, do_sleep, repeats):
        for count in range(repeats):
            PressKey(key_dict[event])
            # time.sleep(10)
            ReleaseKey(key_dict[event])
            time.sleep(do_sleep)

            print('event: {}, Loop : {}'.format(event, count))

    def execute(self):
        self.buffer_time()
        while True:
            self.script_process()



if __name__ == '__main__':
    obj = AutoScript()
    print(obj.script_list)
    obj.execute()
    # app = QApplication([])
    #
    # main_window = MainWindow().get_main_window()
    # main_window.setFixedSize(1024, 768)
    # main_window.show()
    # sys.exit(app.exec_())