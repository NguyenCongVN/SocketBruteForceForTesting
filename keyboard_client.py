import pyautogui
import sys

pyautogui.FAILSAFE = False

if __name__ == '__main__':
    print('Argument List:', str(sys.argv))
    pyautogui.press(str(sys.argv[1]))
