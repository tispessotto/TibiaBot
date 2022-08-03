from ahk import AHK
import win32ui
from ctypes import windll
from PIL import Image
import numpy as np
import time
import cv2
import win32gui
import pytesseract
import settings

a_left = 2135
a_right = 2232
a_bottom = 100
a_top = 52

last_time_healed = 0
last_hp_unit = 0

last_time_mana_up = 0
last_mana_unit = 0
last_time = 0

FIRST_IN_BATTLE_POS = (1958, 568)
UNITS_IN_BATTLE_SIZE = (200, 28)
first_enemy_scan_pos = (FIRST_IN_BATTLE_POS[0], FIRST_IN_BATTLE_POS[1],
                        FIRST_IN_BATTLE_POS[0] + UNITS_IN_BATTLE_SIZE[0],
                        FIRST_IN_BATTLE_POS[1] + UNITS_IN_BATTLE_SIZE[1])

hwnd = win32gui.FindWindow(None, 'OBS 27.2.4 (64-bit, windows) - Profile: Untitled - Scenes: Untitled')
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
ahk = AHK()

CURRENT_HP = -1
CURRENT_MANA = -1


def run_scripts():
    while True:
        screenshot = take_ss()
        update_current_hp_mana(screenshot)
        if CURRENT_HP < settings.LOW_HP_LEVEL:
            heal_up()
        if CURRENT_MANA < settings.LOW_MANA_LEVEL:
            mana_up()
        if settings.EXURA_SIO_ACTIVE:
            scan_sio(screenshot)
        check_speed()


def check_speed():
    global last_time
    now = time.time()
    print(f"This loop took: {now - last_time} seconds!")
    last_time = time.time()


def cooldown_ok(last_time1, last_unit, current_unit):
    now = time.time()
    dif = now - last_time1
    if dif < 1 and current_unit <= last_unit:
        print(f"The loop took: {dif} seconds\n"
              f"Current unit: {current_unit}\n"
              f"Last time unit was: {last_unit}")
        return False
    return True


def take_ss():
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    saveDC.SelectObject(saveBitMap)
    windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 3)
    bmp_info = saveBitMap.GetInfo()
    bmp_str = saveBitMap.GetBitmapBits(True)
    ss = Image.frombuffer(
        'RGB',
        (bmp_info['bmWidth'], bmp_info['bmHeight']),
        bmp_str, 'raw', 'BGRX', 0, 1)
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)
    return ss


def focus_mana_hp(original_ss):
    a = original_ss.crop((a_left, a_top, a_right, a_bottom))
    pix = np.array(a)
    bgr_image = pix.astype(np.uint8)
    gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
    focused_ss = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    return focused_ss


def update_current_hp_mana(original_ss):
    global CURRENT_MANA
    global CURRENT_HP

    focused_ss = focus_mana_hp(original_ss)
    text = pytesseract.image_to_string(focused_ss, config='--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789')
    hp_mana_numbers = text.split("\n")

    try:
        CURRENT_HP = int(hp_mana_numbers[0])
    except:
        CURRENT_HP = 0
        print("Error: CURRENT_HP couldn't be read!")

    try:
        CURRENT_MANA = int(hp_mana_numbers[1])
    except:
        CURRENT_MANA = 0
        print("Error: CURRENT_MANA couldn't be read!")
        ahk.sound_beep()


def mana_up():
    global last_mana_unit
    global last_time_mana_up
    if cooldown_ok(last_time_mana_up, last_mana_unit, CURRENT_MANA):
        last_time_mana_up = time.time()
        last_mana_unit = CURRENT_MANA
        if CURRENT_MANA < settings.CRITICAL_MANA_LEVEL and settings.STRONG_MANA_UP_ACTIVE:
            ahk.key_press(f"{settings.CRITICAL_MANA_HOTKEY}")
        elif settings.LIGHT_MANA_UP_ACTIVE:
            ahk.key_press(f"{settings.LOW_MANA_HOTKEY}")


def heal_up():
    global last_time_healed
    global last_hp_unit
    if cooldown_ok(last_time_healed, last_hp_unit, CURRENT_HP):
        last_time_healed = time.time()
        last_hp_unit = CURRENT_HP
        if CURRENT_HP < settings.CRITICAL_HP_LEVEL and settings.STRONG_HEAL_ACTIVE:
            ahk.key_press(f"{settings.CRITICAL_HP_HOTKEY}")
        elif settings.LIGHT_HEAL_ACTIVE:
            ahk.key_press(f"{settings.LOW_HP_HOTKEY}")


def scan_sio(screenshot2):
    position_to_scan = first_enemy_scan_pos
    while True:
        a = screenshot2.crop(position_to_scan)
        pix = np.array(a)
        bgr_image = pix.astype(np.uint8)
        gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray_image,
                                           config='--psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTU'
                                                  'VWXYZabcdefghijklmnopqrstuvwxyz').split("\n")[0]
        if text in ["", "Tree", "TER", "ASSETS", "BAS", "eiEGAPtts"]:
            return
        elif text == settings.SIO_TARGET:
            pixel_to_scan = (position_to_scan[0] + 8, position_to_scan[1] + 31)
            im = screenshot2.load()
            RGB = im[pixel_to_scan[0], pixel_to_scan[1]]
            if RGB[0] > 100:
                ahk.key_press(settings.EXURA_SIO_HOTKEY)
            return
        else:
            position_to_scan = (
                position_to_scan[0], position_to_scan[1] + 41, position_to_scan[2], position_to_scan[3] + 41)
