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
letters = 0

answersPath = 'shortest.json'

try:
    while True:
        try:
            answerBoxPos = ag.locateOnScreen('screenshots/shortest/answerBox.png', confidence=0.9)
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

            if letters + len(answers[questionStr]) < 48:
                letters += len(answers[questionStr])

                print("letters:", letters)

                ag.moveTo(answerBoxPos)
                with ag.hold('alt'):
                    ag.press('tab')
                    with ag.hold('shift'):
                        ag.press('tab')
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
            else:
                print("letters:", letters + len(answers[questionStr]), "waiting...")
                sleep(5)
        except ag.ImageNotFoundException:
            print('Waiting for question...')
            if letters != 0:
                try:
                    ag.locateOnScreen('screenshots/shortest/MoneyRain.png', confidence=0.9)
                    print("Money rain... reset letter count")
                    letters = 0
                except ag.ImageNotFoundException:
                    pass
        i = (i + 1) % 300
        if i == 0:
            ag.moveTo(100, 900)
            ag.rightClick()
        sleep(1)

except KeyboardInterrupt:
    print('Exiting...')
