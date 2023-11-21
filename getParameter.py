import pyautogui
import cv2
import pyocr
import pyocr.builders
from PIL import Image
import sys
import time
import re


preParamImg = 'tempImg/preParamImg.png'
paramImg = 'tempImg/paramImg.png'
c_nurtureImg= 'tempImg/c_nurtureImg.png'
b_nurtureImg= 'tempImg/b_nurtureImg.png'
preStatusTop = 0
preStatusBottom = 0
statusTop = 0
statusBottom = 0
preTop = 0
height = 0

btnLeft = 0
btnRight = 0

countTop_right=0
countright_pretop=0
countright_height=0


def test():
    preStatusTop = pyautogui.screenshot
    preStatusTop.save('test.png')
    pyautogui.click(250, 400)
    pyautogui.click(250, 400)

    pyautogui.click(250, 400)


def getParameter():

    global preStatusTop
    global preStatusBottom
    global statusTop
    global statusBottom
    global preTop
    global height
    global btnLeft
    global btnRight
    global countTop_left
    global countleft_pretop
    global countleft_height
    global countTop_right
    global countright_pretop
    global countright_height


    preStatusTop = pyautogui.locateOnScreen(
        'refImg/preStatusTop.png', confidence=0.6)

    preStatusBottom = pyautogui.locateOnScreen(
        'refImg/preStatusBottom.png', confidence=0.6)

    statusTop = pyautogui.locateOnScreen(
        'refImg/statusTop.png', confidence=0.6)

    statusBottom = pyautogui.locateOnScreen(
        'refImg/statusBottom.png', confidence=0.6)

    preTop = preStatusTop.top + preStatusTop.height
    height = statusBottom.top - preTop

    btnLeft = pyautogui.locateOnScreen(
        'refImg/btnLeft.png', confidence=0.5)

    btnRight = pyautogui.locateOnScreen(
        'refImg/btnRight.png', confidence=0.9)


    countTop_right=pyautogui.locateOnScreen(
        "refImg/countTop_right.png")

    countright_pretop=countTop_right.top+countTop_right.height
    countright_height=btnRight.top-countright_pretop


def countRight():
    b_nurture= pyautogui.screenshot(
        region=(countTop_right.left, countright_pretop, countTop_right.width,countright_height))
    b_nurture.save(b_nurtureImg)
    b_nurture.show()

    time.sleep(1)

    tools = pyocr.get_available_tools()
    tool = tools[0]
    langs = tool.get_available_languages()
    b_nurture_sc = tool.image_to_string(
        Image.open(b_nurtureImg),
        lang='eng',
        builder=pyocr.builders.DigitBuilder()
    ).split()
    if int(b_nurture_sc) <= 20:
        sys.exit()


def clickLeft():
    btnLeftX, btnLeftY = pyautogui.center(btnLeft)
    pyautogui.click(btnLeftX, btnLeftY)  # retinaDesiplayは/2
    time.sleep(1)


def clickRight():
    btnRightX, btnRightY = pyautogui.center(btnRight)
    pyautogui.click(btnRightX, btnRightY)
    time.sleep(1)


def getSS():
    time.sleep(2)
    preSc = pyautogui.screenshot(
        region=(preStatusTop.left, preTop, preStatusTop.width, height))
    sc = pyautogui.screenshot(
        region=(statusTop.left, preTop, statusTop.width, height))

    preSc.save(preParamImg)
    sc.save(paramImg)

    im = cv2.imread(preParamImg)
    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(preParamImg,im_gray)

    im= cv2.imread(paramImg)
    im_gray= cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    cv2.imwrite(paramImg,im_gray)

    #imgPIL = Image.open(preParamImg)  画像読み込み
    #imgPIL.show()
    #Image.open(paramImg).show()

def getText():
    tools = pyocr.get_available_tools()
    tool = tools[0]
    langs = tool.get_available_languages()
    param = tool.image_to_string(
        Image.open(paramImg),
        lang='eng',
        builder=pyocr.builders.DigitBuilder()
    ).split()
    preParam = tool.image_to_string(
        Image.open(preParamImg),
        lang='eng',
        builder=pyocr.builders.DigitBuilder()
    ).split()


    preParam_sub=[]
    param_sub=[]
    for i in preParam:
        a=(re.sub(r"\D",'',i))
        if a!="":
            preParam_sub.append(a)
    for i in param:
        a=(re.sub(r"\D",'',i))
        if a!="":
            param_sub.append(a)

    preParam=preParam_sub
    param=param_sub

    if len(param)!=4 or len(preParam)!=4:
        sys.exit( )

    strength = int(param[0]) - int(preParam[0])
    agile = int(param[1]) - int(preParam[1])
    inte = int(param[2]) - int(preParam[2])
    physical = int(param[3]) - int(preParam[3])
    total = strength + physical #筋力＋体力 俊敏と知力は無視

    if strength>=30 or strength<=-30 or agile>=30 or agile<=-30 or inte>=30 or  inte<=-30 or physical>=30 or physical<=-30:
        sys.exit()

    print("筋力"+str(strength),"敏捷"+str(agile),"知力"+str(inte),"体力"+str(physical))
    if total > 0 or (total==0 and inte>0):
        print("筋力＋体力"+str(total),"知力"+str(inte))
        clickRight()

        # 結果が表示される。邪魔なので3秒待つ。

    else:
        clickLeft()