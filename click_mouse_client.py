import pyautogui
import sys

pyautogui.FAILSAFE = False

if __name__ == '__main__':
    print('Argument List:', str(sys.argv))
    pyautogui.click(int(sys.argv[1]), int(sys.argv[2]))
