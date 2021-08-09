import time
import tkinter

import cv2
import cv2 as cv
import numpy as np
import pyautogui
from tkinter import *
import keyboard

root = Tk()

set_bol = False
course_num_1 = -1
course_num_2 = -1

# 라벨
label = tkinter.Label(root, text="학수 번호")
label_hyp = tkinter.Label(root, text="-")

def set_pressed():
    global set_bol
    global course_num_1
    global course_num_2

    course_num_1 = input_1.get()
    course_num_2 = input_2.get()
    set_bol = True
    print(course_num_1 + " - " + course_num_2)


def start_pressed():
    if set_bol:
        root.destroy()


# 버튼
set_btn = Button(root, text="설정", command=set_pressed)
start_btn = Button(root, text="수강신청 시작", command=start_pressed)

# 학수 번호 입력 1
input_1 = Entry(root, width=10)
# 학수 번호 입력 2
input_2 = Entry(root, width=5)

# 학수 번호 저장
course_num_1 = -1
course_num_2 = -1


def place_gui():
    # 기본 속성
    root.title("CNU Macaroon")
    root.geometry("270x160")
    root.resizable(False, False)

    # 라벨
    label.place(x=10, y=22)
    label_hyp.place(x=145, y=22)
    # label_confirm.pack()

    # 버튼
    set_btn.place(x=220, y=20)
    start_btn.place(x=95, y=100)

    # 학수번호 입력 텍스트 1
    input_1.place(x=70, y=22)
    input_2.place(x=160, y=22)


def run_gui():
    place_gui()
    course_1 = input_1.get()
    course_2 = input_2.get()
    root.mainloop()

def success_check(target):
    screen = pyautogui.screenshot()
    imgFrame = np.array(screen)
    imgFrame = cv.cvtColor(imgFrame, cv2.COLOR_RGB2BGR)
    threshold = 0.8
    method = 'cv.TM_CCOEFF_NORMED'
    res_ = cv2.matchTemplate(target, imgFrame, eval(method))
    if np.amax(res_) > threshold:
        return True
    else:
        return False


if __name__ == '__main__':

    run_gui()
    print(course_num_1)
    print(course_num_2)

    if course_num_1 == -1 or course_num_2 == -1:
        exit(0)

    # targets val
    target_num_1 = cv.imread('target_1.PNG', cv.IMREAD_COLOR)
    h1, w1 = target_num_1.shape[:2]

    time.sleep(1)
    # 매크로 동작 코드
    pic = pyautogui.screenshot()

    img_frame = np.array(pic)
    img_frame = cv.cvtColor(img_frame, cv.COLOR_RGB2BGR)

    meth = 'cv.TM_CCOEFF_NORMED'

    method = eval(meth)

    res = cv.matchTemplate(target_num_1, img_frame, method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    top_left = max_loc
    bottom_right = (top_left[0] + w1, top_left[1] + h1)

    cv.rectangle(img_frame, top_left, bottom_right, (0, 255, 0), 2)
    print(max_val, top_left)

    # 마우스 클릭 (끝에서 130 픽셀 앞으로 클릭)
    pyautogui.moveTo(top_left[0] + w1 - 130, top_left[1] + h1 - 20)
    pyautogui.click()

    pyautogui.write(course_num_1)
    pyautogui.write(course_num_2)

    time.sleep(1)

    # check for success
    target_success = cv.imread("success.PNG", cv2.IMREAD_COLOR)

    while 1:
        pyautogui.press('Enter')

        #수강 신청 성공시 멈춤
        if success_check(target_success):
            break

        # 종료 코드 : 'ESC' 연타하여 종료
        try:
            if keyboard.is_pressed('ESC'):
                print('is pressed')
                sys.exit(0)
        except:
            break
        time.sleep(1)
