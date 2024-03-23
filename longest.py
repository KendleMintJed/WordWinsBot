import cv2
import easyocr as ocr
import matplotlib.pyplot as plt
import numpy as np
import pyautogui as ag

from time import sleep
import json
import os

questionReigon = (585, 95, 745, 102)
reader = ocr.Reader(['en'])

i = 0

answersPath = 'longest.json'

try:
    while True:
        try:
            answerBoxPos = ag.locateOnScreen('screenshots/longest/AnswerBox.png', confidence=0.9)
            answers = json.load(open(answersPath, 'r'))

            print("Searching question...")

            questionImgPIL = ag.screenshot(region=(questionReigon))
            questionImgCV = cv2.cvtColor(np.array(questionImgPIL), cv2.COLOR_RGB2BGR)

            questionStr = ''.join([v[1] for v in reader.readtext(questionImgCV)]).replace(' ', '').replace('@', 'a').replace('&', 'a')

            print("Question detected:", questionStr)

            if questionStr not in answers.keys():
                print('Question not found...')
                answers[questionStr] = ""
                json.dump(answers, open(answersPath, 'w'))

            print("Answer:", answers[questionStr])
            
            sleep(0.15 * len(answers[questionStr]))
            ag.moveTo(answerBoxPos)
            with ag.hold('alt'):
                ag.press('tab')
                with ag.hold('shift'):
                    ag.press('tab')j
            sleep(0.2)
            ag.doubleClick()
            sleep(0.2)
            ag.typewrite(answers[questionStr])
            sleep(0.2)
            ag.moveRel(350, 0)
            with ag.hold('alt'):
                ag.press('tab')
                with ag.hold('shift'):
                    ag.press('tab')
            sleep(0.2)
            ag.click()
        except ag.ImageNotFoundException:
            print('Waiting for question...')
        i = (i + 1) % 300
        if i == 0:
            ag.moveTo(100, 900)
            ag.rightClick()
        sleep(1)

except KeyboardInterrupt:
    print('Exiting...')
