import time
import tkinter

import cv2 as cv
import numpy as np
import pyautogui
from tkinter import *
import keyboard

root = Tk()

set_bol = False
course_num_1 = -1
course_num_2 = -1

#라벨
label = tkinter.Label(root, text="학수 번호")
label_hyp = tkinter.Label(root, text="-")
# label_confirm = tkinter.Label(root)

def set_pressed():
    global set_bol
    global course_num_1
    global  course_num_2

    course_num_1 = input_1.get()
    course_num_2 = input_2.get()
    set_bol = True
    print(course_num_1 + " - " + course_num_2)

def start_pressed():
    if set_bol:
        root.destroy()

#버튼
set_btn = Button(root, text="설정", command= set_pressed)
start_btn = Button(root, text="수강신청 시작", command=start_pressed)

#학수 번호 입력 1
input_1 = Entry(root, width=10)
#학수 번호 입력 2
input_2 = Entry(root, width=5)

# 학수 번호 저장
course_num_1 = -1
course_num_2 = -1

def place_gui():

    #기본 속성
    root.title("CNU Macaroon")
    root.geometry("270x160")
    root.resizable(False, False)

    #라벨
    label.place(x= 10, y=22)
    label_hyp.place(x=145, y=22)
    # label_confirm.pack()

    #버튼
    set_btn.place(x=220, y =20)
    start_btn.place(x = 95, y = 100)

    #학수번호 입력 텍스트 1
    input_1.place(x=70, y=22)
    input_2.place(x=160, y=22)

def run_gui():
    place_gui()
    course_1 = input_1.get()
    course_2 = input_2.get()
    root.mainloop()

if __name__ == '__main__':
    run_gui()
    print(course_num_1)
    print(course_num_2)

    # targets val
    # target_num_1 = cv.imread('target_1.PNG', cv.IMREAD_COLOR)
    target_num_1 = cv.imread('test_target_1.PNG', cv.IMREAD_COLOR)
    h1,w1 = target_num_1.shape[:2]

    mac_num_target = cv.imread('mac_num_target.PNG', cv.IMREAD_COLOR)
    h2,w2 = mac_num_target.shape[:2]

    time.sleep(1)

    # pic = pyautogui.screenshot()
    # cv.imshow('res', cv.cvtColor(np.array(pic),cv.COLOR_RGB2BGR))
    # cv.waitKey()
    # 매크로 동작 코드
    while 1:
        # pic = pyautogui.screenshot(region=(0, 0, 1000, 1000))
        pic = pyautogui.screenshot()

        img_frame = np.array(pic)
        img_frame = cv.cvtColor(img_frame, cv.COLOR_RGB2BGR)

        meth = 'cv.TM_CCOEFF_NORMED'
        # meth = 'cv.TM_CCOEFF'

        method = eval(meth)

        res = cv.matchTemplate(target_num_1, img_frame, method)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        top_left = max_loc
        bottom_right = (top_left[0] + w1, top_left[1] + h1)

        cv.rectangle(img_frame, top_left, bottom_right, (0, 255, 0), 2)
        print(max_val, top_left)

        # 마우스 클릭 (끝에서 조금 앞으로 클릭)
        # 이후 tab 키 누름
        pyautogui.moveTo(top_left[0]+w1-20 , top_left[1] + h1-10)
        pyautogui.click()

        pyautogui.write(course_num_1)
        pyautogui.press('Tab')
        pyautogui.write(course_num_2)

        # cv.imshow('result', img_frame)
        # cv.waitKey()

        #종료 코드
        try:
            if keyboard.is_pressed('ESC'):
                print('is pressed')
                sys.exit(0)
        except:
            break
