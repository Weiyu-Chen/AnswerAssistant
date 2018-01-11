import urllib, urllib.request, sys, json, time, base64
from bs4 import BeautifulSoup
import pytesseract
import requests
from PIL import (Image, ImageGrab)

# 二值化算法
def binarizing(img,threshold):
    pixdata = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            if pixdata[x, y] < threshold:
                pixdata[x, y] = 0
            else:
                pixdata[x, y] = 255
    return img


# 去除干扰线算法
def depoint(img):   #input: gray image
    pixdata = img.load()
    w,h = img.size
    for y in range(1,h-1):
        for x in range(1,w-1):
            count = 0
            if pixdata[x,y-1] > 245:
                count = count + 1
            if pixdata[x,y+1] > 245:
                count = count + 1
            if pixdata[x-1,y] > 245:
                count = count + 1
            if pixdata[x+1,y] > 245:
                count = count + 1
            if count > 2:
                pixdata[x,y] = 255
    return img

def main():
    while input("答题框出现后按任意键开始识别(0 退出) : ") != '0':
        start = time.time()
        #   图片截取
        #   问题
        imgQuestion = ImageGrab.grab((1420, 180, 1880, 250))
        imgQuestion.save('./imgQuestion.png')
        iQuestion = Image.open("./imgQuestion.png")
        ###   答案一
        imgAnswerOne = ImageGrab.grab((1420, 330, 1880, 370))
        imgAnswerOne = imgAnswerOne.convert('L')
        imgAnswerOne = binarizing(imgAnswerOne, 220)
        imgAnswerOne.save('./imgAnswerOne.png')
        ###   答案二
        imgAnswerTwo = ImageGrab.grab((1420, 420, 1880, 460))
        imgAnswerTwo = imgAnswerTwo.convert('L')
        imgAnswerTwo = binarizing(imgAnswerTwo, 220)
        imgAnswerTwo.save('./imgAnswerTwo.png')
        ###   答案三
        imgAnswerThree = ImageGrab.grab((1420, 500, 1880, 540))
        imgAnswerThree = imgAnswerThree.convert('L')
        imgAnswerThree = binarizing(imgAnswerThree, 220)
        imgAnswerThree.save('./imgAnswerThree.png')
        #   图片识别
        #   问题
        question = pytesseract.image_to_string(imgQuestion, lang='chi_sim')
        question = question.replace(' ','').replace('\n','')
        question = question[question.find('.') + 1:question.find('?')]
        ###   答案一
        answerOne = pytesseract.image_to_string(imgAnswerOne, lang='chi_sim')
        answerOne = answerOne.replace(' ','').replace('\n','')
        answerOne = answerOne[answerOne.find('.') + 1:answerOne.find('?')]
        ###   答案二
        answerTwo = pytesseract.image_to_string(imgAnswerTwo, lang='chi_sim')
        answerTwo = answerTwo.replace(' ','').replace('\n','')
        answerTwo = answerTwo[answerTwo.find('.') + 1:answerTwo.find('?')]
        ###   答案三
        answerThree = pytesseract.image_to_string(imgAnswerThree, lang='chi_sim')
        answerThree = answerThree.replace(' ','').replace('\n','')
        answerThree = answerThree[answerThree.find('.') + 1:answerThree.find('?')]
        print('问题:' + question)
        print('选项一:' + answerOne)
        print('选项二:' + answerTwo)
        print('选项三:' + answerThree)
        

        urllib.request.urlopen('https://www.wukong.com/search/?keyword=' + question)
        end = time.time()
        print('总共用时：' + str( end - start ) + '秒')

if __name__ == '__main__':
    main()